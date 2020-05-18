import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from routepang.model.ArticleModel import Article
from routepang.model.PreciousData import PreciousData

class CrawlingController:

    # aws에 올린 후 수정 필요
    Driver_Dir = "/Users/cy/PycharmProjects/chromedriver"

    def __init__(self):
        self.usrId = PreciousData.id
        self.pwd = PreciousData.password

        self.driver = webdriver.Chrome(self.Driver_Dir)
        self.driver.implicitly_wait(10)

        # ------- Instagram Login -------- #
        self.driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        elem = self.driver.find_element_by_xpath("//input[@name='username']")
        elem.send_keys(self.usrId)
        elem = self.driver.find_element_by_xpath("//input[@name='password']")
        elem.send_keys(self.pwd)
        self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[4]/button").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[2]").click()

        # 페이지가 인스타 그램인지 확인
        assert "Instagram" in self.driver.title

    def __del__(self):
        self.driver.close()

    # 해당 명소에 대한 최신 게시물 url 리스트 return
    def getAllArticle(self, request):
        time.sleep(3)
        t = time.time()
        print(t, 'start get all article:')

        # db에 저장할 url의 리스트를 담아 놓을 리스트
        url_list = []

        elem = self.driver.find_element_by_xpath("//input[@placeholder='검색']")
        # location_name으로 검색창에 검색
        # name에 태그에 들어가면 안되는 문자도 사용 가능
        elem.send_keys(request)

        time.sleep(2)
        # 검색 결과 맨 위를 클릭
        try:
            self.driver.find_element_by_css_selector('div.fuqBx > a').click()
        # 검색 결과가 없는 경우 체크
        except NoSuchElementException:
            return url_list
        # 검색한 페이지가 로딩될 때 까지 대기
        time.sleep(3)

        print(t, request, '-> start')

        # 현재 스크롤 위치
        # cur_height = 0;
        # total_height = self.driver.execute_script("return document.body.scrollHeight")

        now_height = self.driver.execute_script("return document.body.scrollHeight")

        # 스크롤 하면서 article url 크롤링
        while True:
            # if cur_height+1000 > total_height:
            #     cur_height = total_height
            # else:
            #     cur_height = cur_height + 1000
            # self.driver.execute_script("window.scrollTo(0, %s);" % cur_height)

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            print(time.time(), 'pressing pagedown with delay')
            time.sleep(1)

            # Search by Tag
            link_url = self.driver.find_elements_by_css_selector('article.KC1QD > div > div > div > div > a')
            # Search by Location
            if not len(link_url) > 0:
                link_url = self.driver.find_elements_by_css_selector('article.vY_QD > div > div > div > div > a')
            # Search by Page
            if not len(link_url) > 0:
                link_url = self.driver.find_elements_by_css_selector('article.FyNDV > div > div > div > div > a')

            # 해당 게시물에 #{location} 태그가 있는지 확인(보류) #

            for i in link_url:
                # DB에 들어있는 article data 중복 확인
                if not Article.objects.filter(url=i).exists():
                    url_list.append(i.get_attribute('href'))
                #TODO 사진 카테고리 확인해서 목적에 맞지 않는 게시물인 경우

            # 중복 url 제거
            url_list = list(set(url_list))
            # 가져온 게시물이 50개 이상이면 break
            print('length of Url List:', len(url_list))
            if len(url_list) >= 50:
                break


            # print(cur_height, total_height)
            #
            # # 스크롤이 마지막에 도달하면
            # if cur_height == total_height:
            #     time.sleep(10)
            #     total_height = self.driver.execute_script("return document.body.scrollHeight")
            #     print('Updated total height:', total_height)
            #     if cur_height == total_height:
            #         break

            time.sleep(3)
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            if now_height == last_height:
                break
            now_height = last_height


        print(time.time(), 'elapsed time:', time.time() - t)

        return url_list