# [16일차] HTML 표와 CSS 레이아웃 정리

HTML의 표와 시맨틱 구조를 살펴보고, CSS의 박스 모델과 `float`, 텍스트 스타일, `position`을 이용해 요소를 배치하는 방법을 정리한다.

| 구분 | 주요 내용 |
| --- | --- |
| HTML | 표, `div`, `span`, 시맨틱 태그 |
| CSS | 박스 모델, `float`, 텍스트 스타일, `position` |

---

## 1. 표

`table`은 행과 열로 이루어진 표를 만드는 태그다.

표 안에서 `tr`은 하나의 행을 만들고, `td`는 일반 데이터가 들어가는 셀을 만든다.

```html
<table>
    <tr>
        <td>1</td>
        <td>2</td>
    </tr>
    <tr>
        <td>3</td>
        <td>4</td>
    </tr>
</table>
```

| 태그 | 역할 |
| --- | --- |
| `table` | 표 전체를 감싼다 |
| `tr` | 표의 행을 만든다 |
| `th` | 제목 역할을 하는 셀을 만든다 |
| `td` | 일반 데이터가 들어가는 셀을 만든다 |
| `thead` | 표의 제목 영역을 묶는다 |
| `tbody` | 표의 본문 영역을 묶는다 |

### 1.1 열 병합

`colspan`은 하나의 셀이 여러 열을 차지하도록 만든다.

```html
<table border="1" width="50%">
    <tr>
        <td colspan="2">1</td>
    </tr>
    <tr>
        <td>3</td>
        <td>4</td>
    </tr>
</table>
```

`colspan="2"`가 적용된 셀은 두 개의 열을 합친다.

```text
┌───────────────┐
│       1       │
├───────┬───────┤
│   3   │   4   │
└───────┴───────┘
```

### 1.2 행 병합

`rowspan`은 하나의 셀이 여러 행을 차지하도록 만든다.

```html
<table border="1" width="50%">
    <tr>
        <td rowspan="2">5</td>
        <td>6</td>
    </tr>
    <tr>
        <td>8</td>
    </tr>
</table>
```

`rowspan="2"`가 적용된 셀은 두 개의 행을 합친다.

```text
┌───────┬───────┐
│       │   6   │
│   5   ├───────┤
│       │   8   │
└───────┴───────┘
```

### 1.3 표 영역 구분

`thead`는 표의 제목 영역, `tbody`는 실제 데이터가 들어가는 영역이다.

```html
<table>
    <thead>
        <tr>
            <th>이름</th>
            <th>과목</th>
            <th>점수</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="2">김사과</td>
            <td>HTML</td>
            <td>95</td>
        </tr>
        <tr>
            <td>CSS</td>
            <td>92</td>
        </tr>
        <tr>
            <td>반하나</td>
            <td>JavaScript</td>
            <td>88</td>
        </tr>
    </tbody>
</table>
```

`th`는 제목을 나타내는 셀이며 기본적으로 굵은 글씨와 가운데 정렬이 적용된다.

### 1.4 표 스타일

표의 너비, 색상, 테두리와 같은 표현은 CSS를 통해 적용할 수 있다.

```css
table {
    width: 600px;
    border-collapse: collapse;
}

thead {
    background-color: deepskyblue;
    color: white;
}

tbody td {
    padding: 12px;
    border-bottom: 1px solid #ddd;
}

tbody tr:hover {
    background-color: pink;
}
```

`border-collapse: collapse`는 표의 셀 사이에 있는 테두리를 하나로 합친다.

`tbody tr:hover`는 마우스를 올린 행의 배경색을 변경한다.

---

## 2. `div`와 `span`

`div`와 `span`은 특별한 의미 없이 다른 요소나 텍스트를 하나의 영역으로 묶을 때 사용한다.

### 2.1 `div`

`div`는 여러 요소를 하나의 그룹으로 묶거나 페이지의 구조를 나눌 때 사용하는 블록 컨테이너다.

```html
<div>
    이것은 div 태그입니다.
    하나의 블록 영역을 차지합니다.
</div>
```

```css
div {
    width: 500px;
    background-color: gold;
}
```

`div`는 블록 요소이므로 기본적으로 한 줄 전체 영역을 차지하고 다음 요소는 새로운 줄에서 시작한다.

### 2.2 `span`

`span`은 문장이나 텍스트의 일부를 묶을 때 사용하는 인라인 컨테이너다.

```html
<div>
    이것은 div 태그입니다.
    이 문장 안에서
    <span>이 부분만 span 태그</span>로 감쌌습니다.
</div>
```

```css
span {
    font-weight: bold;
    color: red;
}
```

`span`은 인라인 요소이므로 감싼 내용의 크기만큼만 영역을 차지한다.

### 2.3 `div`와 `span` 비교

| 구분 | `div` | `span` |
| --- | --- | --- |
| 형태 | 블록 요소 | 인라인 요소 |
| 차지하는 영역 | 한 줄 전체 | 내용의 크기 |
| 용도 | 영역과 요소 묶기 | 텍스트의 일부 묶기 |
| 자체적인 의미 | 없음 | 없음 |

---

## 3. 시맨틱 구조

시맨틱 태그는 HTML 요소의 겉모양이 아니라 해당 영역의 의미와 역할을 나타내는 태그다.

각 영역의 목적을 명확하게 표현해 브라우저, 검색 엔진, 접근성 도구가 문서의 구조를 이해할 수 있도록 돕는다.

| 태그 | 역할 |
| --- | --- |
| `header` | 페이지의 머리글, 제목, 로고 영역 |
| `nav` | 메뉴와 링크 목록 영역 |
| `main` | 페이지의 핵심 내용 |
| `section` | 주제별로 나눈 콘텐츠 영역 |
| `article` | 게시글처럼 독립적으로 의미를 가지는 콘텐츠 |
| `aside` | 본문과 간접적으로 관련된 부가 콘텐츠 |
| `footer` | 저작권, 작성자 정보와 같은 하단 영역 |

### 3.1 시맨틱 구조 예제

```html
<header>
    <h1>나의 웹사이트</h1>
    <p>사이트 제목/소개 영역</p>
</header>

<nav>
    <p>메뉴 영역</p>
    <a href="#">홈</a>
    <a href="#">소개</a>
    <a href="#">연락</a>
</nav>

<main>
    <section>
        <h2>주제별 구역</h2>
        <p>이 섹션은 하나의 주제를 묶는 영역입니다.</p>
    </section>

    <article>
        <h2>독립 콘텐츠</h2>
        <p>게시글/뉴스처럼 단독으로 의미가 있는 콘텐츠입니다.</p>
    </article>

    <aside>
        <h3>부가 정보</h3>
        <p>본문과 간접적으로 관련된 사이드 내용입니다.</p>
    </aside>

    <footer>
        <p>하단 정보(저작권, 연락처 등)</p>
    </footer>
</main>
```

```text
┌──────────────────────────────┐
│            header            │
├──────────────────────────────┤
│              nav             │
├──────────────────────────────┤
│             main             │
│  ┌────────────────────────┐  │
│  │        section         │  │
│  ├────────────────────────┤  │
│  │        article         │  │
│  ├────────────────────────┤  │
│  │         aside          │  │
│  ├────────────────────────┤  │
│  │         footer         │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

### 3.2 시맨틱 영역 스타일

여러 시맨틱 요소에 같은 스타일을 적용할 때 그룹 선택자를 사용할 수 있다.

```css
header,
nav,
section,
article,
aside,
footer {
    border: 1px solid #cccccc;
    padding: 20px;
    margin-bottom: 15px;
}

header {
    background-color: deepskyblue;
    color: white;
    text-align: center;
}
```

---

## 4. 박스 모델

박스 모델은 HTML 요소 하나하나를 사각형 상자로 보고 크기와 여백을 계산하는 개념이다.

하나의 요소는 `content`, `padding`, `border`, `margin`으로 구성된다.

```text
┌──────────────────────── margin ────────────────────────┐
│  ┌───────────────────── border ─────────────────────┐  │
│  │  ┌────────────────── padding ─────────────────┐  │  │
│  │  │                  content                  │  │  │
│  │  └───────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────┘
```

| 영역 | 역할 |
| --- | --- |
| `content` | 텍스트나 이미지가 들어가는 실제 내용 영역 |
| `padding` | 내용과 테두리 사이의 안쪽 여백 |
| `border` | 요소의 테두리 |
| `margin` | 요소와 다른 요소 사이의 바깥쪽 여백 |

### 4.1 `padding`

`padding`은 콘텐츠와 테두리 사이의 안쪽 여백이다.

```css
h1 {
    padding: 20px;
}
```

값의 개수에 따라 적용되는 방향이 달라진다.

```css
/* 상하좌우 */
padding: 20px;

/* 상하, 좌우 */
padding: 10px 20px;

/* 상, 좌우, 하 */
padding: 10px 20px 30px;

/* 상, 우, 하, 좌 */
padding: 10px 20px 30px 40px;
```

네 개의 값을 작성하면 위쪽부터 시계 방향으로 적용된다.

```text
상 → 우 → 하 → 좌
```

### 4.2 `border`

`border`는 `padding`과 `margin` 사이에 있는 요소의 테두리다.

```css
.box {
    border-width: 3px;
    border-style: dotted;
    border-color: #ccc;
}
```

세 가지 속성을 `border` 축약 속성으로 한 번에 지정할 수 있다.

```css
.box {
    border: 3px dotted #ccc;
}
```

| 속성 | 역할 |
| --- | --- |
| `border-width` | 테두리 두께 |
| `border-style` | `solid`, `dashed`, `dotted` 등의 테두리 모양 |
| `border-color` | 테두리 색상 |
| `border-radius` | 테두리의 모서리를 둥글게 만든다 |

### 4.3 `margin`

`margin`은 요소의 바깥쪽 여백으로 다른 요소와의 간격을 조절한다.

```css
h1 {
    margin: 20px;
}
```

값이 적용되는 방향은 `padding`과 같다.

```css
/* 상하좌우 */
margin: 20px;

/* 상하, 좌우 */
margin: 10px 20px;

/* 상, 좌우, 하 */
margin: 10px 20px 30px;

/* 상, 우, 하, 좌 */
margin: 10px 20px 30px 40px;
```

고정된 너비를 가진 블록 요소를 가로 가운데로 정렬할 때 다음과 같이 작성한다.

```css
.container {
    width: 900px;
    margin: 0 auto;
}
```

### 4.4 마진 병합

위아래로 배치된 블록 요소의 세로 마진은 상황에 따라 하나로 합쳐질 수 있다.

```css
.box1 {
    margin-bottom: 50px;
}

.box2 {
    margin-top: 30px;
}
```

두 요소의 마진이 병합되면 두 값을 더하지 않고 더 큰 값이 요소 사이의 간격으로 적용된다.

```text
50px + 30px = 80px (X)
큰 값인 50px 적용 (O)
```

### 4.5 `box-sizing`

`box-sizing`은 요소의 너비와 높이를 어떤 영역까지 포함해 계산할지 결정한다.

| 값 | 크기 계산 방식 |
| --- | --- |
| `content-box` | `width`와 `height`에 콘텐츠 영역만 포함한다 |
| `border-box` | `width`와 `height`에 `padding`과 `border`까지 포함한다 |

```css
.box1 {
    box-sizing: border-box;
    width: 300px;
    padding: 20px;
    border: 1px solid #ccc;
}
```

`border-box`를 사용하면 `padding`과 `border`를 포함한 전체 너비가 `300px`이 된다.

```css
.box2 {
    width: 300px;
    padding: 20px;
    border: 3px dotted #ccc;
}
```

별도로 `box-sizing`을 지정하지 않으면 기본값인 `content-box`가 적용된다. 이 경우 `width`에 `padding`과 `border`가 더해진다.

### 4.6 박스 모델 예제

```css
.box1 {
    box-sizing: border-box;
    background-color: skyblue;
    padding: 20px;
    margin-bottom: 50px;
    border: 1px solid #ccc;
    width: 300px;
}

.box2 {
    background-color: deeppink;
    padding: 20px;
    margin-top: 30px;
    border: 3px dotted #ccc;
    width: 300px;
}
```

```html
<div class="box1">
    box1
</div>

<div class="box2">
    box2
</div>
```

---

## 5. `float`

`float`는 요소를 문서의 일반적인 흐름에서 왼쪽이나 오른쪽으로 띄우는 속성이다.

주로 이미지 옆에 텍스트를 배치하거나 여러 영역을 가로로 배치할 때 사용한다.

```html
<img src="./spring1.png" alt="봄">

Lorem ipsum dolor sit amet consectetur adipisicing elit.
Alias saepe reiciendis sit obcaecati quae nemo sunt.
```

```css
img {
    float: left;
}
```

이미지가 왼쪽으로 이동하고 뒤에 있는 텍스트는 이미지의 오른쪽 영역에 배치된다.

| 값 | 역할 |
| --- | --- |
| `left` | 요소를 왼쪽으로 띄운다 |
| `right` | 요소를 오른쪽으로 띄운다 |
| `none` | 요소를 띄우지 않는다 |

### 5.1 `clear`

`clear`는 앞에서 `float`가 적용된 요소의 영향을 해제한다.

```css
.clear {
    clear: both;
}
```

| 값 | 역할 |
| --- | --- |
| `left` | 왼쪽으로 떠 있는 요소의 영향을 해제한다 |
| `right` | 오른쪽으로 떠 있는 요소의 영향을 해제한다 |
| `both` | 양쪽에 떠 있는 요소의 영향을 모두 해제한다 |

---

## 6. 2단 레이아웃

왼쪽 콘텐츠 영역과 오른쪽 사이드 영역에 `float: left`를 적용하면 두 영역을 가로로 배치할 수 있다.

```html
<div class="container">
    <header>
        헤더 영역
    </header>

    <main>
        <section class="left">
            왼쪽 콘텐츠 영역 <br>
            padding / border / margin / box-sizing 적용
        </section>

        <aside class="right">
            오른쪽 사이드 영역 <br>
            float로 수평 정렬
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
    padding: 20px;
    border: 2px solid #000;
    margin: 10px;
}

main {
    margin: 10px;
    border: 2px solid #000;
    padding: 10px;
}

.left {
    float: left;
    width: 65%;
    border: 2px solid #000;
    height: 300px;
    padding: 20px;
    margin-right: 10px;
}

.right {
    float: left;
    width: 33.5%;
    border: 2px solid #000;
    padding: 20px;
}

.clear {
    clear: both;
}
```

`left`와 `right`에 `float: left`가 적용되어 두 영역이 왼쪽부터 나란히 배치된다.

마지막의 `.clear` 요소는 `float`의 영향을 해제해 `main` 다음에 오는 `footer`가 아래쪽에 정상적으로 배치되도록 한다.

```text
┌────────────────────────────────────────┐
│                 header                 │
├──────────────────────────┬─────────────┤
│                          │             │
│          left            │    right    │
│          65%             │    33.5%    │
│                          │             │
├──────────────────────────┴─────────────┤
│                 footer                 │
└────────────────────────────────────────┘
```

---

## 7. 웹폰트

웹폰트는 사용자의 컴퓨터에 글꼴이 설치되어 있지 않아도 웹 페이지가 글꼴 파일을 내려받아 같은 글꼴을 표시하는 방식이다.

`@font-face`를 사용해 글꼴의 이름, 파일 경로, 두께를 등록한다.

```css
@font-face {
    font-family: 'OngleipParkDahyeon';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/2411-3@1.0/Ownglyph_ParkDaHyun.woff2')
        format('woff2');
    font-weight: normal;
    font-display: swap;
}
```

### 7.1 여러 글자 두께 등록

같은 `font-family` 이름을 사용하고 `font-weight`를 다르게 지정하면 여러 두께의 글꼴 파일을 등록할 수 있다.

```css
@font-face {
    font-family: 'Paperozi';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-1Thin.woff2')
        format('woff2');
    font-weight: 100;
    font-display: swap;
}

@font-face {
    font-family: 'Paperozi';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-4Regular.woff2')
        format('woff2');
    font-weight: 400;
    font-display: swap;
}

@font-face {
    font-family: 'Paperozi';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/2408-3@1.0/Paperlogy-7Bold.woff2')
        format('woff2');
    font-weight: 700;
    font-display: swap;
}
```

등록한 글꼴은 `font-family` 속성으로 적용한다.

```css
body {
    font-family: 'Paperozi';
}
```

---

## 8. 텍스트 스타일

### 8.1 `font-family`

텍스트에 사용할 글꼴을 지정한다.

```css
h1 {
    font-family: "Noto Sans KR", Arial, sans-serif;
}
```

여러 글꼴을 작성하면 앞의 글꼴이 없을 때 다음 글꼴을 사용한다.

### 8.2 `font-size`

글자의 크기를 지정한다.

```css
h1 {
    font-size: 20px;
}
```

| 단위 | 기준 |
| --- | --- |
| `px` | 지정한 고정 크기 |
| `em` | 부모 요소의 글자 크기 |
| `rem` | 최상위 `html` 요소의 글자 크기 |
| `%` | 부모 요소의 글자 크기에 대한 비율 |

```css
html {
    font-size: 14px;
}

h1 {
    font-size: 3rem;
}

p {
    font-size: 0.8rem;
}

.small-text {
    font-size: 90%;
}
```

`html`의 글자 크기가 `14px`이면 `1rem`은 `14px`이므로 `3rem`은 `42px`이 된다.

### 8.3 `font-weight`

글자의 두께를 지정한다.

```css
.highlight {
    font-weight: bold;
}
```

`normal`, `bold` 또는 `100`부터 `900`까지의 숫자를 사용할 수 있다.

```css
.highlight {
    font-weight: 700;
}
```

실제로 표현되는 두께는 적용한 글꼴이 지원하는 범위에 따라 달라진다.

### 8.4 `font-style`

글자를 기울여 표시한다.

```css
p {
    font-style: italic;
}
```

### 8.5 `font-variant`

영문 소문자를 작은 대문자 형태로 표시할 수 있다.

```css
.vari {
    font-variant: small-caps;
}
```

### 8.6 `line-height`

한 줄의 높이를 설정해 줄 사이의 간격을 조절한다.

```css
body {
    line-height: 2;
}
```

숫자만 작성하면 현재 글자 크기의 배수로 계산된다.

### 8.7 `letter-spacing`

글자와 글자 사이의 간격을 조절한다.

```css
h1 {
    letter-spacing: 5px;
}
```

### 8.8 `word-spacing`

단어와 단어 사이의 간격을 조절한다.

```css
p {
    word-spacing: 4px;
}
```

### 8.9 `text-align`

텍스트를 가로 방향으로 정렬한다.

```css
h1 {
    text-align: center;
}
```

### 8.10 `text-decoration`

텍스트에 밑줄, 윗줄, 취소선과 같은 장식을 적용한다.

```css
.deco {
    text-decoration: line-through;
}
```

| 값 | 효과 |
| --- | --- |
| `none` | 장식을 제거한다 |
| `underline` | 밑줄을 표시한다 |
| `overline` | 윗줄을 표시한다 |
| `line-through` | 취소선을 표시한다 |

### 8.11 텍스트 스타일 예제

```css
html {
    font-size: 14px;
}

body {
    font-family: 'Paperozi';
    line-height: 2;
}

h1 {
    font-size: 3rem;
    text-align: center;
    letter-spacing: 5px;
}

p {
    font-size: 0.8rem;
}

.highlight {
    font-size: 1.1rem;
    font-weight: bold;
}

.small-text {
    font-size: 90%;
    color: deepskyblue;
}

.deco {
    text-decoration: line-through;
}

.vari {
    font-variant: small-caps;
}
```

```html
<h1>눈누 웹폰 예제</h1>

<p>
    이 문장은 기본 본문 텍스트입니다.
    <span class="highlight">이 부분은 em 단위로 강조</span>되어 있습니다.
</p>

<p class="small-text">
    이 문장은 % 단위를 사용한 작은 설명 텍스트입니다.
</p>

<p>
    <span class="deco">
        Lorem ipsum dolor sit amet consectetur adipisicing elit.
    </span>
    <span class="vari">
        Sunt quaerat assumenda optio similique ad?
    </span>
</p>
```

---

## 9. `position`

`position`은 HTML 요소를 문서의 기본 흐름에서 어떻게 배치할지 결정하는 CSS 속성이다.

요소의 위치 기준과 이동 방식을 지정하고 `top`, `right`, `bottom`, `left`와 함께 사용할 수 있다.

| 값 | 특징 |
| --- | --- |
| `static` | 문서의 일반적인 흐름에 따라 배치된다 |
| `relative` | 자신의 원래 위치를 기준으로 이동한다 |
| `fixed` | 브라우저 화면을 기준으로 고정된다 |
| `absolute` | 위치가 지정된 가까운 부모 요소를 기준으로 배치된다 |

### 9.1 `position: static`

모든 HTML 요소의 기본 위치 지정 방식이다.

요소는 작성된 순서에 따라 위에서 아래, 왼쪽에서 오른쪽으로 배치된다.

```css
.box {
    position: static;
}
```

---

## 10. `position: relative`

`relative`는 요소를 일반적인 문서 흐름에 그대로 두면서 자신의 원래 위치를 기준으로 이동한다.

```css
#box1 {
    position: relative;
    width: 150px;
    height: 150px;
    background-color: deeppink;
    top: 30px;
    left: 30px;
    z-index: 10;
}

#box2 {
    position: relative;
    width: 150px;
    height: 150px;
    background-color: deepskyblue;
    top: -30px;
}
```

```html
<div id="box1">박스 1</div>
<div id="box2">박스 2</div>
```

`box1`은 원래 위치에서 아래로 `30px`, 오른쪽으로 `30px` 이동한다.

`box2`는 원래 위치에서 위로 `30px` 이동한다.

### 10.1 `z-index`

`z-index`는 여러 요소가 겹칠 때 어떤 요소를 위에 표시할지 결정한다.

값이 클수록 더 위에 표시된다.

```css
#box1 {
    position: relative;
    z-index: 10;
}
```

`z-index`는 길이가 아니므로 `10px`이 아니라 단위가 없는 `10`처럼 작성한다.

---

## 11. `position: fixed`

`fixed`는 요소를 브라우저 화면을 기준으로 고정한다.

페이지를 스크롤해도 해당 요소는 같은 위치에 머문다.

```css
.fixed-box {
    background-color: orange;
    padding: 15px;
    right: 20px;
    bottom: 20px;
    position: fixed;
}
```

```html
<p>스크롤을 내려보세요.</p>
<p>내용입니다.</p>
<p id="bookmark">내용입니다(도착).</p>
<p>내용입니다.</p>

<p>
    <a href="#bookmark">이동</a>
</p>

<div class="fixed-box">
    <a href="#">fixed 박스</a>
</div>
```

`right: 20px`과 `bottom: 20px`이 적용되어 브라우저 화면의 오른쪽 아래에 고정된다.

```text
브라우저 화면
┌────────────────────────────┐
│                            │
│          콘텐츠              │
│                            │
│                  ┌───────┐ │
│                  │ fixed │ │
│                  └───────┘ │
└────────────────────────────┘
```

---

## 12. `position: absolute`

`absolute`는 요소를 문서의 일반적인 흐름에서 제거한 뒤 가장 가까운 위치가 지정된 부모 요소를 기준으로 배치한다.

부모 요소의 `position`에 `relative`, `absolute`, `fixed` 중 하나가 지정되어 있으면 해당 부모가 위치의 기준이 된다.

```css
.parent {
    position: relative;
    width: 300px;
    height: 200px;
    border: 2px solid #000;
    margin: 50px;
}

.child {
    position: absolute;
    top: 20px;
    right: 20px;
    padding: 10px;
    background-color: deepskyblue;
}
```

```html
<div class="parent">
    부모영역

    <div class="child">
        absolute 박스
    </div>
</div>
```

`parent`에 `position: relative`가 적용되어 있으므로 `child`는 부모 영역을 기준으로 위에서 `20px`, 오른쪽에서 `20px` 떨어진 위치에 배치된다.

```text
parent
┌────────────────────────────┐
│ 부모영역           ┌────────┐ │
│                  │ child  ││
│                  └────────┘│
│                            │
└────────────────────────────┘
```

위치가 지정된 부모 요소가 없다면 브라우저 화면을 기준으로 배치된다.

---

## 13. `position` 비교

| 구분 | 위치 기준 | 기존 공간 |
| --- | --- | --- |
| `static` | 문서의 일반적인 흐름 | 유지된다 |
| `relative` | 자신의 원래 위치 | 유지된다 |
| `fixed` | 브라우저 화면 | 일반적인 흐름에서 제거된다 |
| `absolute` | 위치가 지정된 가까운 부모 요소 | 일반적인 흐름에서 제거된다 |

```text
relative
자신의 원래 위치를 기준으로 이동

fixed
브라우저 화면을 기준으로 고정

absolute
위치가 지정된 가까운 부모를 기준으로 이동
```

---

## 14. 핵심 정리

1. `table`은 행과 열로 이루어진 표를 만든다.
2. `colspan`은 열을 병합하고 `rowspan`은 행을 병합한다.
3. `thead`는 표의 제목 영역, `tbody`는 표의 본문 영역이다.
4. `div`는 블록 컨테이너이고 `span`은 인라인 컨테이너다.
5. 시맨틱 태그는 영역의 의미와 역할을 나타낸다.
6. 박스 모델은 `content`, `padding`, `border`, `margin`으로 구성된다.
7. `border-box`는 `padding`과 `border`를 지정한 크기 안에 포함한다.
8. 위아래 마진은 상황에 따라 병합될 수 있다.
9. `float`는 요소를 왼쪽이나 오른쪽으로 띄운다.
10. `clear`는 `float`의 영향을 해제한다.
11. 웹폰트는 글꼴 파일을 내려받아 동일한 글꼴을 표시한다.
12. `font-size`, `font-weight`, `line-height` 등으로 텍스트의 모양을 지정한다.
13. `relative`는 자신의 원래 위치를 기준으로 이동한다.
14. `fixed`는 브라우저 화면을 기준으로 고정된다.
15. `absolute`는 위치가 지정된 가까운 부모 요소를 기준으로 배치된다.
16. `z-index`는 겹친 요소의 표시 순서를 결정하며 단위 없는 값을 사용한다.
