# Deckel Contour 2 CNC-Simulator

Ein umfassender Python-basierter Simulator für CNC-Fräsmaschinen mit Deckel Contour 2 Steuerung.

## Features

- **G-Code Editor** mit Syntaxhighlighting
- **Parametrier-Hilfe** für G-Code Befehle (Overlay bei Eingabe)
- **Hilfe-Lexikon** mit allen G-Code Befehlen und Beispielen
- **3D-Simulation** des Zerspanungsvorgangs
- Werkzeuginformationen und Material-Maßen Eingabe
- Visuelle Darstellung des Fräsprozesses
- Echtzeit-Simulation mit Pausierung und Schritt-für-Schritt Ausführung

## Installation

```bash
pip install -r requirements.txt
```

## Verwendung

```bash
python main.py
```

## Struktur

```
.
├── main.py                     # Haupteinstiegspunkt
├── requirements.txt            # Python Abhängigkeiten
├── ui/                         # Qt GUI Komponenten
│   ├── main_window.py         # Hauptfenster
│   ├── editor.py              # G-Code Editor mit Syntaxhighlighting
│   ├── simulator_3d.py        # OpenGL 3D Simulator
│   ├── help_panel.py          # Hilfe-Panel
│   ├── parameters_panel.py    # Parameter-Anzeige
│   ├── lexicon.py             # Befehlslexikon
│   ├── config_dialogs.py      # Konfigurations-Dialoge
│   └── simulation_controller.py # Simulations-Steuerung
├── simulator/                 # CNC-Simulationslogik
│   ├── gcode_parser.py        # G-Code Parser und Datenstrukturen
│   └── __init__.py
├── data/                      # Daten und Ressourcen
│   ├── gcode_lexicon.py       # G-Code Befehlsdefinitionen
│   └── __init__.py
└── README.md
```

## Unterstützte G-Code Befehle

### Bewegungsbefehle
- **G00** - Rapid Positioning (Schnellfahrt)
- **G01** - Linear Interpolation (Lineare Interpolation)
- **G02** - Circular Interpolation Clockwise (Kreisfahrt CW)
- **G03** - Circular Interpolation Counter-Clockwise (Kreisfahrt CCW)
- **G04** - Dwell (Verweilzeit)

### Koordinatensystem
- **G20** - Inch Mode
- **G21** - Metric Mode
- **G90** - Absolute Positioning
- **G91** - Incremental Positioning

### Spindelsteuerung
- **M03** - Spindle On (CW)
- **M04** - Spindle On (CCW)
- **M05** - Spindle Off

### Programmsteuerung
- **M00** - Program Stop
- **M01** - Optional Stop
- **M02** - Program End
- **M30** - Program End and Rewind

## Parameter

- **X, Y, Z** - Koordinaten
- **F** - Vorschub (mm/min)
- **S** - Spindeldrehzahl (U/min)
- **I, J, K** - Offset für Kreisinterpolation
- **P** - Zeit/Dauer

## Verwendungsbeispiel

```gcode
G21         ; Metric Mode
G90         ; Absolute Positioning
G00 X10 Y10 Z5  ; Schnellfahrt zur Position
M03 S1500   ; Spindel starten, 1500 U/min
G01 X50 Y50 Z-5 F100  ; Lineare Interpolation mit Vorschub
G01 X50 Y10 Z-5 F100
M05         ; Spindel stoppen
G00 Z10     ; Rückfahrt
M30         ; Programm Ende
```

## Technologien

- **Python 3.8+**
- **PyQt6** - GUI Framework
- **OpenGL** - 3D Visualisierung
- **NumPy** - Numerische Berechnungen

## Lizenz

MIT
