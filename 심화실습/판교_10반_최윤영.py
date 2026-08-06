from pathlib import Path
import json
from collections import defaultdict, Counter
import sys

base = Path(__file__).parent
json_path = base / "Python_Practice2_Data.json"

with open(json_path, encoding="utf-8") as f:
    sales = json.load(f)

#-----------------------------------
# 1) 리스트/딕셔너리 컴프리헨션
# ----------------------------------

# ① amount ≥ 1000인 거래만 필터링
high_sales = [sale for sale in sales if sale["amount"] >= 1000]

# ② 지역별 총매출 dict를 컴프리헨션으로 계산 
regions = {sale["region"] for sale in sales}

region_total = {
    region: sum(sale["amount"] for sale in sales if sale["region"] == region)
    for region in regions
}

print("지역별 총매출 : ", region_total)

# Checkpoint
assert region_total["서울"] == sum(sale["amount"] for sale in sales if sale["region"] == "서울")
assert region_total["부산"] == sum(sale["amount"] for sale in sales if sale["region"] == "부산")
assert region_total["대구"] == sum(sale["amount"] for sale in sales if sale["region"] == "대구")
print("Checkpoint 통과")


# ----------------------------------
# 2) Counter + defaultdict 
# ----------------------------------

# ① 지역별 거래 건수 계산
region_count = Counter(sale["region"] for sale in sales)
print("지역별 거래 건수 : ", region_count)

# ② 카테고리별 amount 리스트
category_amount = defaultdict(list)

for sale in sales:
    category_amount[sale["category"]].append(sale["amount"])

print("카테고리별 금액 리스트 : ", category_amount)

#Checkpoint
print("지역별 거래 건수가 많은 지역부터 출력 : ", region_count.most_common())


# ----------------------------------
# 3) 제너레이터 - 메모리 비교
# ----------------------------------

# 제너레이터
def high_amount_generator(data):
    for sale in data:
        if sale["amount"] > 1000:
            yield sale

generator = high_amount_generator(sales)

# 리스트
high_amount_list = [sale for sale in sales if sale["amount"] > 1000]

print("제네레이터 메모리 : ", sys.getsizeof(generator))
print("리스트 메모리 : ", sys.getsizeof(high_amount_list))

# Checkpoint
assert sys.getsizeof(generator) < sys.getsizeof(high_amount_list)
print("제네레이터가 리스트보다 메모리를 적게 사용합니다.")


# ----------------------------------
# 4) 종합 - 월별 카테고리 매출 집계 
# ----------------------------------

# 월별 기준 총매출 딕셔너리 생성
monthly_category_sales = defaultdict(lambda: defaultdict(int))

for sale in sales:
    monthly_category_sales[sale["month"]][sale["category"]] += sale["amount"]

monthly_category_sales = { 
    month: dict[category]
    for month, category in monthly_category_sales.items()
}

print("월별 카테고리 매출 집계 : ", monthly_category_sales)

# Checkpoint
# Top 3 금액 내림차순 정렬
top3 = sorted(sales, key=lambda x: x["amount"], reverse=True)[:3]

print("Top 3 매출 집계 : ", top3)

assert top3 == sorted(top3, key=lambda x: x["amount"], reverse=True)
print("Top 3 정렬 강화 확인")