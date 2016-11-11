# coding: utf-8
import os
import json
import random
import string

import datetime
import requests
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from django.http import HttpResponse

CONST_GNB_MENU_INFO              = ''
CONST_GNB_MENU_INFO_DATA         = ""
CONST_INIT_APP_INFO              = ""
CONST_DEAL_DETAIL_HEAD           = ""
CONST_DEAL_DETAIL_TAIL           = ""
CONST_URL_DEAL_LIST              = ""
CONST_FILE_TEMPLATE_PATH         = ""
CONST_FILE_BENEFIT_ZONE_DATA     = CONST_FILE_TEMPLATE_PATH + "benefit_zone.json"
CONST_FILE_BENEFIT_ZONE_PAGE     = CONST_FILE_TEMPLATE_PATH + "benefit_zone_page.json"
CONST_FILE_EVENT_LIST_ARRAY_DATA = CONST_FILE_TEMPLATE_PATH + "event_list_array.json"
CONST_FILE_JSON_PATH             = CONST_FILE_TEMPLATE_PATH + "json/"
CONST_DOMAIN                     = ""
# CONST_DOMAIN                     = "http://127.0.0.1:8000/"

def getBenefitZone(request):
    page = int(request.GET.get('page', 1))
    if 1 == page:
        # gnbmenuinfo를 서버에서 받아와서 셋팅 할 수 있게 하기 위한 데이터
        r = requests.get(CONST_GNB_MENU_INFO_DATA, stream=True)

        # json 불러오기
        data = json.loads(r.text)

        jsonMenu = json.loads(CONST_GNB_MENU_INFO)

        # api json을 열어서 데이터 가공함
        with open(CONST_FILE_BENEFIT_ZONE_DATA) as json_file:
            json_data = json.load(json_file)
            json_data["gnbmenuinfo"] = data["gnbmenuinfo"]
            json_data["gnbmenuinfo"]["menulist"].insert(1, jsonMenu)

        # 이벤트 데이터를 가공함
        content_type = request.GET.get('content_type')
        if (content_type == "event_banner") or (content_type == "benefit_banner"):
            is_refresh = int(request.GET.get('is_refresh', 0))
            with open(CONST_FILE_EVENT_LIST_ARRAY_DATA) as json_file:
                json_event_list_array = json.load(json_file)
                json_event_list_array["content_type"] = content_type
                json_data["result_set"].append(json_event_list_array)
                json_data["total_count"] = 30
                json_data["total_page"] = 2
                json_data["per_page"] = 20
                json_data["page"] = page
                json_data["next"] = CONST_DOMAIN + "api/benefitZone?page=2&content_type=" + content_type
                if content_type == "event_banner":
                    json_data["result_set"][1]["data"][1]["is_select"] = 1
                else:
                    json_data["result_set"][1]["data"][2]["is_select"] = 1
            if 0 == is_refresh:
                print json_data["result_set"]
                json_data["result_set"].pop(0) # event 리스트에서는 롤링 제거
        else:
            json_data["result_set"][1]["data"][0]["is_select"] = 1


    elif 1 < page:
        with open(CONST_FILE_BENEFIT_ZONE_PAGE) as json_file:
            json_data = json.load(json_file)
        content_type = request.GET.get('content_type')
        if (content_type == "event_banner") or (content_type == "benefit_banner"):
            json_data["result_set"][0]["content_type"] = content_type

    return HttpResponse(json.dumps(json_data))

def getinitAppInfo(request):
    # gnbmenuinfo를 서버에서 받아와서 셋팅 할 수 있게 하기 위한 데이터
    r = requests.get(CONST_INIT_APP_INFO, stream=True)

    # json 불러오기
    data = json.loads(r.text)

    jsonMenu = json.loads(CONST_GNB_MENU_INFO)

    # api json을 열어서 데이터 가공함
    data["result_set"]["gnb"]["menu"][0]["loc"].insert(1, jsonMenu)
    data["result_set"]["gnb"]["menu"][0]["updatetime"] = 1559846742

    return HttpResponse(json.dumps(data))

def getDealPromotion(request):
    page = int(request.GET.get('page', 1))
    jsonDealPromotion = json.loads('{}')
    jsonDealPromotion["code"] = 1
    jsonDealPromotion["message"] = ""
    jsonDealPromotion["total_count"] = 100
    jsonDealPromotion["total_page"] = 5
    jsonDealPromotion["per_page"] = 20
    jsonDealPromotion["page"] = page
    jsonDealPromotion["result_set"] = json.loads('{"deals":[]}')
    if (1 == page):
        jsonDealPromotion["result_set"]["deals"].append(json.loads('{"title":"1페이지 1번째 그룹","list":[]}'))
        addDeal(jsonDealPromotion["result_set"]["deals"][0]['list'], 0, 5)
        jsonDealPromotion["result_set"]["deals"].append(json.loads('{"title":"1페이지 2번째 그룹","list":[]}'))
        addDeal(jsonDealPromotion["result_set"]["deals"][1]['list'], 5, 20)
    if (2 == page):
        jsonDealPromotion["result_set"]["deals"].append(json.loads('{"title":"","list":[]}'))
        addDeal(jsonDealPromotion["result_set"]["deals"][0]['list'], 20, 25)
        jsonDealPromotion["result_set"]["deals"].append(json.loads('{"title":"2페이지 1번째 그룹","list":[]}'))
        addDeal(jsonDealPromotion["result_set"]["deals"][1]['list'], 25, 40)
    if (3 == page):
        jsonDealPromotion["result_set"]["deals"].append(json.loads('{"title":"","list":[]}'))
        addDeal(jsonDealPromotion["result_set"]["deals"][0]['list'], 40, 60)
    if (4 == page):
        jsonDealPromotion["result_set"]["deals"].append(json.loads('{"title":"4페이지 1번째 그룹","list":[]}'))
        addDeal(jsonDealPromotion["result_set"]["deals"][0]['list'], 60, 62)
        jsonDealPromotion["result_set"]["deals"].append(json.loads('{"title":"","list":[]}'))
        addDeal(jsonDealPromotion["result_set"]["deals"][1]['list'], 62, 67)
        jsonDealPromotion["result_set"]["deals"].append(json.loads('{"title":"4페이지 2번째 그룹","list":[]}'))
        addDeal(jsonDealPromotion["result_set"]["deals"][2]['list'], 67, 80)
    if (5 == page):
        jsonDealPromotion["result_set"]["deals"].append(json.loads('{"title":"","list":[]}'))
        addDeal(jsonDealPromotion["result_set"]["deals"][0]['list'], 80, 84)
        jsonDealPromotion["result_set"]["deals"].append(json.loads('{"title":"5페이지 1번째 그룹","list":[]}'))
        addDeal(jsonDealPromotion["result_set"]["deals"][1]['list'], 84, 100)
    if (5 > page):
        jsonDealPromotion["next"] = CONST_DOMAIN + "api/dealPromotion?page=" + str(page + 1)
    else:
        jsonDealPromotion["next"] = ""

    return HttpResponse(json.dumps(jsonDealPromotion))

def addDeal(data, start, end):
    for i in range(start, end):
        with open(CONST_FILE_JSON_PATH + str(i) + ".json") as json_file:
            print i
            json_data = json.load(json_file)
            data.append(json_data)
    return

def getDealDetail(request, deal_id):
    # gnbmenuinfo를 서버에서 받아와서 셋팅 할 수 있게 하기 위한 데이터
    r = requests.get(CONST_DEAL_DETAIL_HEAD + deal_id + CONST_DEAL_DETAIL_TAIL, stream=True)

    mode = int(request.GET.get("mode", 0))

    if (0 == mode):
        data = getOptionDeal(request, r)
    elif (1 == mode):
        data = getOptionCalendar(request, r)

    return HttpResponse(json.dumps(data))

def date():
    date.date = datetime.datetime.now()

def getOptionCalendar(request, r):

    data = json.loads(r.text)

    is_usable = request.GET.get("is_usable", "N")
    depth = int(request.GET.get("depth", 0))
    range_start = request.GET.get("range_start", "2016-05-10")
    date.date = datetime.datetime.strptime(str(range_start),"%Y-%m-%d")
    is_business_days = int(request.GET.get("is_business_days", 0))

    def date_by_adding_business_days(from_date, add_days):
        business_days_to_add = add_days
        current_date = from_date
        while business_days_to_add > 0:
            current_date += datetime.timedelta(days=1)
            weekday = current_date.weekday()
            if weekday >= 5: # sunday = 6
                continue
            business_days_to_add -= 1
        return current_date

    date.date = date.date - datetime.timedelta(days=1)

    for optionItem in data["option_info"]["list"]:
        item = optionItem["value"]
        if 1 < depth:
            subOptions = item["sub_options"]
            def findSubOptions(subOptions, count):
                count = count + 1
                for subOption in subOptions:
                    if (count > depth):
                        if (1 == is_business_days):
                            date.date = date_by_adding_business_days(date.date, 1)
                        else:
                            date.date = date.date + datetime.timedelta(days=1)
                        subOption["option_date"] = date.date.strftime("%Y-%m-%d")
                        subOption["option_value"] = date.date.strftime("%Y-%m-%d")
                    else:
                        findSubOptions(subOption["sub_options"], count)
            findSubOptions(subOptions, 2)
        else:
            if (1 == is_business_days):
                date.date = date_by_adding_business_days(date.date, 1)
            else:
                date.date = date.date + datetime.timedelta(days=1)
            item["option_date"] = date.date.strftime("%Y-%m-%d")
            item["option_value"] = date.date.strftime("%Y-%m-%d")

    data["calendar_info"] = json.loads('{"is_usable":"' + is_usable + '", "depth":' + str(depth) + ',"current_date":"' + datetime.datetime.now().strftime("%Y-%m-%d") + '","range":{"from":"' + range_start + '", "to":"' + date.date.strftime("%Y-%m-%d") + '"}}')

    return data

def updateDeal(request):
    for page in range(1, 6):
        # 딜을 업데이트 함
        r = requests.get(CONST_URL_DEAL_LIST + str(page), stream=True)

        # json 불러오기
        data = json.loads(r.text)

        if not os.path.isdir(CONST_FILE_JSON_PATH):
            os.mkdir(CONST_FILE_JSON_PATH)

        # api json을 열어서 데이터 가공함
        startIndex = (page - 1) * 20
        for i in data["data"]:
            f = open(CONST_FILE_JSON_PATH + str(startIndex) + ".json", 'w')
            f.write(json.dumps(i))
            f.close()
            startIndex = startIndex + 1

        time.sleep(0.5)

    return HttpResponse('완료')

def makeDummyImage(request):
    font = ImageFont.truetype(CONST_FILE_TEMPLATE_PATH + 'font/Averia-Bold.ttf', 50)
    for page in range(1, 21):

        if (20 > page):
            img = Image.new('RGB', (758, 2048), (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)))
        else:
            img = Image.new('RGB', (758, 200))

        d = ImageDraw.Draw(img)
        d.text((20, 20), 'Deal Detail E Area ' + str(page), fill=(random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)), font=font)

        img.save(CONST_FILE_TEMPLATE_PATH + 'images/e_' + str(page) + '.png')

    return HttpResponse('완료')

def makeDummyThumbNail(request):
    font = ImageFont.truetype(CONST_FILE_TEMPLATE_PATH + 'font/Averia-Bold.ttf', 100)
    for page in range(1, 101):

        img = Image.new('RGB', (460, 460), (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)))

        d = ImageDraw.Draw(img)
        d.text((20, 20), random.choice(string.letters) + random.choice(string.letters) + random.choice(string.letters) + random.choice(string.letters) + random.choice(string.letters), fill=(random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)), font=font)

        img.save(CONST_FILE_TEMPLATE_PATH + 'images/thumb_' + str(page) + '.png')

    return HttpResponse('완료')

def makeDummyType(request):
    font = ImageFont.truetype(CONST_FILE_TEMPLATE_PATH + 'font/Averia-Bold.ttf', 50)
    for page in range(1, 10):

        if (9 > page):
            img = Image.new('RGB', (758, 2048), (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)))
        else:
            img = Image.new('RGB', (758, 200), (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)))

        d = ImageDraw.Draw(img)
        d.text((20, 20), 'Type 9 ' + str(page), fill=(random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)), font=font)

        img.save(CONST_FILE_TEMPLATE_PATH + 'images/type_9_' + str(page) + '.png')

    return HttpResponse('완료')
