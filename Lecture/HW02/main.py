# MNIST KNN without KNN library

import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, KFold


class KNN:
    def __init__(self, k=3):
        self.k = k
        self.X_train = None
        self.y_train = None

    def train(self, X, y):
        self.X_train = X
        self.y_train = y

    def get_distance(self, X_val):
        distances = []
        for x in X_val:
            dist = [euclidean(x, x_train) for x_train in self.X_train]
            distances.append(dist)

        return np.array(distances)

    def predict(self, X_val):
        distances = self.get_distance(X_val)
        y_pred = []
        for dist in distances:
            sorted_indices = np.argsort(dist)[:self.k]
            k_nearest_labels = self.y_train.iloc[sorted_indices]
            unique, counts = np.unique(k_nearest_labels, return_counts=True)
            y_pred.append(unique[np.argmax(counts)])

        return np.array(y_pred)


def main():
    train = pd.read_csv("data/MNIST_train.csv")
    test = pd.read_csv("data/MNIST_test.csv")

    X = train.drop(["label"], axis=1)
    y = train["label"]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)

    model = KNN(k=3)

    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    fold = 1
    for train_index, val_index in kf.split(X):
        print(f"Fold {fold}-----------")

        X_train, X_val = X.iloc[train_index], X.iloc[val_index]
        y_train, y_val = y.iloc[train_index], y.iloc[val_index]
        print(X_train.values)
        model.train(X_train.values, y_train)
        pred = model.predict(X_val.values)

        accuracy = accuracy_score(y_val, pred)

        print(f"ACC = {accuracy * 100:.2f}%")

        fold += 1

    model.train(X_train.values, y_train)

    print("\n-----------------")
    train_pred = model.predict(X_val.values)
    train_acc = accuracy_score(train_pred, y_val)
    print(f"Train-ACC = {train_acc * 100:.2f}%")

    test_pred = model.predict(test.drop(["label"], axis=1).values)
    test_acc = accuracy_score(test_pred, test["label"])
    print(f"Test-ACC = {test_acc * 100:.2f}%")


if __name__ == "__main__":
    main()
