from urllib.request import *
from PIL import Image

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *


dialog_ui = uic.loadUiType('imgview.ui')[0]


class CheckingDialog(QDialog, dialog_ui):
    def __init__(self, media_data=None):
        QDialog.__init__(self, parent=None)
        self.setupUi(self)
        self.setFixedSize(400, 300)
        self.file_name = 'temp.png'

        q_pixmap_var = QPixmap()

        if media_data is None:
            # 테스트 루틴
            url_string = r'https://avatars1.githubusercontent.com/u/44885477?s=460&v=4'
            image_from_web = urlopen(url_string).read()
            q_pixmap_var.loadFromData(image_from_web)
        else:
            urlretrieve(media_data['preview'], self.file_name)

            # 리사이즈
            with Image.open(self.file_name) as image:
                image_small = image.resize((399, 259), Image.ANTIALIAS)
                image_small.save(self.file_name)

            q_pixmap_var.load(self.file_name)

        self.picChecking.setPixmap(q_pixmap_var)
        self.lblTypes.setText(self.file_name)

    def __del__(self):
        # 소멸자에서 파일 삭제
        import os
        if os.path.exists(self.file_name):
            os.remove(self.file_name)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dialog = CheckingDialog()
    res = dialog.exec_()
    print(res)
    sys.exit(app.exec_())
