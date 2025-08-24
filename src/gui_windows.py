import sys
from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    )


class InkanWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inkan")
        self.setFixedSize(600, 400)

def main():
    app = QApplication(sys.argv)
    win = InkanWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
