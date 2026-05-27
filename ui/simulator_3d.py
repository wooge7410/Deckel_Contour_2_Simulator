"""3D CNC Simulator View"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.OpenGL import GL
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math


class Simulator3D(QOpenGLWidget):
    """3D OpenGL visualization of CNC milling"""
    
    def __init__(self):
        super().__init__()
        
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        self.zoom = -10
        
        # Workpiece dimensions (mm)
        self.workpiece_width = 100
        self.workpiece_height = 50
        self.workpiece_depth = 30
        
        # Tool parameters
        self.tool_diameter = 6
        self.tool_length = 60
        
        # Material removed (height map)
        self.height_map = np.zeros((100, 100))
        self.material_height = self.workpiece_depth
        
        # Mouse tracking
        self.last_mouse_x = 0
        self.last_mouse_y = 0
    
    def initializeGL(self):
        """Initialize OpenGL settings"""
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        # Setup lighting
        glLight(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
        glLight(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
        glLight(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
        glLight(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])
    
    def resizeGL(self, w: int, h: int):
        """Handle window resize"""
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (w / h) if h != 0 else 1, 0.1, 500)
        glMatrixMode(GL_MODELVIEW)
    
    def paintGL(self):
        """Render the scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Camera position
        glTranslatef(0, 0, self.zoom)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        glRotatef(self.rotation_z, 0, 0, 1)
        
        # Draw workpiece
        self.draw_workpiece()
        
        # Draw tool
        self.draw_tool()
        
        # Draw axes
        self.draw_axes()
    
    def draw_workpiece(self):
        """Draw the workpiece"""
        glPushMatrix()
        glColor3f(0.8, 0.6, 0.4)  # Brown color
        
        # Draw as a box
        glBegin(GL_QUADS)
        
        # Front face
        glNormal3f(0, 0, 1)
        glVertex3f(-self.workpiece_width/2, -self.workpiece_height/2, self.workpiece_depth/2)
        glVertex3f(self.workpiece_width/2, -self.workpiece_height/2, self.workpiece_depth/2)
        glVertex3f(self.workpiece_width/2, self.workpiece_height/2, self.workpiece_depth/2)
        glVertex3f(-self.workpiece_width/2, self.workpiece_height/2, self.workpiece_depth/2)
        
        # Back face
        glNormal3f(0, 0, -1)
        glVertex3f(-self.workpiece_width/2, -self.workpiece_height/2, -self.workpiece_depth/2)
        glVertex3f(-self.workpiece_width/2, self.workpiece_height/2, -self.workpiece_depth/2)
        glVertex3f(self.workpiece_width/2, self.workpiece_height/2, -self.workpiece_depth/2)
        glVertex3f(self.workpiece_width/2, -self.workpiece_height/2, -self.workpiece_depth/2)
        
        # Top face
        glNormal3f(0, 1, 0)
        glVertex3f(-self.workpiece_width/2, self.workpiece_height/2, -self.workpiece_depth/2)
        glVertex3f(-self.workpiece_width/2, self.workpiece_height/2, self.workpiece_depth/2)
        glVertex3f(self.workpiece_width/2, self.workpiece_height/2, self.workpiece_depth/2)
        glVertex3f(self.workpiece_width/2, self.workpiece_height/2, -self.workpiece_depth/2)
        
        # Bottom face
        glNormal3f(0, -1, 0)
        glVertex3f(-self.workpiece_width/2, -self.workpiece_height/2, -self.workpiece_depth/2)
        glVertex3f(self.workpiece_width/2, -self.workpiece_height/2, -self.workpiece_depth/2)
        glVertex3f(self.workpiece_width/2, -self.workpiece_height/2, self.workpiece_depth/2)
        glVertex3f(-self.workpiece_width/2, -self.workpiece_height/2, self.workpiece_depth/2)
        
        glEnd()
        glPopMatrix()
    
    def draw_tool(self):
        """Draw the cutting tool"""
        glPushMatrix()
        glColor3f(0.5, 0.5, 0.5)  # Gray color
        glTranslatef(0, 0, self.workpiece_depth/2 + self.tool_length/2)
        
        # Draw tool as cylinder
        quad = GLUquadric()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(quad, self.tool_diameter/2, self.tool_diameter/2, self.tool_length, 16, 16)
        
        glPopMatrix()
    
    def draw_axes(self):
        """Draw coordinate axes"""
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        
        # X axis - Red
        glColor3f(1, 0, 0)
        glVertex3f(-50, 0, 0)
        glVertex3f(50, 0, 0)
        
        # Y axis - Green
        glColor3f(0, 1, 0)
        glVertex3f(0, -50, 0)
        glVertex3f(0, 50, 0)
        
        # Z axis - Blue
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, -50)
        glVertex3f(0, 0, 50)
        
        glEnd()
        glEnable(GL_LIGHTING)
    
    def mousePressEvent(self, event):
        """Handle mouse press for rotation"""
        self.last_mouse_x = event.position().x()
        self.last_mouse_y = event.position().y()
    
    def mouseMoveEvent(self, event):
        """Handle mouse movement for rotation"""
        dx = event.position().x() - self.last_mouse_x
        dy = event.position().y() - self.last_mouse_y
        
        self.rotation_y += dx * 0.5
        self.rotation_x += dy * 0.5
        
        self.last_mouse_x = event.position().x()
        self.last_mouse_y = event.position().y()
        
        self.update()
    
    def wheelEvent(self, event):
        """Handle mouse wheel for zoom"""
        self.zoom += event.angleDelta().y() / 120 * 0.5
        self.update()
    
    def update_material(self, x: float, y: float, depth: float):
        """Update material removal at position"""
        # Simple implementation - in real app would use height map
        pass
    
    def set_workpiece_dimensions(self, width: float, height: float, depth: float):
        """Set workpiece dimensions"""
        self.workpiece_width = width
        self.workpiece_height = height
        self.workpiece_depth = depth
        self.update()
    
    def set_tool_parameters(self, diameter: float, length: float):
        """Set tool parameters"""
        self.tool_diameter = diameter
        self.tool_length = length
        self.update()
