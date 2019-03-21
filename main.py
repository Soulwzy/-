from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time

class Spider:

    def __init__(self):
        self.c_service = Service('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        self.c_service.command_line_args()
        self.c_service.start()

        chrome_options = Options()
        chrome_options.add_argument('--headless')                #不显示界面
        #chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options = chrome_options)
        self.url = "https://music.163.com/#/discover/toplist?id=3778678"

        '''找到所有热门歌曲的URL和歌曲名称'''
    def find_allSong(self):
        # self.driver.implicitly_wait(10)
        #print("start")
        WebDriverWait(self.driver, 3, 0.5).until(lambda driver: self.driver.find_element_by_id("g_iframe"))
        #print("All download")
        self.driver.switch_to.frame(self.driver.find_element_by_id("g_iframe"))
        # with open("test3.html",'w',encoding='UTF-8') as file_obj:
        #     file_obj.write(self.driver.page_source)

        # header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
        # response = driver.get(self.url,headers = header)                      #请求网址
        # print(response.request.headers)
        # print(response.headers)

        # print(response.status_code)
        # print(response.content.decode("utf-8"))

        soup = BeautifulSoup(self.driver.page_source, "lxml")  #
        song_list = soup.find('tbody')  # 找到所有歌曲
        all_song = song_list.find_all('tr')
        for each_song in all_song:
            each_info = each_song.find('span', class_="txt")
            # each_info_2 = each_song.find('span', class_="title")
            #each_info = each_song.find_all('span')
            long_time = each_song.find('span',class_ = "u-dur").text
            author = each_song.find('span',class_ = "icn icn-share")['data-res-author']
            link = "https://music.163.com/" + each_info.find('a')['href']
            name = each_info.find('b')['title']
            print('歌曲连接 : {}, 歌曲名 : {},作者 : {}，时长 : {}'.format(link, name, author, long_time))
            self.comment(link,name)     #爬取评论


    def comment(self,link , name ):
        self.driver.execute_script("window.open('%s')"%link)
        # print(self.driver.window_handles)
        # print(self.driver.current_window_handle)
        self.driver.switch_to.window(window_name=self.driver.window_handles[1])
        # print(self.driver.current_window_handle)
        WebDriverWait(self.driver, 3, 0.5).until(lambda driver: self.driver.find_element_by_id("g_iframe"))
        self.driver.switch_to.frame(self.driver.find_element_by_id("g_iframe"))
        page = 0
        with open(name + "-评论信息.csv", 'w', encoding="utf-8") as fp:
            fp.write('评论者,评论内容,评论日期' + '\n')

        while True:
            page += 1
            soup = BeautifulSoup(self.driver.page_source, "lxml")
            all_comment = soup.find_all('div', class_='itm')
            #print(soup)
            for each_comment in all_comment:
                comment_name = each_comment.find('a', class_='s-fc7').text
                tmp = each_comment.find('div', class_='cnt f-brk').text
                date = each_comment.find('div',class_ = 'time s-fc4').text
                comment = tmp.replace(comment_name + '：', '')
                #print(comment_name, comment)

                with open(name +"-评论信息.csv",'a+',encoding="utf-8") as fp:
                    fp.write(comment_name + ',' + comment + ',' + date + '\n')

            '''
            下一页
            '''
            try:
                print("{}--第{}页.".format(name,page))
                next = self.driver.find_element_by_xpath('//*[starts-with(@class,"zbtn znxt") and not(contains(@class,"js-disabled"))]') #xpath路径匹配节点
            except:
                print(self.driver.current_window_handle)
                self.driver.switch_to.window(window_name=self.driver.window_handles[0])
                print(self.driver.current_window_handle)
                self.driver.close()  # 关闭当前窗口

                return
            #last = self.driver.find_element_by_xpath('//*[starts-with(@class,"zbtn znxt js-n") and contains(@class,"js-disabled")]')
            else:
                next.send_keys(Keys.ENTER)

                time.sleep(0.5)


    def run(self):
        self.driver.get(self.url)       #启动浏览器
        self.find_allSong()
        #self.comment()
        #self.driver.close()             # 关闭当前窗口
        self.driver.quit()              # 关闭进程

    def __del__(self):
        self.c_service.stop()


if __name__ == '__main__':
    spider = Spider()
    spider.run()