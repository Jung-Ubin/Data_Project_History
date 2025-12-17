import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import platform

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
df = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/통계적 분석/13-1_성동구_교통이용률_비율_계산.csv", encoding="utf-8-sig")

# 정렬 (이용률 높은 순)
df_sorted = df.sort_values(by='이용률', ascending=False)

# 시각화
plt.figure(figsize=(10, 8))
plt.barh(df_sorted['동 이름'], df_sorted['이용률'], color='#a18cd1')
plt.gca().invert_yaxis()
plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter(1.0))  # 퍼센트 형식

plt.xlabel('교통 이용률 (일평균 교통 이용자 / 생활인구)')
plt.title('성동구 동별 교통 이용률')
plt.tight_layout()
plt.show()