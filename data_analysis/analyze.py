import pandas as pd
import matplotlib.pyplot as plt
import difflib

# Завантаження даних
file_path = r"../web-scraping-data-analysis-djinni/vacancies.csv"
data_frame = pd.read_csv(file_path)

# Перетворення технологій у нижній регістр
data_frame["technologies"] = data_frame["technologies"].str.lower()

# Розділення технологій у окремі рядки
technologies_series = (
    data_frame["technologies"]
    .str.split(",\s*", expand=True)
    .stack()
    .reset_index(level=1, drop=True)
    .rename("technology")
)
data_frame_split = data_frame.drop("technologies", axis=1).join(technologies_series)

# Групування схожих технологій
grouped_technologies = {}
for technology in data_frame_split["technology"].unique():
    similar_technology = difflib.get_close_matches(
        technology, grouped_technologies.keys(), n=1, cutoff=0.8
    )
    if similar_technology:
        grouped_technologies[similar_technology[0]] += data_frame_split[
            data_frame_split["technology"] == technology
        ].shape[0]
    else:
        grouped_technologies[technology] = (
            data_frame_split[data_frame_split["technology"] == technology].shape[0]
        )

# Створення серії з кількістю технологій
technology_counts = pd.Series(grouped_technologies)
technology_counts.sort_values(ascending=False, inplace=True)

# Візуалізація даних
plt.figure(figsize=(10, 6))
technology_counts.head(30).plot(kind="bar", color="skyblue")
plt.title("Top 30 Popular Technologies in Job Vacancies")
plt.xlabel("Technology")
plt.ylabel("Count")
plt.xticks(rotation=90, ha="right")
plt.tight_layout()
plt.show()
