import pandas as pd

# 파일 불러오기
df1 = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/사용할_데이터_정리/05-1_성동구_대중교통_좌표&정보.csv", encoding="utf-8-sig", dtype={'NODE_ID': str}) 
df2 = pd.read_csv("C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/05_성동구_지하철&버스&따릉이&버스노선수&이용객수_좌표.csv", encoding="utf-8-sig", dtype={'NODE_ID': str})  

# NODE_ID 기준으로 병합 (left join)
merged = pd.merge(df2, df1[['NODE_ID', '지번_주소', '도로명_주소']], on='NODE_ID', how='left')

# 주소 붙여넣은 결과를 저장
merged.to_csv("주소_병합_완료(검토필요).csv", index=False, encoding="utf-8-sig")
