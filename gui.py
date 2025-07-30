from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication,
    QGraphicsDropShadowEffect, QMainWindow
)
from PyQt6.QtCore import Qt, QTimer, QEvent, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QMovie, QPixmap
from jarvis_engine import speak, listen
from command_handler import handle_command


class JarvisWorker(QThread):
    result_signal = pyqtSignal(str)

    def run(self):
        query = listen()
        result = handle_command(query)
        self.result_signal.emit(result)


class JarvisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS 1.0")
        self.setMinimumSize(960, 600)
        self.resize(1080, 720)
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowMinimizeButtonHint |
            Qt.WindowType.WindowMaximizeButtonHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.bg = QLabel(self.central)
        self.bg.setPixmap(QPixmap("assets/jarvis_face_glow.png"))
        self.bg.setScaledContents(True)

        self.container = QWidget(self.central)
        self.container.setStyleSheet("""
            background-color: rgba(10, 10, 10, 180);
            border-radius: 15px;
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor("#00ffff"))
        shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(shadow)

        self.label = QLabel("\U0001F916 Welcome to JARVIS", self.container)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Consolas", 20))
        self.label.setStyleSheet("color: #00ffff;")

        self.face_display = QLabel(self.container)
        self.face_display.setPixmap(QPixmap("assets/jarvis_talk.gif"))
        self.face_display.setScaledContents(True)
        self.face_display.setFixedSize(160, 160)
        self.face_display.hide()

        self.loader = QLabel(self.container)
        self.loader.setFixedSize(64, 64)
        self.loader.setScaledContents(True)
        self.loader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.movie = QMovie("assets/loader_ring.gif")
        self.loader.setMovie(self.movie)
        self.loader.setStyleSheet("background: transparent;")

        self.wave = QLabel(self.container)
        self.wave.setFixedSize(250, 60)
        self.wave.setScaledContents(True)
        self.wave.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wave_movie = QMovie("assets/waveform.gif")
        self.wave.setMovie(self.wave_movie)
        self.wave.hide()

        self.io_label = QLabel("\U0001F501 I/O: Awaiting Command...", self.container)
        self.io_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.io_label.setStyleSheet("color: #aaa; font-size: 13px")

        self.button = QPushButton("\U0001F50A Activate", self.container)
        self.button.setFont(QFont("Consolas", 14))
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #111;
                color: #00ffff;
                border: 2px solid #00ffff;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #00ffff;
                color: #000;
            }
        """)
        self.button.clicked.connect(self.activate_jarvis)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        row = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setSpacing(30)
        row.setLayout(row_layout)

        row_layout.addWidget(self.face_display, alignment=Qt.AlignmentFlag.AlignCenter)
        row_layout.addWidget(self.loader, alignment=Qt.AlignmentFlag.AlignCenter)
        row_layout.addWidget(self.wave, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(row)
        layout.addWidget(self.io_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.container.setLayout(layout)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Resize:
            self.resize_elements()
        return super().eventFilter(obj, event)

    def resize_elements(self):
        w = self.width()
        h = self.height()
        self.bg.setGeometry(0, 0, w, h)
        self.container.setGeometry(w // 4, h // 6, w // 2, int(h / 1.5))

    def activate_jarvis(self):
        self.label.setText("\U0001F399 Listening...")
        self.loader.show()
        self.movie.start()
        self.wave.show()
        self.wave_movie.start()
        self.face_display.show()
        self.worker = JarvisWorker()
        self.worker.result_signal.connect(self.handle_result)
        self.worker.start()

    def handle_result(self, result):
        self.loader.hide()
        self.movie.stop()
        self.wave.hide()
        self.wave_movie.stop()

        if result == "exit":
            self.label.setText("\U0001F44B Exiting JARVIS")
            self.io_label.setText("I/O: Exiting")
            speak("Goodbye")
            QTimer.singleShot(1500, self.close)
        else:
            self.label.setText(result)
            self.io_label.setText(f"I/O: {result}")
            speak(result)