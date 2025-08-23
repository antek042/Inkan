import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio
import disk_utils
import app_utils
import os
import shutil


class InkanWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Inkan")
        self.set_default_size(600, 400)
        self.set_resizable(False)
        self.set_modal(True)

        vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20,
            margin_bottom=20,
            margin_start=20,
            margin_end=20,
        )
        self.set_child(vbox)

        self.devices_dict = disk_utils.get_devices_dict()

        self.devices_combo = Gtk.ComboBoxText()
        self.devices_combo.set_hexpand(True)
        for name, device in self.devices_dict.items():
            self.devices_combo.append(device, name)
        self.devices_combo.set_active(0 if self.devices_dict else -1)
        vbox.append(self.devices_combo)

        self.restore_button = Gtk.Button(label="Restore my data!")
        self.restore_button.connect("clicked", self.on_restore_button_clicked)
        vbox.append(self.restore_button)

    def on_restore_button_clicked(self, button):
        device = self.devices_combo.get_active_id()
        if not device:
            print("No device selected")
            return
        try:
            files = os.listdir(device)
        except Exception as e:
            print(f"Error opening {device}: {e}")
            return

        for file in files:
            if file.endswith(".tar.zst"):
                target = os.path.join(os.path.expanduser("~"), file.split(".")[0])
                disk_utils.decompress_folder(os.path.join(device, file), target)
            elif file.endswith(".png") or file.endswith(".jpg"):
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


class InkanApp(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="io.github.Inkan", flags=Gio.ApplicationFlags.FLAGS_NONE
        )

    def do_activate(self):
        win = InkanWindow(self)
        win.present()


if __name__ == "__main__":
    app = InkanApp()
    app.run()
