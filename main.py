#!/usr/bin/env python3
"""Deckel Contour 2 CNC Simulator - Main Entry Point"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Initialize and run the application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Deckel Contour 2 CNC Simulator")
    app.setApplicationVersion("1.0.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
