# Day - 4 협업 일지(중급2)

#### 일자: 2025-09-09 / 정유빈

---

### 팀원들과 논의한 일

- 체험 기간이 길고 결제 안한 유저들 특징 찾아보기
- 지점별로 어떤 차이가 있는지(회사가 많은지, 등등) 확인해보기
- 왜 trial_day 가 많으면 결제율이 높아지는지 원인 찾기
- 지역별 특성을 찾아보기\*(가정한 지점별 근처 회사수, 교통수단, 인구밀집 등)

## \* 오늘 + 내가 한 일

- 지역별(지점별) 특징 찾아보기
  - 각 가정한 지점별 지역 특징을 찾아봐서 정리
  - ex) - 정동본 (site 1)
  - `상가건물들이 상당히 노후화 되어있음`
  - `테이크아웃 커피 전문점들이 굉장히 많음`
  - 통계지리정보서비스(SGIS) 기준 `중구` 내 일자리(행정·사무직, IT 연구개발직, 법률직) 수 정보
    - `시청역` : 657건
    - `충무로역` : 162건
    - `청구역` : 29건
    - `시청 vs 충무로` : 약 4.1배 많음
    - `시청 vs 청구` : 약 22.7배 많음
  - 위 통계로 보았을 때 사무·전문직들이 밀집되어있는 지역으로 볼 수 있음
- 각 site별 미 결제율 확인해보기
- 각 site_id에 해당되는 전체 데이터에서 is_payment == 0 인 구간 비율 확인

- 미결제그룹의 시계열적 특성 확인해보기

  - 미결제그룹의 체험이용 시간 확인해보기
  - 미결제 그룹(체험 2일이상)
    - 평균 체류 시간 : `약 17시간`
    - 평균 총 입실 횟수 : 약 7.3회
    - 평균 총 퇴실 횟수 : 약 7.1회

- 결제 그룹(체험 2일이상)
  - 평균 체류 시간 : `약 14시간`
  - 평균 총 입실 횟수 : 약 6.4회
  - 평균 총 퇴실 횟수 : 약 6.2회

## \* 사용했던 코딩

- `site_id` 별 미 결제 비율

```python
# 전체 사이트별 데이터 수
site_total = df['last_site_id'].value_counts()

# 미결제 그룹 (trial_day>=2 & is_payment==0)
non_payment = df[(df['trial_day'] >= 2) & (df["is_payment"] == 0)]
site_nonpay = non_payment['last_site_id'].value_counts()

# 미결제율 계산 (각 site별 비율)
site_ratio = (site_nonpay / site_total * 100).fillna(0)

# 색상 구분: 데이터 수 200대 vs 300 이상
colors = []
for site in site_ratio.index:
    if 200 <= site_total[site] < 300:
        colors.append("tomato")   # 200대
    elif site_total[site] >= 300:
        colors.append("steelblue")  # 300 이상
    else:
        colors.append("gray")     # 200 미만


# 바 그래프
plt.figure(figsize=(10,6))
bars = site_ratio.plot(kind="bar", color=colors)

plt.title("지점별 미결제율 (trial_day≥2 기준)", fontsize=14)
plt.xlabel("지점 ID", fontsize=12)
plt.ylabel("미결제율 (%)", fontsize=12)
plt.xticks(rotation=45)

# 바 위에 퍼센트 값 표시
for i, v in enumerate(site_ratio):
    plt.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=10)

# 범례 추가
import matplotlib.patches as mpatches
red_patch = mpatches.Patch(color="tomato", label="데이터 수 200대")
blue_patch = mpatches.Patch(color="steelblue", label="데이터 수 300 이상")
gray_patch = mpatches.Patch(color="gray", label="데이터 수 200 미만")
plt.legend(handles=[red_patch, blue_patch, gray_patch])

plt.tight_layout()
plt.show()
```

---

## \*문제점

- 오히려 찾아보는 데이터가 많아지면서 어떤걸 더 분석해야될지 혼동이 왔음
- 데이터를 정리했을 때 만족할만한 결과가 나오지 못해서 아쉬웠음
  - 정리
    - 체험일수↑ → 결제율↑ (but 초반 이탈 방지 중요)
    - 많이 사용하지만 결제 안 하는 유저 존재 → 단순 이용량 기반 전략의 한계
    - 입지 특성이 결제율 차이를 만든다 (사무직 밀집 vs 주거 상권 차이)
    - 초반 이탈자를 잡는 전략이 필요해보임
    - 입지별 직업군을 조사하여 세그먼트적 맟춤형 회원권 기획
  - 확실해보이는 아이템과 결론이 안나와서 답답함

## \* 회고

- EDA를 진행하는 과정에서 새로운 지표를 확인하거나 필터링 조건을 바꿀 때마다 분석 결과가 조금씩 달라졌음
- 그럴 때마다 데이터 해석이 복잡해지고, 팀 내에서 방향을 다시 맞추는 과정이 필요해 어려움이 있었음
- 여러 차례 가설을 세우고 데이터를 확인하며 결론을 수정하는 과정을 반복했는데, 내일은 이를 바탕으로 아이템을 도출할 수 있는 의미 있는 결과가 나오길...
