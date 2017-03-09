# coding:utf-8

import os
import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
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

        time.sleep(4)
        #time.sleep(5)

        print driver.current_url
        # driver.switch_to.window(driver.window_handles[0])
        # driver.get('http://www.justing.com.cn/')
        # element = driver.find_element_by_id('home-recommend')
        driver.get(audio_url)
        driver.switch_to.frame(0)
        print driver.current_url
        driver.implicitly_wait(20)
        print driver.page_source
        # 不知道为啥，Firefox加载不出来下载链接，windows可以。。。
        down_url_list = driver.find_elements(By.XPATH, '//a[@class="opt download-btn"]')
        name_list = []
        for item in down_url_list:
            cur_link = item.get_attribute('href')
            if 'http' in cur_link:
                cur_file_name = cur_link.split('attname=')[1].split('.mp3')[0].encode('utf-8')
                cur_file_name = urllib.unquote(cur_file_name)
                name_list.append(cur_file_name)

        # 遍历目录
        file_list = os.listdir(path)
        count = 1
        for item in name_list:
            if item in file_list:
                new_item = '%02d.%s' % (count, item)
                new_name = os.path.join(path, new_item)
                os.rename(os.path.join(path, item), new_name)
                count += 1




if __name__ == '__main__':
    print '请输入相对网址：'
    audio_url = 'http://www.justing.com.cn/' + raw_input()
    print '请输入音频文件全路径：'
    audio_dir = raw_input()
    rename_files(audio_url, audio_dir)