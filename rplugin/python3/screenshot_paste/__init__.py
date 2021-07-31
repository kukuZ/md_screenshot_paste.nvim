import pynvim
import os
import datetime
from PIL import ImageGrab, Image
import platform


@pynvim.plugin
class ScreenshotPastePlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command("MdWriteImage", eval='expand("%:p")')
    def save_clipborimage(self, file_path):
        pf_type = platform.system()
        if pf_type == "Windows" or pf_type == "Darwin":
            # クリップボード内の情報を取得する
            clipboard_image = ImageGrab.grabclipboard()
            # clioboard_imageがImage.Image型の場合は保存する
            if isinstance(clipboard_image, Image.Image):
                pass
            else:
                self.nvim.out_write("clipboard is null")
                return
        else:
            import gtk

            clipboard = gtk.clipboard_get()
            image = clipboard.wait_for_image()
            if image is not None:
                pass
            else:
                self.nvim.out_write("clipboard is null")
                return

        # 保存先ディレクトリの作成
        base_dire = os.path.dirname(file_path)
        # 拡張子抜きファイル名取得
        f_name = os.path.splitext(os.path.basename(file_path))[0]
        # ディレクトリ作成
        new_dire = os.path.join(base_dire, f_name)
        # ディレクトリ作成
        if not os.path.exists(new_dire):
            os.mkdir(new_dire)
            new_dire = os.path.join(new_dire, "img")
            os.mkdir(new_dire)
        else:
            new_dire = os.path.join(new_dire, "img")
        # img保存
        img_name = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".png"
        w_name = os.path.join(new_dire, img_name)
        if pf_type == "Windows" or pf_type == "Darwin":
            clipboard_image.save(w_name, optimize=True, quality=20)
        else:
            image.save(w_name)

        # md用のタグをh返却
        w_name = os.path.join("./", "f_name", "img", img_name)
        self.nvim.current.line = "![alt text]({})".format(w_name)
