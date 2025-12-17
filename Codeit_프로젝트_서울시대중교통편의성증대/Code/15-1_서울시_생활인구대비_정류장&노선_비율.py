import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 1. 한글 폰트 설정 (예: 맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. CSV 파일 읽기
df = pd.read_csv('C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/데이터 수집/01_서울_행정구별_총생활인구수평균대비_버스노선, 정류장수(전처리).csv', encoding='utf-8-sig')
# 3. 컬럼명 정리
df = df.rename(columns={
    '지역': 'area', 
    '정류장 평균 사용 인구': 'bus_stop',
    '노선 평균 사용 인구': 'route'
})

# 4. 각 그래프 정렬
df_stop_sorted = df.sort_values(by='bus_stop', ascending=False)
df_line_sorted = df.sort_values(by='route', ascending=False)

# 5. 바 색상 설정
def get_bar_colors(지역_시리즈):
    return [
        '#ED7D31' if x == '동작구' else
        '#5DADE2' if x == '성동구' else
        'gray'
        for x in 지역_시리즈
    ]

# 6. 시각화
fig, ax = plt.subplots(ncols=2, figsize=(12, 8))

# 왼쪽 그래프: 정류장
colors_left = get_bar_colors(df_stop_sorted['area'])
ax[0].barh(df_stop_sorted['area'], df_stop_sorted['bus_stop'], color=colors_left)
ax[0].set_xlabel('정류장 평균 사용 인구')
ax[0].invert_xaxis()      # 그래프 방향 바꾸기
ax[0].invert_yaxis()

# 왼쪽 그래프: y축에서 구 강조
highlight_gu = ['동작구', '성동구']
for i, label in enumerate(ax[0].get_yticklabels()):
    if label.get_text() in highlight_gu:
        label.set_backgroundcolor('#FFF2CC')


# 오른쪽 그래프: 노선
colors_right = get_bar_colors(df_line_sorted['area'])
ax[1].barh(df_line_sorted['area'], df_line_sorted['route'], color=colors_right)
ax[1].set_xlabel('노선 평균 사용 인구')
ax[1].invert_yaxis()
ax[1].yaxis.tick_right()

# 오른쪽 그래프: y축에서 구 강조
highlight_gu = ['동작구', '성동구']
for i, label in enumerate(ax[1].get_yticklabels()):
    if label.get_text() in highlight_gu:
        label.set_backgroundcolor('#FFF2CC')


# 전체 제목
fig.suptitle('자치구별 생활인구 대비 정류장 & 노선 이용 비율', fontsize=16)

plt.tight_layout()
plt.show()