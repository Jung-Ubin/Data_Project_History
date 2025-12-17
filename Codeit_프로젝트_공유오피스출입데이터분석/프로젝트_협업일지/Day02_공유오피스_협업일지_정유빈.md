# Day - 2 협업 일지(중급2)

#### 일자: 2025-09-05 / 정유빈

---

### 팀원들과 논의한 일

- 팀원들 각각 전처리를 진행
- 해당 전처리를 활용하여 각 머신러닝 학습 및 분석 진행
- f1-score 0.5 점 이상 목표로 잡고 그 이후 Feature Importace를 확인
- 중요도가 높은 Feature를 중점으로 EDA 진행

## \* 오늘 + 내가 한 일

- RF 모델로 머신러닝 진행
- 데이터 전처리 진행

---

## \* 사용했던 코딩

```python
# X, y 분리 (is_payment는 목표변수, user_uuid 같은 ID 계열은 제거)
X = df.drop(columns=["is_payment", "user_uuid"], errors="ignore")
y = df["is_payment"]

# 학습/테스트 분할
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Optuna 목적 함수 정의
def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
        "max_depth": trial.suggest_int("max_depth", 5, 50),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
        "max_features": trial.suggest_categorical("max_features", ["sqrt", "log2", None]),
        "class_weight": "balanced",
        "random_state": 42,
        "n_jobs": -1
    }

    model = RandomForestClassifier(**params)

    # 교차 검증 (f1-score 기준 최적화)
    score = cross_val_score(
        model, X_train, y_train,
        cv=5, scoring="f1", n_jobs=-1
    ).mean()

    return score

# Optuna 실행
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)  # n_trials=50 → 탐색 횟수

print("Best Trial Params:", study.best_trial.params)
print("Best CV f1 Score:", study.best_value)

# 최적 모델로 학습 후 테스트셋 평가
best_params = study.best_trial.params
best_model = RandomForestClassifier(**best_params)
best_model.fit(X_train, y_train)

y_pred = best_model.predict(X_test)
print(classification_report(y_test, y_pred, digits=4))
```

---

## \*문제점

- 아직 데이터 전처리가 완벽하지 않아 점수가 뚜렷하게 나오지 않는다.
- f1-score가 개선이 되고 있지만, 어떻게 데이터를 처리해야 목표했던 바까지 도달할 지 생각중이다.

## \* 회고

- 데이터를 어떻게 활용해야할지 구조를 잘 짜서 전처리해야겠다.
- 파라미터 튜닝을 진행하며 점수를 올려봤지만, 0.5까지 도달하지 못했다.
- 팀원들과의 활발한 소통을 통해 정보를 수집하여 빠르게 EDA로 들어가야겠다.
