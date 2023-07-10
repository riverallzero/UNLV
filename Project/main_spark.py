from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
from pyspark.ml.classification import LinearSVC
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from pyspark.sql.functions import col as scol

import time


def main():
    spark = SparkSession.builder.appName("UNLV").getOrCreate()

    df = spark.read.csv("data/train.csv", header=True, inferSchema=True)
    df = df.drop("Id").withColumnRenamed("married/single", "married_single")
    df = df.toDF(*(col.lower() for col in df.columns))
    df = df.withColumn("risk_flag", scol("risk_flag").cast("integer"))

    # Category cols to num
    cate_cols = ["married_single", "profession", "house_ownership", "car_ownership", "city", "state"]

    indexers = [StringIndexer(inputCol=col, outputCol=col + "_idx").fit(df) for col in cate_cols]

    pipeline = Pipeline(stages=indexers)
    df = pipeline.fit(df).transform(df)
    df = df.drop(*cate_cols)

    print("Label Encoding-Done.")

    assembler = VectorAssembler(
        inputCols=[col for col in df.columns if col != "risk_flag"],
        outputCol="features"
    )
    df = assembler.transform(df)
    df = df.select(["features", "risk_flag"])

    df.show(5, truncate=False)

    # Define model
    train, val = df.randomSplit([0.8, 0.2], seed=42)

    svm = LinearSVC(labelCol="risk_flag", weightCol="risk_flag", maxIter=100) # default 100

    # Start: training
    start_time = time.time()

    model = svm.fit(train)

    # End: training
    end_time = time.time()
    # Calculate training time
    elapsed_time = end_time - start_time

    predictions = model.transform(val)

    evaluator = BinaryClassificationEvaluator(labelCol="risk_flag", metricName="areaUnderROC")
    auc = evaluator.evaluate(predictions)

    print(f"AUC = {auc:.3f}")
    print(f"Elapsed Time: {elapsed_time // 60} min {elapsed_time % 60:.2f} sec")


if __name__ == "__main__":
    main()
