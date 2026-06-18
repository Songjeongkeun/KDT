# [17일차] Flexbox, Grid와 CSS 효과 정리

CSS를 이용해 여러 영역을 배치하는 방법과 화면 크기에 따라 스타일을 변경하는 방법을 정리한다. 자주 사용하는 값을 CSS 변수로 관리하고, `transition`, `transform`, `animation`을 이용해 요소에 시각적인 효과를 적용한다.

| 구분 | 주요 내용 |
| --- | --- |
| 레이아웃 | `float`, Flexbox, Grid |
| 반응형 | 미디어 쿼리, 브레이크 포인트 |
| 스타일 관리 | CSS 변수, CSS 우선순위 |
| 시각 효과 | `transition`, `transform`, `animation` |

---

## 1. `float`를 이용한 3단 레이아웃

`float`를 사용하면 여러 요소를 왼쪽이나 오른쪽으로 띄워 가로로 배치할 수 있다.

다음 예제는 왼쪽, 가운데, 오른쪽 영역에 `float: left`를 적용해 3단 레이아웃을 만든다.

```html
<div class="container">
    <header>
        헤더 영역
    </header>

    <main>
        <section class="left">
            왼쪽 콘텐츠 영역
        </section>

        <article class="middle">
            중간 콘텐츠 영역
        </article>

        <aside class="right">
            오른쪽 콘텐츠 영역
        </aside>

        <div class="clear"></div>
    </main>

    <footer>
        푸터 영역
    </footer>
</div>
```

```css
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

.container {
    width: 900px;
    margin: 20px auto;
    border: 2px solid #000;
}

header,
footer {
    border: 2px solid #000;
    margin: 10px;
    padding: 10px;
}

main {
    margin: 10px;
    padding: 20px;
    border: 2px solid #000;
}

.left {
    float: left;
    width: 15%;
    height: 300px;
    margin-right: 10px;
    border: 2px solid #000;
}

.middle {
    float: left;
    width: 60%;
    height: 300px;
    margin-right: 10px;
    border: 2px solid #000;
    text-align: center;
}

.right {
    float: left;
    width: 15%;
    height: 300px;
    border: 2px solid #000;
}

.clear {
    clear: both;
}
```

```text
┌────────────────────────────────────────────┐
│                   header                   │
├──────────┬──────────────────────┬──────────┤
│   left   │        middle        │  right   │
│   15%    │         60%          │   15%    │
├──────────┴──────────────────────┴──────────┤
│                   footer                   │
└────────────────────────────────────────────┘
```

각 영역에 `float: left`가 적용되어 왼쪽부터 순서대로 배치된다.

`.clear`는 앞에서 적용된 `float`의 영향을 해제해 `footer`가 세 영역 아래에 배치되도록 한다.

---

## 2. Flexbox

Flexbox는 요소를 한 방향으로 유연하게 배치하고 정렬하기 위한 레이아웃 방식이다.

부모 요소에 `display: flex`를 적용하면 내부의 자식 요소가 Flex 아이템이 된다.

```css
.columns {
    display: flex;
}
```

### 2.1 Flex 컨테이너와 아이템

| 구분 | 의미 |
| --- | --- |
| Flex 컨테이너 | `display: flex`가 적용된 부모 요소 |
| Flex 아이템 | Flex 컨테이너 안에 있는 자식 요소 |

컨테이너는 아이템의 배치 방향, 정렬, 줄바꿈, 간격을 결정한다.

```html
<div class="columns">
    <nav>nav</nav>
    <main>main</main>
    <aside>aside</aside>
</div>
```

위 코드에서는 `.columns`가 Flex 컨테이너가 되고 `nav`, `main`, `aside`가 Flex 아이템이 된다.

### 2.2 `flex-direction`

Flex 아이템이 배치되는 주축의 방향을 결정한다.

```css
.container {
    flex-direction: row;
}
```

| 값 | 배치 방향 |
| --- | --- |
| `row` | 아이템을 가로 방향으로 배치한다 |
| `column` | 아이템을 세로 방향으로 배치한다 |

`row`가 기본값이다.

### 2.3 `justify-content`

주축을 기준으로 아이템을 정렬한다.

```css
.container {
    justify-content: center;
}
```

| 값 | 정렬 방식 |
| --- | --- |
| `flex-start` | 주축의 시작 위치부터 정렬한다 |
| `center` | 가운데로 정렬한다 |
| `space-between` | 양 끝에 아이템을 붙이고 사이 간격을 동일하게 만든다 |
| `space-around` | 각 아이템의 주변에 여백을 만든다 |

### 2.4 `align-items`

주축과 수직인 교차축을 기준으로 아이템을 정렬한다.

```css
.container {
    align-items: center;
}
```

| 값 | 정렬 방식 |
| --- | --- |
| `stretch` | 아이템의 크기가 지정되지 않았다면 교차축 방향으로 늘린다 |
| `center` | 교차축의 가운데에 배치한다 |
| `flex-end` | 교차축의 끝에 배치한다 |

`stretch`가 기본값이다.

### 2.5 `flex-wrap`

아이템이 컨테이너의 한 줄을 넘어갈 때 줄바꿈할지 결정한다.

```css
.container {
    flex-wrap: wrap;
}
```

| 값 | 의미 |
| --- | --- |
| `nowrap` | 줄바꿈하지 않는다 |
| `wrap` | 공간이 부족하면 다음 줄로 이동한다 |

### 2.6 `align-content`

`flex-wrap`으로 여러 줄이 만들어졌을 때 줄 전체를 정렬한다.

```css
.container {
    align-content: center;
}
```

```css
.container {
    align-content: space-between;
}
```

### 2.7 `gap`

Flex 아이템 사이의 간격을 지정한다.

```css
.columns {
    display: flex;
    gap: 20px;
}
```

### 2.8 `flex-grow`

컨테이너에 남는 공간이 있을 때 아이템이 공간을 차지하는 비율을 지정한다.

```css
nav {
    flex-grow: 1;
}

main {
    flex-grow: 2;
}

aside {
    flex-grow: 1;
}
```

전체 남는 공간을 `1 : 2 : 1`의 비율로 나눈다.

### 2.9 `flex-shrink`

컨테이너의 공간이 부족할 때 아이템이 줄어드는 정도를 지정한다.

```css
.item {
    flex-shrink: 1;
}
```

### 2.10 `flex-basis`

Flex 아이템의 시작 크기를 지정한다.

```css
.item {
    flex-basis: 200px;
}
```

### 2.11 `flex`

`flex-grow`, `flex-shrink`, `flex-basis`를 한 번에 작성하는 축약 속성이다.

```css
.item {
    flex: 1 1 200px;
}
```

```text
flex: flex-grow flex-shrink flex-basis
```

다음과 같이 하나의 숫자만 사용할 수도 있다.

```css
nav {
    flex: 1;
}

main {
    flex: 2;
}

aside {
    flex: 1;
}
```

### 2.12 `align-self`

특정 Flex 아이템 하나의 교차축 정렬을 변경한다.

```css
.item {
    align-self: center;
}
```

### 2.13 Flexbox 레이아웃 예제

```html
<div class="container">
    <header>헤더영역</header>

    <div class="columns">
        <nav>nav (왼쪽 메뉴)</nav>
        <main>main (가운데 본문)</main>
        <aside>aside (오른쪽 사이드)</aside>
    </div>

    <footer>footer 영역</footer>
</div>
```

```css
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

.container {
    width: 1000px;
    margin: 20px auto;
    padding: 10px;
    border: 2px solid #000;
}

header,
footer {
    padding: 20px;
    margin-bottom: 10px;
    border: 2px solid #000;
}

.columns {
    display: flex;
    gap: 20px;
    margin-bottom: 10px;
    justify-content: center;
}

nav,
main,
aside {
    min-height: 200px;
    padding: 20px;
    border: 2px solid #000;
}

nav {
    flex: 1;
}

main {
    flex: 2;
}

aside {
    flex: 1;
}
```

```text
┌────────────────────────────────────────────┐
│                   header                   │
├──────────┬──────────────────────┬──────────┤
│   nav    │         main         │  aside   │
│  flex 1  │        flex 2        │  flex 1  │
├──────────┴──────────────────────┴──────────┤
│                   footer                   │
└────────────────────────────────────────────┘
```

---

## 3. Grid

Grid는 행과 열을 기준으로 요소를 배치하는 2차원 레이아웃 방식이다.

부모 요소에 `display: grid`를 적용하면 내부의 자식 요소를 Grid 아이템으로 배치할 수 있다.

```css
.app {
    display: grid;
}
```

### 3.1 Grid 정렬 속성의 기준

```text
align-*   : 세로 방향
justify-* : 가로 방향

*-items : 컨테이너 안의 모든 아이템 정렬
*-self  : 특정 아이템 하나의 정렬
```

### 3.2 `grid-template-columns`

열의 개수와 크기를 지정한다.

```css
.app {
    grid-template-columns: 240px 20px 820px;
}
```

공백으로 구분한 값의 개수가 열의 개수가 된다.

```text
240px 열 | 20px 열 | 820px 열
```

### 3.3 `grid-template-rows`

행의 개수와 크기를 지정한다.

```css
.app {
    grid-template-rows: 80px 60px 500px 60px;
}
```

위 코드는 크기가 다른 네 개의 행을 만든다.

### 3.4 `grid-template-areas`

Grid 영역에 이름을 붙여 레이아웃 구조를 작성한다.

```css
.app {
    grid-template-areas:
        "header header header"
        "nav    nav    nav"
        "sidebar divider main"
        "footer footer footer";
}
```

큰따옴표로 감싼 한 줄이 하나의 행을 의미하며, 한 줄 안의 이름 개수가 열의 개수가 된다.

같은 이름을 연속해서 작성하면 해당 영역이 여러 칸을 차지한다.

```text
┌──────────────────────────────────────┐
│                header                │
├──────────────────────────────────────┤
│                 nav                  │
├───────────┬──────────┬───────────────┤
│  sidebar  │ divider  │     main      │
├───────────┴──────────┴───────────────┤
│                footer                │
└──────────────────────────────────────┘
```

### 3.5 `grid-area`

Grid 아이템에 `grid-template-areas`에서 정의한 영역 이름을 연결한다.

```css
header {
    grid-area: header;
}

nav {
    grid-area: nav;
}

aside {
    grid-area: sidebar;
}

main {
    grid-area: main;
}

footer {
    grid-area: footer;
}

.divider {
    grid-area: divider;
}
```

### 3.6 `gap`

행과 열 사이의 간격을 지정한다.

```css
.app {
    gap: 16px;
}
```

행과 열의 간격을 각각 지정할 수도 있다.

```css
.app {
    row-gap: 20px;
    column-gap: 20px;
}
```

### 3.7 `justify-items`

각 Grid 셀 안에서 아이템을 가로 방향으로 정렬한다.

```css
.app {
    justify-items: center;
}
```

| 값 | 정렬 방식 |
| --- | --- |
| `start` | 셀의 왼쪽에 배치한다 |
| `center` | 셀의 가로 가운데에 배치한다 |
| `end` | 셀의 오른쪽에 배치한다 |
| `stretch` | 셀의 가로 영역을 채우도록 늘린다 |

### 3.8 `align-items`

각 Grid 셀 안에서 아이템을 세로 방향으로 정렬한다.

```css
.app {
    align-items: stretch;
}
```

### 3.9 `place-items`

`align-items`와 `justify-items`를 한 번에 지정한다.

```css
.app {
    place-items: center;
}
```

```text
place-items = align-items + justify-items
```

### 3.10 `grid-column`

Grid 아이템이 가로 방향으로 차지할 영역을 라인 번호로 지정한다.

```css
.item {
    grid-column: 1 / 3;
}
```

1번 라인에서 시작해 3번 라인 직전까지 차지하므로 두 개의 열을 사용한다.

### 3.11 `grid-row`

Grid 아이템이 세로 방향으로 차지할 영역을 라인 번호로 지정한다.

```css
.item {
    grid-row: 1 / 3;
}
```

### 3.12 `justify-self`

특정 Grid 아이템 하나를 셀 안에서 가로 방향으로 정렬한다.

```css
.profile {
    justify-self: start;
}
```

### 3.13 `align-self`

특정 Grid 아이템 하나를 셀 안에서 세로 방향으로 정렬한다.

```css
.item {
    align-self: center;
}
```

### 3.14 `place-self`

`align-self`와 `justify-self`를 한 번에 지정한다.

```css
.item {
    place-self: center;
}
```

```text
place-self = align-self + justify-self
```

### 3.15 `fr`

`fr`은 Grid 컨테이너의 남는 공간을 비율로 나누는 단위다.

```css
.container {
    grid-template-columns: 1fr 2fr;
}
```

남는 공간을 `1 : 2`의 비율로 나눈다.

### 3.16 `repeat()`

같은 크기의 행이나 열을 반복해서 정의한다.

```css
.container {
    grid-template-columns: repeat(3, 1fr);
}
```

위 코드는 다음 코드와 같은 의미다.

```css
.container {
    grid-template-columns: 1fr 1fr 1fr;
}
```

### 3.17 `minmax()`

행이나 열의 최소 크기와 최대 크기를 지정한다.

```css
.container {
    grid-template-columns: minmax(200px, 1fr);
}
```

열의 크기는 최소 `200px`을 유지하고 남는 공간이 있으면 `1fr`까지 늘어난다.

### 3.18 `auto-fit`과 `auto-fill`

`repeat()`와 함께 사용해 컨테이너의 크기에 따라 열의 개수를 자동으로 만든다.

```css
.container {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}
```

| 값 | 의미 |
| --- | --- |
| `auto-fit` | 남는 빈 칸을 접고 아이템이 남는 공간까지 늘어나게 한다 |
| `auto-fill` | 들어갈 수 있는 만큼 열을 만들어 빈 칸도 유지한다 |

### 3.19 Grid 레이아웃 예제

```html
<div class="app">
    <header>
        헤더(header)
    </header>

    <nav>
        네비게이션(nav)
    </nav>

    <aside>
        <div class="profile">
            프로필 영역<br>
            김사과<br>
            관리자
        </div>

        <p style="margin-top: 12px;">
            사이드 메뉴<br>
            - 대시보드<br>
            - 사용자 관리<br>
            - 로그
        </p>
    </aside>

    <div class="divider"></div>

    <main>
        <h2>메인 콘텐츠</h2>
        <p style="margin-top: 10px;">
            Gridbox를 사용해 고정값(px) 기반으로 구성한<br>
            3단 레이아웃입니다.
        </p>
    </main>

    <footer>
        푸터(footer)
    </footer>
</div>
```

```css
.app {
    width: 1100px;
    margin: 20px auto;
    display: grid;

    grid-template-columns: 240px 20px 820px;
    grid-template-rows: 80px 60px 500px 60px;
    gap: 16px;

    grid-template-areas:
        "header header header"
        "nav    nav    nav"
        "sidebar divider main"
        "footer footer footer";

    justify-content: center;
    align-items: stretch;
}

header,
nav,
aside,
main,
footer,
.divider {
    border: 2px solid #000;
    padding: 16px;
}

header {
    grid-area: header;
}

nav {
    grid-area: nav;
}

aside {
    grid-area: sidebar;
}

main {
    grid-area: main;
}

footer {
    grid-area: footer;
}

.divider {
    grid-area: divider;
    padding: 0;
}

.profile {
    width: 180px;
    padding: 10px;
    border: 1px solid #000;
    justify-self: start;
    align-items: start;
}
```

---

## 4. Flexbox와 Grid 비교

| 구분 | Flexbox | Grid |
| --- | --- | --- |
| 배치 기준 | 한 방향 | 행과 열 |
| 주요 구조 | 주축과 교차축 | 행과 열로 이루어진 셀 |
| 컨테이너 선언 | `display: flex` | `display: grid` |
| 간격 | `gap` | `gap`, `row-gap`, `column-gap` |
| 전체 아이템 정렬 | `justify-content`, `align-items` | `justify-items`, `align-items` |
| 개별 아이템 정렬 | `align-self` | `justify-self`, `align-self`, `place-self` |

Flexbox는 가로 또는 세로 중 한 방향을 중심으로 배치하고, Grid는 행과 열을 함께 이용해 배치한다.

---

## 5. 반응형

반응형은 화면의 크기, 해상도, 방향에 따라 레이아웃과 요소의 스타일이 자동으로 달라지도록 구성하는 방식이다.

모바일, 태블릿, 데스크톱처럼 서로 다른 화면 크기에서 적절한 화면을 제공할 때 사용한다.

### 5.1 미디어 쿼리

미디어 쿼리는 화면의 너비, 높이, 해상도, 기기 방향 등의 조건에 따라 다른 CSS를 적용하는 기능이다.

```css
@media (조건) {
    /* 조건을 만족할 때 적용할 CSS */
}
```

### 5.2 브레이크 포인트

브레이크 포인트는 화면 크기에 따라 레이아웃이나 스타일이 바뀌는 기준점이다.

| 화면 크기 | 구분 |
| --- | --- |
| `480px` 이하 | 모바일 |
| `768px` 이하 | 태블릿 |
| `1024px` 이상 | 데스크톱 |
| `1200px` 이상 | 와이드 데스크톱 |

### 5.3 `max-width`

지정한 너비 이하에서 스타일을 적용한다.

```css
@media (max-width: 768px) {
    .box {
        font-size: 14px;
    }
}
```

화면 너비가 `768px` 이하일 때 적용된다.

### 5.4 `min-width`

지정한 너비 이상에서 스타일을 적용한다.

```css
@media (min-width: 1024px) {
    .box {
        font-size: 20px;
    }
}
```

화면 너비가 `1024px` 이상일 때 적용된다.

### 5.5 여러 조건 연결

`and`를 사용하면 여러 조건을 모두 만족할 때만 스타일을 적용할 수 있다.

```css
@media (min-width: 768px) and (max-width: 1023px) {
    .box {
        font-size: 16px;
    }
}
```

화면 너비가 `768px` 이상이고 `1023px` 이하일 때 적용된다.

쉼표로 조건을 구분하면 여러 조건 중 하나를 만족할 때 적용할 수 있다.

```css
@media (max-width: 480px), (min-width: 1200px) {
    .box {
        font-weight: bold;
    }
}
```

화면 너비가 `480px` 이하이거나 `1200px` 이상일 때 적용된다.

### 5.6 반응형 예제

```html
<div class="box">
    화면 크기에 따라 색과 글자 크기가 달라집니다.
</div>
```

```css
body {
    margin: 0;
}

.box {
    padding: 40px;
    text-align: center;
    font-size: 20px;
    background-color: deepskyblue;
}

@media (max-width: 1024px) {
    .box {
        background-color: deeppink;
        font-size: 16px;
    }
}

@media (max-width: 767px) {
    .box {
        background-color: gold;
        font-size: 14px;
    }
}
```

| 화면 너비 | 배경색 | 글자 크기 |
| --- | --- | --- |
| `1024px` 초과 | `deepskyblue` | `20px` |
| `768px`부터 `1024px` | `deeppink` | `16px` |
| `767px` 이하 | `gold` | `14px` |

화면이 `767px` 이하라면 두 미디어 쿼리의 조건을 모두 만족한다. 뒤에 작성된 `767px` 이하의 스타일이 최종적으로 적용된다.

---

## 6. CSS 변수

CSS 변수는 자주 사용하는 스타일 값을 이름으로 정의한 뒤 필요한 위치에서 재사용하는 기능이다.

변수 이름은 `--변수이름` 형태로 선언하고 `var()` 함수로 불러온다.

### 6.1 변수 선언

```css
:root {
    --main-color: #3498db;
    --sub-color: #2ecc71;
    --base-padding: 20px;
    --title-size: 24px;
}
```

`:root`에 선언한 변수는 문서 전체에서 사용할 수 있다.

### 6.2 변수 사용

```css
.box {
    border: 2px solid var(--main-color);
    padding: var(--base-padding);
}

h1 {
    font-size: var(--title-size);
    color: var(--main-color);
}

p {
    color: var(--sub-color);
}
```

```text
변수 선언: --main-color: #3498db;
변수 사용: var(--main-color)
```

### 6.3 기본값 지정

변수가 정의되지 않았을 때 사용할 기본값을 지정할 수 있다.

```css
p {
    color: var(--sub-color, black);
}
```

`--sub-color` 변수가 존재하지 않으면 `black`이 적용된다.

### 6.4 범위별 변수

특정 선택자 안에서 변수를 선언하면 해당 요소와 그 하위 요소에서 사용할 수 있다.

```css
.card {
    --card-padding: 12px;
    padding: var(--card-padding);
}
```

### 6.5 CSS 변수 예제

```html
<div class="box">
    <h1>CSS 변수 예제</h1>
    <p>
        이 예제는 CSS 변수를 사용해 색상과 여백을 관리합니다.
    </p>
</div>
```

```css
:root {
    --main-color: #3498db;
    --sub-color: #2ecc71;
    --base-padding: 20px;
    --title-size: 24px;
}

body {
    font-family: "OngleipParkDahyeon";
    margin: 40px;
}

.box {
    border: 2px solid var(--main-color);
    padding: var(--base-padding);
    margin-bottom: 20px;
}

h1 {
    font-size: var(--title-size);
    color: var(--main-color);
}

p {
    color: var(--sub-color);
}
```

---

## 7. CSS 우선순위

하나의 요소에 여러 CSS 규칙이 적용되면 우선순위에 따라 최종 스타일이 결정된다.

예제에서는 태그 선택자, 클래스 선택자, 아이디 선택자, 인라인 스타일, `!important`의 우선순위를 확인한다.

```css
p {
    color: blue;
}

.text {
    color: green;
}

#target {
    color: red;
}

.text {
    color: purple;
}

.force {
    color: orange !important;
}
```

### 7.1 아이디 선택자

```html
<p id="target" class="text">
    1번: 빨강(id 우선)
</p>
```

`p`, `.text`, `#target`의 스타일이 모두 적용될 수 있지만 아이디 선택자인 `#target`의 우선순위가 더 높으므로 빨간색이 적용된다.

### 7.2 `!important`

```html
<p id="target" class="text force">
    2번: 주황(important 우선)
</p>
```

`.force`에 `!important`가 지정되어 있으므로 주황색이 적용된다.

### 7.3 인라인 스타일과 `!important`

```html
<p
    id="target"
    class="text force"
    style="color: black;"
>
    3번: 주황(important 우선)
</p>
```

인라인 스타일로 검은색을 지정했지만 `.force`의 `!important`가 우선되어 주황색이 적용된다.

### 7.4 인라인 스타일

```html
<p
    id="target"
    class="text"
    style="color: black;"
>
    4번: 검정(인라인 우선)
</p>
```

`!important`가 없으므로 인라인 스타일의 검은색이 적용된다.

### 7.5 같은 선택자의 우선순위

```css
.text {
    color: green;
}

.text {
    color: purple;
}
```

선택자의 우선순위가 같으면 뒤에 작성된 스타일이 적용된다. 따라서 `.text`에는 보라색이 적용된다.

### 7.6 우선순위 정리

```text
!important
    ↓
인라인 스타일
    ↓
아이디 선택자
    ↓
클래스 선택자
    ↓
태그 선택자
```

같은 우선순위를 가진 규칙끼리는 나중에 작성된 규칙이 적용된다.

---

## 8. `transition`

`transition`은 요소의 상태가 변경될 때 스타일이 즉시 바뀌지 않고 일정 시간 동안 부드럽게 변화하도록 만든다.

마우스를 올리는 `:hover`나 클래스 변경 등으로 CSS 속성값이 달라질 때 사용할 수 있다.

```css
선택자 {
    transition: 속성 시간;
}
```

### 8.1 `transition-property`

변화를 적용할 CSS 속성을 지정한다.

```css
.box {
    transition-property: width, background-color;
}
```

### 8.2 `transition-duration`

변화가 진행되는 시간을 지정한다.

```css
.box {
    transition-duration: 0.5s;
}
```

### 8.3 `transition-timing-function`

변화 속도의 흐름을 지정한다.

```css
.box {
    transition-timing-function: ease;
}
```

| 값 | 특징 |
| --- | --- |
| `ease` | 시작과 끝은 느리고 중간은 빠르다 |
| `linear` | 처음부터 끝까지 같은 속도로 진행한다 |
| `ease-in` | 느리게 시작하고 점점 빨라진다 |
| `ease-out` | 빠르게 시작하고 끝으로 갈수록 느려진다 |
| `ease-in-out` | 시작과 끝은 느리고 중간은 빠르다 |

### 8.4 `transition-delay`

변화가 시작되기 전의 대기 시간을 지정한다.

```css
.box {
    transition-delay: 0.2s;
}
```

### 8.5 축약 속성

```css
.box {
    transition: background-color 0.8s ease 0s;
}
```

```text
transition: 속성 시간 타이밍 지연시간
```

### 8.6 단일 전환

```css
.box {
    width: 200px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    cursor: pointer;
}

.single {
    background-color: deepskyblue;
    transition: background-color 0.8s ease;
}

.single:hover {
    background-color: blue;
}
```

```html
<h2>단일 transition</h2>
<div class="box single">hover 해보세요</div>
```

마우스를 올리면 배경색이 `0.8초` 동안 부드럽게 변경된다.

### 8.7 여러 속성 전환

여러 속성에 각각 전환 효과를 지정할 때 쉼표로 구분한다.

```css
.multiple {
    background-color: deeppink;
    transition:
        background-color 0.4s ease,
        transform 0.4s ease,
        box-shadow 0.4s ease;
}

.multiple:hover {
    background-color: pink;
    transform: translateY(-20px) scale(1.1);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
}
```

```html
<h2>여러 transition</h2>
<div class="box multiple">hover 해보세요</div>
```

마우스를 올리면 배경색, 위치와 크기, 그림자가 함께 부드럽게 변경된다.

---

## 9. `transform`

`transform`은 요소의 위치나 형태를 시각적으로 변경하는 속성이다.

요소를 이동하거나, 크기를 바꾸거나, 회전하거나, 기울일 수 있다.

```css
선택자 {
    transform: 변형함수(값);
}
```

`transform`은 문서의 실제 레이아웃 흐름을 변경하지 않고 화면에 보이는 형태만 바꾼다.

### 9.1 `translate`

요소의 위치를 이동한다.

```css
.translate:hover {
    transform: translate(-20px);
}
```

마우스를 올리면 요소가 가로 방향으로 `-20px` 이동한다.

### 9.2 `scale`

요소의 크기를 변경한다.

```css
.scale:hover {
    transform: scale(1.2);
}
```

`1`이 원래 크기이며 `1.2`는 원래 크기의 `1.2배`를 의미한다.

### 9.3 `rotate`

요소를 회전한다.

```css
.rotate:hover {
    transform: rotate(15deg);
}
```

`deg`는 회전 각도를 나타낸다.

### 9.4 `skew`

요소를 기울인다.

```css
.skew:hover {
    transform: skew(10deg, 5deg);
}
```

첫 번째 값은 가로 방향, 두 번째 값은 세로 방향의 기울기다.

### 9.5 여러 변형 함께 사용

여러 변형 함수를 공백으로 이어서 작성할 수 있다.

```css
.box:hover {
    transform: translateY(-20px) scale(1.1);
}
```

요소를 위로 `20px` 이동하면서 크기를 `1.1배`로 확대한다.

### 9.6 변형 함수 예제

```html
<h2>transform 변형 함수</h2>

<div class="container">
    <div class="box translate">translate</div>
    <div class="box scale">scale</div>
    <div class="box rotate">rotate</div>
    <div class="box skew">skew</div>
</div>
```

```css
.container {
    display: flex;
    gap: 30px;
}

.box {
    width: 150px;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: deepskyblue;
    color: white;
    cursor: pointer;
    transition: transform 0.4s ease;
}

.translate:hover {
    transform: translate(-20px);
}

.scale:hover {
    transform: scale(1.2);
}

.rotate:hover {
    transform: rotate(15deg);
}

.skew:hover {
    transform: skew(10deg, 5deg);
}
```

---

## 10. `animation`

`animation`은 `@keyframes`로 여러 단계의 스타일 변화를 정의하고 시간의 흐름에 따라 자동으로 재생하는 기능이다.

`transition`과 달리 마우스 오버 같은 상태 변화가 없어도 애니메이션을 실행할 수 있다.

### 10.1 `@keyframes`

애니메이션의 시작부터 종료까지 각 단계에서 적용할 스타일을 정의한다.

```css
@keyframes 애니메이션이름 {
    0% {
        /* 시작 스타일 */
    }

    100% {
        /* 종료 스타일 */
    }
}
```

`0%`와 `100%` 대신 `from`, `to`를 사용할 수도 있다.

```css
@keyframes fade {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}
```

여러 중간 단계를 지정할 수도 있다.

```css
@keyframes bounce {
    0% {
        transform: translateY(0);
    }

    25% {
        transform: translateY(-50px);
    }

    50% {
        transform: translateY(-10px);
    }

    75% {
        transform: translateY(20px);
    }

    100% {
        transform: translateY(0);
    }
}
```

### 10.2 `animation-name`

적용할 `@keyframes`의 이름을 지정한다.

```css
.box {
    animation-name: fade;
}
```

### 10.3 `animation-duration`

애니메이션이 한 번 실행되는 시간을 지정한다.

```css
.box {
    animation-duration: 2s;
}
```

### 10.4 `animation-timing-function`

애니메이션 속도의 변화 방식을 지정한다.

```css
.box {
    animation-timing-function: ease-in-out;
}
```

### 10.5 `animation-delay`

애니메이션이 시작되기 전의 대기 시간을 지정한다.

```css
.box {
    animation-delay: 1s;
}
```

### 10.6 `animation-iteration-count`

애니메이션의 반복 횟수를 지정한다.

```css
.box {
    animation-iteration-count: 3;
}
```

무한히 반복하려면 `infinite`를 사용한다.

```css
.box {
    animation-iteration-count: infinite;
}
```

### 10.7 `animation-direction`

애니메이션의 재생 방향을 지정한다.

```css
.box {
    animation-direction: alternate;
}
```

| 값 | 재생 방향 |
| --- | --- |
| `normal` | 처음부터 끝까지 재생한다 |
| `reverse` | 끝에서 처음 방향으로 재생한다 |
| `alternate` | 정방향과 역방향을 번갈아 재생한다 |

### 10.8 `animation-fill-mode`

애니메이션이 시작되기 전이나 끝난 후 적용할 스타일을 지정한다.

```css
.box {
    animation-fill-mode: forwards;
}
```

`forwards`는 애니메이션이 끝난 뒤 마지막 단계의 스타일을 유지한다.

### 10.9 `animation-play-state`

애니메이션의 재생 상태를 지정한다.

```css
.box {
    animation-play-state: paused;
}
```

| 값 | 의미 |
| --- | --- |
| `running` | 애니메이션을 재생한다 |
| `paused` | 애니메이션을 일시 정지한다 |

### 10.10 축약 속성

```css
.box {
    animation: fade 2s ease 0s infinite normal none;
}
```

```text
animation:
이름 실행시간 속도방식 지연시간 반복횟수 재생방향 채움방식
```

---

## 11. 토스트 애니메이션

토스트 메시지가 아래에서 위로 이동하면서 나타나는 효과다.

```css
@keyframes toastIn {
    0% {
        transform: translateY(20px);
        opacity: 0;
    }

    100% {
        transform: translateY(0);
        opacity: 1;
    }
}

.toast {
    width: 360px;
    padding: 16px;
    margin-bottom: 30px;
    border: 2px solid #000;

    animation-name: toastIn;
    animation-duration: 0.6s;
    animation-timing-function: ease-out;
    animation-delay: 0.2s;
    animation-fill-mode: forwards;

    opacity: 0;
}
```

```html
<h2>토스트(알림) 등장</h2>

<div class="toast">
    저장되었습니다! (0.2초 후 부드럽게 등장)
</div>
```

처음에는 `opacity: 0`으로 보이지 않으며 `0.2초` 후에 위로 이동하면서 나타난다.

`animation-fill-mode: forwards`가 적용되어 종료 상태인 `opacity: 1`을 유지한다.

---

## 12. 로딩 스피너

원의 한쪽 테두리를 투명하게 만들고 계속 회전시켜 로딩 스피너를 만든다.

```css
@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.spinner {
    width: 46px;
    height: 46px;
    margin-bottom: 30px;
    border: 6px solid #000;
    border-top-color: transparent;
    border-radius: 50%;

    animation: spin 1s linear 0s infinite normal none;
}
```

```html
<h2>로딩 스피너</h2>
<div class="spinner"></div>
```

| 속성 | 적용 값 |
| --- | --- |
| 애니메이션 이름 | `spin` |
| 실행 시간 | `1s` |
| 속도 방식 | `linear` |
| 반복 횟수 | `infinite` |
| 회전 범위 | `0deg`부터 `360deg` |

---

## 13. 펄스 애니메이션

요소의 크기와 투명도를 반복해서 변경해 강조 효과를 만든다.

```css
@keyframes pulse {
    0% {
        transform: scale(1);
        opacity: 0.8;
    }

    100% {
        transform: scale(1.1);
        opacity: 1;
    }
}

.badge {
    display: inline-block;
    padding: 8px 12px;
    margin-bottom: 30px;
    border: 2px solid #000;

    animation: pulse 0.7s ease-in-out 0s infinite alternate none;
}

.badge:hover {
    animation-play-state: paused;
}
```

```html
<h3>강조 배지(펄스)</h3>

<div class="badge">HOT</div>

<div class="pause-hint">
    배지에 마우스를 올리면 애니메이션이 멈춥니다.
</div>
```

`alternate`가 적용되어 확대와 축소를 번갈아 반복한다.

마우스를 올리면 `animation-play-state: paused`가 적용되어 애니메이션이 멈춘다.

---

## 14. `transition`과 `animation` 비교

| 구분 | `transition` | `animation` |
| --- | --- | --- |
| 실행 조건 | 속성값의 상태 변화가 필요하다 | 상태 변화 없이 자동 실행할 수 있다 |
| 변화 단계 | 시작과 종료 상태를 연결한다 | `@keyframes`로 여러 단계를 만든다 |
| 반복 | 기본적으로 한 번의 변화를 처리한다 | 반복 횟수를 지정할 수 있다 |
| 주요 속성 | `transition-property`, `duration` | `animation-name`, `duration`, `iteration-count` |

`transition`은 `:hover`처럼 상태가 바뀔 때 부드러운 변화를 만들고, `animation`은 정의된 단계에 따라 자동으로 움직이는 효과를 만든다.

---

## 15. 핵심 정리

1. `float`를 사용하면 여러 요소를 가로로 배치할 수 있으며 `clear`로 영향을 해제한다.
2. Flexbox는 요소를 한 방향으로 유연하게 배치하는 레이아웃 방식이다.
3. Flex 컨테이너는 `display: flex`로 만들고 아이템의 방향과 정렬을 제어한다.
4. `flex`는 `flex-grow`, `flex-shrink`, `flex-basis`의 축약 속성이다.
5. Grid는 행과 열을 기준으로 요소를 배치하는 2차원 레이아웃 방식이다.
6. `grid-template-columns`와 `grid-template-rows`로 열과 행의 크기를 설정한다.
7. `grid-template-areas`와 `grid-area`를 사용하면 이름으로 영역을 배치할 수 있다.
8. `fr`, `repeat()`, `minmax()`, `auto-fit`, `auto-fill`을 이용해 Grid 크기를 구성한다.
9. 미디어 쿼리는 화면 조건에 따라 다른 CSS를 적용한다.
10. `max-width`는 지정한 너비 이하, `min-width`는 지정한 너비 이상에서 적용된다.
11. CSS 변수는 `--변수이름`으로 선언하고 `var()` 함수로 사용한다.
12. CSS 규칙이 충돌하면 선택자의 우선순위와 작성 순서에 따라 스타일이 결정된다.
13. `!important`는 일반 선언과 인라인 스타일보다 우선 적용된다.
14. `transition`은 속성값이 변할 때 일정 시간 동안 부드럽게 변화시킨다.
15. `transform`은 요소를 이동, 확대·축소, 회전, 기울이기 할 수 있다.
16. `animation`은 `@keyframes`로 여러 단계의 변화를 정의해 자동으로 재생한다.
17. `animation-play-state: paused`를 사용하면 실행 중인 애니메이션을 멈출 수 있다.

