import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import  datetime

from routepang.model.ArticleModel import Article

class ArticleController:

    # 해당 url의 게시물의 정보 추출 후
    # summary, image, favicon 순서의 배열 리턴
    def getInfoFromArticle(self, request):

        print(time.time(), 'start getInfo')
        req = requests.get(request)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        articleInfo = []

        summary = soup.find("meta", property="og:title")
        image = soup.find("meta", property="og:image")
        # favicon = soup.find("link", rel="icon")

        summary = summary["content"] if summary else "No Summary"
        image = image["content"] if image else "No Image"
        # favicon = "https://www.instagram.com" + str(favicon["href"]) if favicon else "No Fav"

        articleInfo.append(summary)
        articleInfo.append(image)
        articleInfo.append(request)

        try:
            data = json.loads(soup.find('script', type='application/ld+json').text)
            reg_date = str(data['uploadDate']).replace("T", " ")
        # 등록 시간이 되있지 않으면
        # 크롤링하는 현재 시간으로 등록
        except AttributeError:
            reg_date = str(datetime.now())[:19]

        articleInfo.append(reg_date)

        print(time.time(), 'end getInfo')

        return articleInfo

    def insertArticle(self, request, locaion_id):

        print(time.time(), 'start insert')

        # 중복검사(url) 추가
        if not Article.objects.filter(url=request[2]).exists():
            Article(location_id=locaion_id, image=request[1], summary=request[0], reg_date=request[3]
                   , url=request[2]).save()

        print(time.time(), 'end inert')

        return