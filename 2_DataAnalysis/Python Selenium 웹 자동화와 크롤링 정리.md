# Python Selenium 웹 자동화와 크롤링 정리

Selenium은 Python 코드로 실제 웹 브라우저를 자동으로 제어할 수 있게 해주는 웹 자동화 라이브러리다.

`requests`와 `BeautifulSoup`은 서버에서 받은 HTML을 분석하는 방식이지만, Selenium은 브라우저를 직접 실행한다. 따라서 버튼 클릭, 검색어 입력, 스크롤, 페이지 이동, JavaScript 실행 결과 확인 같은 사용자 행동을 코드로 자동화할 수 있다.

이번 글에서는 Selenium이 필요한 이유부터 동적 페이지 크롤링, 멜론 검색 결과 수집, 스타벅스 매장 정보 크롤링까지 정리한다.

---

## 1. Selenium이 필요한 이유

웹페이지에는 두 종류가 있다.

```text
정적 페이지
    서버가 HTML에 데이터를 담아 바로 보내는 페이지

동적 페이지
    처음 HTML에는 데이터가 없고,
    JavaScript가 실행된 뒤 화면에 데이터가 추가되는 페이지
```

`requests`는 서버가 처음 응답한 HTML만 가져온다. JavaScript가 실행된 뒤 화면에 추가된 데이터는 가져오지 못할 수 있다.

Selenium은 실제 브라우저를 실행하므로 JavaScript 실행 결과까지 확인할 수 있다.

---

## 2. requests로 동적 페이지를 가져오면 생기는 문제

다음 HTML은 JavaScript가 실행된 뒤 과일 목록을 화면에 추가한다.

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

브라우저에서는 다음 요소가 보인다.

```html
<p class="fruit">사과</p>
<p class="fruit">바나나</p>
<p class="fruit">오렌지</p>
<p class="fruit">딸기</p>
```

하지만 `requests`로 가져오면 JavaScript 실행 전 HTML만 확인할 수 있다.

```python
import requests
from bs4 import BeautifulSoup

url = "http://127.0.0.1:5500/7.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

fruits = soup.select(".fruit")

print(fruits)
```

### 출력 결과

```text
[]
```

`.fruit` 요소는 JavaScript가 실행된 뒤 만들어진다. `requests`는 JavaScript를 실행하지 않기 때문에 빈 리스트가 나온다.

---

## 3. Selenium으로 동적 페이지 가져오기

Selenium은 브라우저를 실제로 실행하고 페이지를 렌더링한다.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

url = "http://127.0.0.1:5500/7.html"
driver.get(url)

time.sleep(2)

fruits = driver.find_elements(By.CLASS_NAME, "fruit")

for fruit in fruits:
    print(fruit.text)

driver.quit()
```

### 출력 결과

```text
사과
바나나
오렌지
딸기
```

`driver.get(url)`로 브라우저에서 페이지를 열고, JavaScript 실행을 기다린 뒤 `.fruit` 요소를 찾는다.

---

## 4. Selenium 기본 구조

Selenium 코드의 기본 흐름은 다음과 같다.

```text
브라우저 실행
    ↓
페이지 이동
    ↓
요소 찾기
    ↓
클릭, 입력, 텍스트 추출
    ↓
브라우저 종료
```

Python 코드로 쓰면 다음과 같다.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://example.com")

element = driver.find_element(By.TAG_NAME, "h1")
print(element.text)

driver.quit()
```

`driver.quit()`은 브라우저를 완전히 종료한다. 자동화 작업이 끝나면 반드시 호출하는 것이 좋다.

---

## 5. 자주 사용하는 import

```python
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
```

| import | 역할 |
| --- | --- |
| `webdriver` | 브라우저 실행 |
| `By` | 요소를 찾는 기준 지정 |
| `Keys` | Enter 같은 키보드 입력 |
| `Options` | 브라우저 실행 옵션 설정 |
| `WebDriverWait` | 특정 조건이 만족될 때까지 대기 |
| `expected_conditions` | 대기 조건 |
| `TimeoutException` | 대기 시간이 초과될 때 발생하는 예외 |

---

## 6. 요소 찾기

Selenium은 다양한 기준으로 HTML 요소를 찾을 수 있다.

### 요소 하나 찾기

```python
element = driver.find_element(By.ID, "top_search")
```

요소를 찾지 못하면 예외가 발생한다.

### 여러 요소 찾기

```python
elements = driver.find_elements(By.CLASS_NAME, "fruit")
```

`find_elements()`는 조건에 맞는 요소를 리스트로 반환한다. 요소를 찾지 못하면 빈 리스트 `[]`를 반환한다.

### 자주 사용하는 선택 방식

| 방식 | 예시 |
| --- | --- |
| ID | `By.ID, "top_search"` |
| Class | `By.CLASS_NAME, "fruit"` |
| Tag | `By.TAG_NAME, "td"` |
| CSS Selector | `By.CSS_SELECTOR, "tbody tr"` |
| XPath | `By.XPATH, '//*[@id="divCollection"]/ul/li[3]/a/span'` |

---

## 7. `find_element()`와 `find_elements()` 비교

| 구분 | `find_element()` | `find_elements()` |
| --- | --- | --- |
| 반환값 | 요소 1개 | 요소 리스트 |
| 찾지 못한 경우 | 예외 발생 | 빈 리스트 반환 |
| 사용 상황 | 검색창, 버튼처럼 하나만 필요한 경우 | 게시글, 상품, 테이블 행처럼 여러 개 필요한 경우 |

예를 들어 테이블의 여러 행을 처리할 때는 `find_elements()`를 사용한다.

```python
rows = song_table.find_elements(By.CSS_SELECTOR, "tbody tr")

for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
```

`row.find_element(By.TAG_NAME, "td")`는 `td` 하나만 반환하므로 `len(cols)`를 사용할 수 없다. 여러 열을 다루려면 `find_elements()`를 사용해야 한다.

---

## 8. XPath

XPath는 XML 또는 HTML 문서에서 특정 요소나 속성을 선택하기 위해 사용하는 경로 표현 언어다.

```python
element = driver.find_element(
    By.XPATH,
    '//*[@id="divCollection"]/ul/li[3]/a/span'
)
```

### XPath의 특징

- 요소의 위치나 속성을 기준으로 찾을 수 있다.
- 복잡한 구조의 페이지에서 특정 요소를 찾을 때 사용할 수 있다.
- 구조가 조금만 바뀌어도 깨질 수 있다.

### full XPath

full XPath는 루트 요소에서 대상 요소까지의 절대 경로다.

브라우저 개발자 도구에서 쉽게 복사할 수 있지만, HTML 구조가 변경되면 경로가 깨질 가능성이 높다.

가능하면 CSS 선택자나 안정적인 속성 기반 선택자를 먼저 고려하는 것이 좋다.

---

## 9. 대기 처리

Selenium에서는 페이지 로딩이나 JavaScript 실행을 기다려야 할 때가 많다.

### 9.1 `time.sleep()`

```python
time.sleep(2)
```

정해진 시간만큼 무조건 기다린다. 간단하지만 비효율적일 수 있다.

### 9.2 `WebDriverWait`

```python
wait = WebDriverWait(driver, 10)

search_box = wait.until(
    EC.presence_of_element_located((By.ID, "top_search"))
)
```

최대 10초 동안 조건을 기다린다. 조건이 빨리 만족되면 바로 다음 코드로 넘어간다.

### 자주 쓰는 조건

| 조건 | 의미 |
| --- | --- |
| `presence_of_element_located` | 요소가 DOM에 존재할 때까지 대기 |
| `element_to_be_clickable` | 요소가 클릭 가능할 때까지 대기 |
| `presence_of_all_elements_located` | 여러 요소가 DOM에 존재할 때까지 대기 |

실전 크롤링에서는 `time.sleep()`보다 `WebDriverWait`을 사용하는 것이 더 안정적이다.

---

## 10. 멜론 검색 결과 크롤링

멜론 메인 페이지에서 검색어를 입력하고, 곡 탭으로 이동한 뒤 곡명, 아티스트, 앨범, 좋아요 수를 수집하는 예제다.

### 전체 흐름

```text
Chrome 실행
    ↓
멜론 접속
    ↓
검색창 찾기
    ↓
검색어 입력 후 Enter
    ↓
곡 탭 클릭
    ↓
곡 목록 테이블 대기
    ↓
각 행에서 곡명, 아티스트, 앨범, 좋아요 수 추출
    ↓
DataFrame 생성
    ↓
CSV 저장
```

---

## 11. 멜론 한 페이지 크롤링 예제

```python
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def melon_search_from_main(keyword):
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    data = []

    try:
        driver.get("https://www.melon.com/")
        time.sleep(2)

        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "top_search"))
        )

        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)

        time.sleep(3)

        song_tab = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="divCollection"]/ul/li[3]/a/span')
            )
        )
        song_tab.click()

        time.sleep(3)

        song_table = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="frm_defaultList"]/div/table')
            )
        )

        rows = song_table.find_elements(By.CSS_SELECTOR, "tbody tr")

        print("찾은 행 개수:", len(rows))

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")

            if len(cols) < 5:
                continue

            title_text = cols[2].text.strip()
            title_lines = [
                line.strip()
                for line in title_text.split("\n")
                if line.strip()
            ]

            title = ""

            for line in title_lines:
                if line.startswith("Title "):
                    title = line.replace("Title ", "").strip()
                    break

            if not title:
                for line in title_lines:
                    if (
                        "재생" not in line
                        and "담기" not in line
                        and "상세정보" not in line
                        and not line.startswith("Title")
                    ):
                        title = line
                        break

            artist_lines = [
                line.strip()
                for line in cols[3].text.split("\n")
                if line.strip()
            ]
            artist = artist_lines[0] if artist_lines else ""

            album_lines = [
                line.strip()
                for line in cols[4].text.split("\n")
                if line.strip()
            ]
            album = album_lines[0] if album_lines else ""

            try:
                like = row.find_element(
                    By.CSS_SELECTOR,
                    "button.like span.cnt"
                ).text.strip()
            except:
                like = ""

            if title:
                data.append({
                    "곡명": title,
                    "아티스트": artist,
                    "앨범": album,
                    "좋아요수": like
                })

        df = pd.DataFrame(data)

        if not df.empty:
            df.index = df.index + 1

        file_name = f"melon_{keyword}_songs.csv"
        df.to_csv(file_name, encoding="utf-8-sig")

        print(f"CSV 저장 완료: {file_name}")
        print(f"총 {len(df)}곡 수집 완료")

        return df

    finally:
        driver.quit()
```

### 실행

```python
melon_search_from_main("신의 키스")
```

---

## 12. 멜론 데이터 추출 방식

곡 목록은 테이블 형태로 구성되어 있으므로 각 행을 반복 처리한다.

```python
rows = song_table.find_elements(By.CSS_SELECTOR, "tbody tr")
```

각 행에서 `td`를 가져온다.

```python
cols = row.find_elements(By.TAG_NAME, "td")
```

곡명은 여러 텍스트가 섞여 있을 수 있으므로 줄 단위로 나눈 뒤 불필요한 값을 제외한다.

```python
title_lines = [
    line.strip()
    for line in cols[2].text.split("\n")
    if line.strip()
]
```

`Title`이 붙은 줄이 있으면 더 정확한 값으로 보정한다.

```python
for line in title_lines:
    if line.startswith("Title "):
        title = line.replace("Title ", "").strip()
        break
```

좋아요 수는 별도의 버튼 안에 들어 있으므로 CSS 선택자로 찾는다.

```python
like = row.find_element(
    By.CSS_SELECTOR,
    "button.like span.cnt"
).text.strip()
```

---

## 13. 현재 페이지 추출 함수 분리

여러 페이지를 크롤링하려면 현재 페이지의 데이터를 추출하는 기능을 별도 함수로 분리하는 것이 좋다.

```python
from selenium.common.exceptions import TimeoutException

def extract_current_page(driver, wait):
    data = []

    try:
        song_table = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="frm_defaultList"]/div/table')
            )
        )
    except TimeoutException:
        return []

    rows = song_table.find_elements(By.CSS_SELECTOR, "tbody tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")

        if len(cols) < 5:
            continue

        title_lines = [
            line.strip()
            for line in cols[2].text.split("\n")
            if line.strip()
        ]

        title = ""

        for line in title_lines:
            if line.startswith("Title "):
                title = line.replace("Title ", "").strip()
                break

        if not title:
            for line in title_lines:
                if (
                    "재생" not in line
                    and "담기" not in line
                    and "상세정보" not in line
                    and not line.startswith("Title")
                ):
                    title = line
                    break

        artist_lines = [
            line.strip()
            for line in cols[3].text.split("\n")
            if line.strip()
        ]
        artist = artist_lines[0] if artist_lines else ""

        album_lines = [
            line.strip()
            for line in cols[4].text.split("\n")
            if line.strip()
        ]
        album = album_lines[0] if album_lines else ""

        try:
            like = row.find_element(
                By.CSS_SELECTOR,
                "button.like span.cnt"
            ).text.strip()
        except:
            like = ""

        if title:
            data.append({
                "곡명": title,
                "아티스트": artist,
                "앨범": album,
                "좋아요수": like
            })

    return data
```

이렇게 분리하면 페이지 이동 로직과 데이터 추출 로직이 섞이지 않아 코드가 더 읽기 좋아진다.

---

## 14. 멜론 여러 페이지 크롤링

멜론 검색 결과는 페이지가 나뉘어 있다.

페이지 이동은 JavaScript 함수인 `pageObj.sendPage()`를 직접 실행하는 방식으로 처리한다.

```python
driver.execute_script(
    f"pageObj.sendPage('{next_start_index}');"
)
```

### 전체 코드

```python
def melon_search_all_pages(keyword, max_page=30):
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    all_data = []

    try:
        driver.get("https://www.melon.com/")
        time.sleep(2)

        search_box = wait.until(
            EC.presence_of_element_located((By.ID, "top_search"))
        )

        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)

        time.sleep(3)

        song_tab = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="divCollection"]/ul/li[3]/a/span')
            )
        )

        song_tab.click()
        time.sleep(3)

        for page in range(1, max_page + 1):
            page_data = extract_current_page(driver, wait)

            if not page_data:
                print(f"{page}페이지 데이터가 없어 종료합니다.")
                break

            all_data.extend(page_data)
            print(f"{page}페이지 크롤링 완료: {len(page_data)}곡")

            next_start_index = page * 50 + 1

            try:
                driver.execute_script(
                    f"pageObj.sendPage('{next_start_index}');"
                )
                time.sleep(3)

            except Exception as e:
                print("다음 페이지 이동 실패:", e)
                break

        df = pd.DataFrame(all_data)

        if not df.empty:
            df = df.drop_duplicates(
                subset=["곡명", "아티스트", "앨범"]
            )
            df.index = df.index + 1

        file_name = f"melon_{keyword}_all_songs.csv"

        df.to_csv(
            file_name,
            encoding="utf-8-sig"
        )

        print(f"CSV 저장 완료: {file_name}")
        print(f"총 {len(df)}곡 수집 완료")

        return df

    finally:
        driver.quit()
```

### 실행

```python
melon_search_all_pages("조용필", 30)
```

### 코드 흐름

```text
검색어 입력
    ↓
곡 탭 이동
    ↓
현재 페이지 데이터 추출
    ↓
pageObj.sendPage()로 다음 페이지 이동
    ↓
데이터가 없거나 이동 실패 시 종료
    ↓
중복 제거
    ↓
CSV 저장
```

---

## 15. `execute_script()`

`execute_script()`는 Selenium에서 브라우저 안의 JavaScript를 직접 실행하는 메서드다.

```python
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
```

멜론 예제에서는 페이지 이동 함수가 JavaScript로 구현되어 있기 때문에 Selenium에서 직접 실행한다.

```python
driver.execute_script("pageObj.sendPage('51');")
```

---

## 16. 스타벅스 서울 전체 매장 크롤링

스타벅스 예제는 메뉴에 마우스를 올리고 하위 메뉴를 클릭한 뒤, 서울 전체 매장 목록을 가져온다.

이 과정에서는 `ActionChains`를 사용한다.

### 필요한 import

```python
import re
import time
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
```

---

## 17. ActionChains

`ActionChains`는 마우스 이동, 클릭, 드래그 같은 복합 동작을 순서대로 실행할 때 사용한다.

```python
action = ActionChains(driver)

action.move_to_element(first_tag) \
      .move_to_element(second_tag) \
      .click() \
      .perform()
```

### 동작 흐름

```text
첫 번째 메뉴로 마우스 이동
    ↓
하위 메뉴로 마우스 이동
    ↓
클릭
    ↓
perform()으로 실행
```

`perform()`을 호출해야 예약한 동작이 실제로 실행된다.

---

## 18. 스타벅스 매장 크롤링 코드

```python
def fetch_starbucks():
    url = "https://www.starbucks.co.kr/index.do"

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    time.sleep(2)

    action = ActionChains(driver)

    first_tag = driver.find_element(
        By.CSS_SELECTOR,
        "#gnb > div > nav > div > ul > li.gnb_nav03"
    )

    second_tag = driver.find_element(
        By.CSS_SELECTOR,
        "#gnb > div > nav > div > ul > li.gnb_nav03 > div > div > div > ul:nth-child(1) > li:nth-child(3) > a"
    )

    action.move_to_element(first_tag) \
          .move_to_element(second_tag) \
          .click() \
          .perform()

    seoul_tag = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#container > div > form > fieldset > div > section > article.find_store_cont > article > article:nth-child(4) > div.loca_step1 > div.loca_step1_cont > ul > li:nth-child(1) > a"
        ))
    )

    seoul_tag.click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "set_gugun_cd_btn")
        )
    )

    gu_elements = driver.find_elements(
        By.CLASS_NAME,
        "set_gugun_cd_btn"
    )

    gu_elements[0].click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "quickResultLstCon")
        )
    )

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    stores = soup.find(
        "ul",
        "quickSearchResultBoxSidoGugun"
    ).find_all("li")

    store_list = []
    addr_list = []
    lat_list = []
    lng_list = []

    for store in stores:
        store_name = store.find("strong").text
        store_addr = store.find("p").text

        store_addr = re.sub(
            r"\d{4}-\d{4}$",
            "",
            store_addr
        ).strip()

        store_lat = store["data-lat"]
        store_lng = store["data-long"]

        store_list.append(store_name)
        addr_list.append(store_addr)
        lat_list.append(store_lat)
        lng_list.append(store_lng)

    df = pd.DataFrame({
        "store": store_list,
        "addr": addr_list,
        "lat": lat_list,
        "lng": lng_list
    })

    driver.quit()

    return df
```

### 실행과 저장

```python
starbucks_df = fetch_starbucks()

starbucks_df.to_csv(
    "starbucks_seoul.csv",
    index=False,
    encoding="utf-8-sig"
)

print("데이터가 starbucks_seoul.csv 파일로 저장되었습니다.")
print(starbucks_df.head())
```

---

## 19. `page_source`와 BeautifulSoup 같이 사용하기

Selenium으로 페이지를 조작한 뒤 최종 HTML만 파싱할 때는 `driver.page_source`를 사용할 수 있다.

```python
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
```

이 방식은 다음 상황에서 유용하다.

- Selenium으로 버튼 클릭이나 지역 선택을 해야 한다.
- 이후 HTML 구조가 안정적으로 만들어진다.
- 반복 추출은 BeautifulSoup으로 처리하는 편이 더 편하다.

즉, Selenium과 BeautifulSoup을 함께 사용할 수 있다.

```text
Selenium
    → 브라우저 조작
    → JavaScript 렌더링 결과 확보

BeautifulSoup
    → HTML 파싱
    → 데이터 추출
```

---

## 20. 정규식으로 전화번호 제거

스타벅스 매장 주소에는 전화번호가 붙어 있을 수 있다.

```python
store_addr = re.sub(
    r"\d{4}-\d{4}$",
    "",
    store_addr
).strip()
```

정규식 의미는 다음과 같다.

| 패턴 | 의미 |
| --- | --- |
| `\d{4}` | 숫자 4자리 |
| `-` | 하이픈 |
| `\d{4}` | 숫자 4자리 |
| `$` | 문자열 끝 |

즉, 주소 끝에 있는 `0000-0000` 형태의 전화번호를 제거한다.

`r"..."`는 raw string으로, 백슬래시를 이스케이프 문자로 처리하지 않고 그대로 사용하게 해준다.

---

## 21. 바나프레소 메뉴 이동 예제

바나프레소 예제는 사이트 메뉴에 마우스를 올린 뒤 하위 메뉴를 클릭하는 자동화 흐름을 보여준다.

```python
def fetch_banapresso():
    url = "https://www.banapresso.com/"

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    time.sleep(2)

    action = ActionChains(driver)

    first_tag = driver.find_element(
        By.CSS_SELECTOR,
        "#wrap > header > div > ul > li:nth-child(2)"
    )

    second_tag = driver.find_element(
        By.CSS_SELECTOR,
        "#wrap > header > div > ul > li:nth-child(2) > ul > li:nth-child(1) > a"
    )

    action.move_to_element(first_tag) \
          .move_to_element(second_tag) \
          .click() \
          .perform()

    driver.quit()
```

### 실행

```python
fetch_banapresso()
```

이 예제는 데이터를 추출하기보다 Selenium으로 메뉴 이동을 자동화하는 방법을 보여준다.

---

## 22. CSV 저장

크롤링 결과를 `DataFrame`으로 만든 뒤 CSV 파일로 저장할 수 있다.

```python
df.to_csv("result.csv", encoding="utf-8-sig")
```

인덱스를 저장하지 않으려면 `index=False`를 사용한다.

```python
df.to_csv("result.csv", index=False, encoding="utf-8-sig")
```

`utf-8-sig`는 Excel에서 한글이 깨지는 문제를 줄이는 데 도움이 된다.

---

## 23. Selenium 크롤링 시 주의사항

Selenium은 실제 브라우저를 실행하기 때문에 `requests`보다 무겁고 느리다.

따라서 다음 기준으로 선택하는 것이 좋다.

| 상황 | 추천 방식 |
| --- | --- |
| HTML에 데이터가 바로 들어 있음 | `requests` + `BeautifulSoup` |
| JavaScript 실행 후 데이터가 생김 | Selenium |
| 버튼 클릭, 검색 입력, 로그인 등이 필요함 | Selenium |
| API가 따로 존재함 | API 요청 |

---

## 24. 크롤링 윤리와 안정성

크롤링할 때는 다음 사항을 지켜야 한다.

- 사이트의 `robots.txt`와 이용약관을 확인한다.
- 서버에 부담을 주지 않도록 요청 간격을 둔다.
- 개인정보나 민감한 정보를 수집하지 않는다.
- 수집한 데이터를 상업적으로 사용하기 전에 권리와 정책을 확인한다.
- 페이지 구조가 변경될 수 있으므로 예외 처리를 작성한다.
- 브라우저는 작업이 끝나면 `driver.quit()`으로 종료한다.

---

## 25. 핵심 정리

### Selenium

- 실제 브라우저를 Python 코드로 제어한다.
- JavaScript로 동적으로 생성된 데이터도 가져올 수 있다.
- 클릭, 입력, 페이지 이동, 스크롤 같은 사용자 행동을 자동화할 수 있다.

### 요소 찾기

- 하나만 찾을 때는 `find_element()`를 사용한다.
- 여러 개를 찾을 때는 `find_elements()`를 사용한다.
- CSS 선택자, XPath, id, class 등 다양한 기준으로 요소를 찾을 수 있다.

### 대기 처리

- `time.sleep()`은 무조건 기다린다.
- `WebDriverWait`은 특정 조건이 만족될 때까지 기다린다.
- 실전에서는 `WebDriverWait`이 더 안정적이다.

### 실전 크롤링

- Selenium으로 화면을 조작하고 `page_source`를 가져온 뒤 BeautifulSoup으로 파싱할 수 있다.
- 여러 페이지는 반복문과 페이지 이동 로직을 함께 사용한다.
- 수집한 데이터는 `pandas.DataFrame`으로 정리하고 CSV로 저장한다.
