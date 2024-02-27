import csv
from collections import defaultdict

def analyze_csv(file_path):
    class_counts = defaultdict(int)
    total_rows = 0

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            class_label = row[-1]  # Assuming 'class' is the last column
            class_counts[class_label] += 1
            total_rows += 1

    percentages = {cls: (count / total_rows) * 100 for cls, count in class_counts.items()}
    return class_counts, percentages

def display_table(dataset_name, counts, percentages):
    print(f"{dataset_name} Dataset:")
    print("-" * 52)
    print(f"{'Class':<30}{'Count':<10}{'Percentage'}")
    print("-" * 52)
    for cls, count in counts.items():
        print(f"{cls:<30}{count:<10}{format(percentages[cls], '.2f')}%")
    print()

def display():
    # Example usage
    diabetes_counts, diabetes_percentages = analyze_csv('./data/diabetes.csv')
    soybean_counts, soybean_percentages = analyze_csv('./data/soybean.csv')

    # Display results in table format
    display_table("Diabetes", diabetes_counts, diabetes_percentages)
    display_table("Soybean", soybean_counts, soybean_percentages)


if __name__=="__main__":
    display()