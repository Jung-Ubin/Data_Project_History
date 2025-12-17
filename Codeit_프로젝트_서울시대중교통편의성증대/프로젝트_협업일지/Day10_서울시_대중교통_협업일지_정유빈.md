# Day - 10 협업 일지

일자: 2025-05-28 / 정유빈

---

### 팀원들과 한 작업

- 보고서 보완 및 발표자료 준비

# \* 내가 한 일

- 보고서 발표 관련 준비

- 보고서 제출 전 다듬기

- 통계 바 그래프 python 코드로 다시 출력하기

---

# \* 사용했던 코딩

(서울시*인구밀집도대비*정류장&노선\_수 시각화(subplot))

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 1. 한글 폰트 설정 (예: 맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False       # 마이너스 기호 깨짐 방지

# 2. CSV 파일 읽기
df = pd.read_csv('C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/01_인구밀도대비노선_정류장_분석(전처리).csv', encoding='utf-8-sig')
# 3. 컬럼명 정리
df = df.rename(columns={
    '구': 'area',
    '인구밀집도 대비 정류장수': 'bus_stop',
    '인구밀집도 대비 노선수': 'route'
})

# 4. 각각 그래프 정렬
df_stop_sorted = df.sort_values(by='bus_stop', ascending=False)
df_line_sorted = df.sort_values(by='route', ascending=False)

# 5. 색상 설정
def get_bar_colors(지역_시리즈):
    return [
        '#ED7D31' if x == '동작구' else          # 지역구 순위 변경될 때 가시성 올리기
        '#5DADE2' if x == '성동구' else
        'gray'
        for x in 지역_시리즈
    ]

# 6. 시각화
fig, ax = plt.subplots(ncols=2, figsize=(12, 8))

# 왼쪽: 정류장
colors_left = get_bar_colors(df_stop_sorted['area'])
ax[0].barh(df_stop_sorted['area'], df_stop_sorted['bus_stop'], color=colors_left)
ax[0].set_xlabel('인구 밀집도 대비 정류장 수')
ax[0].invert_xaxis()                             # 그래프 방향 바꾸기
ax[0].invert_yaxis()

# 왼쪽 그래프 y축에서 구 강조
highlight_gu = ['동작구', '성동구']
for i, label in enumerate(ax[0].get_yticklabels()):
    if label.get_text() in highlight_gu:
        label.set_backgroundcolor('#FFF2CC')     # 연한 노랑 같은 색


# 오른쪽: 노선
colors_right = get_bar_colors(df_line_sorted['area'])
ax[1].barh(df_line_sorted['area'], df_line_sorted['route'], color=colors_right)
ax[1].set_xlabel('인구 밀집도 대비 노선 수')
ax[1].invert_yaxis()
ax[1].yaxis.tick_right()

# 오른쪽 그래프 y축에서 구 강조
highlight_gu = ['동작구', '성동구']
for i, label in enumerate(ax[1].get_yticklabels()):
    if label.get_text() in highlight_gu:
        label.set_backgroundcolor('#FFF2CC')


# 전체 제목
fig.suptitle('자치구별 인구밀집도 대비 정류장 & 노선 수', fontsize=16)

plt.tight_layout()
plt.show()
```

---

# \*문제점

- 분석 요약 파트의 내용이 부실하여 다시 처음부터 작성 시도  
  분석 과정을 3단계로 나눠서 각 파트 별 어떤 과정을 거쳤는지 요약하여 추가함

- 분석 방법(머신러닝활용부분) 설명이 부족하다는 멘토님 피드백을 받음  
  머신러닝을 어떻게 사용했는지 설명 페이지를 추가하여 내용 보충

# \* 회고

- invert_xaxis(), yaxis.tick_right() 이런 코드들은 앞으로 시각화 할 때 자주 사용할 수 있는 코드들 같다.  
  기억해놓으면 좋을 것 같다.

- 보고서 흐름이나 테마(서식) 등 전체적으로 통일감을 줄 수 있는 작성 요령을 키워야겠다.
