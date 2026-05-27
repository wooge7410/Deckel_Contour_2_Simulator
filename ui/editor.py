"""GCode Editor with Syntax Highlighting"""

from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout
from PyQt6.QtGui import QSyntaxHighlighter, QTextDocument, QFont, QColor, QTextCharFormat
from PyQt6.QtCore import Qt, pyqtSignal
import re


class GCodeSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for G-Code"""
    
    def __init__(self, document: QTextDocument):
        super().__init__(document)
        
        # G-Code command format
        self.g_code_format = QTextCharFormat()
        self.g_code_format.setForeground(QColor(0, 0, 255))  # Blue
        self.g_code_format.setFontWeight(700)  # Bold
        
        # Parameter format
        self.parameter_format = QTextCharFormat()
        self.parameter_format.setForeground(QColor(255, 0, 0))  # Red
        
        # Value format
        self.value_format = QTextCharFormat()
        self.value_format.setForeground(QColor(0, 128, 0))  # Green
        
        # Comment format
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(128, 128, 128))  # Gray
        self.comment_format.setFontItalic(True)
    
    def highlightBlock(self, text: str):
        """Highlight a block of text"""
        # Remove comments
        if ';' in text:
            comment_start = text.index(';')
            self.setFormat(comment_start, len(text) - comment_start, self.comment_format)
            text = text[:comment_start]
        
        # Highlight G-codes (G followed by number)
        for match in re.finditer(r'\bG\d{1,3}\b', text, re.IGNORECASE):
            self.setFormat(match.start(), match.end() - match.start(), self.g_code_format)
        
        # Highlight M-codes
        for match in re.finditer(r'\bM\d{1,3}\b', text, re.IGNORECASE):
            self.setFormat(match.start(), match.end() - match.start(), self.g_code_format)
        
        # Highlight parameters (X, Y, Z, F, S, etc.)
        for match in re.finditer(r'\b[XYZFSTU]\s*[+-]?\d+\.?\d*\b', text, re.IGNORECASE):
            # Find the parameter letter
            param_match = re.match(r'\b([XYZFSTU])', match.group(), re.IGNORECASE)
            if param_match:
                self.setFormat(match.start(), 1, self.parameter_format)
                self.setFormat(match.start() + 1, match.end() - match.start() - 1, self.value_format)


class GCodeEditor(QPlainTextEdit):
    """G-Code editor with syntax highlighting"""
    
    cursorPositionChanged = pyqtSignal()
    textChanged = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Set font
        font = QFont("Courier New")
        font.setPointSize(10)
        self.setFont(font)
        
        # Create and set syntax highlighter
        self.highlighter = GCodeSyntaxHighlighter(self.document())
        
        # Settings
        self.setTabStopDistance(40)
        
        # Connect signals
        self.cursorPositionChanged.connect(self._on_cursor_position_changed)
        self.textChanged.connect(self._on_text_changed)
    
    def _on_cursor_position_changed(self):
        """Emit custom signal when cursor changes"""
        self.cursorPositionChanged.emit()
    
    def _on_text_changed(self):
        """Emit custom signal when text changes"""
        self.textChanged.emit()
    
    def get_current_line(self) -> str:
        """Get the current line at cursor position"""
        cursor = self.textCursor()
        block = cursor.block()
        return block.text()
    
    def get_current_command(self) -> str:
        """Extract G-code command from current line"""
        line = self.get_current_line().strip()
        if ';' in line:
            line = line[:line.index(';')]
        
        # Extract first command (G or M code)
        match = re.search(r'\b([GM]\d{1,3})\b', line, re.IGNORECASE)
        if match:
            return match.group(1).upper()
        return ""
    
    def get_line_number(self) -> int:
        """Get current line number"""
        return self.textCursor().blockNumber() + 1
