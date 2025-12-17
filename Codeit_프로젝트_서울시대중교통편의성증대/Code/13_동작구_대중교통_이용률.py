import pandas as pd

# 파일 경로
path = r"C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/통계적 분석"
file_교통 = f"{path}/11_동작구_일일평균_버스,지하철,따릉이_이용률_합계.csv"
file_인구 = f"{path}/12_동작구_동별_생활인구수.csv"

# 파일 불러오기
df_교통 = pd.read_csv(file_교통, encoding='utf-8-sig')
df_인구 = pd.read_csv(file_인구, encoding='utf-8-sig')

# 필요한 컬럼만 선택
df_교통 = df_교통[['동 이름', '동별일평균총승객수']]
df_인구 = df_인구[['동 이름', '총_생활인구_수']]

# 병합
df_합쳐짐 = pd.merge(df_교통, df_인구, on='동 이름')

# 비율 계산
df_합쳐짐['이용률'] = df_합쳐짐['동별일평균총승객수'] / df_합쳐짐['총_생활인구_수']

# 저장
output_file = f"{path}/13_동작구_교통이용률_비율_계산.csv"
df_합쳐짐.to_csv(output_file, index=False, encoding='utf-8-sig')
