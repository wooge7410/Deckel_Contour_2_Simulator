"""Help Panel for displaying G-Code command help"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtCore import Qt
from data.gcode_lexicon import GCODE_COMMANDS


class HelpPanel(QWidget):
    """Panel displaying help for current G-Code command"""
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        # Title
        self.title_label = QLabel("Keine Eingabe")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.title_label)
        
        # Help text
        self.help_text = QTextEdit()
        self.help_text.setReadOnly(True)
        layout.addWidget(self.help_text)
        
        self.setLayout(layout)
    
    def update_help(self, line: str):
        """Update help based on current line"""
        import re
        
        # Extract G or M code
        match = re.search(r'\b([GM]\d{1,3})\b', line, re.IGNORECASE)
        if not match:
            self.title_label.setText("Keine Eingabe")
            self.help_text.setText("")
            return
        
        command = match.group(1).upper()
        
        if command in GCODE_COMMANDS:
            cmd_info = GCODE_COMMANDS[command]
            self.title_label.setText(command)
            
            help_html = f"""
            <h3>{cmd_info['name']}</h3>
            <p><b>Beschreibung:</b> {cmd_info['description']}</p>
            <p><b>Parameter:</b> {cmd_info['parameters']}</p>
            <p><b>Beispiel:</b> <code>{cmd_info['example']}</code></p>
            <p><b>Anmerkungen:</b> {cmd_info['notes']}</p>
            """
            self.help_text.setHtml(help_html)
        else:
            self.title_label.setText(command)
            self.help_text.setText("Befehl nicht in Lexikon gefunden.")
