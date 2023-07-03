# Ph.D Code

import statistics
import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances

train_dataset = pd.read_csv("data/MNIST_train.csv")
test_dataset = pd.read_csv("data/MNIST_test.csv")

train_x = train_dataset.iloc[:, 1:]
train_y = train_dataset.iloc[:, 0]
test_x = test_dataset.iloc[:, 1:]
test_y = test_dataset.iloc[:, 0]

distance = np.argsort(pairwise_distances(test_x, train_x))

k = 5

top_k_distance = distance[:, :k]

preds = []
for idx in top_k_distance:
    # statistics.mode: 주어진 리스트의 다수를 추출
    preds.append(statistics.mode(train_y[idx]))

acc = (preds == test_y).sum() / len(test_y) * 100
print(f"{acc}%")