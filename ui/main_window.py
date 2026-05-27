"""Main Application Window"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTabWidget, QDockWidget
)
from PyQt6.QtCore import Qt
from ui.editor import GCodeEditor
from ui.simulator_3d import Simulator3D
from ui.help_panel import HelpPanel
from ui.parameters_panel import ParametersPanel
from ui.lexicon import LexiconPanel


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deckel Contour 2 CNC Simulator")
        self.setGeometry(100, 100, 1600, 900)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        # Create main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create editor and simulator tabs
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_tabs = QTabWidget()
        
        self.editor = GCodeEditor()
        self.simulator_3d = Simulator3D()
        
        left_tabs.addTab(self.editor, "G-Code Editor")
        left_tabs.addTab(self.simulator_3d, "3D Simulation")
        left_layout.addWidget(left_tabs)
        
        splitter.addWidget(left_widget)
        
        # Create right panel with tabs
        right_tabs = QTabWidget()
        self.help_panel = HelpPanel()
        self.parameters_panel = ParametersPanel(self.editor)
        self.lexicon_panel = LexiconPanel()
        
        right_tabs.addTab(self.help_panel, "Hilfe")
        right_tabs.addTab(self.parameters_panel, "Parameter")
        right_tabs.addTab(self.lexicon_panel, "Lexikon")
        
        splitter.addWidget(right_tabs)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
        
        # Connect signals
        self.editor.cursorPositionChanged.connect(self.on_editor_cursor_changed)
        self.editor.textChanged.connect(self.on_editor_text_changed)
        
    def on_editor_cursor_changed(self):
        """Update help when cursor position changes"""
        current_line = self.editor.get_current_line()
        self.help_panel.update_help(current_line)
        self.parameters_panel.update_parameters(current_line)
    
    def on_editor_text_changed(self):
        """Handle text changes in editor"""
        pass
