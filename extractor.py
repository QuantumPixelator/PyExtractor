from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                               QWidget, QLineEdit, QFileDialog, QLabel, QTextEdit)
from PySide6.QtCore import Qt
import csv

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

# Main GUI class
class CSVExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("PyExtractor")
        self.resize(400, 300)

        # Main widget and layout
        main_widget = QWidget(self)
        layout = QVBoxLayout()

        # Widgets for the GUI
        self.target_string_label = QLabel("Enter the string to search for:")
        self.target_string_input = QLineEdit()

        self.select_files_btn = QPushButton("Select CSV Files")
        self.select_files_btn.clicked.connect(self.select_files)

        self.extract_btn = QPushButton("Extract Data")
        self.extract_btn.clicked.connect(self.extract_data)

        self.feedback_text = QTextEdit()
        self.feedback_text.setReadOnly(True)

        # Add widgets to layout
        layout.addWidget(self.target_string_label)
        layout.addWidget(self.target_string_input)
        layout.addWidget(self.select_files_btn)
        layout.addWidget(self.extract_btn)
        layout.addWidget(self.feedback_text)

        # Set the layout to the main widget
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Styling
        self.apply_styling()

        # File paths to keep track of selected CSV files
        self.file_paths = []

    def select_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select CSV Files", "", "CSV Files (*.csv)")
        if file_paths:
            self.file_paths = file_paths
            self.feedback_text.append("Files selected!")

    def extract_data(self):
        target_string = self.target_string_input.text()
        if not self.file_paths:
            self.feedback_text.append("No files selected. Please select CSV files to search.")
        elif not target_string:
            self.feedback_text.append("Please enter a target string.")
        else:
            extracted_lines = extract_lines(self.file_paths, target_string)
            if not extracted_lines:
                self.feedback_text.append("No lines found containing the target string.")
            else:
                save_path, _ = QFileDialog.getSaveFileName(self, "Save Extracted Data", "extracted_data.csv", "CSV Files (*.csv)")
                if save_path:
                    save_to_new_csv(extracted_lines, save_path)
                    self.feedback_text.append(f"Data found! Extracted lines saved to {save_path}.")

    def apply_styling(self):
        # A simple, clean styling for the app
        self.setStyleSheet("""
            QWidget {
            background-color: #f5f5f5;
        }
        QPushButton {
            background-color: #A755FF;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            font-size: 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #670DC8;
        }
        QLineEdit, QTextEdit {
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        """)

# Create and run the app
if __name__ == "__main__":
    app = QApplication([])
    window = CSVExtractorApp()
    window.show()
    app.exec()
