"""Parameters Panel showing current command parameters"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import re


class ParametersPanel(QWidget):
    """Panel displaying parameters of current G-Code command"""
    
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        
        layout = QVBoxLayout()
        
        # Title
        self.title_label = QLabel("Parameter")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(self.title_label)
        
        # Parameters table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Parameter", "Wert"])
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 100)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def update_parameters(self, line: str):
        """Extract and display parameters from line"""
        self.table.setRowCount(0)
        
        line = line.strip()
        if ';' in line:
            line = line[:line.index(';')]
        
        # Find all parameters (letter followed by number)
        matches = re.finditer(r'([XYZFSTU])\s*([+-]?\d+\.?\d*)', line, re.IGNORECASE)
        
        row = 0
        for match in matches:
            param = match.group(1).upper()
            value = match.group(2)
            
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(param))
            self.table.setItem(row, 1, QTableWidgetItem(value))
            row += 1
