import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import LabelEncoder
from sklearn import svm
from sklearn.utils import compute_sample_weight

import time

import seaborn as sns
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv("data/train.csv")
    df.drop(["Id"], axis=1, inplace=True)

    df.columns = map(str.lower, df.columns)
    df.rename(columns={"married/single": "married_single"}, inplace=True)

    # Category cols to num
    cate_cols = ["married_single", "profession", "house_ownership", "car_ownership", "city", "state"]

    for col in cate_cols:
        le = LabelEncoder()
        le = le.fit(df[col])
        df[col] = le.transform(df[col])

    print("Label Encoding-Done.")

    # Label graph
    sns.displot(df["risk_flag"], kde=True)
    plt.show()

    X = df.drop(["risk_flag"], axis=1)
    y = df["risk_flag"].apply(lambda x: int(x))

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    sample_weights = compute_sample_weight(class_weight="balanced", y=y_train)

    clf = svm.SVC()

    # Start: training
    start_time = time.time()

    clf.fit(X_train, y_train, sample_weight=sample_weights)

    # End: training
    end_time = time.time()
    # Calculate training time
    elapsed_time = end_time - start_time

    y_pred = clf.predict(X_val)

    auc = roc_auc_score(y_val, y_pred)

    print(f"AUC = {auc:.3f}")
    print(f"Elapsed Time: {elapsed_time // 60} min {elapsed_time % 60:.2f} sec")


if __name__ == "__main__":
    main()