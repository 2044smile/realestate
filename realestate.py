import json
import math
import requests
from bs4 import BeautifulSoup


keyword = "서초구"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}
url = "https://m.land.naver.com/search/result/{}".format(keyword)
init_response = requests.get(url, headers=headers)
init_response.raise_for_status()

soup = (str(BeautifulSoup(init_response.text, "lxml")))
"""
filter: {
    lat: '37.483564',
    lon: '127.032594',
    z: '13',
    cortarNo: '1165000000',
    cortarNm: '서초구',
    rletTpCds: '*',
    tradTpCds: '*'
},
"""
value = soup.split("filter: {")[1].split("}")[0].replace(" ", "").replace("'", "") # .replace(" ", "") 공백 제거 .replace("'", "") 작은따옴표 제거
lat = value.split("lat:")[1].split(",")[0] # "lat:" 제거, "," 제거 > lat:는 제거하고 뒤에 있는 값을 가지고 있는다
lon = value.split("lon:")[1].split(",")[0]
z = value.split("z:")[1].split(",")[0]
cortarNo = value.split("cortarNo:")[1].split(",")[0]
rletTpCds = value.split("rletTpCds:")[1].split(",")[0]
tradTpCds = value.split("tradTpCds:")[1].split()[0]

# lat - btm : 37.550985 - 37.4331698 = 0.1178152
# top - lat : 37.6686142 - 37.550985 = 0.1176292
lat_margin = 0.118

# lon - lft : 126.849534 - 126.7389841 = 0.1105499
# rgt - lon : 126.9600839 - 126.849534 = 0.1105499
lon_margin = 0.111

btm=float(lat)-lat_margin
lft=float(lon)-lon_margin
top=float(lat)+lat_margin
rgt=float(lon)+lon_margin

# 최초 요청 시 디폴트 값으로 설정되어 있으나, 원하는 값으로 구성
# rletTpCds="SG" #상가
tradTpCds="B1" #매매/전세/월세 매물 확인

# clusterList?view 를 통한 그룹(단지)의 데이터를 가져온다.
detail_url = "https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo={}&rletTpCd={}&tradTpCd={}&z={}&lat={}&lon={}&btm={}&lft={}&top={}&rgt={}"\
     .format(cortarNo, rletTpCds, tradTpCds, z, lat, lon,btm,lft,top,rgt)

detail_response = requests.get(detail_url, headers=headers)
json_str = json.loads(json.dumps(detail_response.json()))

values = json_str['data']['ARTICLE']
result_data = []

# 큰 원으로 구성되어 있는 전체 매물그룹(values)을 load 하여 한 그룹씩 세부 쿼리 진행
for v in values:
    lgeo = v['lgeo']
    count = v['count']
    z2 = v['z']
    lat2 = v['lat']
    lon2 = v['lon']

    len_pages = count / 20 + 1
    for idx in range(1, math.ceil(len_pages)):
        
        l_url = "https://m.land.naver.com/cluster/ajax/articleList?""itemId={}&mapKey=&lgeo={}&showR0=&" \
               "rletTpCd={}&tradTpCd={}&z={}&lat={}&""lon={}&totCnt={}&cortarNo={}&page={}"\
            .format(lgeo, lgeo, rletTpCds, tradTpCds, z2, lat2, lon2, count,cortarNo, idx)
        
        l_response = requests.get(l_url, headers=headers)
        l_data = l_response.json()

"""
{'code': 'success', 
    'paidPreSale': {  # 광고
        'preSaleComplexNumber': 6026967, 
        'preSaleComplexName': '서초아트래디앙', 
        'preSaleAddress': '서울시 서초구 서초동', 
        'preSaleAddressSector': '서초동',
        'preSaleDetailAddress': '1582-16', 
        'preSaleStageCode': 'C12', '
        'preSaleTypeCode': 'IA01', 
        'preSaleFormCode': '11', 
        'occupancyYearMonth': '2023.06', 
        'thumbnail': 'https://landthumb-phinf.pstatic.net/20231226_174/land_naver_1703553605142hVV1V_PNG/uploadfile_202303233002535.png', 
        'featureMarkTypeCode': '1', 
        'minPreSalePrice': 1455000000, 
        'maxPreSalePrice': 2600000000, 
        'minPreSaleArea': 60.74, 
        'maxPreSaleArea': 102.17, 
        'totalHouseholdsNumber': 24, 
        'preSaleHouseholdsNumber': 24, 
        'xcoordinate': 127.010792, 
        'ycoordinate': 37.486794, 
        'preSaleDetailsPageURL': 'https://isale.land.naver.com/NewiSaleMobile/Home/#SYDetail?build_dtl_cd=6026967&supp_cd=9038457'
    }, 
    'hasPaidPreSale': True, 'more': True, 'TIME': False, 'z': 13, 'page': 1, 
    'body': [
        {'atclNo': '2504375518', # 매물번호
        'cortarNo': '1165010600', 
        'atclNm': '잠원대우아이빌', 
        'atclStatCd': 'R0', 
        'rletTpCd': 'A01', 
        'uprRletTpCd': 'A01', 
        'rletTpNm': '아파트', 
        'tradTpCd': 'B1', # A1: 매매, B1: 전세, C1: 월세
        'tradTpNm': '전세', # 매매, 전세, 월세
        'vrfcTpCd': 'SITE', 
        'flrInfo': '중/12', # 층수
        'prc': 35000, 
        'rentPrc': 0, 
        'hanPrc': '3억 5,000', 
        'spc1': '51', 
        'spc2': '35.38', 
        'direction': '동향', 
        'atclCfmYmd': '25.01.24.', # 확인 날짜
        'repImgUrl': 
        '/20250124_283/1737727863849jsQnj_JPEG/591b46a118ff3b92e3f8bc97e59bb52a.JPG', 
        'repImgTpCd': 'SITE', 
        'repImgThumb': 'f130_98', 
        'lat': 37.511488, 
        'lng': 127.01827, 
        'atclFetrDesc': '원룸 분리형 융자무  전세대출가능 빠른입주가능', # 매물특징
        'tagList': ['25년이내', '역세권', '세대분리'], 
        'bildNm': '3동', 
        'minute': 0, 
        'sameAddrCnt': 1, 
        'sameAddrDirectCnt': 0, 
        'cpid': 'NEONET', 
        'cpNm': '부동산뱅크', 
        'cpCnt': 1, 
        'rltrNm': '부동산멘토공인중개사사무소', 
        'directTradYn': 'N', 
        'minMviFee': 0, 
        'maxMviFee': 0, 
        'etRoomCnt': 0, 
        'tradePriceHan': '', 
        'tradeRentPrice': 0, 
        'tradeCheckedByOwner': False, 
        'cpLinkVO': {
            'cpId': 'NEONET', 
            'mobileArticleLinkTypeCode': 'NONE', 
            'mobileBmsInspectPassYn': 'Y', 
            'pcArticleLinkUseAtArticleTitle': False, 
            'pcArticleLinkUseAtCpName': False, 
            'mobileArticleLinkUseAtArticleTitle': False, 
            'mobileArticleLinkUseAtCpName': False
        }, 
        'dtlAddrYn': 'N', 
        'dtlAddr': '', 
        'isVrExposed': False}, 
    }
}
"""