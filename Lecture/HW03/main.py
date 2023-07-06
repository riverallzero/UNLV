# MNIST Linear Classification without library

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, KFold


def linear_classification(X, y):
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    learning_rate = 0.01
    num_iterations = 100

    weights = np.zeros(X.shape[1])

    for iteration in range(num_iterations):
        scores = np.dot(X_train, weights)
        predictions = np.where(scores >= 0.5, 6, 5)
        errors = y_train - predictions
        gradient = np.dot(X_train.T, errors)
        weights += learning_rate * gradient

    scores = np.dot(X_val, weights)
    predictions = np.where(scores >= 0.5, 6, 5)

    return y_val, predictions


def linear_classification_kfold(X, y, n):
    kf = KFold(n_splits=n, shuffle=True, random_state=42)

    acc_score = []
    tpr_score = []
    fpr_score = []
    fold = 1
    for train_index, val_index in kf.split(X):
        X_train, X_val = X.iloc[train_index], X.iloc[val_index]
        y_train, y_val = y.iloc[train_index], y.iloc[val_index]

        learning_rate = 0.01
        num_iterations = 100

        weights = np.zeros(X.shape[1])

        for iteration in range(num_iterations):
            scores = np.dot(X_train, weights)
            predictions = np.where(scores >= 0.5, 6, 5)
            errors = y_train - predictions
            gradient = np.dot(X_train.T, errors)
            weights += learning_rate * gradient

            fold += 1

        scores = np.dot(X_val, weights)
        predictions = np.where(scores >= 0.5, 6, 5)
        accuracy = accuracy_score(y_val, predictions)
        acc_score.append(accuracy * 100)

        tpr = sum(a == b for a, b in zip(y_val.values, predictions)) / len(predictions)
        tpr_score.append(tpr * 100)
        fpr = sum(a != b for a, b in zip(y_val.values, predictions)) / len(predictions)
        fpr_score.append(fpr * 100)

    return acc_score, tpr_score, fpr_score


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

    results = linear_classification(X, y)
    accuracy = accuracy_score(results[0], results[1])
    print(f"Val-ACC = {accuracy * 100:.2f}%")
    tpr = sum(a == b for a, b in zip(results[0].values, results[1])) / len(results[1])
    print(f"Val-TPR = {tpr * 100:.2f}%")
    fpr = sum(a != b for a, b in zip(results[0].values, results[1])) / len(results[1])
    print(f"Val-FPR = {fpr * 100:.2f}%")

    print("---------KFold---------")
    kfold = linear_classification_kfold(X, y, 10)
    print(f"KFold-ACC: {kfold[0]}")
    print(f"KFold-TPR: {kfold[1]}")
    print(f"KFold-FPR: {kfold[2]}")

    print("-------Mean KFold-------")
    print(f"Mean KFold-ACC = {sum(kfold[0]) / len(kfold[0]):.2f}%")
    print(f"Mean KFold-TPR = {sum(kfold[1]) / len(kfold[1]):.2f}%")
    print(f"Mean KFold-FPR = {sum(kfold[2]) / len(kfold[2]):.2f}%")


if __name__ == "__main__":
    main()