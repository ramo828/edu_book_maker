import sys
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QLineEdit, QTextEdit, QComboBox, QLabel, QFormLayout,
    QFileDialog, QMessageBox, QSplitter, QMenu,  QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class EducationAppManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eğitim Uygulaması Yöneticisi")
        self.setGeometry(100, 100, 1200, 800)
        
        self.data = {"appTitle": "Eğitim Uygulaması", "sections": []}
        self.load_initial_data()
        
        self.setup_ui()
        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; color: #ffffff; }
            QTreeWidget { background-color: #3c3c3c; color: #ffffff; border: 1px solid #555555; }
            QLineEdit, QTextEdit, QComboBox { background-color: #4d4d4d; color: #ffffff; border: 1px solid #666666; border-radius: 5px; padding: 5px; }
            QPushButton { background-color: #228B22; color: #ffffff; border: 1px solid #777777; border-radius: 5px; padding: 8px; }
            QPushButton:hover { background-color: #2E8B57; }
            QLabel { color: #e0e0e0; font-weight: bold; font-size: 14px; }
        """)
        self.refresh_tree()

    def load_initial_data(self):
        initial_json = {
            "appTitle": "Eğitim Uygulaması",
            "sections": [
                {"id": "intro", "title": "Giriş ve Kurulum TR", "lessons": [
                    {"id": "lesson1", "title": "Arduino IDE Kurulumu",
                     "images": [{"id": "ide_download", "path": "assets/images/global/ide_download.png", "type": "image", "caption": "İndirme sayfası ekran görüntüsü", "align": "center"},
                                {"id": "setup_guide", "path": "assets/images/global/downloading-and-installing-img01.png", "type": "image", "caption": "Kurulum adımları ekran görüntüsü", "align": "center"},
                                {"id": "setup_guide_2", "path": "assets/images/global/downloading-and-installing-img02.png", "type": "image", "caption": "Kurulum adımları ekran görüntüsü", "align": "center"}],
                     "codes": [{"id": "code1", "path": "assets/codes/lesson1.ino", "caption": "Basit seri iletişim kodu"}],
                     "links": [{"id": "link1", "url": "https://arduino.cc/en/download", "name": "Arduino IDE İndir"}],
                     "subsections": [{"type": "text", "content": "Öncelikle, IDE'yi <bold>resmi web sitesinden</bold> [link1] indirin. IDE arayüzü [ide_download] böyle görünür. Kurulum aşaması bu sekilde devam etmeli . [setup_guide] [setup_guide_2] İşletim sisteminizle <underline>uyumluluğu kontrol edin</underline> ve [setup_guide] kurulum adımlarını izleyin. Bu <italic>önemli</italic> bir adımdır. Daha fazla yardım için"},
                                     {"type": "tinkercad", "url": "https://tinkercad.com/things/example1", "description": "Temel devre şeması"},
                                     {"type": "text", "content": "Kurulumdan sonra IDE'yi açın ve bu <italic>basit</italic> örneği deneyin."}]
                    }
                ]},
                {"id": "arduino_basics", "title": "Arduino Temelleri", "lessons": [
                    {"id": "lesson2", "title": "LED Yakma",
                     "images": [{"id": "led_circuit", "path": "assets/images/global/circuit_tr.png", "type": "image", "caption": "LED devre şeması", "align": "center"},
                                {"id": "resistor", "path": "assets/images/global/resistor.png", "type": "image", "caption": "Direnç şeması", "align": "center"}],
                     "codes": [{"id": "code2", "path": "assets/codes/lesson2.ino", "caption": "LED yakma kodu"}],
                     "links": [{"id": "link3", "url": "https://arduino.cc/reference/en/language/functions/digital-io/digitalwrite/", "name": "link"}],
                     "subsections": [{"type": "text", "content": "Bir LED'i <bold>Arduino</bold> ile <underline>kontrol</underline> etmek için PIN 13 kullanın. Devre [led_circuit] böyle görünür. Direnç renk kodları ise bu şekilde. [resistor] [code2] Daha fazla bilgi için [link3] dokümanını okuyun."}]
                    }
                ]}
            ]
        }
        self.data = initial_json

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Eğitim Yapısı")
        self.tree.itemClicked.connect(self.on_item_selected)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        left_layout.addWidget(self.tree)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.add_section_btn = QPushButton("Yeni Bölüm")
        self.add_section_btn.clicked.connect(self.add_section_dialog)
        btn_layout.addWidget(self.add_section_btn)
        
        left_layout.addLayout(btn_layout)
        splitter.addWidget(left_panel)
        
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.addWidget(QLabel("Seçili Öğe Düzenle", alignment=Qt.AlignCenter))
        self.form_widget = QWidget()
        self.form_layout = QFormLayout(self.form_widget)
        self.right_layout.addWidget(self.form_widget)
        self.save_changes_btn = QPushButton("Değişiklikleri Kaydet")
        self.save_changes_btn.clicked.connect(self.save_changes)
        self.right_layout.addWidget(self.save_changes_btn)
        splitter.addWidget(self.right_panel)
        
        bottom_layout = QHBoxLayout()
        self.save_json_btn = QPushButton("JSON Kaydet")
        self.save_json_btn.clicked.connect(self.save_json)
        bottom_layout.addWidget(self.save_json_btn)
        self.load_json_btn = QPushButton("JSON Yükle")
        self.load_json_btn.clicked.connect(self.load_json)
        bottom_layout.addWidget(self.load_json_btn)
        main_layout.addLayout(bottom_layout)
        
        splitter.setSizes([400, 800])

    def refresh_tree(self, select_section_id=None, select_lesson_id=None):
        self.tree.clear()
        app_title_item = QTreeWidgetItem(self.tree, [self.data["appTitle"]])
        app_title_item.setData(0, Qt.UserRole, {"type": "app_title"})
        app_title_item.setFont(0, QFont("", -1, QFont.Bold))
        
        sections_item = QTreeWidgetItem(app_title_item, ["Bölümler"])
        sections_item.setData(0, Qt.UserRole, {"type": "sections"})
        
        selected_item = None
        
        for section in self.data["sections"]:
            section_item = QTreeWidgetItem(sections_item, [section["title"]])
            section_item.setData(0, Qt.UserRole, {"type": "section", "section_id": section["id"]})
            
            lessons_item = QTreeWidgetItem(section_item, ["Dersler"])
            lessons_item.setData(0, Qt.UserRole, {"type": "lessons", "section_id": section["id"]})
            
            for lesson in section.get("lessons", []):
                lesson_item = QTreeWidgetItem(lessons_item, [lesson["title"]])
                lesson_item.setData(0, Qt.UserRole, {"type": "lesson", "section_id": section["id"], "lesson_id": lesson["id"]})
                
                if select_section_id == section["id"] and select_lesson_id == lesson["id"]:
                    selected_item = lesson_item
                
                images_item = QTreeWidgetItem(lesson_item, ["Resimler"])
                images_item.setData(0, Qt.UserRole, {"type": "images", "section_id": section["id"], "lesson_id": lesson["id"]})
                for img in lesson.get("images", []):
                    img_item = QTreeWidgetItem(images_item, [img["id"]])
                    img_item.setData(0, Qt.UserRole, {"type": "image", "section_id": section["id"], "lesson_id": lesson["id"], "image_id": img["id"]})
                
                codes_item = QTreeWidgetItem(lesson_item, ["Kodlar"])
                codes_item.setData(0, Qt.UserRole, {"type": "codes", "section_id": section["id"], "lesson_id": lesson["id"]})
                for code in lesson.get("codes", []):
                    code_item = QTreeWidgetItem(codes_item, [code["id"]])
                    code_item.setData(0, Qt.UserRole, {"type": "code", "section_id": section["id"], "lesson_id": lesson["id"], "code_id": code["id"]})
                
                links_item = QTreeWidgetItem(lesson_item, ["Linkler"])
                links_item.setData(0, Qt.UserRole, {"type": "links", "section_id": section["id"], "lesson_id": lesson["id"]})
                for link in lesson.get("links", []):
                    link_item = QTreeWidgetItem(links_item, [link["id"]])
                    link_item.setData(0, Qt.UserRole, {"type": "link", "section_id": section["id"], "lesson_id": lesson["id"], "link_id": link["id"]})
                
                subsections_item = QTreeWidgetItem(lesson_item, ["Alt Bölümler"])
                subsections_item.setData(0, Qt.UserRole, {"type": "subsections", "section_id": section["id"], "lesson_id": lesson["id"]})
                for sub_idx, sub in enumerate(lesson.get("subsections", [])):
                    sub_title = f"{sub['type']}: {(sub.get('content', '') or sub.get('description', ''))[:20]}..."
                    sub_item = QTreeWidgetItem(subsections_item, [sub_title])
                    sub_item.setData(0, Qt.UserRole, {"type": "subsection", "section_id": section["id"], "lesson_id": lesson["id"], "sub_idx": sub_idx})
        
        self.tree.expandAll()
        if selected_item:
            self.tree.setCurrentItem(selected_item)
            self.on_item_selected(selected_item)
        else:
            self.tree.setCurrentItem(app_title_item)
            self.on_item_selected(app_title_item)

    def get_selected_data(self):
        item = self.tree.currentItem()
        return item.data(0, Qt.UserRole) if item else None

    def show_context_menu(self, position):
        item = self.tree.itemAt(position)
        if not item:
            return
        
        data = item.data(0, Qt.UserRole)
        menu = QMenu(self)
        
        if data["type"] == "sections":
            menu.addAction("Yeni Bölüm Ekle", self.add_section_dialog)
        elif data["type"] == "section":
            menu.addAction("Yeni Ders Ekle", self.add_lesson_dialog)
            menu.addAction("Sil", self.delete_item)
        elif data["type"] == "lessons":
            menu.addAction("Yeni Ders Ekle", self.add_lesson_dialog)
        elif data["type"] == "lesson":
            menu.addAction("Yeni Resim Ekle", self.add_image_dialog)
            menu.addAction("Yeni Kod Ekle", self.add_code_dialog)
            menu.addAction("Yeni Link Ekle", self.add_link_dialog)
            menu.addAction("Yeni Alt Bölüm Ekle", self.add_subsection_dialog)
            menu.addAction("Sil", self.delete_item)
        elif data["type"] == "images":
            menu.addAction("Yeni Resim Ekle", self.add_image_dialog)
        elif data["type"] == "codes":
            menu.addAction("Yeni Kod Ekle", self.add_code_dialog)
        elif data["type"] == "links":
            menu.addAction("Yeni Link Ekle", self.add_link_dialog)
        elif data["type"] == "subsections":
            menu.addAction("Yeni Alt Bölüm Ekle", self.add_subsection_dialog)
        elif data["type"] in ["image", "code", "link", "subsection"]:
            menu.addAction("Sil", self.delete_item)
        
        menu.exec(self.tree.viewport().mapToGlobal(position))

    def on_item_selected(self, item):
        if not item:
            self.clear_form()
            return
        
        data = item.data(0, Qt.UserRole)
        if not data:
            self.clear_form()
            return
        
        self.clear_form()
        item_type = data["type"]
        if item_type == "app_title":
            self.title_edit = QLineEdit(self.data["appTitle"])
            self.form_layout.addRow("Uygulama Başlığı:", self.title_edit)
        elif item_type == "section":
            section = self.find_section(data["section_id"])
            self.edit_simple(section, ["id", "title"])
        elif item_type == "lesson":
            lesson = self.find_lesson(data["section_id"], data["lesson_id"])
            self.edit_simple(lesson, ["id", "title"])
        elif item_type == "image":
            image = self.find_image(data["section_id"], data["lesson_id"], data["image_id"])
            self.edit_image(image)
        elif item_type == "code":
            code = self.find_code(data["section_id"], data["lesson_id"], data["code_id"])
            self.edit_code(code)
        elif item_type == "link":
            link = self.find_link(data["section_id"], data["lesson_id"], data["link_id"])
            self.edit_simple(link, ["id", "url", "name"])
        elif item_type == "subsection":
            subsection = self.find_subsection(data["section_id"], data["lesson_id"], data["sub_idx"])
            self.edit_subsection(subsection)

    def clear_form(self):
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
        # Clean up attributes to avoid deleted widget access
        attrs = ['title_edit', 'id_edit', 'path_edit', 'type_edit', 'caption_edit', 'align_combo', 'url_edit', 'name_edit', 'content_edit', 'desc_edit', 'type_combo']
        for attr in attrs:
            if hasattr(self, attr):
                delattr(self, attr)

    def edit_simple(self, data, fields):
        for field in fields:
            edit = QLineEdit(data[field])
            setattr(self, f"{field}_edit", edit)
            self.form_layout.addRow(f"{field.capitalize()}:", edit)

    def edit_image(self, img):
        self.id_edit = QLineEdit(img["id"])
        self.path_edit = QLineEdit(img["path"])
        browse_btn = QPushButton("Gözat")
        browse_btn.clicked.connect(lambda: self.path_edit.setText(QFileDialog.getOpenFileName(self, "Resim Seç")[0]))
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(browse_btn)
        self.type_edit = QLineEdit(img["type"])
        self.caption_edit = QLineEdit(img["caption"])
        self.align_combo = QComboBox()
        self.align_combo.addItems(["center", "left", "right"])
        self.align_combo.setCurrentText(img["align"])
        self.form_layout.addRow("ID:", self.id_edit)
        self.form_layout.addRow("Yol:", path_layout)
        self.form_layout.addRow("Tip:", self.type_edit)
        self.form_layout.addRow("Başlık:", self.caption_edit)
        self.form_layout.addRow("Hizalama:", self.align_combo)

    def edit_code(self, code):
        self.id_edit = QLineEdit(code["id"])
        self.path_edit = QLineEdit(code["path"])
        browse_btn = QPushButton("Gözat")
        browse_btn.clicked.connect(lambda: self.path_edit.setText(QFileDialog.getOpenFileName(self, "Kod Dosyası Seç")[0]))
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(browse_btn)
        self.caption_edit = QLineEdit(code["caption"])
        self.form_layout.addRow("ID:", self.id_edit)
        self.form_layout.addRow("Yol:", path_layout)
        self.form_layout.addRow("Başlık:", self.caption_edit)

    def edit_subsection(self, sub):
        self.type_combo = QComboBox()
        self.type_combo.addItems(["text", "tinkercad"])
        self.type_combo.setCurrentText(sub["type"])
        self.form_layout.addRow("Tip:", self.type_combo)
        self.type_combo.currentTextChanged.connect(lambda typ: self.update_subsection_form(typ, sub))
        self.update_subsection_form(sub["type"], sub)

    def update_subsection_form(self, typ, sub=None):
        for attr in ['content_edit', 'url_edit', 'desc_edit']:
            if hasattr(self, attr):
                widget = getattr(self, attr)
                if widget:
                    row = self.form_layout.indexOf(widget)
                    if row != -1:
                        self.form_layout.removeRow(row)
                    widget.deleteLater()
                delattr(self, attr)
        if typ == "text":
            self.content_edit = QTextEdit(sub.get("content", "") if sub else "")
            self.form_layout.addRow("İçerik:", self.content_edit)
        else:
            self.url_edit = QLineEdit(sub.get("url", "") if sub else "")
            self.desc_edit = QLineEdit(sub.get("description", "") if sub else "")
            self.form_layout.addRow("URL:", self.url_edit)
            self.form_layout.addRow("Açıklama:", self.desc_edit)

    def save_changes(self):
        data = self.get_selected_data()
        if not data:
            return
        
        item_type = data["type"]
        
        if item_type == "app_title":
            self.data["appTitle"] = self.title_edit.text()
            self.refresh_tree()  # No section_id or lesson_id needed
        elif item_type == "section":
            section = self.find_section(data["section_id"])
            section["id"] = self.id_edit.text()
            section["title"] = self.title_edit.text()
            self.refresh_tree(data["section_id"])
        elif item_type in ["lesson", "image", "code", "link", "subsection"]:
            section_id = data["section_id"]
            lesson_id = data.get("lesson_id")
            if item_type == "lesson":
                lesson = self.find_lesson(section_id, lesson_id)
                lesson["id"] = self.id_edit.text()
                lesson["title"] = self.title_edit.text()
            elif item_type == "image":
                image = self.find_image(section_id, lesson_id, data["image_id"])
                image["id"] = self.id_edit.text()
                image["path"] = self.path_edit.text()
                image["type"] = self.type_edit.text()
                image["caption"] = self.caption_edit.text()
                image["align"] = self.align_combo.currentText()
            elif item_type == "code":
                code = self.find_code(section_id, lesson_id, data["code_id"])
                code["id"] = self.id_edit.text()
                code["path"] = self.path_edit.text()
                code["caption"] = self.caption_edit.text()
            elif item_type == "link":
                link = self.find_link(section_id, lesson_id, data["link_id"])
                link["id"] = self.id_edit.text()
                link["url"] = self.url_edit.text()
                link["name"] = self.name_edit.text()
            elif item_type == "subsection":
                subsection = self.find_subsection(section_id, lesson_id, data["sub_idx"])
                subsection["type"] = self.type_combo.currentText()
                if subsection["type"] == "text":
                    subsection["content"] = self.content_edit.toPlainText()
                    subsection.pop("url", None)
                    subsection.pop("description", None)
                else:
                    subsection["url"] = self.url_edit.text()
                    subsection["description"] = self.desc_edit.text()
                    subsection.pop("content", None)
            self.refresh_tree(section_id, lesson_id)
        
        QMessageBox.information(self, "Başarılı", "Değişiklikler kaydedildi.")

    def add_section_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni Bölüm Ekle")
        layout = QFormLayout()
        id_edit = QLineEdit(f"section_{len(self.data['sections']) + 1}")
        title_edit = QLineEdit(f"Yeni Bölüm {len(self.data['sections']) + 1}")
        layout.addRow("ID:", id_edit)
        layout.addRow("Başlık:", title_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        if dialog.exec() == QDialog.Accepted:
            if not id_edit.text() or not title_edit.text():
                QMessageBox.warning(self, "Hata", "ID ve Başlık alanları boş olamaz!")
                return
            new_section_id = id_edit.text()
            if self.find_section(new_section_id):
                QMessageBox.warning(self, "Hata", "Bu ID ile bir bölüm zaten var!")
                return
            new_section = {"id": new_section_id, "title": title_edit.text(), "lessons": []}
            self.data["sections"].append(new_section)
            self.refresh_tree(new_section_id)

    def add_lesson_dialog(self):
        data = self.get_selected_data()
        if not data or data["type"] not in ["section", "lessons"]:
            QMessageBox.warning(self, "Hata", "Lütfen bir bölüm veya dersler kategorisi seçin!")
            return
        
        section_id = data["section_id"]
        section = self.find_section(section_id)
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni Ders Ekle")
        layout = QFormLayout()
        id_edit = QLineEdit(f"lesson_{len(section['lessons']) + 1}")
        title_edit = QLineEdit(f"Yeni Ders {len(section['lessons']) + 1}")
        layout.addRow("ID:", id_edit)
        layout.addRow("Başlık:", title_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        if dialog.exec() == QDialog.Accepted:
            if not id_edit.text() or not title_edit.text():
                QMessageBox.warning(self, "Hata", "ID ve Başlık alanları boş olamaz!")
                return
            new_lesson_id = id_edit.text()
            if self.find_lesson(section_id, new_lesson_id):
                QMessageBox.warning(self, "Hata", "Bu ID ile bir ders zaten var!")
                return
            new_lesson = {"id": new_lesson_id, "title": title_edit.text(), "images": [], "codes": [], "links": [], "subsections": []}
            section["lessons"].append(new_lesson)
            self.refresh_tree(section_id, new_lesson_id)

    def add_image_dialog(self):
        data = self.get_selected_data()
        if not data or data["type"] not in ["lesson", "images"]:
            QMessageBox.warning(self, "Hata", "Lütfen bir ders veya resimler kategorisi seçin!")
            return
        
        section_id = data["section_id"]
        lesson_id = data["lesson_id"]
        lesson = self.find_lesson(section_id, lesson_id)
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni Resim Ekle")
        layout = QFormLayout()
        id_edit = QLineEdit(f"img_{len(lesson['images']) + 1}")
        path_edit = QLineEdit()
        browse_btn = QPushButton("Gözat")
        browse_btn.clicked.connect(lambda: path_edit.setText(QFileDialog.getOpenFileName(dialog, "Resim Seç")[0]))
        path_layout = QHBoxLayout()
        path_layout.addWidget(path_edit)
        path_layout.addWidget(browse_btn)
        type_edit = QLineEdit("image")
        caption_edit = QLineEdit()
        align_combo = QComboBox()
        align_combo.addItems(["center", "left", "right"])
        align_combo.setCurrentText("center")
        layout.addRow("ID:", id_edit)
        layout.addRow("Yol:", path_layout)
        layout.addRow("Tip:", type_edit)
        layout.addRow("Başlık:", caption_edit)
        layout.addRow("Hizalama:", align_combo)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        if dialog.exec() == QDialog.Accepted:
            if not id_edit.text() or not path_edit.text():
                QMessageBox.warning(self, "Hata", "ID ve Yol alanları boş olamaz!")
                return
            new_image_id = id_edit.text()
            if self.find_image(section_id, lesson_id, new_image_id):
                QMessageBox.warning(self, "Hata", "Bu ID ile bir resim zaten var!")
                return
            new_image = {
                "id": new_image_id,
                "path": path_edit.text(),
                "type": type_edit.text(),
                "caption": caption_edit.text(),
                "align": align_combo.currentText()
            }
            lesson["images"].append(new_image)
            self.refresh_tree(section_id, lesson_id)

    def add_code_dialog(self):
        data = self.get_selected_data()
        if not data or data["type"] not in ["lesson", "codes"]:
            QMessageBox.warning(self, "Hata", "Lütfen bir ders veya kodlar kategorisi seçin!")
            return
        
        section_id = data["section_id"]
        lesson_id = data["lesson_id"]
        lesson = self.find_lesson(section_id, lesson_id)
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni Kod Ekle")
        layout = QFormLayout()
        id_edit = QLineEdit(f"code_{len(lesson['codes']) + 1}")
        path_edit = QLineEdit()
        browse_btn = QPushButton("Gözat")
        browse_btn.clicked.connect(lambda: path_edit.setText(QFileDialog.getOpenFileName(dialog, "Kod Dosyası Seç")[0]))
        path_layout = QHBoxLayout()
        path_layout.addWidget(path_edit)
        path_layout.addWidget(browse_btn)
        caption_edit = QLineEdit()
        layout.addRow("ID:", id_edit)
        layout.addRow("Yol:", path_layout)
        layout.addRow("Başlık:", caption_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        if dialog.exec() == QDialog.Accepted:
            if not id_edit.text() or not path_edit.text():
                QMessageBox.warning(self, "Hata", "ID ve Yol alanları boş olamaz!")
                return
            new_code_id = id_edit.text()
            if self.find_code(section_id, lesson_id, new_code_id):
                QMessageBox.warning(self, "Hata", "Bu ID ile bir kod zaten var!")
                return
            new_code = {
                "id": new_code_id,
                "path": path_edit.text(),
                "caption": caption_edit.text()
            }
            lesson["codes"].append(new_code)
            self.refresh_tree(section_id, lesson_id)

    def add_link_dialog(self):
        data = self.get_selected_data()
        if not data or data["type"] not in ["lesson", "links"]:
            QMessageBox.warning(self, "Hata", "Lütfen bir ders veya linkler kategorisi seçin!")
            return
        
        section_id = data["section_id"]
        lesson_id = data["lesson_id"]
        lesson = self.find_lesson(section_id, lesson_id)
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni Link Ekle")
        layout = QFormLayout()
        id_edit = QLineEdit(f"link_{len(lesson['links']) + 1}")
        url_edit = QLineEdit()
        name_edit = QLineEdit()
        layout.addRow("ID:", id_edit)
        layout.addRow("URL:", url_edit)
        layout.addRow("İsim:", name_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        if dialog.exec() == QDialog.Accepted:
            if not id_edit.text() or not url_edit.text():
                QMessageBox.warning(self, "Hata", "ID ve URL alanları boş olamaz!")
                return
            new_link_id = id_edit.text()
            if self.find_link(section_id, lesson_id, new_link_id):
                QMessageBox.warning(self, "Hata", "Bu ID ile bir link zaten var!")
                return
            new_link = {
                "id": new_link_id,
                "url": url_edit.text(),
                "name": name_edit.text()
            }
            lesson["links"].append(new_link)
            self.refresh_tree(section_id, lesson_id)

    def add_subsection_dialog(self):
        data = self.get_selected_data()
        if not data or data["type"] not in ["lesson", "subsections"]:
            QMessageBox.warning(self, "Hata", "Lütfen bir ders veya alt bölümler kategorisi seçin!")
            return
        
        section_id = data["section_id"]
        lesson_id = data["lesson_id"]
        lesson = self.find_lesson(section_id, lesson_id)
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni Alt Bölüm Ekle")
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        type_combo = QComboBox()
        type_combo.addItems(["text", "tinkercad"])
        form_layout.addRow("Tip:", type_combo)
        content_widget = QTextEdit()
        url_edit = QLineEdit()
        desc_edit = QLineEdit()
        def update_form(typ):
            if typ == "text":
                form_layout.addRow("İçerik:", content_widget)
                if form_layout.indexOf(url_edit) != -1:
                    form_layout.removeRow(url_edit)
                if form_layout.indexOf(desc_edit) != -1:
                    form_layout.removeRow(desc_edit)
            else:
                form_layout.addRow("URL:", url_edit)
                form_layout.addRow("Açıklama:", desc_edit)
                if form_layout.indexOf(content_widget) != -1:
                    form_layout.removeRow(content_widget)
        update_form("text")
        type_combo.currentTextChanged.connect(update_form)
        layout.addLayout(form_layout)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        if dialog.exec() == QDialog.Accepted:
            typ = type_combo.currentText()
            if typ == "text" and not content_widget.toPlainText():
                QMessageBox.warning(self, "Hata", "İçerik alanı boş olamaz!")
                return
            if typ == "tinkercad" and (not url_edit.text() or not desc_edit.text()):
                QMessageBox.warning(self, "Hata", "URL ve Açıklama alanları boş olamaz!")
                return
            new_sub = {"type": typ}
            if typ == "text":
                new_sub["content"] = content_widget.toPlainText()
            else:
                new_sub["url"] = url_edit.text()
                new_sub["description"] = desc_edit.text()
            lesson["subsections"].append(new_sub)
            self.refresh_tree(section_id, lesson_id)

    def delete_item(self):
        data = self.get_selected_data()
        if not data or data["type"] in ["app_title", "sections", "lessons", "images", "codes", "links", "subsections"]:
            return
        
        item_type = data["type"]
        section_id = data["section_id"]
        section = self.find_section(section_id)
        
        if item_type == "section":
            self.data["sections"].remove(section)
            self.refresh_tree()
            return
        
        lesson_id = data["lesson_id"]
        lesson = self.find_lesson(section_id, lesson_id)
        
        if item_type == "lesson":
            section["lessons"].remove(lesson)
            self.refresh_tree(section_id)
            return
        
        if item_type == "image":
            image_id = data["image_id"]
            image = self.find_image(section_id, lesson_id, image_id)
            lesson["images"].remove(image)
        elif item_type == "code":
            code_id = data["code_id"]
            code = self.find_code(section_id, lesson_id, code_id)
            lesson["codes"].remove(code)
        elif item_type == "link":
            link_id = data["link_id"]
            link = self.find_link(section_id, lesson_id, link_id)
            lesson["links"].remove(link)
        elif item_type == "subsection":
            sub_idx = data["sub_idx"]
            del lesson["subsections"][sub_idx]
        
        self.refresh_tree(section_id, lesson_id)

    def save_json(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "JSON Kaydet", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "Başarılı", "JSON dosyası kaydedildi.")

    def load_json(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "JSON Yükle", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            self.refresh_tree()

    def find_section(self, section_id):
        for section in self.data["sections"]:
            if section["id"] == section_id:
                return section
        return None

    def find_lesson(self, section_id, lesson_id):
        section = self.find_section(section_id)
        if section:
            for lesson in section["lessons"]:
                if lesson["id"] == lesson_id:
                    return lesson
        return None

    def find_image(self, section_id, lesson_id, image_id):
        lesson = self.find_lesson(section_id, lesson_id)
        if lesson:
            for img in lesson["images"]:
                if img["id"] == image_id:
                    return img
        return None

    def find_code(self, section_id, lesson_id, code_id):
        lesson = self.find_lesson(section_id, lesson_id)
        if lesson:
            for code in lesson["codes"]:
                if code["id"] == code_id:
                    return code
        return None

    def find_link(self, section_id, lesson_id, link_id):
        lesson = self.find_lesson(section_id, lesson_id)
        if lesson:
            for link in lesson["links"]:
                if link["id"] == link_id:
                    return link
        return None

    def find_subsection(self, section_id, lesson_id, sub_idx):
        lesson = self.find_lesson(section_id, lesson_id)
        if lesson:
            return lesson["subsections"][sub_idx]
        return None
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EducationAppManager()
    window.show()
    sys.exit(app.exec())