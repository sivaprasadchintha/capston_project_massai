import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def create_univariate_charts(df):
    """
    Create histogram and boxplot for Age and Fare.
    Saves all charts inside the charts/ folder.
    """

    os.makedirs("charts", exist_ok=True)

    numeric_columns = ["age", "fare"]

    for column in numeric_columns:

        # -----------------------------
        # Histogram
        # -----------------------------
        plt.figure(figsize=(8, 5))

        sns.histplot(
            data=df,
            x=column,
            bins=30,
            kde=True
        )

        plt.title(f"{column.title()} Distribution")
        plt.xlabel(column.title())
        plt.ylabel("Frequency")

        plt.tight_layout()

        plt.savefig(f"charts/{column}_histogram.png")

        plt.close()

        # -----------------------------
        # Box Plot
        # -----------------------------
        plt.figure(figsize=(8, 2))

        sns.boxplot(
            x=df[column]
        )

        plt.title(f"{column.title()} Box Plot")

        plt.tight_layout()

        plt.savefig(f"charts/{column}_boxplot.png")

        plt.close()

    print("\n✓ Histograms and Boxplots saved inside charts/")

def survival_by_gender(df):

    plt.figure(figsize=(7,5))

    sns.countplot(
        data=df,
        x="sex",
        hue="survived"
    )

    plt.title("Survival by Gender")

    plt.tight_layout()

    plt.savefig("charts/survival_gender.png")

    plt.close()

    print("✓ Survival by Gender chart saved.")

def survival_by_class(df):

    plt.figure(figsize=(7,5))

    sns.countplot(
        data=df,
        x="pclass",
        hue="survived"
    )

    plt.title("Survival by Passenger Class")

    plt.tight_layout()

    plt.savefig("charts/survival_class.png")

    plt.close()

    print("✓ Survival by Passenger Class chart saved.")

def correlation_heatmap(df):
    """
    Correlation Heatmap using only the required columns.
    """

    plt.figure(figsize=(10, 8))

    # Use only the six columns specified in the assignment
    corr_columns = [
        "survived",
        "pclass",
        "age",
        "sibsp",
        "parch",
        "fare"
    ]

    corr_matrix = df[corr_columns].corr()

    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="coolwarm",
        linewidths=0.5
    )

    plt.title("Correlation Heatmap")

    plt.tight_layout()

    plt.savefig("charts/correlation_heatmap.png")

    plt.close()

    print("✓ Correlation Heatmap saved.")

def multivariate_analysis(df):

    # Scatter Plot
    plt.figure(figsize=(8,5))

    sns.scatterplot(
        data=df,
        x="age",
        y="fare",
        hue="survived"
    )

    plt.title("Age vs Fare")

    plt.tight_layout()

    plt.savefig("charts/scatter_age_fare.png")

    plt.close()

    # Pair Plot
    sns.pairplot(
        df[
            [
                "age",
                "fare",
                "pclass",
                "survived"
            ]
        ],
        hue="survived"
    )

    plt.savefig("charts/pairplot.png")

    plt.close()

    # Violin Plot
    plt.figure(figsize=(8,5))

    sns.violinplot(
        data=df,
        x="sex",
        y="age",
        hue="survived",
        split=True
    )

    plt.tight_layout()

    plt.savefig("charts/violin_plot.png")

    plt.close()

    # Boxplot
    plt.figure(figsize=(8,5))

    sns.boxplot(
        data=df,
        x="class",
        y="fare"
    )

    plt.tight_layout()

    plt.savefig("charts/class_boxplot.png")

    plt.close()

    print("✓ Multivariate Charts saved.") 

from sklearn.preprocessing import StandardScaler


def standardization_check(df):

    scaler = StandardScaler()

    scaled = scaler.fit_transform(
        df[
            [
                "age",
                "fare"
            ]
        ]
    )

    scaled_df = pd.DataFrame(
        scaled,
        columns=["age_scaled", "fare_scaled"]
    )

    plt.figure(figsize=(8,5))

    sns.boxplot(data=scaled_df)

    plt.title("Standardized Features")

    plt.tight_layout()

    plt.savefig("charts/standardization.png")

    plt.close()

    print("✓ Standardization Check saved.") 

def print_survival_rates(df):
    """
    Print survival rates using boolean masking.
    """

    print("\n" + "=" * 60)
    print("SURVIVAL RATE ANALYSIS")
    print("=" * 60)

    # -----------------------------
    # Survival Rate by Gender
    # -----------------------------
    print("\nSurvival Rate by Gender")

    male_rate = (
        df[df["sex"] == "male"]["survived"].mean() * 100
    )

    female_rate = (
        df[df["sex"] == "female"]["survived"].mean() * 100
    )

    print(f"Male   : {male_rate:.2f}%")
    print(f"Female : {female_rate:.2f}%")

    # -----------------------------
    # Survival Rate by Passenger Class
    # -----------------------------
    print("\nSurvival Rate by Passenger Class")

    for pclass in sorted(df["pclass"].unique()):

        rate = (
            df[df["pclass"] == pclass]["survived"].mean() * 100
        )

        print(f"Class {pclass} : {rate:.2f}%")

    # -----------------------------
    # Survival Rate by Gender + Class
    # -----------------------------
    print("\nSurvival Rate by Gender and Passenger Class")

    for gender in ["female", "male"]:

        for pclass in sorted(df["pclass"].unique()):

            rate = (
                df[
                    (df["sex"] == gender) &
                    (df["pclass"] == pclass)
                ]["survived"].mean() * 100
            )

            print(f"{gender.title()} Class {pclass} : {rate:.2f}%")
                