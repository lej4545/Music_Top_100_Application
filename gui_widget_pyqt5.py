import sys
from PyQt5.QtWidgets import *
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import random
import datetime
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self, melonDict):
        super().__init__()
        # 윈도우 설정
        self.setGeometry(300, 300, 800, 770)  # x, y, w, h
        self.setWindowTitle('음악 차트 TOP 100 프로그램')

        # --- label 생성
        time = datetime.datetime.now().strftime('%Y년 %m월 %d일 %H시 기준')
        self.time_label = QLabel(self)
        self.time_label.setGeometry(540, 10, 800, 50)
        self.time_label.setText(time)
        self.font = self.time_label.font()
        self.font.setFamily('Times New Roman')
        self.font.setBold(True)
        self.time_label.setFont(self.font)

        self.label1 = QLabel(self)
        self.label1.setGeometry(25, 35, 400, 60)
        self.label1.setText('듣고 싶은 노래를 더블클릭 해주세요!')
        self.font1 = self.label1.font()
        self.font1.setBold(True)
        self.label1.setFont(self.font1)

        self.setupTableUI(melonDict)
        self.tableWidget.cellDoubleClicked.connect(self.DoubleClicked_tablewidget)

        # --- 랜덤 재생 버튼 생성
        self.random_button = QPushButton(self);
        self.random_button.move(25, 710)
        self.random_button.setText('랜덤 재생')

        # 선택 재생 버튼 시그널
        self.random_button.clicked.connect(self.clicked_random_button)

    # Table 위젯 설정
    def setupTableUI(self, melonDict):
        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(750, 600)
        self.tableWidget.setRowCount(100)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setTableWidgetData(melonDict)
        self.tableWidget.move(25,85)

    # Table 위젯에 들어갈 데이터 입력
    def setTableWidgetData(self, melonDict):
        column_headers = ['노래 제목', '가수 이름']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        for rank in melonDict:
            for idx in range(2):
                self.tableWidget.setItem(rank-1, idx, QTableWidgetItem(melonDict[rank][idx]))

        self.tableWidget.setColumnWidth(0, 450)
        self.tableWidget.setColumnWidth(1, 230)

    # cell 더블 클릭시 실행 함수
    def DoubleClicked_tablewidget(self, row, column):
        if column == 0:
            title = self.tableWidget.item(row, column).text()
            name = self.tableWidget.item(row, column+1).text()
        elif column == 1:
            title = self.tableWidget.item(row, column-1).text()
            name = self.tableWidget.item(row, column).text()
        keyword = title + ' ' + name
        self.start_youtube(keyword)


    # 랜덤 버튼 클릭시 실행 함수
    def clicked_random_button(self):
        row = random.randrange(0, 100)
        title = self.tableWidget.item(row, 0).text()
        name = self.tableWidget.item(row, 1).text()
        keyword = title + ' ' + name
        self.start_youtube(keyword)

    # 랜덤 재생 버튼 클릭 시 youtube 실행 함수
    def start_youtube(self, keyword):
        youtube_req = requests.get('https://www.youtube.com/results?search_query=' + keyword)
        youtube_html = youtube_req.text
        youtube_parse = BeautifulSoup(youtube_html, 'html.parser')
        script = youtube_parse.select('html > body > script')[13]
        if 'ytInitialData = ' in script.text:
            jsonStr = script.text.strip()
            jsonStr = jsonStr.replace('var ytInitialData = ', '')
            jsonObj = json.loads(jsonStr[:-1])

        video_url = \
        jsonObj['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0][
            'itemSectionRenderer']['contents'][0]['videoRenderer']['navigationEndpoint']['commandMetadata'][
            'webCommandMetadata']['url']
        video_url = 'https://www.youtube.com' + video_url
        driver = webdriver.Chrome(r'C:\Users\EunJin\PycharmProjects\lol_project\chromedriver.exe')
        driver.get(video_url)