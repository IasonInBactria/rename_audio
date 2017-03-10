# coding:utf-8

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def rename_files(url, path):
    audio_url = url
    if not os.path.isdir(path):
        print '路径有误，请检查！'
    else:
        driver = webdriver.Firefox()

        # 先登录且为会员才能获取到链接
        driver.maximize_window()
        driver.get('http://www.justing.com.cn/auth/login')
        email_addr = driver.find_element_by_id('username')
        email_addr.send_keys('swjasonyang@gmail.com')
        password = driver.find_element_by_id('password')
        password.send_keys('0205006')
        login_button = driver.find_element_by_xpath('//a[@class="submit-btn"]')
        login_button.click()
        time.sleep(4)
        print driver.current_url
        driver.get(audio_url)
        driver.switch_to.frame(0)
        print driver.current_url
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'opt download-btn')))
        except:
            driver.close()
        down_url_list = driver.find_elements(By.XPATH, '//a[@class="opt download-btn"]')
        name_list = []
        for item in down_url_list:
            cur_link = item.get_attribute('href')
            if 'http' in cur_link:
                cur_file_name = cur_link.split('attname=')[1].split('.mp3')[0].encode('utf-8')
                cur_file_name = urllib.unquote(cur_file_name)
                name_list.append(cur_file_name)

if __name__ == '__main__':
    print '请输入相对网址：'
    input_url = 'http://www.justing.com.cn/' + raw_input()
    print '请输入音频文件全路径：'
    audio_dir = raw_input()
    rename_files(input_url, audio_dir)