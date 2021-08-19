import gi
import configparser
import os
import shutil
from pathlib import Path


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


PATH_SYSTEM_DIR = Path.home()
DESKTOP_DIR = "Área\ de\ trabalho"
IMAGE_DIR = "Imagens"
DOWNLOAD_DIR = "Downloads"
DOCUMENT_DIR = "Documentos"

CONFIG_FILE = 'config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)    

class DialogExample(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Iniciar backup", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_border_width(20)
        self.set_size_request(5, 5)

        label = Gtk.Label(label="Iniciando backup dos arquivos pode ser que demore dependendo da quantidade de arquivos.")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class Main(Gtk.Window):
    def __init__(self):
        super().__init__(title="Backup")
        self.set_border_width(20)
        self.set_size_request(5, 5)    

        grid = Gtk.Grid()

        label = Gtk.Label(label="Diretório Backup")
        grid.attach(label, 0, 0, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text(config["DEFAULT"]["destine_dir"])
        grid.attach(self.entry, 1, 0, 1, 1)

        self.my_desktop = Gtk.CheckButton(label="Área de Trabalho")
        self.my_desktop.connect("toggled", self.on_editable_toggled)
        self.my_desktop.set_active(True if config["DEFAULT"]["my_desktop"] == "True" else False)
        grid.attach(self.my_desktop, 0, 1, 1, 1)

        self.my_images = Gtk.CheckButton(label="Minhas imagens")
        self.my_images.connect("toggled", self.on_editable_toggled)
        self.my_images.set_active(True if config["DEFAULT"]["my_images"] == "True" else False)
        grid.attach(self.my_images, 1, 1, 1, 1)

        self.my_downloads = Gtk.CheckButton(label="Meus downloads")
        self.my_downloads.connect("toggled", self.on_editable_toggled)
        self.my_downloads.set_active(True if config["DEFAULT"]["my_downloads"] == "True" else False)
        grid.attach(self.my_downloads, 2, 1, 1, 1)

        self.my_documents = Gtk.CheckButton(label="Meus Documentos")
        self.my_documents.connect("toggled", self.on_editable_toggled)
        self.my_documents.set_active(True if config["DEFAULT"]["my_documents"] == "True" else False)
        grid.attach(self.my_documents, 3, 1, 1, 1)

        button = Gtk.Button.new_with_label("Salvar")
        button.connect("clicked", self.on_save)
        grid.attach(button, 3, 2, 1, 1)

        button = Gtk.Button.new_with_label("Iniciar Backup")
        button.connect("clicked", self.on_click_me_clicked)
        grid.attach(button, 3, 3, 1, 1)

        self.add(grid)

    def create_backup_dir(self):
        directory = os.path.dirname(self.entry.get_text())
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def copy(self, src, dst):
        try:
            os.system("cp -Rf {} {}".format(src, dst))
        except:
            # TODO: criar move para windows
            pass

    def backup(self):
        directory = self.create_backup_dir()

        if self.my_desktop.get_active():
            self.copy("{}/{}".format(PATH_SYSTEM_DIR, DESKTOP_DIR), "{}/{}".format(directory, DESKTOP_DIR))
        if self.my_images.get_active():
            self.copy("{}/{}".format(PATH_SYSTEM_DIR, IMAGE_DIR), "{}/{}".format(directory, IMAGE_DIR))
        if self.my_downloads.get_active():
            self.copy("{}/{}".format(PATH_SYSTEM_DIR, DOWNLOAD_DIR), "{}/{}".format(directory, DOWNLOAD_DIR))
        if self.my_documents.get_active():
            self.copy("{}/{}".format(PATH_SYSTEM_DIR, DOCUMENT_DIR), "{}/{}".format(directory, DOCUMENT_DIR))

        print("Backup realizado com sucesso")

    def on_editable_toggled(self, button):
        value = button.get_active()
        self.entry.set_editable(value)

    def on_save(self, button):
        self.set_border_width(6)

        print(self.my_desktop.get_active())
        config["DEFAULT"]["destine_dir"] = self.entry.get_text()
        config["DEFAULT"]["my_desktop"] = str(self.my_desktop.get_active())
        config["DEFAULT"]["my_images"] = str(self.my_images.get_active())
        config["DEFAULT"]["my_downloads"] = str(self.my_downloads.get_active())
        config["DEFAULT"]["my_documents"] = str(self.my_documents.get_active())

        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

        print("Diretório salvo")

    def on_click_me_clicked(self, button):
        self.set_border_width(30)

        dialog = DialogExample(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.backup()
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()


win = Main()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()