import os
import hashlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QWidget, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class DuplicateFinderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Duplicate File Finder")
        self.setGeometry(100, 100, 500, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.select_folder_button = QPushButton("Select Folder", self)
        self.select_folder_button.clicked.connect(self.select_folder)
        self.layout.addWidget(self.select_folder_button)

        self.scan_button = QPushButton("Scan for Duplicates", self)
        self.scan_button.clicked.connect(self.scan_duplicates)
        self.layout.addWidget(self.scan_button)

        self.duplicate_list = QTextEdit(self)
        self.layout.addWidget(self.duplicate_list)

        self.delete_button = QPushButton("Delete Duplicates", self)
        self.delete_button.clicked.connect(self.delete_duplicates)
        self.layout.addWidget(self.delete_button)

        self.watermark_label = QLabel("Made with love by Arun ❤️", self)
        self.watermark_label.setFont(QFont("Times New Roman", 10))
        self.watermark_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.watermark_label)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.selected_folder = None
        self.file_hashes = {}
        self.duplicates = []

    def select_folder(self):
        self.selected_folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if self.selected_folder:
            self.duplicate_list.clear()
            self.file_hashes.clear()
            self.duplicates.clear()

    def scan_duplicates(self):
        if self.selected_folder:
            self.file_hashes.clear()
            self.duplicates.clear()

            for root, dirs, files in os.walk(self.selected_folder):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    file_hash = self.calculate_hash(file_path)

                    if file_hash in self.file_hashes:
                        self.duplicates.append((file_path, self.file_hashes[file_hash]))
                    else:
                        self.file_hashes[file_hash] = file_path

            if self.duplicates:
                self.duplicate_list.clear()
                for duplicate in self.duplicates:
                    self.duplicate_list.append(f"Duplicate 1: {duplicate[0]}\nDuplicate 2: {duplicate[1]}")
            else:
                self.duplicate_list.setPlainText("No duplicates found.")
        else:
            self.duplicate_list.setPlainText("Please select a folder first.")

    def calculate_hash(self, file_path):
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(65536)  # 64KB chunks
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()

    def delete_duplicates(self):
        if self.selected_folder and self.duplicates:
            for duplicate_pair in self.duplicates:
                try:
                    for file_path in duplicate_pair:
                        os.remove(file_path)
                        self.duplicate_list.append(f"Deleted: {file_path}")
                except Exception as e:
                    self.duplicate_list.append(f"Error deleting {file_path}: {e}")
            self.duplicates.clear()
        else:
            self.duplicate_list.setPlainText("No duplicates to delete.")

if __name__ == "__main__":
    app = QApplication([])
    window = DuplicateFinderApp()
    window.show()
    app.exec_()
