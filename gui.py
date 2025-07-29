from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
from jarvis_engine import speak, listen

class JarvisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("J.A.R.V.I.S.")
        self.setFixedSize(500, 300)
        self.setStyleSheet("background-color: black; color: cyan; font-size: 18px;")

        self.label = QLabel("🔊 Press to Activate JARVIS", alignment=Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("padding: 20px;")

        self.button = QPushButton("🟢 Start Listening")
        self.button.clicked.connect(self.activate_jarvis)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #00FFAA;
                border: none;
                padding: 10px;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #00CC88;
            }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def activate_jarvis(self):
        self.label.setText("⏳ Listening...")
        QTimer.singleShot(100, self.process_command)

    def process_command(self):
        query = listen()
        self.label.setText(f"You said: {query}")
        speak(query if "hello" in query else "Command received.")
