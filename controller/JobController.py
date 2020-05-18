from routepang.controller.LocalController import LocationController
from routepang.controller.CrawlingController import CrawlingController
from routepang.controller.UrlController import UrlController
from routepang.controller.ArticleController import ArticleController

from routepang.model.LocationModel import Location
from routepang.model.UrlModel import Url

from datetime import datetime
from time import time

def urlTask():

    print("Crawling start at: " + str(datetime.now()))

    # -------- ( Add Location ) -------- #
    # TODO 테스트용 주석
    # location_controller = LocationController()
    # # 추후 도시 추가
    # # Country + City
    # location_controller.getLocationList(request="프랑스+파리")

    # -------- ( Add Url ) -------- #

    crawling_controller = CrawlingController()
    url_controller = UrlController()

    nameList = Location.objects.all()

    for location in nameList:
        # -----url을 얼마나 가져울지 판단(100개 정도)----- (보류) #
        # 해당 location에 해당하는 게시물들중, 현재 날짜를 기준으로 오래된 게시물들 삭제 (보류)

        place = str(location.name)
        urlList = crawling_controller.getAllArticle(request=place)

        for url in urlList:
            url_controller.insertUrl(request=url, location_id=location.location_id)

    del crawling_controller
    # del location_controller
    del url_controller

    return


def infoTask():

    # append를 사용하기 위한 list 선언
    urlList = []
    article_controller = ArticleController()
    for obj in Url.objects.all():
        urlList.append(obj)

    for url in urlList:
        info = article_controller.getInfoFromArticle(request=url.url)
        article_controller.insertArticle(request=info, locaion_id=url.location_id)

        # TODO : 도중에 데이터가 들어가는 것을 감안
        current_urlList = Url.objects.all()
        # 현재 db에 있는 url 양이 더 많을 경우
        if len(urlList) < current_urlList.count():
            # 새로운 url만큼 urlList에 추가
            for new_url in current_urlList[len(urlList):current_urlList.count()]:
                urlList.append(new_url)

    del article_controller

    return