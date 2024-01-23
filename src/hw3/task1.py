import pandas as pd
import numpy as np
from prettytable import PrettyTable

def analyze_diabetes_dataset(file_path):
    data = pd.read_csv(file_path)
    n = len(data)
    classes = np.unique(list(data['class!']), return_counts=True)[0]
    samples = np.unique(list(data['class!']), return_counts=True)[1]

    print("Dataset Name: ", 'diabetes.csv')
    print("Number of classes: ", len(classes))
    print("Number of rows: ", n)

    table = PrettyTable()
    table.field_names = ["Class Name", "Percentage"]

    for i in range(len(classes)):    
        table.add_row([classes[i], round((samples[i] / n) * 100, 2)])

    print(table)

file_path = "../../Data/diabetes.csv"
analyze_diabetes_dataset(file_path)