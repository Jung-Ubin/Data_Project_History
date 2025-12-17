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
df = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/통계적 분석/13_동작구_교통이용률_비율_계산.csv", encoding="utf-8-sig")

# 정렬 (이용률 높은 순)
df_sorted = df.sort_values(by='이용률', ascending=False)

plt.figure(figsize=(12, 6))
plt.bar(df_sorted['동 이름'], df_sorted['이용률'], color='skyblue')

# X축 글자가 겹치지 않도록 회전
plt.xticks(rotation=45)

# Y축을 퍼센트 형식으로 표시
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

plt.ylabel('교통 이용률 (일평균 교통 이용자 / 생활인구)')
plt.title('동작구구 동별 교통 이용률')
plt.tight_layout()
plt.show()