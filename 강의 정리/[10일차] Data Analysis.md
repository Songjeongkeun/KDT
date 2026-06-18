# [10일차] 데이터분석

## Pandas 기본

```python
# pandas 라이브러리를 pd라는 이름으로 불러오기
import pandas as pd

# pandas 버전 확인
print(pd.__version__)
```

출력 예시:

```text
2.2.3
```

## 1. Series 만들기

`pd.Series()`는 1차원 데이터를 만드는 함수이다. 값과 인덱스를 함께 저장할 수 있다.

기본 형식:

```python
pd.Series(data, index=None)
```

매개변수:
- `data`: Series에 들어갈 실제 데이터
- `index`: 각 데이터에 붙일 이름표

```python
import pandas as pd

# 인덱스로 사용할 이름 목록
idx = ['김사과', '반하나', '오렌지', '이메론', '배애리']

# 실제 점수 데이터
data = [67, 75, 90, 62, 98]

# 값과 인덱스를 사용해 Series 생성
ser1 = pd.Series(data, index=idx)

print(ser1)
print(ser1.index)
print(ser1.values)
print(type(ser1.values))
```

출력 예시:

```text
김사과    67
반하나    75
오렌지    90
이메론    62
배애리    98
dtype: int64

Index(['김사과', '반하나', '오렌지', '이메론', '배애리'], dtype='object')
[67 75 90 62 98]
<class 'numpy.ndarray'>
```

- `Series`는 1차원 데이터이다.
- 값과 인덱스가 함께 있다.
- `values`는 NumPy 배열 형태로 나온다.

## 2. DataFrame 만들기

`pd.DataFrame()`은 행과 열이 있는 2차원 표 데이터를 만드는 함수이다.

기본 형식:

```python
pd.DataFrame(data=None, index=None, columns=None)
```

매개변수:
- `data`: 표에 들어갈 실제 데이터
- `index`: 행 이름
- `columns`: 열 이름

```python
import pandas as pd

# 2차원 점수 데이터
data = [
    [67, 93, 91],
    [75, 68, 96],
    [87, 81, 82],
    [62, 70, 75],
    [98, 56, 87]
]

# 행 이름
idx = ['김사과', '반하나', '오렌지', '이메론', '배애리']

# 열 이름
col = ['국어', '영어', '수학']

# DataFrame 생성
df = pd.DataFrame(data=data, index=idx, columns=col)

print(df)
print(df.index)
print(df.columns)
print(df.values)
```

출력 예시:

```text
      국어  영어  수학
김사과   67  93  91
반하나   75  68  96
오렌지   87  81  82
이메론   62  70  75
배애리   98  56  87

Index(['김사과', '반하나', '오렌지', '이메론', '배애리'], dtype='object')
Index(['국어', '영어', '수학'], dtype='object')
[[67 93 91]
 [75 68 96]
 [87 81 82]
 [62 70 75]
 [98 56 87]]
```

## 3. 딕셔너리로 DataFrame 만들기

딕셔너리를 `pd.DataFrame()`에 넣으면 딕셔너리의 key가 컬럼명이 되고, value가 컬럼 데이터가 된다.

기본 형식:

```python
pd.DataFrame(data=딕셔너리, index=행이름)
```

매개변수:
- `data`: 컬럼명과 데이터를 가진 딕셔너리
- `index`: 행 이름

```python
import pandas as pd

idx = ['김사과', '반하나', '오렌지', '이메론', '배애리']

# 딕셔너리의 key가 컬럼명이 된다.
dic = {
    '국어': [67, 75, 76, 62, 98],
    '영어': [93, 68, 81, 70, 56],
    '수학': [91, 96, 82, 75, 87]
}

df = pd.DataFrame(data=dic, index=idx)

print(df)
```

출력 예시:

```text
      국어  영어  수학
김사과   67  93  91
반하나   75  68  96
오렌지   76  81  82
이메론   62  70  75
배애리   98  56  87
```

## 4. CSV 파일 읽기

`pd.read_csv()`는 CSV 파일을 읽어서 DataFrame으로 만드는 함수이다.

기본 형식:

```python
pd.read_csv(filepath_or_buffer, encoding=None)
```

매개변수:
- `filepath_or_buffer`: 읽어올 CSV 파일 경로
- `encoding`: 파일 문자 인코딩 방식

```python
import pandas as pd

# CSV 파일을 읽어서 DataFrame으로 만들기
df = pd.read_csv('./광고모델_브랜드평판.csv')

# 데이터 타입 확인
print(type(df))

# 데이터 기본 정보 확인
df.info()

# 컬럼명 확인
print(df.columns)
```

출력 예시:

```text
<class 'pandas.core.frame.DataFrame'>

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 20 entries, 0 to 19
Data columns (total 7 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   이름      20 non-null     object
 1   소속사     20 non-null     object
 2   성별      20 non-null     object
 ...

Index(['이름', '소속사', '성별', '생년월일', '키', '혈액형', '브랜드평판지수'], dtype='object')
```

- 실제 출력은 CSV 파일의 컬럼명과 데이터 개수에 따라 달라진다.

## 5. 컬럼명 변경

```python
# 새 컬럼명 목록
new_columns = ['name', 'company', 'gender', 'birthday', 'height', 'blood', 'brand']

# 기존 컬럼명을 새 컬럼명으로 변경
df.columns = new_columns

print(df.head())
```

출력 예시:

```text
  name company gender    birthday height blood      brand
0  김사과      애플     여자  2000-01-01  160cm     A  1,234,567
1  반하나     바나나     여자  1999-03-12  165cm     B  2,345,678
...
```

- 기존 컬럼 개수와 새 컬럼명 개수가 반드시 같아야 한다.

## 6. head(), tail()

`head()`는 위쪽 데이터를 확인하고, `tail()`은 아래쪽 데이터를 확인하는 메서드이다.

기본 형식:

```python
df.head(n=5)
df.tail(n=5)
```

매개변수:
- `n`: 출력할 행 개수

```python
# 위에서 5개 행 출력
print(df.head())

# 위에서 3개 행 출력
print(df.head(3))

# 아래에서 5개 행 출력
print(df.tail())

# 아래에서 2개 행 출력
print(df.tail(2))
```

출력 예시:

```text
head(3)
  name company gender    birthday height blood      brand
0  김사과      애플     여자  2000-01-01  160cm     A  1,234,567
1  반하나     바나나     여자  1999-03-12  165cm     B  2,345,678
2  오렌지     오렌지     남자  1998-07-20  180cm     O  3,456,789
```

## 7. describe()

`describe()`는 데이터의 통계 요약 정보를 확인하는 메서드이다.

기본 형식:

```python
df.describe(include=None)
```

매개변수:
- `include`: 요약할 데이터 타입 지정

```python
# 숫자형 컬럼의 통계 정보 확인
print(df.describe())

# 문자열 컬럼의 통계 정보 확인
print(df.describe(include=str))
```

출력 예시:

```text
          height         brand
count  20.000000  2.000000e+01
mean  174.250000  3.512300e+06
std     8.100000  1.250000e+06
min   160.000000  1.234567e+06
...
```

- `height`, `brand`가 문자열이면 숫자 통계가 제대로 나오지 않는다.

## 8. 문자열 숫자 변환

```python
# height 컬럼에서 cm 제거 후 float으로 변환
df['height'] = df['height'].str.replace('cm', '').astype(float)

# brand 컬럼에서 쉼표 제거 후 int로 변환
df['brand'] = df['brand'].str.replace(',', '').astype(int)

df.info()
print(df.head())
```

출력 예시:

```text
 #   Column    Dtype  
---  ------    -----  
 0   name      object 
 1   company   object 
 2   gender    object 
 3   birthday  object 
 4   height    float64
 5   blood     object 
 6   brand     int64  
```

- 숫자처럼 보여도 문자열이면 계산과 정렬이 이상해질 수 있다.
- `astype()`으로 실제 숫자 타입으로 바꿔야 한다.

## 9. 정렬하기

`sort_index()`는 인덱스를 기준으로 정렬하고, `sort_values()`는 특정 컬럼 값을 기준으로 정렬하는 메서드이다.

기본 형식:

```python
df.sort_index(ascending=True)
df.sort_values(by, ascending=True)
```

매개변수:
- `by`: 정렬 기준 컬럼명
- `ascending`: 오름차순 여부

```python
# 인덱스 기준 오름차순 정렬
print(df.sort_index())

# 인덱스 기준 내림차순 정렬
print(df.sort_index(ascending=False))

# 키 기준 오름차순 정렬
print(df.sort_values(by='height').head())

# 키 기준 내림차순 정렬
print(df.sort_values(by='height', ascending=False).head())
```

출력 예시:

```text
height 오름차순
   name  height
0   김사과   160.0
5   이메론   162.0
1   반하나   165.0
...

height 내림차순
    name  height
10  배애리   185.0
2   오렌지   180.0
...
```

## 10. 여러 기준 정렬

`sort_values()`는 여러 컬럼을 기준으로 정렬할 수도 있다.

기본 형식:

```python
df.sort_values(by=[컬럼1, 컬럼2], ascending=[True, False], na_position='last')
```

매개변수:
- `by`: 정렬 기준 컬럼 목록
- `ascending`: 각 컬럼의 오름차순 여부
- `na_position`: 결측값을 앞에 둘지 뒤에 둘지 지정

```python
# 1차 기준: height 내림차순
# 2차 기준: brand 내림차순
result = df.sort_values(
    by=['height', 'brand'],
    ascending=[False, False],
    na_position='first'
)

print(result.head())
```

출력 예시:

```text
    name  height    brand
10  배애리   185.0  8000000
2   오렌지   180.0  5000000
7   이메론   180.0  3000000
...
```

## 11. 컬럼 선택

```python
# blood 컬럼 선택
print(df['blood'])

# 컬럼명이 간단한 영문이면 점 표기법도 가능
print(df.blood)
```

출력 예시:

```text
0     A
1     B
2     O
3    AB
Name: blood, dtype: object
```

- `df.blood`보다 `df['blood']`가 더 안전하다.
- 컬럼명에 공백, 한글, 특수문자가 있으면 점 표기법이 안 된다.

## 12. loc 인덱싱

`loc[]`는 행 이름과 컬럼명을 기준으로 데이터를 선택하는 인덱서이다.

기본 형식:

```python
df.loc[행조건, 열조건]
```

매개변수처럼 들어가는 값:
- `행조건`: 선택할 행 이름, 범위, 조건
- `열조건`: 선택할 컬럼명

```python
# 모든 행의 name 컬럼 선택
print(df.loc[:, 'name'])

# 2번부터 5번 인덱스까지 name 컬럼 선택
print(df.loc[2:5, 'name'])

# 2번부터 5번까지 name, gender, height 컬럼 선택
print(df.loc[2:5, ['name', 'gender', 'height']])

# 2번과 5번 행만 선택
print(df.loc[[2, 5], ['name', 'gender', 'height']])
```

출력 예시:

```text
   name gender  height
2   오렌지     남자   180.0
3   이메론     남자   172.0
4   배애리     여자   168.0
5   김사과     여자   160.0
```

- `loc`는 이름, 라벨 기준이다.
- `loc[2:5]`는 5를 포함한다.

## 13. iloc 인덱싱

`iloc[]`는 숫자 위치를 기준으로 데이터를 선택하는 인덱서이다.

기본 형식:

```python
df.iloc[행위치, 열위치]
```

매개변수처럼 들어가는 값:
- `행위치`: 선택할 행의 숫자 위치
- `열위치`: 선택할 열의 숫자 위치

```python
# 모든 행의 0번째 컬럼 선택
print(df.iloc[:, 0])

# 모든 행의 0, 1, 2번째 컬럼 선택
print(df.iloc[:, 0:3])

# 모든 행의 0번째, 3번째 컬럼 선택
print(df.iloc[:, [0, 3]])

# 1~4번째 행, 0~1번째 컬럼 선택
print(df.iloc[1:5, 0:2])
```

출력 예시:

```text
  name company
1  반하나     바나나
2  오렌지     오렌지
3  이메론      멜론
4  배애리       배
```

- `iloc`는 숫자 위치 기준이다.
- `iloc[1:5]`는 5를 포함하지 않는다.

## 14. 조건 필터링

```python
# height가 180 이상인지 True/False로 확인
print(df['height'] >= 180)

# height가 180 이상인 행만 선택
print(df[df['height'] >= 180])

# height가 180 이상인 사람의 name만 선택
print(df[df['height'] >= 180]['name'])

# 조건에 맞는 행에서 원하는 컬럼만 선택
print(df.loc[df['height'] >= 180, ['name', 'gender', 'height']])
```

출력 예시:

```text
   name gender  height
2   오렌지     남자   180.0
10  배애리     여자   185.0
```

## 15. isin()

`isin()`은 컬럼 값이 특정 목록 안에 포함되어 있는지 검사하는 메서드이다.

기본 형식:

```python
df['컬럼명'].isin(values)
```

매개변수:
- `values`: 비교할 값 목록

```python
# 찾고 싶은 혈액형 목록
blood = ['A', 'B']

# blood 컬럼 값이 A 또는 B인지 확인
print(df['blood'].isin(blood))

# 혈액형이 A 또는 B인 행만 선택
print(df[df['blood'].isin(blood)])
```

출력 예시:

```text
   name blood
0   김사과     A
1   반하나     B
5   이메론     A
...
```

## 16. 결측값 확인

```python
# 결측값이면 True
print(df.isna())

# 결측값이면 True
print(df.isnull())

# 결측값이 아니면 True
print(df.notna())

# height 컬럼의 결측값 확인
print(df['height'].isna())
```

출력 예시:

```text
0     False
1     False
2     False
8      True
19     True
Name: height, dtype: bool
```

## 17. 결측값 넣기

```python
import numpy as np

# 8번, 19번 행의 height 값을 NaN으로 변경
df.loc[[8, 19], 'height'] = np.nan

# height가 결측값인 행만 출력
print(df[df['height'].isna()])
```

출력 예시:

```text
    name company gender    birthday  height blood    brand
8   홍길동      ...     남자  1997-01-01     NaN     A  1234567
19  김철수      ...     남자  1995-05-05     NaN     O  2345678
```

## 18. 결측값이 아닌 데이터 선택

```python
# height가 비어 있지 않은 행만 선택
print(df[df['height'].notnull()])

# 위 코드와 같은 의미
print(df[~df['height'].isnull()])

# height가 있는 사람의 일부 컬럼만 선택
print(df.loc[df['height'].notnull(), ['name', 'company', 'gender']])
```

출력 예시:

```text
   name company gender
0   김사과      애플     여자
1   반하나     바나나     여자
...
```

## 19. fillna()

`fillna()`는 결측값을 특정 값으로 채우는 메서드이다.

기본 형식:

```python
df['컬럼명'].fillna(value)
```

매개변수:
- `value`: 결측값 대신 넣을 값

```python
# 원본 보호를 위해 복사본 생성
df_copy = df.copy()

# height 결측값을 0으로 채운 결과
print(df_copy['height'].fillna(0))

# 실제 컬럼에 반영하려면 다시 저장해야 함
df_copy['height'] = df_copy['height'].fillna(0)

print(df_copy['height'])
```

출력 예시:

```text
0     160.0
1     165.0
8       0.0
19      0.0
Name: height, dtype: float64
```

## 20. 평균과 중앙값으로 결측값 채우기

```python
df_copy = df.copy()

# height 평균 계산
height_mean = df_copy['height'].mean()

# 결측값을 평균으로 채우기
df_copy['height'] = df_copy['height'].fillna(height_mean)

print(height_mean)
print(df_copy['height'])
```

출력 예시:

```text
174.25
0     160.00
1     165.00
8     174.25
19    174.25
Name: height, dtype: float64
df_copy = df.copy()

# height 중앙값 계산
height_median = df_copy['height'].median()

# 결측값을 중앙값으로 채우기
df_copy['height'] = df_copy['height'].fillna(height_median)

print(height_median)
```

출력 예시:

```text
173.5
```

## 21. dropna()

`dropna()`는 결측값이 있는 행이나 열을 제거하는 메서드이다.

기본 형식:

```python
df.dropna(axis=0)
```

매개변수:
- `axis=0`: 결측값이 있는 행 제거
- `axis=1`: 결측값이 있는 열 제거

```python
df_copy = df.copy()

# 결측값이 하나라도 있는 행 제거
print(df_copy.dropna())

# 결측값이 하나라도 있는 열 제거
print(df_copy.dropna(axis=1))
```

출력 예시:

```text
dropna()
결측값이 있는 8번, 19번 행이 제거된 DataFrame

dropna(axis=1)
height 컬럼에 결측값이 있으면 height 열 전체가 제거됨
```

## 22. 행 추가

```python
df_copy = df.copy()

# 추가할 한 사람의 데이터
dic = {
    'name': '김사과',
    'company': '애플',
    'gender': '여자',
    'birthday': '2000-01-01',
    'height': 160.0,
    'blood': 'A',
    'brand': 1234567
}

# 마지막 행 다음 위치에 새 행 추가
df_copy.loc[len(df_copy)] = dic

print(df_copy.tail())
```

출력 예시:

```text
    name company gender    birthday  height blood    brand
20  김사과      애플     여자  2000-01-01   160.0     A  1234567
```

## 23. 열 추가와 값 변경

```python
df_copy = df.copy()

# 모든 행에 nation 컬럼 추가
df_copy['nation'] = '대한민국'

# name이 김사과인 행의 nation만 미국으로 변경
df_copy.loc[df_copy['name'] == '김사과', 'nation'] = '미국'

print(df_copy.tail())
```

출력 예시:

```text
    name company gender  height nation
18   ...     ...     ...   175.0  대한민국
19   ...     ...     ...     NaN  대한민국
20  김사과      애플     여자   160.0     미국
```

## 24. 행과 열 삭제

`drop()`은 특정 행이나 열을 삭제하는 메서드이다.

기본 형식:

```python
df.drop(labels, axis=0)
```

매개변수:
- `labels`: 삭제할 행 인덱스 또는 컬럼명
- `axis=0`: 행 삭제
- `axis=1`: 열 삭제

```python
# 20번 행 삭제
print(df_copy.drop(20, axis=0))

# 여러 행 삭제
print(df_copy.drop([1, 3, 5, 7, 20], axis=0))

# nation 컬럼 삭제
print(df_copy.drop('nation', axis=1))

# 여러 컬럼 삭제
print(df_copy.drop(['nation', 'company'], axis=1))
```

출력 예시:

```text
drop(20, axis=0)
20번 행이 빠진 DataFrame

drop('nation', axis=1)
nation 컬럼이 빠진 DataFrame
```

- `drop()`은 기본적으로 원본을 바꾸지 않는다.
- 결과를 유지하려면 다시 저장해야 한다.

```python
df_copy = df_copy.drop('nation', axis=1)
```

## 25. 통계 함수

```python
print(df_copy['height'].sum())     # 합계
print(df_copy['height'].count())   # 개수, NaN 제외
print(df_copy['height'].mean())    # 평균
print(df_copy['height'].median())  # 중앙값
print(df_copy['height'].max())     # 최대값
print(df_copy['height'].min())     # 최소값
print(df_copy['height'].var())     # 분산
print(df_copy['height'].std())     # 표준편차
```

출력 예시:

```text
3485.0
20
174.25
173.5
185.0
160.0
65.23
8.07
```

## 26. groupby()

`groupby()`는 특정 컬럼 값을 기준으로 데이터를 그룹으로 묶는 메서드이다.

기본 형식:

```python
df.groupby(by)
```

매개변수:
- `by`: 그룹으로 묶을 기준 컬럼명

```python
# 혈액형별 데이터 개수
print(df_copy.groupby('blood').count())

# 혈액형별 숫자 컬럼 평균
print(df_copy.groupby('blood').mean(numeric_only=True))

# 혈액형별 숫자 컬럼 합계
print(df_copy.groupby('blood').sum(numeric_only=True))
```

출력 예시:

```text
       height      brand
blood                   
A       170.2  3000000.0
B       175.5  4200000.0
O       178.0  3900000.0
AB      169.0  2500000.0
```

## 27. 여러 기준 groupby()

```python
# 혈액형과 성별별 평균
print(df_copy.groupby(['blood', 'gender']).mean(numeric_only=True))

# 혈액형과 성별별 height 평균만 출력
print(df_copy.groupby(['blood', 'gender'])['height'].mean())
```

출력 예시:

```text
blood  gender
A      남자        178.0
       여자        165.5
B      남자        180.0
       여자        168.0
Name: height, dtype: float64
```

## 28. drop_duplicates(), value_counts()

`drop_duplicates()`는 중복 값을 제거하고, `value_counts()`는 값별 개수를 세는 메서드이다.

기본 형식:

```python
df['컬럼명'].drop_duplicates()
df['컬럼명'].value_counts(dropna=True)
```

매개변수:
- `dropna`: 결측값을 개수에 포함할지 여부

```python
# blood 컬럼의 중복 제거
print(df_copy['blood'].drop_duplicates())

# blood 값별 개수
print(df_copy['blood'].value_counts())
```

출력 예시:

```text
A     6
B     5
O     5
AB    4
Name: blood, dtype: int64
```

## 29. concat()

`pd.concat()`은 여러 DataFrame을 위아래 또는 좌우로 이어 붙이는 함수이다.

기본 형식:

```python
pd.concat(objs, axis=0)
```

매개변수:
- `objs`: 이어 붙일 DataFrame 목록
- `axis=0`: 아래 방향으로 붙이기
- `axis=1`: 오른쪽 방향으로 붙이기

```python
# df1과 df1_copy를 아래로 이어 붙이기
df1_concat = pd.concat([df1, df1_copy])

# 인덱스를 0부터 다시 설정
df1_concat = df1_concat.reset_index(drop=True)

print(df1_concat.head())
print(df1_concat.tail())
```

출력 예시:

```text
원래 20행짜리 df 두 개를 붙이면 40행이 됨
인덱스는 0부터 39까지 다시 설정됨
# df1_copy와 df2_copy를 옆으로 붙이기
print(pd.concat([df1_copy, df2_copy], axis=1))
```

출력 예시:

```text
df1_copy의 컬럼들 + df2_copy의 컬럼들이 옆으로 붙음
인덱스가 맞지 않는 행은 NaN 발생 가능
```

## 30. merge()

`pd.merge()`는 공통 컬럼을 기준으로 DataFrame을 병합하는 함수이다.

기본 형식:

```python
pd.merge(left, right, on=None, how='inner')
```

매개변수:
- `left`: 왼쪽 DataFrame
- `right`: 오른쪽 DataFrame
- `on`: 병합 기준 컬럼명
- `how`: 병합 방식

```python
# 이름 컬럼을 기준으로 왼쪽 DataFrame 기준 병합
print(pd.merge(df1_copy, df2_copy, on='이름', how='left'))

# 이름 컬럼을 기준으로 오른쪽 DataFrame 기준 병합
print(pd.merge(df1_copy, df2_copy, on='이름', how='right'))

# 양쪽에 공통으로 있는 이름만 병합
print(pd.merge(df1_copy, df2_copy, on='이름', how='inner'))
```

출력 예시:

```text
left  : df1_copy의 이름은 모두 유지, df2_copy에 없으면 NaN
right : df2_copy의 이름은 모두 유지, df1_copy에 없으면 NaN
inner : 양쪽에 모두 있는 이름만 남음
```

컬럼명이 다를 때:

```python
# 왼쪽은 이름, 오른쪽은 성함 컬럼을 기준으로 병합
print(pd.merge(df1_copy, df2_copy, left_on='이름', right_on='성함', how='inner'))
```

출력 예시:

```text
이름과 성함 값이 같은 행끼리 병합된 DataFrame
```

## 31. 날짜 타입 변환

`pd.to_datetime()`은 문자열을 날짜 타입으로 변환하는 함수이다.

기본 형식:

```python
pd.to_datetime(arg)
```

매개변수:
- `arg`: 날짜로 변환할 값 또는 컬럼

```python
# 문자열 생년월일을 datetime 타입으로 변환
df1_copy['생년월일'] = pd.to_datetime(df1_copy['생년월일'])

print(df1_copy['생년월일'].dtypes)
print(df1_copy['생년월일'].dt.year)
print(df1_copy['생년월일'].dt.month)
print(df1_copy['생년월일'].dt.day)
print(df1_copy['생년월일'].dt.dayofweek)
```

출력 예시:

```text
datetime64[ns]

0    2000
1    1999
2    1998
Name: 생년월일, dtype: int32

0    1
1    3
2    7
Name: 생년월일, dtype: int32
```

요일:

```text
0 = 월요일
1 = 화요일
2 = 수요일
3 = 목요일
4 = 금요일
5 = 토요일
6 = 일요일
```

## 32. select_dtypes()

`select_dtypes()`는 특정 데이터 타입의 컬럼만 선택하는 메서드이다.

기본 형식:

```python
df.select_dtypes(include=None, exclude=None)
```

매개변수:
- `include`: 포함할 데이터 타입
- `exclude`: 제외할 데이터 타입

```python
# 문자열 컬럼만 선택
print(df1_copy.select_dtypes(include='str'))

# 문자열 컬럼을 제외하고 선택
print(df1_copy.select_dtypes(exclude='str'))

# 문자열 컬럼 이름만 저장
str_cols = df1_copy.select_dtypes(include='str').columns

print(str_cols)
print(df1_copy[str_cols])
```

출력 예시:

```text
Index(['이름', '소속사', '성별', '혈액형'], dtype='object')
```

## 33. apply()

`apply()`는 Series 또는 DataFrame의 각 값에 함수를 적용하는 메서드이다.

기본 형식:

```python
df['컬럼명'].apply(func)
```

매개변수:
- `func`: 각 값에 적용할 함수

```python
# 성별 문자열을 숫자로 바꾸는 함수
def male_or_female(x):
    if x == '남':
        return 1
    elif x == '여':
        return 0
    else:
        return None

# 성별 컬럼의 각 값에 함수 적용
print(df1_copy['성별'].apply(male_or_female))

# 람다 함수로 같은 작업 수행
df1_copy['성별2'] = df1_copy['성별'].apply(lambda x: 1 if x == '남' else 0)

print(df1_copy.head())
```

출력 예시:

```text
0    1
1    0
2    1
3    0
Name: 성별, dtype: int64

   이름 성별  성별2
0  김사과  남    1
1  반하나  여    0
```

## 34. map()

`map()`은 Series의 값을 다른 값으로 치환하는 메서드이다.

기본 형식:

```python
df['컬럼명'].map(arg)
```

매개변수:
- `arg`: 변환 규칙을 가진 딕셔너리 또는 함수

```python
# 바꿀 규칙을 딕셔너리로 작성
map_gender = {'남': 1, '여': 0}

# 성별 값을 딕셔너리 규칙에 따라 변환
df1_copy['성별3'] = df1_copy['성별'].map(map_gender)

print(df1_copy[['성별', '성별3']].head())
```

출력 예시:

```text
  성별  성별3
0  남     1
1  여     0
2  남     1
3  여     0
```

차이:
- `apply()`는 함수를 적용할 때 좋다.
- `map()`은 값 치환 규칙이 명확할 때 좋다.

## 35. DataFrame 산술 연산

```python
df1 = pd.DataFrame({
    '파이썬': [60, 70, 80, 90, 95],
    '데이터분석': [40, 60, 70, 55, 87],
    '머신러닝딥러닝': [35, 40, 30, 70, 55]
})

# 세 과목 점수를 더해 총점 컬럼 생성
df1['총점'] = df1['파이썬'] + df1['데이터분석'] + df1['머신러닝딥러닝']

# 총점을 3으로 나누어 평균 컬럼 생성
df1['평균'] = df1['총점'] / 3

print(df1)
```

출력 예시:

```text
   파이썬  데이터분석  머신러닝딥러닝   총점         평균
0   60     40       35  135  45.000000
1   70     60       40  170  56.666667
2   80     70       30  180  60.000000
3   90     55       70  215  71.666667
4   95     87       55  237  79.000000
# 컬럼별 합계
print(df1.sum())

# 컬럼별 평균
print(df1.mean())
```

출력 예시:

```text
파이썬          395.0
데이터분석       312.0
머신러닝딥러닝    230.0
총점           937.0
평균           312.333333
dtype: float64
```

## 36. DataFrame 연산 시 주의점

```python
df1 = pd.DataFrame({
    '데이터분석': [40, 60, 70, 55, 87],
    '머신러닝딥러닝': [35, 40, 30, 70, 55]
})

df2 = pd.DataFrame({
    '데이터분석': [40, 60, 70, 55],
    '머신러닝딥러닝': [35, 40, 30, 70]
})

# 행 개수가 다르면 맞지 않는 위치는 NaN이 된다.
print(df1 + df2)
```

출력 예시:

```text
   데이터분석  머신러닝딥러닝
0   80.0      70.0
1  120.0      80.0
2  140.0      60.0
3  110.0     140.0
4    NaN       NaN
```

## 37. get_dummies()

`pd.get_dummies()`는 범주형 데이터를 원-핫 인코딩하는 함수이다.

기본 형식:

```python
pd.get_dummies(data)
```

매개변수:
- `data`: 원-핫 인코딩할 Series 또는 DataFrame

```python
# blood 컬럼을 원-핫 인코딩
dummy_blood = pd.get_dummies(df['blood'])

print(dummy_blood.head())
```

출력 예시:

```text
      A      AB      B      O
0  True   False  False  False
1  False  False   True  False
2  False  False  False   True
3  False   True  False  False
```

숫자 0과 1로 보고 싶다면:

```python
dummy_blood = pd.get_dummies(df['blood']).astype(int)
print(dummy_blood.head())
```

출력 예시:

```text
   A  AB  B  O
0  1   0  0  0
1  0   0  1  0
2  0   0  0  1
3  0   1  0  0
```

- 문자열이라고 무조건 원-핫 인코딩하지 않는다.
- 생년월일은 문자열처럼 보여도 날짜 타입으로 바꾸는 것이 자연스럽다.
- 학년, 등급, 지역 코드처럼 숫자로 보여도 실제 의미는 범주형일 수 있다.

## 38. 자주 쓰는 전체 흐름 예시

```python
import pandas as pd
import numpy as np

# CSV 파일 읽기
df = pd.read_csv('./광고모델_브랜드평판.csv')

# 컬럼명 변경
df.columns = ['name', 'company', 'gender', 'birthday', 'height', 'blood', 'brand']

# 문자열 숫자 변환
df['height'] = df['height'].str.replace('cm', '').astype(float)
df['brand'] = df['brand'].str.replace(',', '').astype(int)

# 결측값 확인
print(df.isna().sum())

# height 결측값을 중앙값으로 채우기
df['height'] = df['height'].fillna(df['height'].median())

# 키가 180 이상인 데이터만 선택
tall_people = df.loc[df['height'] >= 180, ['name', 'gender', 'height']]
print(tall_people)

# 혈액형별 평균 키
height_by_blood = df.groupby('blood')['height'].mean()
print(height_by_blood)

# 성별 숫자 변환
df['gender_code'] = df['gender'].map({'남': 1, '여': 0})

# 혈액형 원-핫 인코딩
blood_dummies = pd.get_dummies(df['blood']).astype(int)
print(blood_dummies.head())
```

출력 예시:

```text
name        0
company     0
gender      0
birthday    0
height      2
blood       0
brand       0
dtype: int64

   name gender  height
2   오렌지     남자   180.0
10  배애리     여자   185.0

blood
A     171.2
AB    169.0
B     175.5
O     178.0
Name: height, dtype: float64
```

