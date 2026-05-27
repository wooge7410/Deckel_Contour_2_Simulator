"""Tool and Material Configuration Dialog"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, 
    QDoubleSpinBox, QComboBox, QPushButton, QGroupBox
)
from simulator.gcode_parser import ToolInfo, MaterialInfo


class ToolConfigDialog(QDialog):
    """Dialog for configuring tool parameters"""
    
    def __init__(self, tool_info: ToolInfo = None):
        super().__init__()
        self.setWindowTitle("Werkzeug Konfiguration")
        self.setGeometry(200, 200, 400, 300)
        
        if tool_info is None:
            tool_info = ToolInfo()
        
        self.tool_info = tool_info
        
        layout = QVBoxLayout()
        
        # Diameter
        diameter_layout = QHBoxLayout()
        diameter_layout.addWidget(QLabel("Durchmesser (mm):"))
        self.diameter_spin = QDoubleSpinBox()
        self.diameter_spin.setValue(tool_info.diameter)
        self.diameter_spin.setRange(1, 100)
        self.diameter_spin.setSingleStep(0.1)
        diameter_layout.addWidget(self.diameter_spin)
        layout.addLayout(diameter_layout)
        
        # Length
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel("Länge (mm):"))
        self.length_spin = QDoubleSpinBox()
        self.length_spin.setValue(tool_info.length)
        self.length_spin.setRange(10, 200)
        self.length_spin.setSingleStep(1)
        length_layout.addWidget(self.length_spin)
        layout.addLayout(length_layout)
        
        # Flutes
        flutes_layout = QHBoxLayout()
        flutes_layout.addWidget(QLabel("Schneiden:"))
        self.flutes_spin = QSpinBox()
        self.flutes_spin.setValue(tool_info.flutes)
        self.flutes_spin.setRange(1, 12)
        flutes_layout.addWidget(self.flutes_spin)
        layout.addLayout(flutes_layout)
        
        # Material
        material_layout = QHBoxLayout()
        material_layout.addWidget(QLabel("Material:"))
        self.material_combo = QComboBox()
        self.material_combo.addItems(["HSS", "Carbide", "Ceramic"])
        self.material_combo.setCurrentText(tool_info.material)
        material_layout.addWidget(self.material_combo)
        layout.addLayout(material_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Abbrechen")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_tool_info(self) -> ToolInfo:
        """Get configured tool info"""
        return ToolInfo(
            diameter=self.diameter_spin.value(),
            length=self.length_spin.value(),
            flutes=self.flutes_spin.value(),
            material=self.material_combo.currentText()
        )


class MaterialConfigDialog(QDialog):
    """Dialog for configuring material parameters"""
    
    def __init__(self, material_info: MaterialInfo = None):
        super().__init__()
        self.setWindowTitle("Rohmaterial Konfiguration")
        self.setGeometry(200, 200, 400, 350)
        
        if material_info is None:
            material_info = MaterialInfo()
        
        self.material_info = material_info
        
        layout = QVBoxLayout()
        
        # Width
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Breite (mm):"))
        self.width_spin = QDoubleSpinBox()
        self.width_spin.setValue(material_info.width)
        self.width_spin.setRange(10, 1000)
        self.width_spin.setSingleStep(10)
        width_layout.addWidget(self.width_spin)
        layout.addLayout(width_layout)
        
        # Height
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Höhe (mm):"))
        self.height_spin = QDoubleSpinBox()
        self.height_spin.setValue(material_info.height)
        self.height_spin.setRange(10, 1000)
        self.height_spin.setSingleStep(10)
        height_layout.addWidget(self.height_spin)
        layout.addLayout(height_layout)
        
        # Depth
        depth_layout = QHBoxLayout()
        depth_layout.addWidget(QLabel("Tiefe (mm):"))
        self.depth_spin = QDoubleSpinBox()
        self.depth_spin.setValue(material_info.depth)
        self.depth_spin.setRange(10, 1000)
        self.depth_spin.setSingleStep(10)
        depth_layout.addWidget(self.depth_spin)
        layout.addLayout(depth_layout)
        
        # Material Type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Material:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Aluminum", "Steel", "Brass", "Copper", "Wood"])
        self.type_combo.setCurrentText(material_info.material_type)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Abbrechen")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_material_info(self) -> MaterialInfo:
        """Get configured material info"""
        return MaterialInfo(
            width=self.width_spin.value(),
            height=self.height_spin.value(),
            depth=self.depth_spin.value(),
            material_type=self.type_combo.currentText()
        )
