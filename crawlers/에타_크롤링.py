import os
import sys
import time
import random
from time import sleep
import urllib.request
from urllib.request import urlretrieve

import numpy as np
import pandas as pd
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image

# ChromeDriver 자동 설치 및 경로 설정
chromedriver_autoinstaller.install()

# 크롬 옵션 설정 (GUI 안 띄우고 싶다면 headless 사용)
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('lang=ko_KR')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# 드라이버 실행
driver = webdriver.Chrome(options=chrome_options)

# 웹페이지 접속
driver.get('https://everytime.kr/login')
driver.implicitly_wait(5)

# 로그인 시도

#wait = WebDriverWait(driver, 10)
#login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"]')))
#login_btn.click()

# 수동 로그인 안내 및 대기
print("브라우저에서 아이디/비밀번호를 입력하고 로그인 버튼을 눌러주세요.")
input("로그인 후 이 콘솔에 돌아와 엔터 키를 눌러 계속합니다.")

# 에브리타임 크롤링
dictionary = {}
page = 0

content_, comment_, like_, comment_count_, scrap_, time_texts = [], [], [], [], [], []
wait = WebDriverWait(driver, 10)

while True:
    print('page', page)
    if page > 499:
        break
    page += 1
    driver.get(f"https://everytime.kr/375120/p/{page}")
    sleep(1)

    posts = driver.find_elements(By.CSS_SELECTOR, 'article > a.article')
    links = [p.get_attribute('href') for p in posts]

    for link in links:
        driver.get(link)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
        sleep(0.5)

        post = driver.find_element(By.TAG_NAME, 'article')
        status = post.find_element(By.CSS_SELECTOR, 'ul.status.left')

        like_.append(status.find_element(By.CSS_SELECTOR, 'li.vote').text)
        comment_count_.append(status.find_element(By.CSS_SELECTOR, 'li.comment').text)
        scrap_.append(status.find_element(By.CSS_SELECTOR, 'li.scrap').text)

        time_texts.append(post.find_element(By.CSS_SELECTOR, 'time.large').text)

        title = post.find_element(By.CSS_SELECTOR, 'h2.large').text
        paras = post.find_elements(By.CSS_SELECTOR, 'p.large')
        comment_list = []
        for i, p in enumerate(paras):
            if i == 0:
                content_.append(f"{title} {p.text}")
            else:
                comment_list.append(p.text)
        comment_.append(comment_list)

# DataFrame 구성
df = pd.DataFrame({
    'content':       content_,
    'comment':       comment_,
    'like':          like_,
    'comment_count': comment_count_,
    'scrap':         scrap_,
    'date':          time_texts
})

df.to_csv('everytime_crawling.csv', index=False)
print("크롤링 완료: everytime_crawling.csv로 저장되었습니다.")