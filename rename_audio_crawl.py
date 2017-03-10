# coding:utf-8

import os
import requests
from lxml import html
import json
import urllib


def rename_files(url, path):
    audio_url = url
    if not os.path.isdir(path):
        print '路径有误，请检查！'
    else:
        header = {}
        header['Host'] = 'www.justing.com.cn'
        header['Origin'] = 'http://www.justing.com.cn'
        header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 ' \
                                '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        header['Referer'] = 'http://www.justing.com.cn/auth/login'

        # 模拟登录
        login_url = 'http://www.justing.com.cn/auth/login?nextUrl='
        up_form = {'username': 'swjasonyang@gmail.com', 'password': '0205006'}
        login_session = requests.session()
        ret = login_session.post(login_url, data=up_form, headers=header)
        if ret.status_code != 200:
            print '获取信息失败！状态码%d，%s' % (ret.status_code, str(ret.reason))
            return False
        else:
            # 跳转到书籍对应页面
            header['Referer'] = 'http://www.justing.com.cn/'
            ret = login_session.get(audio_url, headers=header)
            if ret.status_code != 200:
                print '跳转页面失败！状态码%d，%s' % (ret.status_code, str(ret.reason))
                return False
            else:
                name_list = []
                ret_html = ret.text
                print ret_html
                xpath_tree = html.fromstring(ret_html)
                # 获取book_id
                book_id = xpath_tree.xpath('//div[@id="books-detail"]/@data-book_id')[0].encode('utf-8')
                # 获取audio_id
                raw_audio_list = xpath_tree.xpath('//ul[@class="list list-col main-audios-list book-audios-list"]'
                                                  '/li[@class="item cf  " or @class="item cf default-hide-item "]'
                                                  '/@data-audio_id')
                audio_id_list = []
                for item in raw_audio_list:
                    audio_id_list.append(item.encode('utf-8'))
                header['Referer'] = audio_url
                for item in audio_id_list:
                    req_url = 'http://www.justing.com.cn/audios/files/api?book_id=' \
                              '%s&audio_id=%s&action=download' % (book_id, item)
                    ret = login_session.get(req_url, headers=header)
                    if ret.status_code != 200:
                        print '获取当前文件名%s失败！状态码%d，%s' % (item, ret.status_code, str(ret.reason))
                    else:
                        ret_json = json.loads(ret.text)
                        cur_file_name = ret_json['files']['file'].split('attname=')[1].split('.mp3')[0].encode('utf-8')
                        # 解析形如%E7%A9%BF%E8%B6%8A%E7%99%BE%E5%B9%B4%E4%B8'的URL字符串
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
    input_url = 'http://www.justing.com.cn/' + raw_input()
    print '请输入音频文件全路径：'
    audio_dir = raw_input()
    rename_files(input_url, audio_dir)