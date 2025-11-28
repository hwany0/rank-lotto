# 완전 최종판: lotto_all.json 자동 업데이트 + 빠른 검색
import requests
from bs4 import BeautifulSoup
import json
import os
import time

# 1. 최신 회차 가져오기 (메인 페이지 크롤링)
def get_latest_round():
    try:
        url = "https://dhlottery.co.kr/common.do?method=main"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        latest = soup.find("strong", id="lottoDrwNo").text.strip()
        return int(latest)
    except Exception as e:
        print(f"최신 회차 가져오기 실패: {e}")
        return None

# 2. 특정 회차 번호 가져오기
def get_lotto_numbers(drwNo):
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drwNo}"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        if data["returnValue"] == "success":
            return {
                "round": data["drwNo"],
                "numbers": [data[f"drwtNo{i}"] for i in range(1,7)],
                "bonus": data["bnusNo"],
                "date": data["drwNoDate"]
            }
    except:
        pass
    return None

# 3. lotto_all.json 자동 업데이트 (기존 있으면 추가만!)
def update_lotto_db():
    latest = get_latest_round()
    if not latest:
        print("최신 회차를 가져오지 못했습니다.")
        return

    if os.path.exists("lotto_all.json"):
        print("기존 데이터 불러오는 중...")
        with open("lotto_all.json", "r", encoding="utf-8") as f:
            lotto_db = json.load(f)
        print(f"현재 저장된 회차: {max(lotto_db.keys())})회까지")
    else:
        lotto_db = {}
        print("새로 저장 시작")

    start_no = max([int(k) for k in lotto_db.keys()], default=0) + 1
    if start_no > latest:
        print(f"이미 최신 데이터입니다! ({latest}회차까지 있음)")
        return lotto_db

    print(f"{start_no}회부터 {latest}회까지 추가 저장 중...")
    added = 0
    for no in range(start_no, latest + 1):
        result = get_lotto_numbers(no)
        if result:
            lotto_db[str(no)] = result
            added += 1
            if added % 10 == 0:
                print(f"   → {no}회차 추가 완료 ({added}개)")
        time.sleep(0.05)  # 서버 부하 방지

    # 저장
    with open("lotto_all.json", "w", encoding="utf-8") as f:
        json.dump(lotto_db, f, ensure_ascii=False, indent=2)

    print(f"업데이트 완료! 총 {len(lotto_db)}회차 저장됨 (신규 {added}회 추가)")
    return lotto_db

# 4. 실행!
lotto_db = update_lotto_db()
