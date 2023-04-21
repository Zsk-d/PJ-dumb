import requests
import json, time
from os import makedirs  
from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# INDEX_URL="https://t.bilibili.com/774047106626224280" 
INDEX_URL="https://www.bilibili.com/video/BV1ba4y1N7s4" 
RESULTS_DIR='results'
#结果文件夹 
RESULTS_FILE='comments.xlsx'
RESULTS_FILE2 ='comments2.xlsx'

exists(RESULTS_DIR)or makedirs(RESULTS_DIR)
#文件夹不存在就新建
                               
import os  
import pandas as pd


#修改完整代码  
def crawlComments():  
    print('hi*1')
    # 反屏蔽选项设置  
    options = webdriver.ChromeOptions()  
  
    options.add_argument("--no-sandbox")  
    options.add_experimental_option('excludeSwitches',['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    print('hi*2')
    browser = webdriver.Chrome(options=options)

    wait = WebDriverWait(browser,120,poll_frequency=0.5,ignored_exceptions=None)
    print('hi*3')
    try:  
        print('hi*4')
        browser.get(INDEX_URL)
        wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='reply-end-mark']")))
        # 判断是否有元素:loading-state 文本：没有更多评论  
        js = "window.scrollTo(0,document.body.scrollHeight)"  
        while True:  
            browser.execute_script(js)
            try:
                time.sleep(2)  
                end = browser.find_element(By.CSS_SELECTOR, ".reply-end-mark")  
            except: 
                end=browser.find_element(By.CSS_SELECTOR,".reply-end") 
                if end.text == "没有更多评论":  
                    break
                
                
        # 提取评论  
        names = browser.find_elements(By.CSS_SELECTOR, ".user-name") 
        texts = browser.find_elements(By.CSS_SELECTOR, ".root-reply > .reply-content")  
        times = browser.find_elements(By.CSS_SELECTOR, ".reply-info > .reply-time")

        # 将评论转换为数据列表  
        data = []  
        
        for i in range(len(names)):  
            # 将图标替换为文本  
            if texts[i].text == "":  
                temp = texts[i].find_element(By.CSS_SELECTOR, "img").get_attribute("alt")  
            else:  
                temp = texts[i].text  
            data.append((names[i].text, temp, times[i].text))

    except Exception:  
        print("访问超时")

    # 将评论数据保存到 Excel 文件中  
    header = ["ID", "留言", "时间"]  
    df = pd.DataFrame(data, columns=header)  
    df.to_excel(f'{RESULTS_DIR}/{RESULTS_FILE}', index=False, header=header)  


if __name__ == '__main__':
    html=crawlComments() # 爬取评论                                                                                              