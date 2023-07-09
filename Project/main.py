import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn import svm
from sklearn.utils import compute_sample_weight

import time

import seaborn as sns
import matplotlib.pyplot as plt


def main():
    train = pd.read_csv("data/train.csv")
    train.drop(["Id"], axis=1, inplace=True)

    train.columns = map(str.lower, train.columns)
    train.rename(columns={"married/single": "married_single"}, inplace=True)

    # Category cols to num
    cate_cols = ["married_single", "profession", "house_ownership", "car_ownership", "city", "state"]

    for col in cate_cols:
        le = LabelEncoder()
        le = le.fit(train[col])
        train[col] = le.transform(train[col])

    print("Label Encoding-Done.")

    # Label graph
    sns.displot(train["risk_flag"], kde=True)
    plt.show()

    X = train.drop(["risk_flag"], axis=1)
    y = train["risk_flag"].apply(lambda x: int(x))

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    sample_weights = compute_sample_weight(class_weight="balanced", y=y_train)

    clf = svm.SVC()

    # 시작 시간 기록
    start_time = time.time()

    clf.fit(X_train, y_train, sample_weight=sample_weights)

    # 종료 시간 기록
    end_time = time.time()
    # 학습 시간 계산
    elapsed_time = end_time - start_time

    y_pred = clf.predict(X_val)

    acc = accuracy_score(y_pred, y_val)

    print(f"ACC = {acc * 100:.2f}%")
    print(f"Elapsed Time: {elapsed_time // 60} min {elapsed_time % 60:.2f} sec")


if __name__ == "__main__":
    main()