import requests
import json
import time
from bs4 import BeautifulSoup

from django.contrib.gis.geos import GEOSGeometry
from routepang.model.LocationModel import Location
from routepang.model.PreciousData import PreciousData

# request에 해당하는 명소(영어명)
# 최대 60개까지 가져옴
# json배열 형태로 return
class LocationController:

    def __init__(self):
        self.google_api_key = PreciousData.mapKey
        self.category = ["attraction", "food", "cafe"]

    def getLocationList(self, request):

        for i in range(3):
            location_list = []
            next_page_token = ""

            # next_page_token이 없을 때까지 넘어가면서 파싱
            while True:
                # attraction / food / cafe 정도로 category를 나눌 예정
                request_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + request + "+" + \
                              self.category[i] + "&key=" + self.google_api_key + "&pagetoken=" + next_page_token + \
                              "&language=ko"

                req = requests.get(request_url)
                html = req.text
                soup = BeautifulSoup(html, 'html.parser')

                # json 형태로 데이터 정제
                json_data = json.loads(str(soup))
                json_loaction_result = json_data["results"]

                location_list = location_list + json_loaction_result

                try:
                    next_page_token = json_data["next_page_token"]
                    # 마지막 페이지에서는
                    # next_page_token 키가 없기 때문에
                    # 키에러가 발생
                except KeyError:
                    next_page_token = "END"

                if next_page_token == "END":
                    break
                else:
                    time.sleep(2)

            self.insertLocation(request=location_list, category=i+1)

            # for i in location_list:
            #     print(i)

        return

    # 인스크램 크롤링 목록
    # 태그 검색을 위해 공백 X
    def getLocationNameList(self, request):

        nameList = []

        for i in request:
            # replace를 쓰기 위해 string으로 형변환
            place = str(i["name"])
            nameList.append(place.replace(" ", ""))

        return nameList

    # json 배열을 request
    # json형태의 데이터를 디비에 저장
    def insertLocation(self, request, category):

        for i in request:
            name = i["name"]

            # location_name으로 중복 검사
            if not Location.objects.filter(name=name).exists():

                place_id = i["place_id"]
                address = i["formatted_address"]

                lon = i["geometry"]["location"]["lng"]
                lat = i["geometry"]["location"]["lat"]
                coordinates = GEOSGeometry('POINT(' + str(lon) + ' ' + str(lat) + ')')

                #category는 추후 개선

                try:
                    image = i["photos"][0]["photo_reference"]
                except KeyError:
                    image = "no image"

                Location(place_id=place_id, address=address, name=name, coordinates=coordinates,
                         image=image, category=category).save()

        return
