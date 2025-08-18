import flet as ft
import disk_utils

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
        selected_node = e.control.value
        print(selected_node)
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

ft.app(main)
