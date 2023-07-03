# Visualize the MNIST data using PCA.
# Reduce the data dimension to two or three and plot the data of reduced dimension.
# Must plot all the data of ten groups (0 to 9). (40 points)

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def main():
    df = pd.read_csv("data/MNIST_100.csv")
    print(f"1. Shape\n{df.shape}\n------------")

    # Seperate label & feature
    labels = df["label"]
    features = df.drop(["label"], axis=1)

    # Standardize the features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    print(f"2. Standardize\n{scaled_features}\n------------")

    # Perform PCA
    pca = PCA(n_components=2)
    reduced_features = pca.fit_transform(scaled_features)
    print(f"3. PCA\n{reduced_features}\n------------")

    # Create a DataFrame for the reduced features
    reduced_data = pd.DataFrame(reduced_features, columns=["PC1", "PC2"])
    reduced_data["label"] = labels
    print(f"4. PCA-df\n{reduced_data.head(3)}\n------------")

    # Plot the data
    plt.figure(figsize=(10, 8))
    for i in range(10):
        subset = reduced_data[reduced_data["label"] == i]
        plt.scatter(subset["PC1"], subset["PC2"], cmap="coolwarm", label=str(i))
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("MNIST Data Visualization using PCA", size=20)
    plt.xlim(-15, 30)
    plt.ylim(-15, 30)
    plt.legend()
    plt.tight_layout()
    plt.savefig("graph/task1.png")
    plt.show()


if __name__ == "__main__":
    main()