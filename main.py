from gui import JarvisApp
import sys
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisApp()
    window.show()
    sys.exit(app.exec())
