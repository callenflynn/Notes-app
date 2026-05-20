import sys
import os
import ctypes
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFrame, QColorDialog, QFileDialog, QSizeGrip, QMessageBox
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor, QIcon, QFont, QKeySequence, QShortcut, QTextDocument, QTextFormat

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class RoundButton(QWidget):
    def __init__(self, color, action, parent=None):
        super().__init__(parent)
        self.color = QColor(color)
        self.action = action
        self.setFixedSize(14, 14)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.action()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(self.color)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(0, 0, 14, 14)

class ImageTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def insertFromMimeData(self, source):
        if source.hasImage():
            image = source.imageData()
            self.textCursor().insertImage(image)
            return
        super().insertFromMimeData(source)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            cursor = self.textCursor()
            char_format = cursor.charFormat()
            if char_format.isImageFormat():
                image_format = char_format.toImageFormat()
                current_width = image_format.width() if image_format.width() > 0 else 300
                current_height = image_format.height() if image_format.height() > 0 else 300
                delta = event.angleDelta().y()
                scale_factor = 1.1 if delta > 0 else 0.9
                new_width = max(30, min(2000, current_width * scale_factor))
                new_height = max(30, min(2000, current_height * scale_factor))
                image_format.setWidth(new_width)
                image_format.setHeight(new_height)
                cursor.mergeCharFormat(image_format)
                self.setCurrentCharFormat(image_format)
                event.accept()
                return
        super().wheelEvent(event)

class SleepyCatApp(QWidget):
    def __init__(self):
        super().__init__()
        # Standard-Hintergrund für das App-Fenster (Dunkelgrau)
        self.window_bg_color = QColor(25, 25, 25)
        # Die Custom-Farbe, die wir nur für das Textfeld nutzen wollen
        self.text_bg_color = QColor(35, 35, 35) 
        
        self.lang = "de"
        self.old_pos = QPoint()
        self.session_file = "last_note.html" 
        self.text_edit = None

        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("sleepy.cat.pro.v2")

        self.setMinimumSize(400, 300)
        self.resize(800, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowMinimizeButtonHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.apply_my_icon()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        
        self.start_language_selection()

    def apply_my_icon(self):
        icon_path = resource_path("app_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_sub_layout(item.layout())

    def clear_sub_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_sub_layout(child.layout())

    def start_language_selection(self):
        self.clear_layout()
        label = QLabel("Sprache / Language")
        label.setStyleSheet("color: white; font-size: 18pt; font-weight: bold; background: transparent;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label)
        
        btns = QHBoxLayout()
        de = QPushButton("DE 🇩🇪"); en = QPushButton("EN 🇺🇸")
        for b in [de, en]:
            b.setFixedSize(150, 50)
            b.setStyleSheet("background: #333; color: white; border-radius: 10px; border: none;")
            btns.addWidget(b)
        de.clicked.connect(lambda: self.set_language("de"))
        en.clicked.connect(lambda: self.set_language("en"))
        self.layout.addLayout(btns)

    def set_language(self, lang):
        self.lang = lang
        self.start_color_selection()

    def start_color_selection(self):
        self.clear_layout()
        btn = QPushButton("🎨")
        btn.setFixedSize(80, 80)
        btn.setStyleSheet("background: #444; border-radius: 40px; font-size: 30pt; border: none;")
        btn.clicked.connect(self.pick_initial_color)
        self.layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def pick_initial_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            # WICHTIG: Die ausgewählte Farbe wird jetzt als Textfeld-Hintergrund gespeichert!
            self.text_bg_color = color
            self.start_note_menu()

    def start_note_menu(self):
        self.clear_layout()
        self.text_edit = None
        
        header = QHBoxLayout()
        header.addWidget(RoundButton("#FF605C", self.close_app, self))
        header.addWidget(RoundButton("#FFBD44", self.toggle_max, self))
        header.addWidget(RoundButton("#28C940", self.showMinimized, self))
        header.addStretch()
        
        if os.path.exists(self.session_file):
            forward_btn = QPushButton(">")
            forward_btn.setFixedSize(30, 30)
            forward_btn.setStyleSheet("background: rgba(255,255,255,0.1); color: white; border-radius: 5px; font-weight: bold; border: none;")
            forward_btn.clicked.connect(self.setup_main_ui)
            header.addWidget(forward_btn)
            
        self.layout.addLayout(header)

        label = QLabel("Meine Notizen" if self.lang == "de" else "My Notes")
        label.setStyleSheet("color: white; font-size: 20pt; font-weight: bold; background: transparent;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label)

        menu_layout = QHBoxLayout()
        menu_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if os.path.exists(self.session_file):
            display_name = self.session_file.replace(".html", ".txt")
            last_btn = QPushButton(f"{display_name}")
            last_btn.setFixedSize(200, 100)
            last_btn.setStyleSheet("background: rgba(255,255,255,0.1); color: white; border-radius: 15px; font-size: 10pt; border: none;")
            last_btn.clicked.connect(self.setup_main_ui)
            menu_layout.addWidget(last_btn)

        new_btn = QPushButton("+")
        new_btn.setFixedSize(100, 100)
        new_btn.setStyleSheet("background: #000000; color: white; border-radius: 50px; font-size: 40pt; font-weight: bold; border: none;")
        new_btn.clicked.connect(self.create_new_note)
        menu_layout.addWidget(new_btn)

        self.layout.addLayout(menu_layout)

    def setup_main_ui(self):
        self.clear_layout()
        
        header = QHBoxLayout()
        header.addWidget(RoundButton("#FF605C", self.close_app, self))
        header.addWidget(RoundButton("#FFBD44", self.toggle_max, self))
        header.addWidget(RoundButton("#28C940", self.showMinimized, self))
        
        back_btn = QPushButton("<")
        back_btn.setFixedSize(30, 30)
        back_btn.setStyleSheet("background: rgba(255,255,255,0.1); color: white; border-radius: 5px; font-weight: bold; border: none;")
        back_btn.clicked.connect(self.go_back_to_menu)
        header.addWidget(back_btn)
        
        header.addStretch()
        
        t_open = "Öffnen" if self.lang == "de" else "Open"
        self.open_btn = QPushButton(t_open)
        self.open_btn.setFixedSize(80, 25)
        self.open_btn.setStyleSheet("background: rgba(255,255,255,0.1); color: white; border-radius: 5px; font-size: 10px; border: none;")
        self.open_btn.clicked.connect(self.open_file)
        header.addWidget(self.open_btn)
        self.layout.addLayout(header)

        tools = QHBoxLayout()
        for t, f in [("B", self.set_bold), ("I", self.set_italic), ("U", self.set_underline), ("🖼️", self.insert_image)]:
            btn = QPushButton(t)
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("background: rgba(255,255,255,0.1); color: white; border-radius: 5px; border: none;")
            btn.clicked.connect(f)
            tools.addWidget(btn)
        tools.addStretch()
        self.layout.addLayout(tools)
        
        self.text_edit = ImageTextEdit()
        
        # FIX: Hier weisen wir der Style-Sheet-Regel NUR für das Textfeld dynamisch deine Custom-Farbe zu!
        self.text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.text_bg_color.name()}; 
                color: white; 
                border-radius: 5px; 
                padding: 10px; 
                font-size: 13pt; 
                border: none;
            }}
        """)
        self.layout.addWidget(self.text_edit)

        self.shortcut_date = QShortcut(QKeySequence("Ctrl+D"), self)
        self.shortcut_date.activated.connect(self.insert_timestamp)
        
        self.shortcut_help = QShortcut(QKeySequence("Ctrl+C"), self)
        self.shortcut_help.activated.connect(self.show_help_shortcuts)

        self.load_session()

        footer = QHBoxLayout()
        footer.addStretch()
        t_save = "Speichern" if self.lang == "de" else "Save"
        self.save_btn = QPushButton(t_save)
        self.save_btn.setFixedSize(120, 35)
        self.save_btn.setStyleSheet("background: #34C759; color: white; border-radius: 17px; font-weight: bold; border: none;")
        self.save_btn.clicked.connect(self.save_file)
        footer.addWidget(self.save_btn)
        footer.addStretch()
        
        self.grip = QSizeGrip(self)
        footer.addWidget(self.grip, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        self.layout.addLayout(footer)

    def show_help_shortcuts(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Shortcuts")
        text = "Features:\n\nStrg + V: Bilder einfügen\nStrg + D: Datum & Uhrzeit\n\n💡 BILDER VERGRÖSSERN:\nSTRG + Mausrad drehen!"
        if self.lang != "de":
            text = "Features:\n\nCtrl + V: Paste images\nCtrl + D: Date & Time\n\n💡 RESIZE IMAGES:\nCTRL + scroll mouse wheel!"
        msg.setText(text)
        msg.exec()

    def go_back_to_menu(self):
        self.save_session()
        self.start_note_menu()

    def create_new_note(self):
        if os.path.exists(self.session_file):
            os.remove(self.session_file)
        self.setup_main_ui()

    def insert_timestamp(self):
        if self.text_edit:
            now = datetime.now().strftime("%d.%m.%Y %H:%M")
            self.text_edit.insertPlainText(f"\n--- {now} ---\n")

    def insert_image(self):
        if self.text_edit:
            title = "Bild auswählen" if self.lang == "de" else "Select Image"
            path, _ = QFileDialog.getOpenFileName(self, title, "", "Bilder (*.png *.jpg *.jpeg *.bmp *.gif)")
            if path:
                image = QIcon(path).pixmap(300, 300).toImage()
                self.text_edit.textCursor().insertImage(image)

    def save_session(self):
        try:
            if self.text_edit is not None:
                content = self.text_edit.toHtml()
                with open(self.session_file, "w", encoding="utf-8") as f:
                    f.write(content)
        except RuntimeError:
            pass 

    def load_session(self):
        if os.path.exists(self.session_file) and self.text_edit:
            with open(self.session_file, "r", encoding="utf-8") as f:
                self.text_edit.setHtml(f.read())

    def close_app(self):
        self.save_session()
        self.close()

    def open_file(self):
        title = "Datei öffnen" if self.lang == "de" else "Open File"
        path, _ = QFileDialog.getOpenFileName(self, title, "", "Sleepy Notes (*.html);;Text (*.txt);;Alle Dateien (*)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                if self.text_edit:
                    if path.endswith(".html"):
                        self.text_edit.setHtml(f.read())
                    else:
                        self.text_edit.setPlainText(f.read())

    def save_file(self):
        title = "Speichern" if self.lang == "de" else "Save"
        path, _ = QFileDialog.getSaveFileName(self, title, "", "Sleepy Notes (*.html)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                if self.text_edit:
                    f.write(self.text_edit.toHtml())
            self.save_session()

    def toggle_max(self):
        if self.isMaximized(): self.showNormal()
        else: self.showMaximized()

    def set_bold(self):
        if self.text_edit:
            fmt = self.text_edit.currentCharFormat()
            fmt.setFontWeight(QFont.Weight.Bold if fmt.fontWeight() != QFont.Weight.Bold else QFont.Weight.Normal)
            self.text_edit.setCurrentCharFormat(fmt)

    def set_italic(self):
        if self.text_edit:
            fmt = self.text_edit.currentCharFormat()
            fmt.setFontItalic(not fmt.fontItalic())
            self.text_edit.setCurrentCharFormat(fmt)

    def set_underline(self):
        if self.text_edit:
            fmt = self.text_edit.currentCharFormat()
            fmt.setFontUnderline(not fmt.fontUnderline())
            self.text_edit.setCurrentCharFormat(fmt)

    # FIX: Das Paint-Event zeichnet jetzt IMMER das cleane Dunkelgrau für das Hauptfenster,
    # ganz egal welche Farbe im Farbdialog für das Notizfeld gewählt wurde!
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(self.window_bg_color)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(self.rect(), 15, 15)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton and e.position().y() < 40:
            self.old_pos = e.globalPosition().toPoint()

    def mouseMoveEvent(self, e):
        if hasattr(self, 'old_pos') and e.buttons() == Qt.MouseButton.LeftButton and e.position().y() < 40:
            delta = e.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = e.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SleepyCatApp()
    ex.show()
    sys.exit(app.exec())
