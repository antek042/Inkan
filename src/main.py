import flet as ft
import disk_utils
import os


def main(page: ft.Page):
    page.title = "Inkan"
    page.window.width = 300
    page.window.height = 200
    page.window.center()

    devices_dict = disk_utils.get_devices_dict()

    def get_devices_options():
        options = []
        for name, device in devices_dict.items():
            options.append(
                ft.dropdown.Option(
                    key=device,
                    text=name,
                )
            )
        return options

    def devices_changed(e):
        page.update()

    devices = ft.Dropdown(
        editable=True,
        label="Devices",
        options=get_devices_options(),
        on_change=devices_changed,
        width=200,
        enable_search=False,
    )

    page.add(devices)

    def on_restore_button_clicked(e):
        if not devices.value:
            print("No device selected")
            return
        files = os.listdir(devices.value)
        for file in files:
            disk_utils.decompress_folder(
                f"{devices.value}/{file}",
                f"{os.path.expanduser('~')}/{file.split('.')[0]}",
            )

    restore_button = ft.FilledTonalButton(
        text="Restore my data!",
        on_click=on_restore_button_clicked,
    )

    page.add(restore_button)


ft.app(main)
