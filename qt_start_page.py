from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
from worker import Worker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_dialog = None
        self.content = QWidget()
        content_layout = QVBoxLayout(self.content)
        self.lineEdit = QLineEdit()
        content_layout.addWidget(self.lineEdit)
        self.select_button = QPushButton(self.tr("选择文件夹"))
        self.start_button = QPushButton(self.tr("开始整理"))
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.start_button)
        content_layout.addLayout(button_layout)
        self.select_button.clicked.connect(self.open_file_dialog)
        self.start_button.clicked.connect(self.start_worker)
        self.setCentralWidget(self.content)
        self.setWindowTitle(self.tr("ToolBox"))

    @pyqtSlot(str)
    def on_file_selected(self, file: str):
        self.lineEdit.setText(file)

    @pyqtSlot()
    def start_worker(self):
        working_directory = self.lineEdit.text()
        if not os.access(working_directory, os.F_OK | os.R_OK | os.W_OK):
            print(self.tr("working directory not exist or not readable or writable"))
            QMessageBox.warning(self, self.tr("Working directory error"), self.tr("Working directory must be a "
                                                                                  "directory which "
                                                                                  "is readable and writable"))
            return
        print(self.tr("start worker"))
        worker = Worker(working_directory)
        worker.start()

    @pyqtSlot()
    def open_file_dialog(self):
        if self.file_dialog is None:
            self.file_dialog = QFileDialog()
            self.file_dialog.fileSelected.connect(self.on_file_selected)
            self.file_dialog.selectFile("/home/astrea/Desktop/test_folder")
            self.file_dialog.setFileMode(QFileDialog.Directory)
        result = self.file_dialog.exec()
        if not result:
            print(self.tr("select error"))


a = QApplication(sys.argv)
w = MainWindow()
w.resize(400, 100)
w.show()
a.exec()
