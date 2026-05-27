"""G-Code Commands Lexicon/Reference Data"""

GCODE_COMMANDS = {
    "G00": {
        "name": "Rapid Positioning",
        "description": "Schnelle Positionierung ohne Material zu zerspanen. Die Vorschub ist Maximum (Maschinenspeed).",
        "parameters": "X, Y, Z (Zielkoordinaten), optional: I, J, K",
        "example": "G00 X100 Y50 Z10",
        "notes": "Dies ist die schnellste Bewegung ohne Zerspanung. Meist wird dies zum Positionieren verwendet.",
        "see_also": "G01, G02, G03"
    },
    "G01": {
        "name": "Linear Interpolation",
        "description": "Lineare Interpolation mit eingestelltem Vorschub. Material wird mit konstanter Geschwindigkeit zerspant.",
        "parameters": "X, Y, Z (Zielkoordinaten), F (Vorschub in mm/min)",
        "example": "G01 X100 Y50 Z-5 F100",
        "notes": "Die Schnittkraft ist konstant. Dies ist der Standardbefehl für das Zerspanung.",
        "see_also": "G00, G02, G03"
    },
    "G02": {
        "name": "Circular Interpolation Clockwise",
        "description": "Kreisförmige Interpolation im Uhrzeigersinn.",
        "parameters": "X, Y, Z (Endpunkt), I, J, K (Mittelpunkt-Offset), F (Vorschub)",
        "example": "G02 X100 Y100 I50 J50 F100",
        "notes": "I, J sind Offsets vom aktuellen Punkt zum Kreismittelpunkt.",
        "see_also": "G01, G03"
    },
    "G03": {
        "name": "Circular Interpolation Counter-Clockwise",
        "description": "Kreisförmige Interpolation gegen den Uhrzeigersinn.",
        "parameters": "X, Y, Z (Endpunkt), I, J, K (Mittelpunkt-Offset), F (Vorschub)",
        "example": "G03 X100 Y100 I50 J50 F100",
        "notes": "Ähnlich wie G02, aber in entgegengesetzter Richtung.",
        "see_also": "G01, G02"
    },
    "G04": {
        "name": "Dwell",
        "description": "Verweilzeit/Pause. Die Maschine bleibt für die angegebene Zeit stehen.",
        "parameters": "P (Zeit in Millisekunden) oder X (Zeit in Sekunden)",
        "example": "G04 P1000",
        "notes": "Nützlich für Stabilisierung oder Wartezeiten.",
        "see_also": "M00, M01"
    },
    "G20": {
        "name": "Inch Mode",
        "description": "Schaltet in Zoll-Modus (Imperial Units).",
        "parameters": "Keine",
        "example": "G20",
        "notes": "Alle nachfolgenden Koordinaten werden in Zoll interpretiert.",
        "see_also": "G21"
    },
    "G21": {
        "name": "Metric Mode",
        "description": "Schaltet in Millimeter-Modus (Metric Units).",
        "parameters": "Keine",
        "example": "G21",
        "notes": "Alle nachfolgenden Koordinaten werden in Millimetern interpretiert.",
        "see_also": "G20"
    },
    "G90": {
        "name": "Absolute Positioning",
        "description": "Absolute Positionierung. Koordinaten beziehen sich auf den Ursprung.",
        "parameters": "Keine",
        "example": "G90",
        "notes": "Dies ist normalerweise der Standardmodus.",
        "see_also": "G91"
    },
    "G91": {
        "name": "Incremental Positioning",
        "description": "Inkrementale Positionierung. Koordinaten sind relativ zur aktuellen Position.",
        "parameters": "Keine",
        "example": "G91",
        "notes": "Nächste Bewegungen sind relativ.",
        "see_also": "G90"
    },
    "M00": {
        "name": "Program Stop",
        "description": "Stoppt das Programm. Der Benutzer kann es mit START fortsetzen.",
        "parameters": "Keine",
        "example": "M00",
        "notes": "Programmpause mit Benutzereingriff.",
        "see_also": "M01, M02, M30"
    },
    "M01": {
        "name": "Optional Stop",
        "description": "Optionaler Stopp. Stoppt nur, wenn eine Stoppfunktion aktiviert ist.",
        "parameters": "Keine",
        "example": "M01",
        "notes": "Wird oft für Werkzeugwechsel verwendet.",
        "see_also": "M00, M02, M30"
    },
    "M02": {
        "name": "Program End",
        "description": "Beendet das Programm.",
        "parameters": "Keine",
        "example": "M02",
        "notes": "Programm wird beendet ohne Spindel zu stoppen.",
        "see_also": "M00, M01, M30"
    },
    "M03": {
        "name": "Spindle On (Clockwise)",
        "description": "Startet die Spindel im Uhrzeigersinn.",
        "parameters": "S (Drehzahl in U/min)",
        "example": "M03 S1500",
        "notes": "Vor dem Bohren/Fräsen immer aktivieren.",
        "see_also": "M04, M05"
    },
    "M04": {
        "name": "Spindle On (Counter-Clockwise)",
        "description": "Startet die Spindel gegen den Uhrzeigersinn.",
        "parameters": "S (Drehzahl in U/min)",
        "example": "M04 S1500",
        "notes": "Selten verwendet, normalerweise M03.",
        "see_also": "M03, M05"
    },
    "M05": {
        "name": "Spindle Off",
        "description": "Stoppt die Spindel.",
        "parameters": "Keine",
        "example": "M05",
        "notes": "Nach dem Fertigstellen oder zum Werkzeugwechsel.",
        "see_also": "M03, M04"
    },
    "M30": {
        "name": "Program End and Rewind",
        "description": "Beendet das Programm und setzt es zurück.",
        "parameters": "Keine",
        "example": "M30",
        "notes": "Stoppt Spindel, schaltet aus und positioniert zum Anfang.",
        "see_also": "M00, M01, M02"
    },
    "F": {
        "name": "Feed Rate",
        "description": "Setzt die Vorschubgeschwindigkeit.",
        "parameters": "Numerischer Wert in mm/min",
        "example": "F100 (100 mm/min)",
        "notes": "Wird mit G01, G02, G03 verwendet. Höher = schneller.",
        "see_also": "G00, G01"
    },
    "S": {
        "name": "Spindle Speed",
        "description": "Setzt die Spindeldrehzahl.",
        "parameters": "Numerischer Wert in U/min (Umdrehungen pro Minute)",
        "example": "S1500 (1500 U/min)",
        "notes": "Wird mit M03/M04 verwendet. Je nach Werkzeug anpassen.",
        "see_also": "M03, M04, M05"
    },
}
