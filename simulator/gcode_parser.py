"""G-Code Parser and Simulator Engine"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class Point:
    """3D Point"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def distance_to(self, other) -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)


@dataclass
class ToolInfo:
    """Tool/Werkzeug Information"""
    diameter: float = 6.0  # mm
    length: float = 60.0   # mm
    flutes: int = 4
    material: str = "HSS"  # High Speed Steel


@dataclass
class MaterialInfo:
    """Rohmaterial Information"""
    width: float = 100.0   # mm
    height: float = 50.0   # mm
    depth: float = 30.0    # mm
    material_type: str = "Aluminum"  # Material type


class GCodeParser:
    """Parser for G-Code commands"""
    
    def __init__(self):
        self.commands = []
        self.current_pos = Point()
        self.absolute_mode = True
        self.metric_mode = True
        self.feed_rate = 100  # mm/min
        self.spindle_speed = 1000  # RPM
        self.spindle_on = False
    
    def parse_line(self, line: str) -> Optional[Dict]:
        """Parse a single G-Code line"""
        # Remove whitespace and comments
        line = line.strip()
        if not line or line.startswith(';'):
            return None
        
        if ';' in line:
            line = line[:line.index(';')]
        
        command = {
            'raw': line,
            'gcode': None,
            'mcode': None,
            'params': {}
        }
        
        # Extract G-code
        g_match = re.search(r'\bG(\d{1,3})\b', line, re.IGNORECASE)
        if g_match:
            command['gcode'] = f"G{g_match.group(1)}"
        
        # Extract M-code
        m_match = re.search(r'\bM(\d{1,3})\b', line, re.IGNORECASE)
        if m_match:
            command['mcode'] = f"M{m_match.group(1)}"
        
        # Extract parameters
        for param in ['X', 'Y', 'Z', 'I', 'J', 'K', 'F', 'S', 'P']:
            param_match = re.search(rf'\b{param}\s*([+-]?\d+\.?\d*)\b', line, re.IGNORECASE)
            if param_match:
                command['params'][param] = float(param_match.group(1))
        
        return command
    
    def parse_program(self, gcode_text: str) -> List[Dict]:
        """Parse entire G-Code program"""
        commands = []
        for line in gcode_text.split('\n'):
            cmd = self.parse_line(line)
            if cmd:
                commands.append(cmd)
        return commands
    
    def execute_command(self, command: Dict) -> bool:
        """Execute a parsed command"""
        if command['gcode'] == 'G00':
            return self._execute_g00(command)
        elif command['gcode'] == 'G01':
            return self._execute_g01(command)
        elif command['gcode'] == 'G02':
            return self._execute_g02(command)
        elif command['gcode'] == 'G03':
            return self._execute_g03(command)
        elif command['gcode'] == 'G20':
            self.metric_mode = False
            return True
        elif command['gcode'] == 'G21':
            self.metric_mode = True
            return True
        elif command['gcode'] == 'G90':
            self.absolute_mode = True
            return True
        elif command['gcode'] == 'G91':
            self.absolute_mode = False
            return True
        elif command['mcode'] == 'M03':
            self.spindle_on = True
            if 'S' in command['params']:
                self.spindle_speed = command['params']['S']
            return True
        elif command['mcode'] == 'M04':
            self.spindle_on = True
            if 'S' in command['params']:
                self.spindle_speed = command['params']['S']
            return True
        elif command['mcode'] == 'M05':
            self.spindle_on = False
            return True
        
        return False
    
    def _execute_g00(self, command: Dict) -> bool:
        """Rapid positioning"""
        new_pos = self._calculate_target_pos(command['params'])
        self.current_pos = new_pos
        return True
    
    def _execute_g01(self, command: Dict) -> bool:
        """Linear interpolation"""
        if 'F' in command['params']:
            self.feed_rate = command['params']['F']
        new_pos = self._calculate_target_pos(command['params'])
        self.current_pos = new_pos
        return True
    
    def _execute_g02(self, command: Dict) -> bool:
        """Circular interpolation clockwise"""
        if 'F' in command['params']:
            self.feed_rate = command['params']['F']
        new_pos = self._calculate_target_pos(command['params'])
        self.current_pos = new_pos
        return True
    
    def _execute_g03(self, command: Dict) -> bool:
        """Circular interpolation counter-clockwise"""
        if 'F' in command['params']:
            self.feed_rate = command['params']['F']
        new_pos = self._calculate_target_pos(command['params'])
        self.current_pos = new_pos
        return True
    
    def _calculate_target_pos(self, params: Dict) -> Point:
        """Calculate target position from parameters"""
        new_pos = Point(
            params.get('X', self.current_pos.x),
            params.get('Y', self.current_pos.y),
            params.get('Z', self.current_pos.z)
        )
        
        if not self.absolute_mode:
            new_pos = self.current_pos + new_pos
        
        return new_pos
