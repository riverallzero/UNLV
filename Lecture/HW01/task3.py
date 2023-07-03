# Visualize the housing data using violin plot. Use only continues value (30 points)

import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


def main():
    df = pd.read_csv("data/housing_training.csv")
    column_names = ["col{}".format(i) for i in range(1, df.shape[1] + 1)]
    df.columns = column_names
    df.dropna(inplace=True)

    # Check Unique value(categorical)
    unique_counts = df.nunique()
    columns_to_delete = unique_counts[unique_counts < 100].index
    categorical_col = columns_to_delete
    continuous_col = df.drop(columns=columns_to_delete).columns
    print(f"Categorical\n{categorical_col}\n-------\nContinuous\n{continuous_col}")
    print(f"-------\n{df.describe()}")

    ## Draw graph - contrast columns
    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
    # sns.violinplot(data=df, x="col9", y="col14", ax=ax1)
    # ax1.set_title("Violin Plots(col9 & col14)", ha="center", size=20)
    #
    # sns.violinplot(data=df, x="col9", y="col13", ax=ax2)
    # ax2.set_title("Violin Plots(col9 & col13)", ha="center", size=20)
    #
    # plt.tight_layout()
    # plt.savefig("graph/task3.png")
    # plt.show()

    # Draw graph - Standardize the features
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(df)
    print(f"Standardize\n{scaled_df}\n------------")

    positions = list(range(len(df.columns)))  # Convert positions to numerical values
    widths = np.full(len(df.columns), 0.5)  # Example widths, adjust according to your needs

    plt.violinplot(scaled_df, positions=positions, widths=widths, showmeans=True)
    plt.title("Housing Dataset - violinplot", size=20)
    plt.tight_layout()
    plt.savefig("graph/task3.png")
    plt.show()


if __name__ == "__main__":
    main()