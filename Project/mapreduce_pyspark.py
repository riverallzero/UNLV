import numpy as np

from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, StandardScaler
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.functions import rand

import time
from tqdm import tqdm


def split_data_into_partitions(X, y, num_partitions):
    data_partitions = []
    chunk_size = len(X) // num_partitions

    for i in range(num_partitions):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size
        X_partition = X[start_idx:end_idx]
        y_partition = y[start_idx:end_idx]
        data_partitions.append((X_partition, y_partition))

    return data_partitions


def map_function(data_partition, params):
    # Using OLS
    X, y = data_partition
    gradients = np.dot(X.T, np.dot(X, params.value) - y)

    return gradients


def reduce_function(intermediate_results, learning_rate):
    total_gradients = np.sum(intermediate_results, axis=0)
    updated_params = learning_rate * total_gradients

    return updated_params


def main():
    # Initialize SparkSession
    spark = SparkSession.builder.getOrCreate()

    # --------------------
    # STEP 1: Load Data
    df = spark.read.csv("train.csv", header=True, inferSchema=True)
    df = df.drop("Id")
    df = df.toDF(*[col.lower() for col in df.columns])
    df = df.withColumnRenamed("married/single", "married_single")

    # Label Encoding
    cate_cols = ["married_single", "profession", "house_ownership", "car_ownership", "city", "state"]
    indexers = [StringIndexer(inputCol=col, outputCol=col+"_index").fit(df) for col in cate_cols]
    pipeline = Pipeline(stages=indexers)
    df = pipeline.fit(df).transform(df)
    df = df.drop(*cate_cols)
    print("[1] Label Encoding-Done.")

    # Down sampling
    class_0_count = df.filter("risk_flag = 1").count()
    class_1_df = df.filter("risk_flag = 0")
    sampled_1_df = class_1_df.orderBy(rand(seed=42)).limit(class_0_count)
    df = sampled_1_df.union(df.filter("risk_flag = 1"))
    print("[2] Down Sampling-Done.")

    # Data split
    train_val_data, test_data = df.randomSplit([0.8, 0.2], seed=42)
    train_data, val_data = train_val_data.randomSplit([0.8, 0.2], seed=42)
    train_label_counts = train_data.groupBy("risk_flag").count().collect()
    val_label_counts = val_data.groupBy("risk_flag").count().collect()
    test_label_counts = test_data.groupBy("risk_flag").count().collect()

    print(f"Train-Label: {train_label_counts}")
    print(f"Val-Label: {val_label_counts}")
    print(f"Test-Label: {test_label_counts}")

    # Feature Assembling
    feature_cols = df.columns
    feature_cols.remove("risk_flag")
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    train_data = assembler.transform(train_data)
    val_data = assembler.transform(val_data)
    test_data = assembler.transform(test_data)

    # StandardScaler
    scaler = StandardScaler(inputCol="features", outputCol="scaled_features")

    scaler_model = scaler.fit(train_data)
    train_data = scaler_model.transform(train_data)
    val_data = scaler_model.transform(val_data)
    test_data = scaler_model.transform(test_data)

    train_data = train_data.withColumn("label", train_data["risk_flag"].cast("integer"))
    val_data = val_data.withColumn("label", val_data["risk_flag"].cast("integer"))
    test_data = test_data.withColumn("label", test_data["risk_flag"].cast("integer"))

    train_data = train_data.select("scaled_features", "label")
    val_data = val_data.select("scaled_features", "label")
    test_data = test_data.select("scaled_features", "label")
    print("[3] Standard Scaling-Done.\n")

    # --------------------
    # STEP 2: MapReduce
    num_partitions = 4

    # Define data for linear regression
    X = np.array(train_data.select("scaled_features").rdd.flatMap(lambda x: x).collect())
    X_transposed = X.T.tolist()

    y = train_data.select("label").rdd.flatMap(lambda x: x).collect()

    # Split the data into partitions
    data_partitions = split_data_into_partitions(X, y, num_partitions)

    # Broadcast the initial model parameters to all workers
    params = spark.sparkContext.broadcast(np.zeros(len(X_transposed)))

    # Set learning rate and number of iterations
    learning_rate = 0.001
    num_iterations = 100
    

    start_time = time.time()
    for _ in tqdm(range(num_iterations)):
        rdd = spark.sparkContext.parallelize(data_partitions)

        # Map step: compute gradients on each data partition in parallel
        intermediate_results = rdd.map(lambda x: map_function(x, params)).collect()

        # Reduce step: combine gradients and update model parameters
        params = spark.sparkContext.broadcast(reduce_function(intermediate_results, learning_rate))
    end_time = time.time()
    print(f"Time: {(end_time - start_time) // 60}min {(end_time - start_time) % 60:.3f}sec\n")

    # --------------------
    # STEP 3: Prediction
    X_val = np.array(val_data.select("scaled_features").rdd.flatMap(lambda x: x).collect())
    val_scores = np.dot(X_val, params.value)
    val_pred = np.where(val_scores >= 0.5, 1, 0)

    X_test = np.array(test_data.select("scaled_features").rdd.flatMap(lambda x: x).collect())
    test_scores = np.dot(X_test, params.value)
    test_pred = np.where(test_scores >= 0.5, 1, 0)

    val_acc = (val_pred == val_data.select("label").rdd.flatMap(lambda x: x).collect()).sum() / len(val_pred) * 100
    test_acc = (test_pred == test_data.select("label").rdd.flatMap(lambda x: x).collect()).sum() / len(test_pred) * 100
    print(f"\nVal-ACC = {val_acc:.3f}")
    print(f"Test-ACC = {test_acc:.3f}")

    spark.stop()


if __name__ == "__main__":
    main()
