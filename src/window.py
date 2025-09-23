# window.py
#
# Copyright 2023 SilverOS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
        """Reload current image
        Args:
            idk (none): not useful but need to put it.
        """
        # Start loading
        self.spinner.set_visible(True)
        self.spinner.start()
        # Get waifu image
        nsfwsetting = self.settings.get_preference("nsfw")
        if nsfwsetting:
            nsfw = True
        else:
            nsfw = False
        ct = WaifuDownloaderAPI()
        url = ct.get_neko(nsfw)
        self.info = ct.info
        if url is not None:
            content = ct.get_image(url)
        self.imagecontent = content
        # Display image
        loader = GdkPixbuf.PixbufLoader()
        loader.write_bytes(GLib.Bytes.new(content))
        loader.close()
        # Convert to a texture for GtkPicture so it can scale to the container
        texture = Gdk.Texture.new_for_pixbuf(loader.get_pixbuf())
        self.image.set_paintable(texture)
        # Stop loading and display image
        self.spinner.stop()
        self.spinner.set_visible(False)
        self.image.set_visible(True)

    def async_reloadimage(self, az=None):
        """Call the function to load the image on another thread
        """
        t = threading.Thread(target=self.reloadimage, args=[az])
        t.start()

    def file_chooser_dialog(self, ae=None):
        """Displays the dialog to save the image
        """
        self.dialog = Gtk.FileChooserDialog(title="Save, file", parent=self,
                                            action=Gtk.FileChooserAction.SAVE)

        # Add correct extension to file name
        file_extension = self.info["images"][0]["extension"][1:]
        image_filter = Gtk.FileFilter()
        image_filter.set_name(f"{file_extension.upper()} files")
        image_filter.add_pattern(f"*.{file_extension}")
        self.dialog.add_filter(image_filter)

        # Suggest a sensible default filename
        # using this format ensures the image source can easily be found from its name
        image_id = self.info["images"][0]["image_id"]
        self.dialog.set_current_name(f"waifu.im_{image_id}.{file_extension}")

        # Buttons
        self.dialog.add_button('Cancel', Gtk.ResponseType.CANCEL)
        self.dialog.add_button('Save', Gtk.ResponseType.OK)
        self.dialog.connect('response', self.responsehandler)
        self.dialog.show()

    def responsehandler(self, dialog, response_id):
        """Save image and destroy file chooser"""
        if response_id == Gtk.ResponseType.OK:
            file = dialog.get_file()
            filename = file.get_path()
            f = open(filename, "wb+")
            f.write(self.imagecontent)
            f.close()
        dialog.destroy()
