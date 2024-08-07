# if you want to use this, 
# install ffmpeg.exe to the project folder

import os
import sys
import yt_dlp
import datetime

from pathlib import Path

from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QDir, Qt, QUrl, QSize, QObject, QTimer
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QSlider, QStyle,
                             QVBoxLayout, QWidget, QStatusBar, QLineEdit, QComboBox, QFileDialog)

class App(QWidget):

    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        self.mainFont = self.font()
        self.mainFont.setPointSize(13)

        self.ru_RU = 'ru_RU'
        self.en_US = 'en_US'

        self.path = os.path.expanduser('~/Downloads').replace(os.sep, '/')

        self.videoLink = QLineEdit()
        self.downloadBtn = QPushButton()
        self.directory = QLineEdit()
        self.searchFolderBtn = QPushButton()

        self.videoLink.setPlaceholderText("Insert video link")
        self.downloadBtn.setText("     Download     ")
        self.directory.setPlaceholderText("Select a folder (default: downloads)")
        self.searchFolderBtn.setText("  Select  ")

        self.videoLink.setFont(self.mainFont)

        self.downloadBtn.setFont(self.mainFont)
        self.downloadBtn.clicked.connect(self.download_video)

        self.directory.setFont(self.mainFont)

        self.searchFolderBtn.setFont(self.mainFont)
        self.searchFolderBtn.clicked.connect(self.search)

        self.restoreDir()

        videoLayout = QHBoxLayout()
        videoLayout.addWidget(self.videoLink)
        videoLayout.addWidget(self.downloadBtn)

        dirLayout = QHBoxLayout()
        dirLayout.addWidget(self.directory)
        dirLayout.addWidget(self.searchFolderBtn)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(10, 0, 10, 0)
        mainLayout.addLayout(videoLayout)
        mainLayout.addLayout(dirLayout)

        self.setMaximumHeight(170)
        self.setMaximumWidth(520)
        self.setLayout(mainLayout)

    def download_video(self):
        try:
            url = self.videoLink.text()
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
                'outtmpl': os.path.join(self.path, '%(title)s.%(ext)s'),
                'timestamp': datetime.date.today()
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                ydl.process_ie_result(info_dict, download=True)
        except Exception as e:
            print(e)

    def search(self):
        self.path = QFileDialog.getExistingDirectory()
        self.directory.setText(self.path)

        if os.path.isfile("data.txt"):
            with open("data.txt", "w") as data:
                data.write(f'{self.path}')
        else:
            with open("data.txt", "x") as data:
                data.write(f'{self.path}')

    def restoreDir(self):
        if os.path.isfile("data.txt"):
            with open("data.txt", "r+") as data:
                self.path = data.read()
                if self.path != '' and self.path != os.path.expanduser('~/Downloads').replace(os.sep, '/'):
                    self.directory.setText(self.path)
                else:
                    self.path = os.path.expanduser('~/Downloads').replace(os.sep, '/')
                    with open("data.txt", 'w') as dat:
                        dat.write(f'{self.path}')
        else:
            with open("data.txt", "x") as data:
                self.path = os.path.expanduser('~/Downloads').replace(os.sep, '/')
                data.write(f'{self.path}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = App()
    downloader.setWindowTitle("Video downloader")
    downloader.resize(520, 170)
    downloader.show()
    sys.exit(app.exec())
