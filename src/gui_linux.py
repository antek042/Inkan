import sys
import os
import shutil
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QMessageBox,
)
import disk_utils
import app_utils


class InkanWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inkan")
        self.setFixedSize(200, 150)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.devices_dict = disk_utils.get_devices_dict("Linux")

        self.devices_combo = QComboBox()
        for name, device in self.devices_dict.items():
            self.devices_combo.addItem(name, device)
        layout.addWidget(self.devices_combo)

        self.restore_button = QPushButton("Restore my data!")
        self.restore_button.clicked.connect(self.on_restore_button_clicked)
        layout.addWidget(self.restore_button)

    def on_restore_button_clicked(self):
        index = self.devices_combo.currentIndex()
        if index == -1:
            QMessageBox.warning(self, "Błąd", "No device selected")
            return

        device = self.devices_combo.itemData(index)

        try:
            files = os.listdir(device)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error opening {device}: {e}")
            return

        for file in files:
            if file.endswith(".tar.zst"):
                target = os.path.join(os.path.expanduser("~"), file.split(".")[0])
                disk_utils.decompress_folder(os.path.join(device, file), target)

            elif file.endswith((".png", ".jpg")):
                wallpaper_path = os.path.join(
                    os.path.expanduser("~"), f".local/share/backgrounds/{file}"
                )
                shutil.move(os.path.join(device, file), wallpaper_path)
                disk_utils.set_wallpaper(wallpaper_path)

            elif file == "apps.txt":
                with open(os.path.join(device, file), "r") as f:
                    apps = [line.strip() for line in f]
                for app in apps:
                    if name := app_utils.search_for_app(app):
                        app_utils.download_from_flathub(name)
                    elif name := app_utils.search_for_alternatives(app):
                        app_utils.download_from_flathub(name)

        QMessageBox.information(
            self, "Success", "All files decompressed and copied. Hello Linux!"
        )


def main():
    app = QApplication(sys.argv)
    win = InkanWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
