"""Simulation Controller - Manages simulation playback and interaction"""

from PyQt6.QtCore import QTimer, pyqtSignal, QObject
from simulator.gcode_parser import GCodeParser, Point
from typing import List, Dict, Optional


class SimulationController(QObject):
    """Controls G-Code simulation playback"""
    
    # Signals
    command_executed = pyqtSignal(dict)  # Emitted when a command is executed
    simulation_started = pyqtSignal()
    simulation_paused = pyqtSignal()
    simulation_stopped = pyqtSignal()
    simulation_finished = pyqtSignal()
    position_changed = pyqtSignal(Point)  # Current tool position
    error_occurred = pyqtSignal(str)  # Error message
    progress_updated = pyqtSignal(int, int)  # Current command index, total commands
    
    def __init__(self):
        super().__init__()
        self.parser = GCodeParser()
        self.commands: List[Dict] = []
        self.current_command_index = 0
        self.is_running = False
        self.is_paused = False
        
        # Timer for step-by-step execution
        self.timer = QTimer()
        self.timer.timeout.connect(self._execute_next_command)
        self.execution_speed = 500  # ms between commands
    
    def load_gcode(self, gcode_text: str) -> bool:
        """Load and parse G-Code"""
        try:
            self.commands = self.parser.parse_program(gcode_text)
            self.current_command_index = 0
            return len(self.commands) > 0
        except Exception as e:
            self.error_occurred.emit(f"Parse Error: {str(e)}")
            return False
    
    def start_simulation(self):
        """Start simulation playback"""
        if not self.commands:
            self.error_occurred.emit("No G-Code loaded")
            return
        
        self.is_running = True
        self.is_paused = False
        self.current_command_index = 0
        self.simulation_started.emit()
        self.timer.start(self.execution_speed)
    
    def pause_simulation(self):
        """Pause simulation playback"""
        if self.is_running:
            self.timer.stop()
            self.is_paused = True
            self.simulation_paused.emit()
    
    def resume_simulation(self):
        """Resume simulation playback"""
        if self.is_paused:
            self.is_paused = False
            self.timer.start(self.execution_speed)
    
    def stop_simulation(self):
        """Stop simulation and reset"""
        self.timer.stop()
        self.is_running = False
        self.is_paused = False
        self.current_command_index = 0
        self.simulation_stopped.emit()
    
    def step_forward(self):
        """Execute one command step"""
        self._execute_next_command()
    
    def step_backward(self):
        """Go back one command (reset state)"""
        if self.current_command_index > 0:
            self.current_command_index -= 1
            # Reset to beginning and re-execute up to previous command
            self.parser = GCodeParser()
            for i in range(self.current_command_index):
                self.parser.execute_command(self.commands[i])
            self.position_changed.emit(self.parser.current_pos)
            self.progress_updated.emit(self.current_command_index, len(self.commands))
    
    def set_execution_speed(self, speed_ms: int):
        """Set delay between command execution (in milliseconds)"""
        self.execution_speed = max(10, speed_ms)  # Minimum 10ms
        if self.timer.isActive():
            self.timer.setInterval(self.execution_speed)
    
    def get_current_position(self) -> Point:
        """Get current tool position"""
        return self.parser.current_pos
    
    def get_current_command_info(self) -> Optional[Dict]:
        """Get info about current command"""
        if 0 <= self.current_command_index < len(self.commands):
            return self.commands[self.current_command_index]
        return None
    
    def _execute_next_command(self):
        """Execute the next command in sequence"""
        if self.current_command_index >= len(self.commands):
            self.timer.stop()
            self.is_running = False
            self.simulation_finished.emit()
            return
        
        command = self.commands[self.current_command_index]
        
        try:
            self.parser.execute_command(command)
            self.command_executed.emit(command)
            self.position_changed.emit(self.parser.current_pos)
            self.progress_updated.emit(self.current_command_index + 1, len(self.commands))
            self.current_command_index += 1
        except Exception as e:
            self.error_occurred.emit(f"Execution Error: {str(e)}")
            self.stop_simulation()
