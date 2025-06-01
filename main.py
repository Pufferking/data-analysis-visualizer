import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def clean_and_analyze_csv(file_path):
    # Try loading with UTF-8, fall back to Latin-1 if encoding fails
    try:
        df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="latin1", on_bad_lines="skip")

    # Remove duplicates
    df = df.drop_duplicates()

    # Clean column names: strip spaces and replace with underscores
    df.columns = [col.strip().replace(" ", "_") for col in df.columns]

    # Fill missing values temporarily for analysis (optional customization)
    df[df.select_dtypes(include="object").columns] = df.select_dtypes(include="object").fillna("-")

    # Convert 'Age' column to numeric if it exists
    if "Age" in df.columns:
        df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

    # Convert 'Joined_Date' column to datetime if it exists
    if "Joined_Date" in df.columns:
        df["Joined_Date"] = pd.to_datetime(df["Joined_Date"], errors="coerce")

    # Show Data Info
    print("\nData Info:")
    print(df.info())

    # Show Descriptive Statistics
    print("\nDescriptive Statistics:")
    print(df.describe(include='all'))

    # --- Visualizations ---

    # 1. Score Distribution (if 'Score' exists)
    if "Score" in df.columns:
        sns.histplot(df["Score"].dropna(), kde=True)
        plt.title("Score Distribution")
        plt.savefig("score_distribution.png")
        plt.close()

    # 2. Count by City (if 'City' exists)
    if "City" in df.columns:
        sns.countplot(data=df, x="City")
        plt.title("Count by City")
        plt.xticks(rotation=45)
        plt.savefig("city_counts.png")
        plt.close()

    # 3. Timeline of Join Dates (if 'Joined_Date' exists)
    if "Joined_Date" in df.columns:
        df["Join_Year"] = df["Joined_Date"].dt.year
        sns.countplot(data=df, x="Join_Year")
        plt.title("Join Year Distribution")
        plt.savefig("join_years.png")
        plt.close()

    # Save cleaned CSV
    df.to_csv("cleaned_sample.csv", index=False)
    print("\nCleaned CSV saved as 'cleaned_sample.csv'")
    print("Visualizations saved as PNG files.")

# Run the script
if __name__ == "__main__":
    clean_and_analyze_csv("sample.csv")
