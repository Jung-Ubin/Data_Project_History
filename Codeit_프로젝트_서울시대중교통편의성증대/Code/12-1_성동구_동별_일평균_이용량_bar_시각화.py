import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
df = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/통계적 분석/11-1_성동구_일일평균_버스,지하철,따릉이_이용률_합계.csv", encoding="utf-8-sig")


# 정렬
df = df.sort_values(by='동별일평균총승객수', ascending=False)

# 시각화
plt.figure(figsize=(14, 6))
ax = sns.barplot(data=df, x='동 이름', y='동별일평균총승객수', palette='viridis')

# 막대 위에 값 표시
for container in ax.containers:
    ax.bar_label(container, fmt='%.0f', padding=3)

# 제목 및 라벨
plt.title("성동구 동별 일평균 대중교통 이용객 수", fontsize=16)
plt.xlabel("동 이름", fontsize=12)
plt.ylabel("일평균 이용객 수", fontsize=12)
plt.xticks(rotation=45)
plt.ylim(0)  # Y축 0부터 시작

plt.tight_layout()
plt.show()
