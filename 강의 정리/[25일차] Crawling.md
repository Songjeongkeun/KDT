# Python 웹크롤링 기초 정리

웹크롤링(Crawling)은 웹사이트의 HTML 문서나 API 데이터를 자동으로 수집해 원하는 정보를 추출하는 기술이다.

사람이 직접 웹페이지를 열어 뉴스, 상품 정보, 이미지, 댓글, 주가, 날씨 등을 확인하는 과정을 프로그램이 대신 수행한다고 생각하면 이해하기 쉽다.

이번 글에서는 로컬 HTML 예제를 대상으로 크롤링의 기본 흐름을 익히고, 실제 웹사이트에서 데이터를 수집해 `DataFrame`과 CSV 파일로 저장하는 방법까지 정리한다.

---

## 1. 웹크롤링 전체 흐름

크롤링은 보통 다음 순서로 진행한다.

```text
웹페이지 요청
    ↓
HTML 응답 받기
    ↓
HTML 파싱
    ↓
원하는 태그 선택
    ↓
텍스트, 링크, 이미지 등 데이터 추출
    ↓
DataFrame 또는 파일로 저장
```

Python 코드로 표현하면 다음과 같다.

```python
import requests
from bs4 import BeautifulSoup

url = "http://127.0.0.1:5500/1.html"

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

title = soup.find("h1").text
print(title)
```

---

## 2. 크롤링에 사용하는 주요 라이브러리

### 2.1 Requests

`requests`는 Python에서 웹 서버에 HTTP 요청을 보내고 응답을 받아오기 위해 사용하는 대표적인 라이브러리다.

웹 브라우저가 사이트에 접속할 때처럼 Python 코드에서도 웹페이지, 이미지, JSON 데이터 등을 서버로부터 가져올 수 있게 해준다.

```python
import requests

response = requests.get("https://example.com")
```

### 자주 사용하는 기능

| 코드 | 설명 |
| --- | --- |
| `requests.get(url)` | URL에 GET 요청을 보낸다 |
| `requests.post(url, data=data)` | URL에 POST 요청을 보낸다 |
| `response.status_code` | 응답 상태 코드를 확인한다 |
| `response.text` | 응답 HTML을 문자열로 가져온다 |
| `response.content` | 이미지, 파일 같은 바이너리 데이터를 가져온다 |
| `response.raise_for_status()` | 요청 실패 시 예외를 발생시킨다 |

### HTTP 상태 코드

| 상태 코드 | 의미 |
| --- | --- |
| `200번대` | 정상 응답 |
| `300번대` | 리다이렉션 |
| `400번대` | 사용자의 요청 오류 |
| `500번대` | 서버 오류 |

---

## 3. BeautifulSoup

`BeautifulSoup`은 HTML이나 XML 문서를 분석하고 원하는 데이터를 쉽게 추출하기 위해 사용하는 라이브러리다.

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
```

`html.parser`는 Python 기본 HTML 파서다.

BeautifulSoup을 사용하면 태그 이름, id, class, CSS 선택자 등을 기준으로 원하는 요소를 찾을 수 있다.

---

## 4. 기본 HTML 문서 크롤링

### 예제 HTML

```html
<!doctype html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>내 웹페이지</title>
</head>

<body>
    <h1>안녕하세요</h1>
    <p>파이썬 크롤링 수업입니다.</p>
</body>

</html>
```

### Python 코드

```python
import requests
from bs4 import BeautifulSoup

url = "http://127.0.0.1:5500/1.html"

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

h1 = soup.find("h1").text
p = soup.find("p").text

print("제목:", h1)
print("내용:", p)
```

### 출력 결과

```text
제목: 안녕하세요
내용: 파이썬 크롤링 수업입니다.
```

---

## 5. `find()`로 태그 찾기

`find()`는 HTML 문서에서 조건에 맞는 첫 번째 태그를 찾는다.

```python
soup.find("h1")
```

태그 안의 글자만 가져오려면 `.text`를 사용한다.

```python
soup.find("h1").text
```

### 정리

| 코드 | 의미 |
| --- | --- |
| `soup.find("h1")` | 첫 번째 `<h1>` 태그 찾기 |
| `soup.find("p")` | 첫 번째 `<p>` 태그 찾기 |
| `태그.text` | 태그 내부의 텍스트 추출 |

---

## 6. 부모 태그 안에서 자식 태그 찾기

뉴스처럼 하나의 영역 안에 제목과 내용이 들어있는 경우가 많다.

### 예제 HTML

```html
<div>
    <h1>뉴스 제목</h1>
    <p>뉴스 내용</p>
</div>
```

### Python 코드

```python
url = "http://127.0.0.1:5500/2.html"

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

div = soup.find("div")

news_title = div.find("h1").text
news_content = div.find("p").text

print("뉴스 제목:", news_title)
print("뉴스 내용:", news_content)
```

### 출력 결과

```text
뉴스 제목: 뉴스 제목
뉴스 내용: 뉴스 내용
```

먼저 부모 태그인 `div`를 찾고, 그 안에서 다시 `h1`, `p`를 찾는다.

---

## 7. 여러 태그 가져오기: `find_all()`

`find_all()`은 조건에 맞는 모든 태그를 리스트처럼 가져온다.

### 예제 HTML

```html
<a href="https://naver.com">네이버</a>
<a href="https://google.com">구글</a>
```

### Python 코드

```python
url = "http://127.0.0.1:5500/3.html"

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

links = soup.find_all("a")

for link in links:
    text = link.text
    href = link["href"]

    print("사이트 이름:", text)
    print("링크 주소:", href)
    print()
```

### 출력 결과

```text
사이트 이름: 네이버
링크 주소: https://naver.com

사이트 이름: 구글
링크 주소: https://google.com
```

`link["href"]`는 `<a>` 태그의 `href` 속성 값을 가져온다.

---

## 8. 이미지 다운로드

이미지 태그의 `src` 속성을 가져오면 이미지 파일 주소를 알 수 있다.

### 예제 HTML

```html
<img src="류지.jpeg" />
```

### 필요한 모듈

```python
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
```

`urljoin()`은 상대 경로를 절대 URL로 바꿀 때 사용한다.

```python
url = "http://127.0.0.1:5500/4.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

img_tag = soup.find("img")
img_src = img_tag["src"]

img_url = urljoin(url, img_src)
print(img_url)
```

### 출력 예시

```text
http://127.0.0.1:5500/류지.jpeg
```

### images 폴더 생성

```python
os.makedirs("images", exist_ok=True)
```

`exist_ok=True`는 폴더가 이미 있어도 오류가 발생하지 않게 한다.

### 이미지 저장

```python
img_response = requests.get(img_url)

file_name = img_url.split("/")[-1]
save_path = os.path.join("images", file_name)

with open(save_path, "wb") as file:
    file.write(img_response.content)
```

이미지는 텍스트가 아니라 바이너리 데이터이므로 `"wb"` 모드로 저장한다.

---

## 9. `open()` 함수

`open()` 함수는 파일을 읽거나 저장할 때 사용하는 함수다.

텍스트 파일, CSV 파일, 이미지 파일 등을 열어서 데이터를 읽거나 저장할 수 있다.

```python
파일객체 = open("파일명", "모드", encoding="utf-8")
```

### 자주 사용하는 모드

| 모드 | 의미 |
| --- | --- |
| `"r"` | 읽기 |
| `"w"` | 쓰기 |
| `"a"` | 이어쓰기 |
| `"rb"` | 바이너리 읽기 |
| `"wb"` | 바이너리 쓰기 |

파일을 열고 닫는 과정을 안전하게 처리하려면 `with`문을 사용하는 것이 좋다.

```python
with open("sample.txt", "w", encoding="utf-8") as file:
    file.write("안녕하세요")
```

---

## 10. 표 데이터 추출

HTML 표는 `table`, `tr`, `th`, `td` 태그로 구성된다.

### 예제 HTML

```html
<table border="1">
    <tr>
        <th>이름</th>
        <th>나이</th>
    </tr>
    <tr>
        <td>김사과</td>
        <td>20</td>
    </tr>
</table>
```

### Python 코드

```python
url = "http://127.0.0.1:5500/5.html"

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

table = soup.find("table")

headers = table.find_all("th")
datas = table.find_all("td")

print("제목")
for header in headers:
    print(header.text, end=" ")

print()
print("내용")
for data in datas:
    print(data.text, end=" ")
```

### 출력 결과

```text
제목
이름 나이
내용
김사과 20
```

---

## 11. CSS 선택자로 데이터 추출

BeautifulSoup은 CSS 선택자도 사용할 수 있다.

### 예제 HTML

```html
<div id="title">IT</div>

<div class="item">
    <h2>노트북</h2>
    <p>150만원</p>
</div>

<div class="item">
    <h2>키보드</h2>
    <p>10만원</p>
</div>
```

### Python 코드

```python
url = "http://127.0.0.1:5500/6.html"

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

title = soup.select_one("#title").text
print("카테고리:", title)

items = soup.select(".item")

for item in items:
    name = item.select_one("h2").text
    price = item.select_one("p").text

    print("상품명:", name)
    print("가격:", price)
    print()
```

### 출력 결과

```text
카테고리: IT
상품명: 노트북
가격: 150만원

상품명: 키보드
가격: 10만원
```

### `select_one()`과 `select()`

| 코드 | 의미 |
| --- | --- |
| `soup.select_one("#title")` | id가 `title`인 첫 번째 요소 |
| `soup.select(".item")` | class가 `item`인 모든 요소 |
| `item.select_one("h2")` | item 내부의 첫 번째 `h2` |

---

## 12. `find()`와 `select()` 비교

| 구분 | `find()` / `find_all()` | `select_one()` / `select()` |
| --- | --- | --- |
| 기준 | 태그 이름, 속성 조건 | CSS 선택자 |
| 첫 번째 요소 | `find()` | `select_one()` |
| 여러 요소 | `find_all()` | `select()` |
| id 선택 | `find(id="title")` | `select_one("#title")` |
| class 선택 | `find_all(class_="item")` | `select(".item")` |

CSS 선택자에 익숙하다면 `select()` 방식이 편할 수 있다.

---

## 13. JavaScript로 생성되는 동적 페이지

다음 HTML은 JavaScript가 실행된 뒤 과일 목록이 화면에 추가된다.

```html
<h1>오늘의 과일 목록</h1>
<div id="fruit-list"></div>

<script>
    const fruits = ["사과", "바나나", "오렌지", "딸기"];
    const div = document.getElementById("fruit-list");

    fruits.forEach((fruit) => {
        div.innerHTML += `<p class="fruit">${fruit}</p>`;
    });
</script>
```

브라우저에서는 과일 목록이 보인다.

하지만 `requests`는 서버가 처음 보낸 HTML만 가져온다. JavaScript를 실행한 결과까지 자동으로 반영하지 않는다.

즉, `requests`와 `BeautifulSoup`만으로는 JavaScript가 동적으로 만든 요소를 가져오지 못할 수 있다.

이런 경우에는 다음 방법을 고려한다.

- 실제 데이터가 들어있는 API 요청을 찾는다.
- Selenium, Playwright 같은 브라우저 자동화 도구를 사용한다.
- 페이지 소스가 아니라 네트워크 요청을 분석한다.

---

## 14. 실제 사이트 크롤링: 영어 회화 토픽

예제에서는 `basicenglishspeaking.com`의 일상 영어 회화 토픽 목록을 수집한다.

```python
import requests
import pandas as pd
from bs4 import BeautifulSoup

site = "https://basicenglishspeaking.com/daily-english-conversation-topics/"

request = requests.get(site)
soup = BeautifulSoup(request.text, "html.parser")

div = soup.find("div", {"class": "thrv-columns"})
links = div.find_all("a")

data = []

for i, link in enumerate(links, start=1):
    topic = link.text.strip()
    url = link.get("href")

    data.append({
        "번호": i,
        "토픽": topic,
        "링크": url
    })

df = pd.DataFrame(data)
df
```

### 코드 흐름

```text
사이트 요청
    ↓
HTML 파싱
    ↓
토픽 링크가 들어있는 div 찾기
    ↓
a 태그 전체 추출
    ↓
번호, 토픽, 링크를 딕셔너리로 저장
    ↓
DataFrame 생성
```

---

## 15. Pandas DataFrame으로 정리하기

크롤링한 데이터를 리스트와 딕셔너리 형태로 모은 뒤 `DataFrame`으로 만들면 표 형태로 다루기 좋다.

```python
data = [
    {"번호": 1, "토픽": "Family", "링크": "https://..."},
    {"번호": 2, "토픽": "Restaurant", "링크": "https://..."}
]

df = pd.DataFrame(data)
```

`DataFrame`으로 만들면 다음 작업을 쉽게 할 수 있다.

- 표 형태로 확인
- CSV 저장
- 중복 제거
- 조건 필터링
- 데이터 분석

---

## 16. 다음 뉴스 기사 크롤링

뉴스 기사 페이지에서 제목과 본문을 가져오는 함수다.

```python
def daum_news(news_id):
    url = f"https://v.daum.net/v/{news_id}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()

        soup = BeautifulSoup(request.text, "html.parser")

        title = soup.find("h3", {"class": "tit_view"})

        if title:
            title = title.text.strip()
        else:
            title = "제목없음"

        content = soup.find("div", {"class": "article_view"})

        if content:
            content = content.text.strip()
        else:
            content = "내용없음"

        return {
            "title": title,
            "content": content
        }

    except Exception as e:
        print("에러 발생:", e)
        return None
```

### 사용 예제

```python
news = daum_news("20260624085206643")

print("제목:")
print(news["title"])

print("\n본문:")
print(news["content"])
```

### 코드에서 중요한 부분

```python
request.raise_for_status()
```

요청이 실패하면 예외를 발생시킨다. 크롤링 함수에서는 요청 실패를 그냥 넘기지 않고 예외 처리를 하는 것이 좋다.

```python
if title:
    title = title.text.strip()
else:
    title = "제목없음"
```

페이지 구조가 바뀌어 태그를 찾지 못할 수도 있으므로 조건문으로 처리한다.

---

## 17. headers와 User-Agent

`headers`는 웹 브라우저가 서버에 보내는 추가 정보다.

크롤링에서는 서버가 요청을 정상적인 브라우저 접속으로 인식하도록 도와주는 역할을 한다.

```python
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
```

### User-Agent

User-Agent는 어떤 브라우저와 운영체제로 접속했는지 나타내는 정보다.

일부 사이트는 User-Agent가 없거나 비정상적이면 프로그램 접속으로 판단해 응답을 차단하거나 빈 페이지를 반환할 수 있다.

### Referer

Referer는 어떤 페이지에서 이동해 왔는지를 나타내는 정보다.

일부 사이트는 내부 페이지 이동처럼 보여야 정상 응답을 주는 경우가 있어 함께 설정하기도 한다.

```python
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://music.bugs.co.kr/"
}
```

---

## 18. robots.txt

`robots.txt`는 웹사이트 운영자가 검색 엔진이나 크롤링 프로그램에게 어떤 페이지를 수집해도 되는지 알려주는 규칙 파일이다.

보통 사이트 주소 뒤에 `/robots.txt`를 붙여 확인한다.

```text
https://example.com/robots.txt
```

이 파일에는 특정 경로를 수집 금지하거나 허용하는 규칙이 들어있다.

```text
User-agent: *
Disallow: /private/
Allow: /
```

`robots.txt`는 기술적으로 강제 차단 시스템이라기보다 사이트 운영 정책을 알려주는 규칙에 가깝다.

실무에서는 반드시 `robots.txt`와 사이트 이용약관을 확인하고, 서버에 무리를 주지 않는 범위에서 크롤링해야 한다.

---

## 19. 벅스 아티스트 곡 리스트 크롤링

벅스 아티스트 페이지에서 곡명, 아티스트, 앨범명을 수집하는 예제다.

```python
import pandas as pd

def bugs_artist_tracks(artist_id):
    url = f"https://music.bugs.co.kr/artist/{artist_id}/tracks"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://music.bugs.co.kr/"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.select("table.list.trackList tbody tr")

    data = []

    for row in rows:
        title_tag = row.select_one("p.title a")
        artist_tag = row.select_one("p.artist a")
        album_tag = row.select_one("a.album")

        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        artist = artist_tag.get_text(strip=True) if artist_tag else ""
        album = album_tag.get_text(strip=True) if album_tag else ""

        data.append({
            "곡명": title,
            "아티스트": artist,
            "앨범명": album
        })

    df = pd.DataFrame(data)
    df.index = df.index + 1

    file_name = f"bugs_artist_{artist_id}_tracks.csv"
    df.to_csv(file_name, encoding="utf-8-sig")

    return df

df = bugs_artist_tracks("20260859")
df
```

### 선택자 분석

| 선택자 | 의미 |
| --- | --- |
| `table.list.trackList tbody tr` | 곡 목록 테이블의 각 행 |
| `p.title a` | 곡명 |
| `p.artist a` | 아티스트 |
| `a.album` | 앨범명 |

### CSV 저장

```python
df.to_csv(file_name, encoding="utf-8-sig")
```

`utf-8-sig`를 사용하면 Excel에서 한글이 깨지는 문제를 줄일 수 있다.

---

## 20. 여러 페이지 크롤링

한 페이지에 모든 데이터가 없으면 페이지 번호를 바꿔가며 반복 수집한다.

```python
import time

def bugs_artist_tracks_all_pages(artist_id, max_page=20):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://music.bugs.co.kr/"
    }

    all_data = []

    for page in range(1, max_page + 1):
        url = (
            f"https://music.bugs.co.kr/artist/{artist_id}/tracks"
            f"?type=RELEASE&sort=P&page={page}&roleCode=0&highQualityOnly="
        )

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.select("table.trackList tbody tr")

        page_data = []

        for row in rows:
            title_tag = row.select_one("p.title a")
            artist_tag = row.select_one("p.artist a")
            album_tag = row.select_one("a.album")

            if title_tag is None:
                continue

            page_data.append({
                "곡명": title_tag.get_text(strip=True),
                "아티스트": artist_tag.get_text(strip=True) if artist_tag else "",
                "앨범명": album_tag.get_text(strip=True) if album_tag else "",
                "페이지": page
            })

        if len(page_data) == 0:
            print(f"{page}페이지에 곡이 없어 종료합니다.")
            break

        all_data.extend(page_data)
        print(f"{page}페이지 크롤링 완료: {len(page_data)}곡")

        time.sleep(0.5)

    df = pd.DataFrame(all_data)

    if not df.empty:
        df = df.drop_duplicates(subset=["곡명", "아티스트", "앨범명"])
        df.index = df.index + 1

    file_name = f"bugs_artist_{artist_id}_tracks.csv"
    df.to_csv(file_name, encoding="utf-8-sig")

    print(f"CSV 저장 완료: {file_name}")
    print(f"총 {len(df)}곡 수집 완료")

    return df
```

### 실행

```python
bugs_artist_tracks_all_pages("80021125")
```

### 코드 흐름

```text
1페이지부터 max_page까지 반복
        ↓
페이지별 URL 생성
        ↓
요청 후 HTML 파싱
        ↓
곡 목록 행 선택
        ↓
곡명, 아티스트, 앨범명 추출
        ↓
데이터가 없으면 반복 종료
        ↓
중복 제거
        ↓
CSV 저장
```

### `time.sleep()`

```python
time.sleep(0.5)
```

요청 사이에 잠깐 쉬는 코드다. 너무 빠르게 많은 요청을 보내면 서버에 부담을 줄 수 있으므로 크롤링에서는 요청 간격을 두는 것이 좋다.

---

## 21. 크롤링 시 주의사항

웹크롤링은 기술적으로 가능하다고 해서 항상 해도 되는 것은 아니다.

다음 사항을 지켜야 한다.

- `robots.txt`를 확인한다.
- 사이트 이용약관을 확인한다.
- 서버에 부담을 주지 않도록 요청 간격을 둔다.
- 개인정보나 민감 정보를 수집하지 않는다.
- 상업적 사용 전에는 권리와 정책을 확인한다.
- 크롤링 결과를 저장할 때 출처와 수집 시점을 기록한다.

---

## 22. 핵심 정리

### Requests

- 웹 서버에 요청을 보내고 응답을 받는다.
- `response.text`는 HTML 문자열이다.
- `response.content`는 이미지 같은 바이너리 데이터다.
- `raise_for_status()`로 요청 실패를 예외 처리할 수 있다.

### BeautifulSoup

- HTML을 파싱해 태그를 객체처럼 다룬다.
- `find()`는 첫 번째 태그를 찾는다.
- `find_all()`은 모든 태그를 찾는다.
- `select_one()`은 CSS 선택자에 맞는 첫 번째 요소를 찾는다.
- `select()`는 CSS 선택자에 맞는 모든 요소를 찾는다.

### 데이터 저장

- 리스트 안에 딕셔너리를 넣으면 표 형태 데이터로 만들기 좋다.
- `pandas.DataFrame()`으로 데이터를 표처럼 다룰 수 있다.
- `to_csv()`로 CSV 파일을 저장할 수 있다.
- 한글 CSV는 `encoding="utf-8-sig"`를 사용하면 Excel에서 깨짐을 줄일 수 있다.

### 실전 크롤링

- 실제 사이트는 구조가 바뀔 수 있으므로 예외 처리가 필요하다.
- JavaScript로 동적으로 생성되는 데이터는 `requests`만으로 가져오지 못할 수 있다.
- `headers`를 설정하면 브라우저 요청처럼 보이게 할 수 있다.
- 여러 페이지를 수집할 때는 반복문과 `time.sleep()`을 함께 사용한다.
