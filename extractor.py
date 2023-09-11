import csv
import tkinter as tk
from tkinter import filedialog

""" This script will search through any number of CSV files and extract all lines that include the matching string input variable, then save it to a new file """

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window, only need the file dialog to show up
    file_paths = filedialog.askopenfilenames(title="Select CSV Files", filetypes=[("CSV files", "*.csv")])
    return file_paths

def extract_lines(file_paths, target_string):
    extracted_lines = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                for cell in row:
                    if target_string in cell:
                        extracted_lines.append(row)
                        break
    return extracted_lines

def save_to_new_csv(extracted_lines, output_filename):
    with open(output_filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(extracted_lines)

if __name__ == "__main__":
    target_string = input("Enter the string to search for: ")
    file_paths = open_file_dialog()

    if not file_paths:
        print("No files selected, goodbye.")
    else:
        extracted_lines = extract_lines(file_paths, target_string)

        if not extracted_lines:
            print("No lines found containing the target string.")
        else:
            output_filename = "extracted_data.csv"
            save_to_new_csv(extracted_lines, output_filename)
            print(f"Data found! Extracted lines saved to {output_filename}. Goodbye.")
