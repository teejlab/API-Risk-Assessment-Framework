from kmodes.kprototypes import KPrototypes
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
import pandas as pd
import plotnine as p9
import math


def plot_clustering(train_file, output_path):
    """
    Plot the clustering of the dataframe.
    Parameters
    ----------
    train_file : str
        The path to the training file.
    output_path : str
        The path to the output file.
    Returns
    -------
    None
    """
    # Load the data
    df = pd.read_excel(train_file)
    # Separate the Target and the Features
    X_train = df.drop(["Risk_Label"], axis=1)
    y_train = df["Risk_Label"].fillna(value="Missing")

    # Feature names
    numerical_features = ["NRI score", "metadata_fields_count", "parameters_count"]
    categorical_features = list(X_train.drop(numerical_features, axis=1).columns.values)
    categorical_idx = [
        X_train.columns.get_loc(c) for c in categorical_features if c in X_train
    ]

    # Convert the categorical features to strings
    X_train[categorical_features] = X_train[categorical_features].astype(str)

    # Elbow curve to find optimal K
    cost = []
    K = range(1, 6)
    for num_clusters in list(K):
        kproto = KPrototypes(n_clusters=num_clusters, init="Cao", n_init=10, n_jobs=-1)
        kproto.fit_predict(X_train, categorical=categorical_idx)
        cost.append(kproto.cost_)
        
    # Plot the elbow curve
    plt.plot(K, cost, "bx-")
    plt.xlabel("No. of clusters")
    plt.ylabel("Cost")
    plt.title("Elbow Method For Optimal k")
    plt.savefig(output_path + "/elbow_clustering.png")

    # Visualize the clusters
    kproto = KPrototypes(n_clusters=3, init="Cao", n_init=10, n_jobs=-1)
    clusters = kproto.fit_predict(X_train, categorical=categorical_idx)
    FAMD_components, processed_df = _FAMD(
        X_train, 3, numerical_features, categorical_features
    )

    # Create a new dataframe with the clusters
    k_proto_pca = pd.DataFrame(
        {
            "x": FAMD_components[:, 0],
            "y": FAMD_components[:, 1],
            "clusters": clusters,
            "target": y_train,
        }
    )
    k_proto_pca["clusters"] = k_proto_pca["clusters"].apply(str)

    # Plot the clusters
    p1 = (
        p9.ggplot(k_proto_pca, p9.aes(x="x", y="y", fill="clusters", color="clusters"))
        + p9.geom_point(alpha=0.5, size=2)
        + p9.ggtitle("PCA Visualization (Our Clustering)")
        + p9.theme_bw()
    )

    p2 = (
        p9.ggplot(k_proto_pca, p9.aes(x="x", y="y", fill="target", color="target"))
        + p9.geom_point(alpha=0.5, size=2)
        + p9.ggtitle("PCA Visualization (Rule-based Label)")
        + p9.theme_bw()
    )
    # Save the plot
    p1.save(output_path + "/pca_clustering.png")
    p2.save(output_path + "/pca_label.png")


def _FAMD(df, n_components, numerical_features, categorical_features):
    """
    Factorial Analysis of Mixed Data (FAMD),
    which generalizes the Principal Component Analysis (PCA)
    algorithm to datasets containing numerical and categorical variables

    a) For the numerical variables
      - Standard scale (= get the z-score)

    b) For the categorical variables:
      - Get the one-hot encoded columns
      - Divide each column by the square root of its probability sqrt(μₘ)
      - Center the columns

    c) Apply a PCA algorithm over the table obtained!
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to be transformed.
    n_components : int
        The number of components to be kept.
    numerical_features : list
        The numerical features to be transformed.
    categorical_features : list
        The categorical features to be transformed.
    Returns
    -------
    FAMD_components : numpy.ndarray
        The transformed data.
    processed_df : pandas.DataFrame
        The transformed dataframe.
    """
    # Separate the numerical and categorical features
    numeric_cols = df[numerical_features]
    cat_cols = df[categorical_features]

    # numeric process
    normalized_df = _calculate_zscore(df, numeric_cols)
    normalized_df = normalized_df[numeric_cols.columns]

    # categorical process
    cat_one_hot_df, one_hot_cols = _one_hot_encode(df, cat_cols)
    cat_one_hot_norm_df = _normalize_column_modality(cat_one_hot_df, one_hot_cols)
    cat_one_hot_norm_center_df = _center_columns(cat_one_hot_norm_df, one_hot_cols)

    # Merge DataFrames
    processed_df = pd.concat([normalized_df, cat_one_hot_norm_center_df], axis=1)

    # Perform (PCA)
    pca = PCA(n_components=n_components)
    principalComponents = pca.fit_transform(processed_df)

    return principalComponents, processed_df


def _calculate_zscore(df, columns):
    """
    scales columns in dataframe using z-score
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to be scaled.
    columns : list
        The columns to be scaled.
    Returns
    -------
    df : pandas.DataFrame
        The scaled dataframe.
    """
    df = df.copy()
    for col in columns:
        df[col] = (df[col] - df[col].mean()) / df[col].std(ddof=0)

    return df


def _one_hot_encode(df, columns):
    """
    one hot encodes list of columns and
    concatenates them to the original df
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to be transformed.
    columns : list
        The categorical features to be transformed.
    Returns
    -------
    one_hot_df : pandas.DataFrame
        The transformed dataframe.
    """

    concat_df = pd.concat(
        [pd.get_dummies(df[col], drop_first=True, prefix=col) for col in columns],
        axis=1,
    )
    one_hot_cols = concat_df.columns

    return concat_df, one_hot_cols


def _normalize_column_modality(df, columns):
    """
    divides each column by the probability μₘ of the modality
    (number of ones in the column divided by N) only for one hot columns
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to be normalized.
    columns : list
        The columns to be normalized.
    Returns
    -------
    pandas.DataFrame
        The normalized dataframe.
    """
    length = len(df)
    for col in columns:

        weight = math.sqrt(sum(df[col]) / length)
        df[col] = df[col] / weight

    return df


def _center_columns(df, columns):
    """
    center columns by subtracting the mean value
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to be centered.
    columns : list
        The columns to be centered.
    Returns
    -------
    pandas.DataFrame
        The centered dataframe.
    """
    for col in columns:
        df[col] = df[col] - df[col].mean()

    return df


plot_clustering("data/processed/df_full.xlsx")
