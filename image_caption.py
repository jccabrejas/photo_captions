import flet as ft
import os


class ImageToBeCaptioned(ft.Row):

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        caption_file_path = image_path + ".txt"
        try:
            with open(caption_file_path, "r") as f:
                self.caption_text = f.read()
        except FileNotFoundError:
            self.caption_text = ""
        self.image = ft.Image(
            src=self.image_path, width=100, height=100, fit=ft.ImageFit.CONTAIN
        )
        self.image_caption = ft.TextField(
            label="Caption",
            width=600,
            value=self.caption_text,
            on_change=lambda _: self.update_caption(),
        )
        self.caption_length = ft.Text(value=f"{len(self.caption_text)} characters")
        self.save_caption_button = ft.Button(
            "Save", on_click=lambda _: self.save_caption()
        )
        self.controls = [
            self.image,
            self.image_caption,
            self.save_caption_button,
            self.caption_length,
        ]

    def update_caption(self):
        setattr(self, "caption_text", self.image_caption.value)
        self.caption_length.value = f"{len(self.caption_text)}  characters"
        self.update()

    def save_caption(self):
        self.update()
        if self.image_path:
            caption_file_path = self.image_path + ".txt"
            with open(caption_file_path, "w") as f:
                f.write(self.caption_text)


def main(page: ft.Page):
    page.title = "Image Captioning App"
    page.scroll = "always"
    selected_folder = ft.Text("No folder selected for photos")
    image_list = ft.Column()

    def pick_files(e: ft.FilePickerResultEvent):
        if e.path:
            selected_folder.value = e.path
            image_list.controls.clear()  # Clear previous images
            for filename in os.listdir(e.path):
                if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(e.path, filename)
                    image_list.controls.append(
                        ImageToBeCaptioned(image_path=image_path)
                    )
            page.update()

    file_picker = ft.FilePicker(on_result=pick_files)
    page.overlay.append(file_picker)

    page.add(
        ft.ElevatedButton(
            "Select Folder", on_click=lambda _: file_picker.get_directory_path()
        ),
        selected_folder,
        image_list,
    )


ft.app(target=main)
