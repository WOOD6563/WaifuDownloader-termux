# window.py

from gi.repository import Gtk, Adw, GdkPixbuf, Gdk, GLib
from .waifu import WaifuDownloaderAPI
import threading
from .preferences import UserPreferences


@Gtk.Template(resource_path='/moe/nyarchlinux/waifudownloader/../data/ui/window.ui')
class WaifudownloaderWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'WaifudownloaderWindow'

    refresh_button = Gtk.Template.Child("refresh_button")
    spinner = Gtk.Template.Child("spinner")
    image = Gtk.Template.Child("image")
    save_button = Gtk.Template.Child("savebutton")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = UserPreferences()

        self.refresh_button.connect("clicked", self.async_reloadimage)
        self.save_button.connect("clicked", self.file_chooser_dialog)

        self.async_reloadimage()
        print(GLib.get_user_config_dir())

    def reloadimage(self, idk=None):
        """Reload current image"""

        self.spinner.set_visible(True)
        self.spinner.start()

        nsfw = bool(self.settings.get_preference("nsfw"))

        ct = WaifuDownloaderAPI()
        url = ct.get_neko(nsfw)

        self.info = ct.info

        if url is None:
            return

        content = ct.get_image(url)
        self.imagecontent = content

        loader = GdkPixbuf.PixbufLoader()
        loader.write_bytes(GLib.Bytes.new(content))
        loader.close()

        texture = Gdk.Texture.new_for_pixbuf(loader.get_pixbuf())
        self.image.set_paintable(texture)

        self.spinner.stop()
        self.spinner.set_visible(False)
        self.image.set_visible(True)

    def async_reloadimage(self, az=None):
        """Run reload in a separate thread"""

        t = threading.Thread(target=self.reloadimage, args=[az])
        t.start()

    def file_chooser_dialog(self, ae=None):
        """Open save dialog"""

        dialog = Gtk.FileChooserDialog(
            title="Save file",
            parent=self,
            action=Gtk.FileChooserAction.SAVE
        )

        item = self.info["items"][0]
        file_extension = item["extension"].lstrip(".")

        image_filter = Gtk.FileFilter()
        image_filter.set_name(f"{file_extension.upper()} files")
        image_filter.add_pattern(f"*.{file_extension}")
        dialog.add_filter(image_filter)

        image_id = item["id"]
        dialog.set_current_name(f"waifu.im_{image_id}.{file_extension}")

        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Save", Gtk.ResponseType.OK)

        dialog.connect("response", self.responsehandler)
        dialog.show()

    def responsehandler(self, dialog, response_id):
        """Save image"""

        if response_id == Gtk.ResponseType.OK:
            file = dialog.get_file()
            filename = file.get_path()

            with open(filename, "wb") as f:
                f.write(self.imagecontent)

        dialog.destroy()
