# coding:utf-8

import os
import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import platform
import time


def rename_files(url, path):
    audio_url = url
    if not os.path.isdir(path):
        print '路径有误，请检查！'
    else:
        # header = {}
        # header['Host'] = 'www.justing.com.cn'
        # header['Origin'] = 'http://www.justing.com.cn'
        # header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 ' \
        #                         '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        # header['Referer'] = 'http://www.justing.com.cn/auth/login'
        #
        # # 模拟登录
        # login_url = 'http://www.justing.com.cn/auth/login?nextUrl='
        # up_form = {'username': 'swjasonyang@gmail.com', 'password': '0205006'}
        # login_session = requests.session()
        # ret = login_session.post(login_url, data=up_form, headers=header)
        # if ret.status_code != 200:
        #     print '获取信息失败！状态码%d，%s' % (ret.status_code, str(ret.reason))
        #     return False
        # else:
        #     # 跳转到书籍对应页面
        #     header['Referer'] = 'http://www.justing.com.cn/'
        #     ret = login_session.get(audio_url, headers=header)
        #     if ret.status_code != 200:
        #         print '跳转页面失败！状态码%d，%s' % (ret.status_code, str(ret.reason))
        #         return False
        #     else:
        #         name_list = []
        #         ret_html = ret.text
        #         print ret_html
        #         xpath_tree = html.fromstring(ret_html)
            # raw_list = xpath_tree.xpath('//a[@class="opt download-btn"]/@href')
            # for item in raw_list:
            #     name_list.append(item.encode('utf-8').split('attrname=')[1])
            #     print item

            # 遍历目录
            # file_list = os.listdir(path)
            # count = 1
            # for item in name_list:
            #     item_content = item.split('\n')[1].encode('utf-8')
            #     print item_content
                # if item_content in file_list:
                #     new_item = '%02d.%s' % (count, item_content)
                #     new_name = os.path.join(path, new_item)
                #     os.rename(os.path.join(path, item_content), new_name)
                #     count += 1

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


        # try:
        #     element = WebDriverWait(driver).until(
        #         EC.presence_of_element_located((By.CLASS_NAME,
        #                 'list list-col5 main-books-list-col5 newest-books-list-col5')))
        # except:
        #     driver.quit()
        time.sleep(4)
        #time.sleep(5)

        print driver.current_url
        # driver.switch_to.window(driver.window_handles[0])
        # driver.get('http://www.justing.com.cn/')
        # element = driver.find_element_by_id('home-recommend')
        driver.get(audio_url)
        # cur_window = driver.current_window_handle
        # driver.implicitly_wait(4)
        # driver.refresh()
        # cur_window = driver.current_window_handle
        # try:
        #     element = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.CLASS_NAME,
        #                 'list list-col main-audios-list book-audios-list')))
        # except:
        #     driver.quit()
        # driver.switch_to.window(driver.window_handles[0])
        #time.sleep(10)
        driver.switch_to.frame(0)
        print driver.current_url
        down_url_list = driver.find_elements_by_xpath('//li[@class="item cf"]')
        for item in down_url_list:
            if '.mp3' in item:
                print item.split('attrname=')[1]
        # down_url = driver.find_elements_by_class_name('list list-col main-audios-list book-audios-list')
        # for item in down_url:
        #     print item
        print driver.page_source



if __name__ == '__main__':
    print '请输入相对网址：'
    audio_url = 'http://www.justing.com.cn/' + raw_input()
    print '请输入音频文件全路径：'
    audio_dir = raw_input()
    rename_files(audio_url, audio_dir)