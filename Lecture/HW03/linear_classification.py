# MNIST Linear Classification without library(threshold=0.5)
# by min-max normalization, i.e. divide by 255

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split, KFold


def linear_classification(X, y, i):
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # 절편(intercept)을 포함하기 위해 X_ 상수 열 추가
    X_train = np.concatenate((np.ones((X_train.shape[0], i)), X_train), axis=1)
    X_val = np.concatenate((np.ones((X_val.shape[0], i)), X_val), axis=1)

    # OLS를 위한 가중치 추정식 계산
    weights = np.linalg.pinv(X_train.T.dot(X_train)).dot(X_train.T).dot(y_train)

    scores = X_val.dot(weights)
    predictions = np.where(scores >= 5.5, 6, 5)

    return y_val, predictions


def linear_classification_kfold(X, y, n):
    kf = KFold(n_splits=n, shuffle=True, random_state=42)

    acc_score = []
    auc_score = []
    tpr_score = []
    fpr_score = []

    fold = 1

    for train_index, val_index in kf.split(X):
        X_train, X_val = X.iloc[train_index], X.iloc[val_index]
        y_train, y_val = y.iloc[train_index], y.iloc[val_index]

        # 절편(intercept)을 포함하기 위해 X_train에 상수 열 추가
        X_train = np.concatenate((np.ones((X_train.shape[0], 1)), X_train), axis=1)

        # OLS를 위한 가중치 추정식 계산
        weights = np.linalg.pinv(X_train.T.dot(X_train)).dot(X_train.T).dot(y_train)

        # X_val에 절편 열 추가
        X_val = np.concatenate((np.ones((X_val.shape[0], 1)), X_val), axis=1)

        scores = X_val.dot(weights)
        predictions = np.where(scores >= 5.5, 6, 5)

        fold += 1

        acc = accuracy_score(y_val, predictions)
        acc_score.append(acc * 100)
        auc = roc_auc_score(y_val, predictions)
        auc_score.append(auc * 100)

        tpr = sum(a == b for a, b in zip(y_val.values, predictions)) / len(predictions)
        tpr_score.append(tpr * 100)
        fpr = sum(a != b for a, b in zip(y_val.values, predictions)) / len(predictions)
        fpr_score.append(fpr * 100)

    return acc_score, auc_score, tpr_score, fpr_score


def main():
    features = pd.read_csv("data/MNIST_15_15.csv")
    features.columns = ["col{}".format(i) for i in range(1, features.shape[1] + 1)]

    labels = pd.read_csv("data/MNIST_LABEL.csv")
    labels.columns = ["label"]

    for col in features.columns:
        features[col] = features[col].apply(lambda x: x / 255)

    df = pd.concat([features, labels], axis=1)

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    results = linear_classification(X, y, 1)
    acc = accuracy_score(results[0], results[1])
    print(f"Val-ACC = {acc * 100:.2f}%")
    auc = roc_auc_score(results[0], results[1])
    print(f"Val-AUC = {auc * 100:.2f}%")
    tpr = sum(a == b for a, b in zip(results[0].values, results[1])) / len(results[1])
    print(f"Val-TPR = {tpr * 100:.2f}%")
    fpr = sum(a != b for a, b in zip(results[0].values, results[1])) / len(results[1])
    print(f"Val-FPR = {fpr * 100:.2f}%")

    print("---------KFold---------")
    kfold = linear_classification_kfold(X, y, 10)
    print(f"KFold-ACC: {kfold[0]}")
    print(f"KFold-AUC: {kfold[1]}")
    print(f"KFold-TPR: {kfold[2]}")
    print(f"KFold-FPR: {kfold[3]}")

    print("-------Mean KFold-------")
    print(f"Mean KFold-ACC = {sum(kfold[0]) / len(kfold[0]):.2f}%")
    print(f"Mean KFold-AUC = {sum(kfold[0]) / len(kfold[1]):.2f}%")
    print(f"Mean KFold-TPR = {sum(kfold[1]) / len(kfold[2]):.2f}%")
    print(f"Mean KFold-FPR = {sum(kfold[2]) / len(kfold[3]):.2f}%")


if __name__ == "__main__":
    main()