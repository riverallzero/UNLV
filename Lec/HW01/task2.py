# Visualize the MNIST data using t-SNE library. (30 points)

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


def main():

    # Load the MNIST dataset
    df = pd.read_csv("data/MNIST_100.csv")

    # Prepare the data for t-SNE
    features = df.drop(["label"], axis=1)
    labels = df["label"]

    # Apply t-SNE to reduce the dimensionality of the data
    tsne = TSNE(n_components=2, random_state=42)
    feature_tsne = tsne.fit_transform(features)

    # Visualize the t-SNE results
    plt.figure(figsize=(10, 8))
    plt.scatter(feature_tsne[:, 0], feature_tsne[:, 1], c=labels, cmap="coolwarm")
    plt.colorbar(ticks=range(10))
    plt.title("t-SNE Visualization of MNIST", size=20)
    plt.xlim(-40, 40)
    plt.ylim(-40, 40)
    plt.xlabel("t-SNE Dimension 1")
    plt.ylabel("t-SNE Dimension 2")
    plt.tight_layout()
    plt.savefig("graph/task2.png")
    plt.show()


if __name__ == "__main__":
    main()