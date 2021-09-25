from gui_widget_pyqt5 import *

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
melon = requests.get('https://www.melon.com/chart/index.htm', headers=header) # Top 100 차트 크롤링
melon_html = melon.text
melon_parse = BeautifulSoup(melon_html, 'html.parser')

lst100 = melon_parse.select('.lst50,.lst100')

melonDict = {}
for i in lst100:
    temp_list = [i.select_one('.ellipsis.rank01').a.text, i.select_one('.ellipsis.rank02').a.text]
    melonDict[int(i.select_one('.rank').text)] = temp_list

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow(melonDict)
    mainWindow.show()
    sys.exit(app.exec_())