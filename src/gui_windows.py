import sys
import os
import shutil
from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QVBoxLayout,
    QComboBox,
    QCheckBox,
    QPushButton,
    QMessageBox,
    QGroupBox,
    QSizePolicy,
)
import disk_utils


class InkanWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inkan")
        self.setFixedSize(400, 280)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        main_layout.setSpacing(10)

        # Devices list
        self.devices_dict = disk_utils.get_devices_dict("Windows")
        self.devices_combo = QComboBox()
        for name, device in self.devices_dict.items():
            self.devices_combo.addItem(name, device)
        main_layout.addWidget(self.devices_combo)

        folder_group = QGroupBox("Choose folder to save")
        group_layout = QVBoxLayout()
        folder_group.setLayout(group_layout)

        # CheckBoxes for folders
        folder_names = ["Documents", "Music", "Pictures", "Videos"]
        self.folder_checkboxes = [QCheckBox(name) for name in folder_names]
        self.selected_folders = set()

        for checkbox in self.folder_checkboxes:
            checkbox.toggled.connect(self.on_folder_toggled)
            group_layout.addWidget(checkbox)

        group_layout.setSpacing(5)
        main_layout.addWidget(folder_group)

        # Start button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.on_start_clicked)
        main_layout.addWidget(self.start_button)

    def on_folder_toggled(self, checked):
        sender = self.sender()
        folder_name = sender.text()
        if checked:
            self.selected_folders.add(folder_name)
        else:
            self.selected_folders.remove(folder_name)

    def on_start_clicked(self):
        current_index = self.devices_combo.currentIndex()
        if current_index == -1:
            QMessageBox.warning(self, "Error", "No device selected")
            return

        device_path = self.devices_combo.itemData(current_index)
        for folder in self.selected_folders:
            disk_utils.compress_folder(
                os.path.join(os.path.expanduser("~"), folder),
                os.path.join(device_path, folder),
            )

        # Copy wallpaper
        shutil.copy2(
            os.path.join(
                os.path.expanduser("~"),
                "AppData",
                "Roaming",
                "Microsoft",
                "Windows",
                "Themes",
                "TranscodedWallpaper",
            ),
            os.path.join(device_path, "wallpaper.png"),
        )

        # Create apps file
        programs = disk_utils.get_installed_windows_programs()

        with open(os.path.join(device_path, "apps.txt"), "w") as f:
            for program in programs:
                print(program, file=f)

        QMessageBox.information(
            self, "Success", "All files compressed and copied. Bye Windows!"
        )


def main():
    app = QApplication(sys.argv)
    window = InkanWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
