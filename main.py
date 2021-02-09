import sys
import os

from PyQt5.QtWidgets import *
from PyQt5 import uic

from checkingDialog import CheckingDialog
from from_tweeter import *


main_form_class = uic.loadUiType('main.ui')[0]


class WindowClass(QMainWindow, main_form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(266, 277)
        self.is_check_image = False
        self.user_list = []
        self.download_path = os.path.join(os.getcwd(), 'downloaded')

        # 버튼 시그널
        self.btnAdd.clicked.connect(self.id_add)
        self.btnCrawl.clicked.connect(self.crawl_tweet)
        self.btnOpenExplorer.clicked.connect(self.open_explorer)
        self.btnClear.clicked.connect(self.clear_list)

        # 체크 박스 시그널
        self.chkCheckImage.stateChanged.connect(self.change_check_image)

        # 텍스트 박스 시그널
        self.txtInput.returnPressed.connect(self.id_add)

        # 리스트 위젯 시그널
        self.lstUsers.itemDoubleClicked.connect(self.id_remove)

        # 폴더 생성
        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)

    def change_check_image(self):
        # for Debug
        print(self.chkCheckImage.isChecked())

        self.is_check_image = self.chkCheckImage.isChecked()

    def id_add(self):
        user_id = self.txtInput.text()

        # 리스트 박스 아이템 추가
        self.lstUsers.addItem(user_id)

        # 텍스트 박스 지우기
        self.txtInput.setText('')

        # 유저 리스트에 추가
        self.user_list.append(user_id)

        # for Debug
        print(self.user_list)

    def clear_list(self):
        self.lstUsers.clear()

    def id_remove(self):
        # 리스트 위젯에서 아이템 삭제
        id_row = self.lstUsers.currentRow()
        self.lstUsers.takeItem(id_row)

        # 리스트에서 아이템 삭제
        del(self.user_list[id_row])

        # for Debug
        print(self.user_list)

    def open_explorer(self):
        #  이미 있는지 홧인
        path = os.path.realpath('./downloaded')
        os.startfile(path)

    def crawl_tweet(self):
        if any(self.user_list):
            # 다운로드 큐 생성
            download_list = []
            for user in self.user_list:
                # 폴더 생성
                saved_folder = os.path.join(self.download_path, user)
                if not os.path.exists(saved_folder):
                    os.mkdir(saved_folder)

                # 스핀 박스에서 값 가져옴
                tweet_count = self.spChunk.value()
                print(f'spinbox value: {tweet_count}')
                
                for status in get_status_by_id(user, tweet_count):
                    download_list.extend(get_media_from_status(status))

                for media in download_list:
                    if self.is_check_image:
                        dialog = CheckingDialog(media_data=media)

                        # ok = 1, cancel = 0
                        if dialog.exec_() == 1:
                            download(media['url'], saved_folder, media['file_name'])

                    else:
                        download(media['url'], saved_folder, media['file_name'])

                    # 다운로드 이후 작업
                    print('download ' + media['file_name'])

            QMessageBox.about(self, "Complete", "크롤링이 끝났습니다.")

        else:
            QMessageBox.warning(self, "It's Empty", "유저 목록이 비었습니다.")
    

if __name__ == '__main__':
    # 참고 자료 : https://wikidocs.net/35482

    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
