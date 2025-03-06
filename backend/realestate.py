import re
import json
import math
import time
import random
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


class NaverLandCrawler:
    def __init__(self, trad_tp_cds, rlet_tp_cds, tags, wprc_max, z, regions):
        self.base_url = "https://m.land.naver.com"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

        self.trad_tp_cds = trad_tp_cds # 거래 유형 코드 eg. "B1" 전세, "A1" 매매, "B2" 월세
        self.rlet_tp_cds = rlet_tp_cds # 매물 유형 코드 eg. "DDDGG" 오피스텔, "VL" 빌라, "APT" 아파트
        self.tags = tags # 특정 조건 태그 eg. "TWOROOM" 투룸 매물, "PARKINGYN" 주차 가능 매물
        self.wprc_max = wprc_max # 최대 가격 eg. 30000 3억 원
        self.z = z # 지도 줌 레벨 eg. "13" 구 단위, "14" 동

        self.regions = regions
        self.result_data = []

    def get_region_info(self, keyword):
        """지역 검색 후 위도, 경도 및 cortarNo(지역 코드) 가져오기"""
        url = f"{self.base_url}/search/result/{keyword}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            print(f"[Error] {keyword} 지역 정보 요청 실패: {response.status_code}")
            return None
        
        soup = str(BeautifulSoup(response.text, "lxml"))
        try:
            value = soup.split("filter: {")[1].split("}")[0].replace(" ", "").replace("'", "")
            lat = value.split("lat:")[1].split(",")[0]
            lon = value.split("lon:")[1].split(",")[0]
            cortar_no = value.split("cortarNo:")[1].split(",")[0]
            return lat, lon, cortar_no
        except IndexError:
            print(f"[Error] {keyword} 지역 정보 파싱 실패")
            return None

    def fetch_listings(self, lat, lon, cortar_no, region_name):
        """해당 지역의 매물 리스트 가져오기"""
        lat_margin, lon_margin = 0.118, 0.111
        btm, lft, top, rgt = float(lat) - lat_margin, float(lon) - lon_margin, float(lat) + lat_margin, float(lon) + lon_margin
        trad_tp_cds, rlet_tp_cds, tags, wprc_max, z = "B1", "DDDGG,VL", "TWOROOM,PARKINGYN", 30000, 13

        detail_url = f"{self.base_url}/cluster/clusterList?view=atcl&cortarNo={cortar_no}&tradTpCd={trad_tp_cds}&rletTpCd={rlet_tp_cds}&z={z}&lat={lat}&lon={lon}&tag={tags}&btm={btm}&lft={lft}&top={top}&rgt={rgt}&wprcMax={wprc_max}"
        response = requests.get(detail_url, headers=self.headers)
        
        if response.status_code != 200:
            print(f"[Error] {region_name} 매물 리스트 요청 실패: {response.status_code}")
            return []

        try:
            json_data = response.json()
            return json_data.get('data', {}).get('ARTICLE', [])
        except json.JSONDecodeError:
            print(f"[Error] {region_name} JSON 파싱 실패")
            return []

    def fetch_articles(self, listings, cortar_no, region_name):
        """개별 매물 상세 정보 가져오기"""
        trad_tp_cds, rlet_tp_cds, tags, wprc_max, z = "B1", "DDDGG,VL", "TWOROOM,PARKINGYN", 30000, 13

        for listing in listings:
            lgeo, count, lat2, lon2 = listing['lgeo'], listing['count'], listing['lat'], listing['lon']
            len_pages = math.ceil(count / 20)

            for idx in range(1, len_pages + 1):
                print(f"[{region_name}] 매물 {lgeo} - 페이지 {idx}")
                list_url = f"{self.base_url}/cluster/ajax/articleList?itemId={lgeo}&lgeo={lgeo}&tradTpCd={trad_tp_cds}&rletTpCd={rlet_tp_cds}&tag={tags}&z={z}&lat={lat2}&lon={lon2}&totCnt={count}&cortarNo={cortar_no}&page={idx}&wprcMax={wprc_max}"
                
                time.sleep(random.uniform(1, 3))
                response = requests.get(list_url, headers=self.headers)

                if not response.text.strip():
                    print("[Error] 응답이 비어 있음")
                    continue
                
                try:
                    json_data = response.json()
                except json.JSONDecodeError:
                    print("[Error] JSON 파싱 실패")
                    continue

                articles = json_data.get('body', [])
                for article in articles:
                    self.parse_article(article, region_name)

    def parse_article(self, article, region_name):
        """매물 상세 정보 파싱"""
        atcl_no = article.get('atclNo')
        if not atcl_no:
            print("[Error] 매물 번호 없음")
            return
        
        atcl_url = f"https://fin.land.naver.com/articles/{atcl_no}"
        response = requests.get(atcl_url, headers=self.headers)

        if response.status_code != 200:
            print(f"[Error] 매물 상세 페이지 요청 실패: {atcl_url}")
            return

        description = re.search(r'<span class="ArticleDetailInfo_description__AFP5K">(.*?)</span>', response.text, re.DOTALL)
        price = re.search(r'<span class="ArticleSummary_info-price__BD9wv">(.*?)</span>', response.text, re.DOTALL)
        cost = re.search(r'<div class="ArticlePriceInfo_area-data__Ec_SF">(.*?)</span>', response.text, re.DOTALL)

        description_text = description.group(1) if description else ""
        price_text = price.group(1) if price else ""
        cost_text = cost.group(1).split('<')[0] if cost else ""
        location_url = f"{self.base_url}/near/article/{atcl_no}" # 매물 주소

        self.result_data.append({
            'region': region_name,
            'atcl_no': atcl_no,
            'atcl_url': atcl_url,
            'atcl_price': " ".join(price_text.split(' ')[1:]),
            'atcl_cost': cost_text,
            'atcl_description': description_text,
            'atcl_location_': location_url
        })

    def save_to_csv(self, region):
        """결과를 CSV 파일로 저장"""
        today = datetime.now().strftime("%Y%m%d")
        df = pd.DataFrame(self.result_data)
        file_name = f"./data/{region}_{today}.csv"
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        print(f"[Success] 데이터 저장 완료: {file_name}")

    def run(self):
        """크롤러 실행"""
        for region in self.regions:
            region_info = self.get_region_info(region)
            if not region_info:
                continue
            lat, lon, cortar_no = region_info
            listings = self.fetch_listings(lat, lon, cortar_no, region)
            self.fetch_articles(listings, cortar_no, region)
            self.save_to_csv(region=region)


# 서울시 전체 구 리스트
regions = ["강남구"]
# regions = ["강남구", "서초구", "종로구", "마포구", "송파구", "용산구"]
crawler = NaverLandCrawler(regions)
crawler.run()
