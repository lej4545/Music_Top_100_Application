from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome(r'C:\Users\EunJin\PycharmProjects\lol_project\chromedriver.exe')

driver.get("https://www.melon.com/chart/index.htm")
title = driver.find_elements_by_class_name('ellipsis.rank01')
singer = driver.find_elements_by_class_name('ellipsis.rank02')

melonList = {}

for i in range(100):
    melonList[i+1] = [title[i].text, singer[i].text]

driver.close()

print('순위','[노래 제목,가수 이름]')
for rank_number,song in melonList.items():
    print(rank_number, song)


ranking_number = int(input('\n몇번째 순위의 음악을 들을지 입력해주세요(1 ~ 100)'))

keyword = melonList[ranking_number][0] + ' ' + melonList[ranking_number][1]
url = 'https://www.youtube.com/results?search_query={}'.format(keyword)
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()

print('음악을 검색 중입니다...잠시만 기다려주세요.')

video_url = soup.select('a#video-title')
video_url = 'https://www.youtube.com' + video_url[0].get('href')
print(video_url)

