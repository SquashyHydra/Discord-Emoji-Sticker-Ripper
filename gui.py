import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QMessageBox, QProgressDialog, QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap, QMovie
import requests
import os

class FetchThread(QThread):
    result = pyqtSignal(object, object, object)
    def __init__(self, id_text):
        super().__init__()
        self.id_text = id_text
    def run(self):
        sticker_url = f"https://media.discordapp.net/stickers/{self.id_text}.png"
        emoji_url = f"https://cdn.discordapp.com/emojis/{self.id_text}.png"
        gif_url = f"https://cdn.discordapp.com/emojis/{self.id_text}.gif"
        link_list = [sticker_url, gif_url, emoji_url]
        def get_img(link_list: list):
            for url in link_list:
                try:
                    resp = requests.get(url, timeout=5)
                    if resp.status_code == 200:
                        content = resp.content
                        return content, url
                except Exception:
                    pass
        data, url = get_img(link_list)
        if data:
            if "stickers" in url:
                label_type = "Sticker"
            elif ".gif" in url:
                label_type = "GIF"
            else:
                label_type = "Emoji"
        else:
            label_type = None
        self.result.emit(data, label_type, True if label_type == "GIF" or "Sticker" else False)

class EmojiRipperGUI(QWidget):
    def __init__(self):
        super().__init__()
        flags = self.windowFlags()
        flags |= Qt.WindowType.CustomizeWindowHint
        flags &= ~Qt.WindowType.WindowMinMaxButtonsHint
        flags &= ~Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags | Qt.WindowType.Dialog)
        self.setWindowIcon(QIcon(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "assets", "icon.ico"))))
        self.setWindowTitle("Discord Emoji/Sticker Ripper PRO")
        self.setMinimumWidth(420)
        self.setStyleSheet("""
            QWidget { 
                background: #23272A;
                color: #fff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit, QLabel { 
                background: transparent;
                color: #e810d6;
                font-size: 16px;
            }
            QLineEdit {
                border: 1px solid #f01ade;
                border-radius: 6px;
                padding: 2px;    
            }
            QLineEdit:hover {
                border: 2px solid #f01ade;
                border-radius: 6px;
                padding: 4px;
            }
            QPushButton { 
                background: #f01ade;
                color: #fff;
                border-radius: 6px;
                padding: 8px 18px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #cc10bc;
            }
            QGroupBox {
                border: 1.258px solid #f01ade;
                border-radius: 8px;
                margin-top: 10px;
                background: transparent;
            }
            QGroupBox::title {
                background: transparent;
                color: #e810d6;
            }
        """)
        self.init_ui()

    def custom_context_menu(self, pos):
        menu = self.id_input.createStandardContextMenu()
        for action in menu.actions():
            menu.removeAction(action)
        paste_action = menu.addAction("Paste")
        paste_action.triggered.connect(self.id_input.paste)
        menu.exec(self.id_input.mapToGlobal(pos))

    def init_ui(self):
        layout = QVBoxLayout()

        # Input Section
        input_group = QGroupBox("")
        input_layout = QHBoxLayout()
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter Discord ID (numbers only)")
        self.id_input.setClearButtonEnabled(True)
        self.id_input.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.id_input.customContextMenuRequested.connect(self.custom_context_menu)
        input_layout.addWidget(self.id_input)
        self.fetch_btn = QPushButton("Fetch")
        self.fetch_btn.clicked.connect(self.fetch_images)
        input_layout.addWidget(self.fetch_btn)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Image Display Section
        self.image_group = QGroupBox("Preview")
        self.image_layout = QVBoxLayout()
        self.data_label = QLabel("")
        self.data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_layout.addWidget(self.data_label)
        self.image_group.setLayout(self.image_layout)
        layout.addWidget(self.image_group)

        # Download Button
        self.download_btn = QPushButton("Download")
        self.download_btn.setEnabled(True)
        self.download_btn.clicked.connect(self.download_image)
        layout.addWidget(self.download_btn)

        self.setLayout(layout)

    def warning_box(self, title, message):
        self.Warning_box = QMessageBox(self)
        self.Warning_box.setWindowTitle(title)
        self.Warning_box.setText(f"<div style='text-align:center;'><b>{message}</b></div>")
        self.Warning_box.setStyleSheet("""
            QMessageBox {
                background: #23272A;
                color: #e810d6;
                border-width: 3px;
                border-style: solid;
                border-color: #f01ade;
                border-radius: 4px;
                padding: 8px;
            }
            QLabel {
                color: #e810d6;
                font-size: 16px;
                qproperty-alignment: AlignCenter;
                padding: 32px, 0px, 8px, 0px;
                qproperty-wordWrap: true;
                background: transparent;
            }
        """)
        self.Warning_box.setIconPixmap(QPixmap(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "assets", "warning.png"))))
        self.Warning_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.Warning_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        self.Warning_box.setEscapeButton(QMessageBox.StandardButton.NoButton)
        self.Warning_box.setWindowModality(Qt.WindowModality.ApplicationModal)
        # Prevent moving and resizing
        flags = self.Warning_box.windowFlags()
        flags |= Qt.WindowType.CustomizeWindowHint
        flags &= ~Qt.WindowType.WindowCloseButtonHint
        flags &= ~Qt.WindowType.WindowMinMaxButtonsHint
        flags &= ~Qt.WindowType.WindowStaysOnTopHint
        flags &= ~Qt.WindowType.WindowTitleHint
        self.Warning_box.setWindowFlags(flags | Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        # Center the dialog on the parent window
        self.Warning_box.show()
        self.Warning_box.raise_()
        self.Warning_box.activateWindow()
        parent_rect = self.geometry()
        warning_rect = self.Warning_box.frameGeometry()
        center_point = parent_rect.center()
        warning_rect.moveCenter(center_point)
        self.Warning_box.move(warning_rect.topLeft())

    def fetch_images(self):
        id_text = self.id_input.text().strip()
        if not id_text.isdigit():
            self.warning_box("Invalid ID", "Please enter a valid numeric Discord ID.")
            return
        self.fetch_btn.setEnabled(False)
        self.progress = QProgressDialog(self)
        self.progress.setLabelText("<div style='text-align:center;'><b>Fetching images...</b></div>")
        self.progress.setWindowTitle("Loading...")
        self.progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress.setCancelButton(None)
        self.progress.setMinimumDuration(0)
        self.progress.setRange(0, 0)
        self.progress.setFixedSize(260, 100)
        self.progress.setStyleSheet("""
            QProgressDialog {
                background: #23272A;
                color: #e810d6;
                border-width: 3px;
                border-style: solid;
                border-color: #f01ade;
                border-radius: 4px;
                padding: 8px;
            }
            QLabel {
                color: #e810d6;
                font-size: 16px;
                qproperty-alignment: AlignCenter;
                background: transparent;
            }
        """)
        # Prevent moving and resizing
        flags = self.progress.windowFlags()
        flags |= Qt.WindowType.CustomizeWindowHint
        flags &= ~Qt.WindowType.WindowCloseButtonHint
        flags &= ~Qt.WindowType.WindowMinMaxButtonsHint
        flags &= ~Qt.WindowType.WindowStaysOnTopHint
        flags &= ~Qt.WindowType.WindowTitleHint
        self.progress.setWindowFlags(flags | Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        # Center the dialog on the parent window
        parent_rect = self.geometry()
        progress_rect = self.progress.frameGeometry()
        center_point = parent_rect.center()
        progress_rect.moveCenter(center_point)
        self.progress.move(progress_rect.topLeft())
        self.progress.show()
        self.thread = FetchThread(id_text)
        self.thread.result.connect(self.display_images)
        self.thread.finished.connect(self.progress.close)
        self.thread.finished.connect(lambda: self.fetch_btn.setEnabled(True))
        self.thread.start()

    def display_images(self, data, label_type, is_gif=False):
        self._last_data = data
        self._last_label_type = label_type
        self._last_is_gif = is_gif
        if data:
            if label_type == "Sticker":
                # Check if APNG (animated PNG)
                is_apng = False
                if data[:8] == b'\x89PNG\r\n\x1a\n' and b'acTL' in data:
                    is_apng = True
                if is_apng:
                    import io
                    import tempfile
                    from PIL import Image
                    import imageio.v3 as iio
                    import numpy as np
                    import os
                    try:
                        # Extract all frames from APNG
                        im = Image.open(io.BytesIO(data))
                        frames = []
                        durations = []
                        for frame in range(getattr(im, 'n_frames', 1)):
                            im.seek(frame)
                            frames.append(np.array(im.convert('RGBA')))
                            durations.append(im.info.get('duration', 100))
                        # Save as GIF to a temp file
                        temp_gif = tempfile.NamedTemporaryFile(delete=False, suffix='.gif')
                        iio.imwrite(temp_gif.name, frames, format='GIF', duration=[d/1000 for d in durations])
                        temp_gif.close()
                        movie = QMovie(temp_gif.name)
                        self.data_label.setMovie(movie)
                        movie.start()
                        self.data_label.setText("")
                        def cleanup():
                            try:
                                os.remove(temp_gif.name)
                            except Exception:
                                pass
                        movie.finished.connect(cleanup)
                    except Exception:
                        self.data_label.setText("Animated Sticker (APNG) detected. Animation preview not supported.")
                        self.data_label.setPixmap(QPixmap())
                else:
                    pixmap = QPixmap()
                    pixmap.loadFromData(data)
                    self.data_label.setPixmap(pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                    self.data_label.setText("")
            elif is_gif:
                import tempfile
                import os
                temp_gif = tempfile.NamedTemporaryFile(delete=False, suffix='.gif')
                temp_gif.write(data)
                temp_gif.close()
                movie = QMovie(temp_gif.name)
                self.data_label.setMovie(movie)
                movie.start()
                self.data_label.setText("")
                def cleanup():
                    try:
                        os.remove(temp_gif.name)
                    except Exception:
                        pass
                movie.finished.connect(cleanup)
            else:
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                self.data_label.setPixmap(pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                self.data_label.setText("")
        else:
            self.data_label.setText(f"{label_type} not found.")
            self.data_label.setPixmap(QPixmap())
            if hasattr(self.data_label, 'setMovie'):
                self.data_label.setMovie(None)

    def info_box(self, title, message):
        self.Info_box = QMessageBox(self)
        self.Info_box.setWindowTitle(title)
        self.Info_box.setText(f"<div style='text-align:center;'><b>{message}</b></div>")
        self.Info_box.setStyleSheet("""
            QMessageBox {
                background: #23272A;
                color: #e810d6;
                border-width: 3px;
                border-style: solid;
                border-color: #f01ade;
                border-radius: 4px;
                padding: 8px;
            }
            QLabel {
                color: #e810d6;
                font-size: 16px;
                qproperty-alignment: AlignCenter;
                padding: 32px, 0px, 8px, 0px;
                qproperty-wordWrap: true;
                background: transparent;
            }
        """)
        self.Info_box.setIconPixmap(QPixmap(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "assets", "info.png"))))
        self.Info_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.Info_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        self.Info_box.setEscapeButton(QMessageBox.StandardButton.NoButton)
        self.Info_box.setWindowModality(Qt.WindowModality.ApplicationModal)
        # Prevent moving and resizing
        flags = self.Info_box.windowFlags()
        flags |= Qt.WindowType.CustomizeWindowHint
        flags &= ~Qt.WindowType.WindowCloseButtonHint
        flags &= ~Qt.WindowType.WindowMinMaxButtonsHint
        flags &= ~Qt.WindowType.WindowStaysOnTopHint
        flags &= ~Qt.WindowType.WindowTitleHint
        self.Info_box.setWindowFlags(flags | Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        # Center the dialog on the parent window
        self.Info_box.show()

    def download_image(self):
        data = getattr(self, '_last_data', None)
        label_type = getattr(self, '_last_label_type', None)
        is_gif = getattr(self, '_last_is_gif', False)
        if not data or not label_type:
            self.warning_box("No Image", "No image to download.")
            return
        if label_type == "Sticker":
            is_apng = False
            if data[:8] == b'\x89PNG\r\n\x1a\n' and b'acTL' in data:
                is_apng = True
            if is_apng:
                ext = 'gif'
                file_filter = 'GIF Files (*.gif)'
                default_name = 'sticker.gif'
            else:
                ext = 'png'
                file_filter = 'PNG Files (*.png)'
                default_name = 'sticker.png'
        elif label_type == "GIF":
            ext = 'gif'
            file_filter = 'GIF Files (*.gif)'
            default_name = 'emoji.gif'
        elif label_type == "Emoji":
            ext = 'png'
            file_filter = 'PNG Files (*.png)'
            default_name = 'emoji.png'
        # Use the native file dialog for a more Explorer-like appearance
        options = QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.HideNameFilterDetails | QFileDialog.Option.DontConfirmOverwrite
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            default_name,
            file_filter,
            options=options  # Use native dialog
        )
        if not file_path:
            return
        # Ensure correct extension
        if not file_path.lower().endswith(f'.{ext}'):
            file_path += f'.{ext}'
        try:
            with open(file_path, 'wb') as f:
                f.write(data)
            self.info_box("Saved", f"File saved to: {file_path}")
        except Exception as e:
            self.warning_box("Error", f"Failed to save file: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmojiRipperGUI()
    window.show()
    sys.exit(app.exec())
