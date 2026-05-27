"""Lexicon Panel for G-Code commands reference"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QTextEdit, QPushButton
from PyQt6.QtCore import Qt
from data.gcode_lexicon import GCODE_COMMANDS


class LexiconPanel(QWidget):
    """Panel displaying G-Code lexicon/reference"""
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nach Befehl suchen (z.B. G01, M30)...")
        self.search_input.textChanged.connect(self.on_search_changed)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Command list
        self.command_list = QListWidget()
        self.command_list.itemClicked.connect(self.on_command_selected)
        layout.addWidget(self.command_list)
        
        # Command details
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        layout.addWidget(self.details_text)
        
        # Populate list
        self.populate_list()
        
        self.setLayout(layout)
    
    def populate_list(self, filter_text: str = ""):
        """Populate command list"""
        self.command_list.clear()
        
        filter_text = filter_text.upper()
        
        for cmd_key, cmd_info in sorted(GCODE_COMMANDS.items()):
            if filter_text == "" or cmd_key.startswith(filter_text):
                item = QListWidgetItem(cmd_key)
                item.setData(Qt.ItemDataRole.UserRole, cmd_key)
                self.command_list.addItem(item)
    
    def on_search_changed(self, text: str):
        """Handle search input changes"""
        self.populate_list(text)
    
    def on_command_selected(self, item: QListWidgetItem):
        """Display command details when selected"""
        command = item.data(Qt.ItemDataRole.UserRole)
        
        if command in GCODE_COMMANDS:
            cmd_info = GCODE_COMMANDS[command]
            
            html = f"""
            <h2>{command} - {cmd_info['name']}</h2>
            
            <h3>Beschreibung</h3>
            <p>{cmd_info['description']}</p>
            
            <h3>Parameter</h3>
            <p>{cmd_info['parameters']}</p>
            
            <h3>Beispiele</h3>
            <pre>{cmd_info['example']}</pre>
            
            <h3>Anmerkungen</h3>
            <p>{cmd_info['notes']}</p>
            
            <h3>Siehe auch</h3>
            <p>{cmd_info['see_also']}</p>
            """
            
            self.details_text.setHtml(html)
