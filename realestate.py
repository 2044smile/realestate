import re
import json
import math
import time
import random
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


keyword = "서초구"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}
url = "https://m.land.naver.com/search/result/{}".format(keyword)
init_response = requests.get(url, headers=headers)
init_response.raise_for_status()

if init_response.status_code != 200:
    print(f"Error: Received status code {init_response.status_code}")
    print("Response text:", init_response.text)

soup = (str(BeautifulSoup(init_response.text, "lxml")))

value = soup.split("filter: {")[1].split("}")[0].replace(" ", "").replace("'", "")
lat = value.split("lat:")[1].split(",")[0]
lon = value.split("lon:")[1].split(",")[0]
z = value.split("z:")[1].split(",")[0]
cortarNo = value.split("cortarNo:")[1].split(",")[0]

lat_margin = 0.118
lon_margin = 0.111

btm = float(lat) - lat_margin
lft = float(lon) - lon_margin
top = float(lat) + lat_margin
rgt = float(lon) + lon_margin

tradTpCds = "B1"
rletTpCds = "DDDGG,VL"
tags = "TWOROOM,PARKINGYN"

detail_url = "https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo={}&tradTpCd={}&rletTpCd={}&z={}&lat={}&lon={}&tag={}&btm={}&lft={}&top={}&rgt={}"\
    .format(cortarNo, tradTpCds, rletTpCds, z, lat, lon, tags, btm, lft, top, rgt)

detail_response = requests.get(detail_url, headers=headers)
json_str = json.loads(json.dumps(detail_response.json()))

values = json_str['data']['ARTICLE']
"""
{'lgeo': '212032330', 'count': 326, 'lat': 37.4765625, 'lon': 126.99853516, 'psr': 0.8, 'tourExist': True}, 
{'lgeo': '212210111', 'count': 1117, 'lat': 37.50625, 'lon': 127.01679688, 'psr': 0.8, 'tourExist': False}
"""
result_data = []

for v in values:
    lgeo = v['lgeo']
    count = v['count']
    z2 = z  # 지역구에 따라 정해지는 것 같음
    lat2 = v['lat']
    lon2 = v['lon']

    len_pages = math.ceil(count / 20)

    l_data = []  # l_data를 리스트로 초기화
    for idx in range(1, len_pages + 1):
        print(f"{v}-{idx}")
        l_url = "https://m.land.naver.com/cluster/ajax/articleList?itemId={}&mapKey=&lgeo={}&showR0=&" \
                "tradTpCd={}&rletTpCd={}&tag={}&z={}&lat={}&lon={}&tag=&totCnt={}&cortarNo={}&page={}"\
            .format(lgeo, lgeo, tradTpCds, rletTpCds, tags, z2, lat2, lon2, count, cortarNo, idx)
        
        time.sleep(random.uniform(1, 3))
        l_response = requests.get(l_url, headers=headers)

        if not l_response.text.strip():  # 응답이 비어 있는 경우
            print("Error: Response is empty")
        else:
            try:
                l_data = l_response.json()
            except json.JSONDecodeError:
                print("Error: Response is not a valid JSON")
                print(l_response.text)  # 응답 내용을 출력해서 문제 파악

        if 'body' not in l_data:
            print("Error: 'body' key not found in response")
            print(l_data)  # 문제 파악을 위해 출력
            continue  # 다음 페이지로 이동

        for article in l_data['body']:
            atcl_no = article.get('atclNo')

            if not atcl_no:
                print("No atclNo found in article.")
                continue
                
            f_url = f"https://fin.land.naver.com/articles/{atcl_no}"
            f_response = requests.get(f_url, headers=headers)
            if f_response.status_code != 200:
                print(f"Error: Received status code {f_response.status_code} for article URL: {f_url}")
                continue
            
            introduction_to_sale = re.search(r'<span class="ArticleDetailInfo_description__AFP5K">(.*?)</span>', f_response.text, re.DOTALL) # 매물소개
            # price = re.search(r'<span class="ArticleSummary_info-price__BD9wv">(.*?)</span>', f_response.text, re.DOTALL) # 매물 전세가
            # cost = re.search(r'<div class="ArticlePriceInfo_area-data__Ec_SF">(.*?)</span>', f_response.text, re.DOTALL) # 매물 관리비
            if introduction_to_sale:
                description_text = introduction_to_sale.group(1)
            else:
                description_text = ''

            article_info = {
                'lgeo': lgeo,
                'count': count,
                'z': z2,
                'lat': lat2,
                'lon': lon2,
                'atcl_no': atcl_no,
                # 'atcl_price': price,
                'atcl_description': description_text
            }

            # article_info를 리스트에 추가
            result_data.append(article_info)

# today 날짜를 사용해 파일 이름을 생성
today = datetime.now()
formatted_data = today.strftime("%Y%m%d")

# result_data를 사용해 DataFrame 생성
df = pd.DataFrame(result_data)

# CSV 파일로 저장
file_name = f"./data/{formatted_data}.csv"
df.to_csv(file_name, index=False, encoding='utf-8-sig')