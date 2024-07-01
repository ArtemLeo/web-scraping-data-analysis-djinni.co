import pandas as pd
import matplotlib.pyplot as plt
import difflib

file_path = r"../scrape_djinny/vacancies.csv"
df = pd.read_csv(file_path)

df["technologies"] = df["technologies"].str.lower()

df_technologies = (
    df["technologies"]
    .str.split(",\s*", expand=True)
    .stack()
    .reset_index(level=1, drop=True)
    .rename("technology")
)
df_split = df.drop("technologies", axis=1).join(df_technologies)

grouped_technologies = {}
for tech in df_split["technology"].unique():
    similar_tech = difflib.get_close_matches(
        tech, grouped_technologies.keys(), n=1, cutoff=0.8
    )
    if similar_tech:
        grouped_technologies[similar_tech[0]] += df_split[
            df_split["technology"] == tech
        ].shape[0]
    else:
        grouped_technologies[tech] = (
            df_split[df_split["technology"] == tech].shape
        )[0]


technology_counts = pd.Series(grouped_technologies)
technology_counts.sort_values(ascending=False, inplace=True)
plt.figure(figsize=(10, 6))
technology_counts.head(30).plot(kind="bar", color="skyblue")
plt.title("Top 30 Popular Technologies in Job Vacancies")
plt.xlabel("Technology")
plt.ylabel("Count")
plt.xticks(rotation=90, ha="right")
plt.tight_layout()
plt.show()
