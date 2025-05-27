from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel,
    QHBoxLayout, QScrollArea, QComboBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sys
import os
import ast

from .ast_visualizer import ASTVisualizer as PythonVisualizer
from c_code.c_ast_visualizer import CASTVisualizer as CVisualizer


class ASTApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AST Visualizer & Syntax Checker")
        self.resize(1200, 800)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        main_layout = QVBoxLayout()

        
        self.language_selector = QComboBox()
        self.language_selector.addItems(["Python", "C"])
        main_layout.addWidget(QLabel("Select Language:"))
        main_layout.addWidget(self.language_selector)


        self.label = QLabel("Enter Code:")
        main_layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        main_layout.addWidget(self.text_edit)

        
        button_layout = QHBoxLayout()
        self.button = QPushButton("Generate AST")
        self.button.clicked.connect(self.generate_ast)
        button_layout.addWidget(self.button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)

        main_layout.addLayout(button_layout)

        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.image_label)

        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def generate_ast(self):
        code = self.text_edit.toPlainText()
        if not code.strip():
            self.image_label.setText("Please enter valid code.")
            return

        language = self.language_selector.currentText()
        print(f"Selected language: {language}")

        if language == "Python":
    
            try:
                tree = ast.parse(code)
            except SyntaxError as e:
                self.image_label.setText(
                    f"❌ Syntax Error: {e.msg} at line {e.lineno}, column {e.offset}"
                )
                return

            
            try:
                exec(code, {})
            except Exception as e:
                self.image_label.setText(
                    f"❌ Runtime Error: {type(e).__name__} - {str(e)}"
                )
                return

            
            visualizer = PythonVisualizer()
            image_path = visualizer.visualize(code)
        else:  
            
            visualizer = CVisualizer()
            result = visualizer.visualize(code)

            if result.endswith(".png"):
                image_path = result
            else:
                self.image_label.setText(result)
                return

        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.adjustSize()
        else:
            self.image_label.setText("Error: AST image not found.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ASTApp()
    window.show()
    sys.exit(app.exec())
