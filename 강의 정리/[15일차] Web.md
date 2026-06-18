# HTML과 CSS 기초 정리

HTML 문서의 기본 구조와 자주 사용하는 태그를 살펴보고, CSS를 적용하는 방법과 다양한 선택자를 학습한다.ㅓ

웹 페이지는 크게 **구조**, **표현**, **동작**으로 구성된다.

| 기술 | 역할 | 예시 |
| --- | --- | --- |
| HTML | 웹 페이지의 구조와 의미를 정의한다 | 제목, 문단, 이미지, 링크 |
| CSS | HTML 요소의 모양과 배치를 지정한다 | 색상, 크기, 여백, 정렬 |
| JavaScript | 웹 페이지의 동작을 구현한다 | 클릭 이벤트, 데이터 변경 |

---

## 1. HTML이란?

HTML(HyperText Markup Language)은 웹 페이지의 구조와 콘텐츠를 표현하는 마크업 언어다.

프로그래밍 언어처럼 계산이나 조건 처리를 수행하는 것이 아니라, 태그를 사용해 콘텐츠가 제목인지, 문단인지, 이미지인지와 같은 의미를 브라우저에 전달한다.

```html
<h1>HTML이란?</h1>
<p>HTML은 웹 페이지의 구조를 표현하는 언어다.</p>
```

### 태그의 기본 구조

```html
<태그명 속성="속성값">내용</태그명>
```

예를 들어 다음 코드는 `a` 태그에 `href` 속성을 지정한 것이다.

```html
<a href="https://www.naver.com">네이버</a>
```

- `<a>`: 시작 태그다.
- `href`: 이동할 주소를 지정하는 속성이다.
- `네이버`: 화면에 표시되는 내용이다.
- `</a>`: 종료 태그다.

`img`, `meta`, `br`, `hr`처럼 내용을 감싸지 않는 요소는 별도의 종료 태그를 작성하지 않는다.

---

## 2. HTML 문서의 기본 구조

```html
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML</title>
</head>

<body>
    <!--
        HTML 주석문
        작성일: 2026-06-10
        작성자: 송정근
    -->
    HTML이란?
</body>

</html>
```

### `<!DOCTYPE html>`

현재 문서가 HTML5 문서라는 것을 브라우저에 알린다.

```html
<!DOCTYPE html>
```

태그는 아니지만 HTML 문서의 가장 위에 작성하는 선언문이다.

### `<html>`

HTML 문서 전체를 감싸는 최상위 요소다.

```html
<html lang="ko">
```

`lang` 속성은 문서의 주 언어를 나타낸다. 검색 엔진과 화면 낭독기 같은 보조 기술이 문서를 올바르게 처리할 수 있도록 한국어 문서에는 `ko`를 사용한다.

### `<head>`

문서 자체에 관한 정보를 작성하는 영역이다. 일반적으로 화면에 직접 표시되지 않는다.

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML</title>
</head>
```

| 요소 | 역할 |
| --- | --- |
| `meta charset="UTF-8"` | 문자의 인코딩 방식을 UTF-8로 설정한다 |
| `meta name="viewport"` | 모바일 화면의 너비와 배율을 설정한다 |
| `title` | 브라우저 탭에 표시할 문서 제목을 지정한다 |

### `<body>`

제목, 문단, 이미지처럼 브라우저 화면에 표시할 콘텐츠를 작성한다.

```html
<body>
    <h1>HTML이란?</h1>
    <p>HTML 기본 문서를 학습한다.</p>
</body>
```

### HTML 주석

주석은 코드에 설명을 남길 때 사용하며 브라우저 화면에는 표시되지 않는다.

```html
<!-- HTML 주석 -->
```

---

## 3. 블록 요소와 인라인 요소

HTML 요소는 화면에서 공간을 차지하는 방식에 따라 블록 요소와 인라인 요소로 구분할 수 있다.

### 블록 요소

블록 요소는 기본적으로 사용할 수 있는 가로 영역 전체를 차지하며, 다음 요소는 새로운 줄에서 시작한다.

대표적인 블록 요소는 다음과 같다.

```text
h1 ~ h6, p, ul, ol, li, div
```

### 인라인 요소

인라인 요소는 콘텐츠 크기만큼만 공간을 차지하며 줄바꿈 없이 이어진다.

대표적인 인라인 요소는 다음과 같다.

```text
a, img, strong, em, span
```

> CSS의 `display` 속성을 사용하면 요소의 기본 표시 방식을 변경할 수 있다. 따라서 블록과 인라인 구분은 절대적인 형태라기보다 기본 표시 방식으로 이해하면 된다.

---

## 4. 텍스트 관련 태그

### 제목 태그

`h1`부터 `h6`까지 문서의 제목과 소제목을 표현한다.

```html
<h1>안녕하세요. Heading</h1>
<h2>안녕하세요. Heading</h2>
<h3>안녕하세요. Heading</h3>
<h4>안녕하세요. Heading</h4>
<h5>안녕하세요. Heading</h5>
<h6>안녕하세요. Heading</h6>
```

숫자가 작을수록 더 높은 수준의 제목이다. 단순히 글자 크기를 조절하려고 제목 태그를 선택하기보다 문서의 계층 구조에 맞게 사용해야 한다.

```text
h1: 페이지의 핵심 제목
└─ h2: 주요 단원
   └─ h3: 단원의 세부 항목
```

### 문단 태그

`p` 태그는 하나의 문단을 만든다.

```html
<p>문단을 만드는 태그</p>
<p>새로운 문단이다.</p>
```

HTML 소스에서 여러 번 줄을 바꾸거나 공백을 입력해도 브라우저는 대부분 하나의 공백으로 처리한다.

```html
일반 텍스트
일반 텍스트
일반 텍스트
```

### 줄바꿈과 구분선

`br`은 현재 위치에서 줄을 바꾸고, `hr`은 주제가 전환되는 지점을 수평선으로 표현한다.

```html
일반 텍스트<br>
줄바꿈된 텍스트

<hr>
```

문단을 구분할 때는 여러 개의 `br`을 사용하기보다 `p` 태그를 사용하는 편이 의미상 적절하다.

### 공백 문자

여러 개의 공백을 화면에 표시해야 할 때 `&nbsp;` 문자 엔티티를 사용할 수 있다.

```html
일반&nbsp;&nbsp;&nbsp;텍스트
```

다만 레이아웃을 조절하기 위해 `&nbsp;`를 반복해서 사용하기보다 CSS의 `margin`, `padding` 등을 사용하는 것이 좋다.

### 텍스트 서식

```html
<p><b>굵게</b> 표현하기</p>
<p><strong>중요한 내용</strong> 표현하기</p>
<p><i>이탤릭체</i> 표현하기</p>
<p><em>강조하는 내용</em> 표현하기</p>
<p><ins>추가된 내용</ins> 표현하기</p>
<p><del>삭제된 내용</del> 표현하기</p>
<p>x<sup>2</sup> + y<sup>3</sup> = z</p>
<p>H<sub>2</sub>O</p>
```

| 태그 | 의미 |
| --- | --- |
| `b` | 특별한 중요성 없이 시각적으로 굵게 표시한다 |
| `strong` | 중요한 내용을 의미하며 기본적으로 굵게 표시된다 |
| `i` | 다른 어조나 전문 용어 등을 표현하며 기본적으로 기울여 표시된다 |
| `em` | 문맥상 강조할 내용을 의미하며 기본적으로 기울여 표시된다 |
| `ins` | 추가된 내용을 나타낸다 |
| `del` | 삭제된 내용을 나타낸다 |
| `sup` | 위 첨자를 나타낸다 |
| `sub` | 아래 첨자를 나타낸다 |

`strong`과 `em`은 단순한 모양뿐 아니라 의미도 전달한다. 화면 낭독기나 검색 엔진도 이러한 의미를 활용할 수 있다.

---

## 5. 목록 태그

HTML은 순서 없는 목록, 순서 있는 목록, 설명 목록을 제공한다.

### 순서 없는 목록

항목의 순서가 중요하지 않을 때 `ul`을 사용한다. 각각의 항목은 `li`로 작성한다.

```html
<ul>
    <li>김사과</li>
    <li>오렌지</li>
    <li>반하나</li>
</ul>
```

화면에는 일반적으로 글머리 기호와 함께 표시된다.

```text
• 김사과
• 오렌지
• 반하나
```

### 순서 있는 목록

항목의 진행 순서나 순위가 중요할 때 `ol`을 사용한다.

```html
<ol>
    <li>김사과</li>
    <li>오렌지</li>
    <li>반하나</li>
</ol>
```

```text
1. 김사과
2. 오렌지
3. 반하나
```

### 설명 목록

용어와 그에 대한 설명을 함께 표현할 때 `dl`, `dt`, `dd`를 사용한다.

```html
<dl>
    <dt>류정원 선생님</dt>
    <dd>김사과</dd>
    <dd>오렌지</dd>
    <dd>반하나</dd>
</dl>
```

| 태그 | 역할 |
| --- | --- |
| `dl` | 설명 목록 전체를 감싼다 |
| `dt` | 설명할 용어나 이름을 나타낸다 |
| `dd` | 해당 용어에 대한 설명이나 값을 나타낸다 |

### 목록을 중첩하는 방법

하위 목록은 반드시 `li` 요소 안에 작성한다.

```html
<ul>
    <li>
        과일
        <ul>
            <li>사과</li>
            <li>바나나</li>
        </ul>
    </li>
    <li>채소</li>
</ul>
```

`ul`과 `ol`의 직접적인 자식으로는 `li`를 사용해야 한다.

---

## 6. 이미지 태그

`img` 태그는 웹 페이지에 이미지를 표시한다.

```html
<img src="spring1.png" alt="봄 풍경">
```

| 속성 | 역할 |
| --- | --- |
| `src` | 표시할 이미지의 경로를 지정한다 |
| `alt` | 이미지를 불러오지 못했을 때 표시할 대체 텍스트다 |

`alt`는 단순한 오류 메시지가 아니다. 화면 낭독기를 사용하는 사람에게 이미지의 의미를 전달하므로 이미지의 목적을 설명하도록 작성해야 한다.

### 웹에서 사용하는 이미지 형식

| 형식 | 특징 |
| --- | --- |
| PNG | 투명 배경을 지원하며 로고, 아이콘에 적합하다 |
| JPEG/JPG | 사진처럼 색상이 많은 이미지에 적합하다 |
| GIF | 간단한 애니메이션을 지원한다 |
| WebP | 비교적 작은 용량으로 높은 화질을 제공한다 |
| SVG | 벡터 기반이므로 확대해도 선명하다 |

### 외부 이미지 경로

인터넷에 공개된 이미지 URL을 사용할 수 있다.

```html
<img
    src="https://tcpschool.com/img/logo.png"
    alt="TCP스쿨 로고"
>
```

외부 서버의 이미지가 삭제되거나 주소가 변경되면 표시되지 않을 수 있다는 점에 주의한다.

### 상대 경로

현재 HTML 파일의 위치를 기준으로 이미지 경로를 작성한다.

```html
<img src="spring1.png" alt="봄 풍경">
<img src="images/spring2.png" alt="봄 풍경">
```

폴더 구조가 다음과 같다고 가정한다.

```text
4_HTML_CSS/
├── 4_이미지.html
├── spring1.png
└── images/
    └── spring2.png
```

- `spring1.png`: HTML 파일과 같은 폴더의 이미지다.
- `images/spring2.png`: 현재 폴더 안의 `images` 폴더에 있는 이미지다.
- `../image.png`: 현재 폴더의 상위 폴더에 있는 이미지다.

### 로컬 절대 경로 사용 시 주의점

```html
<img
    src="/Users/songjeong-geun/Desktop/KDT/4_HTML_CSS/spring1.png"
    alt="봄"
>
```

이 경로는 작성자의 컴퓨터에서만 유효한 로컬 파일 경로다. Live Server나 배포된 웹 서버에서는 접근할 수 없으므로 웹 프로젝트에서는 상대 경로를 사용하는 것이 좋다.

```html
<img src="./spring1.png" alt="봄">
```

### 이미지 크기

HTML 속성으로도 크기를 지정할 수 있지만, 일반적으로 CSS를 사용한다.

```html
<img class="spring-image" src="./spring1.png" alt="봄 풍경">
```

```css
.spring-image {
    width: 300px;
    height: auto;
}
```

`height: auto`를 사용하면 원본 이미지의 비율을 유지할 수 있다.

---

## 7. 하이퍼링크

`a` 태그는 다른 페이지나 현재 페이지의 특정 위치로 이동하는 링크를 만든다.

```html
<a href="https://www.naver.com">네이버</a>
```

`href` 속성에는 이동할 주소를 지정한다.

### 외부 페이지 링크

```html
<a href="https://www.naver.com">네이버</a>
```

새 탭에서 링크를 열려면 `target="_blank"`를 사용할 수 있다.

```html
<a
    href="https://www.naver.com"
    target="_blank"
    rel="noopener noreferrer"
>
    네이버
</a>
```

새 탭을 사용할 때 `rel="noopener noreferrer"`를 함께 지정하면 새 페이지가 기존 페이지의 창 객체에 접근하는 것을 방지하는 데 도움이 된다.

### 이미지 링크

`a` 태그 안에 `img` 태그를 넣으면 이미지를 클릭할 수 있는 링크가 된다.

```html
<a href="https://tcpschool.com">
    <img
        src="https://tcpschool.com/img/logo.png"
        alt="TCP스쿨 홈페이지로 이동"
    >
</a>
```

### 상대 경로 링크

프로젝트 내부의 다른 HTML 문서로 이동할 때 상대 경로를 사용할 수 있다.

```html
<a href="./4_이미지.html">이미지 페이지</a>
<a href="./pages/subpage.html">서브페이지</a>
```

```text
4_HTML_CSS/
├── 4_이미지.html
├── 5_하이퍼링크.html
└── pages/
    └── subpage.html
```

### 페이지 내부 링크

`href`에 `#아이디`를 지정하면 같은 문서에서 해당 `id`를 가진 요소로 이동한다.

```html
<a href="#html-section">HTML 설명으로 이동</a>

<h2 id="html-section">HTML</h2>
```

`id`는 한 HTML 문서 안에서 중복되지 않게 작성해야 한다.

---

## 8. CSS란?

CSS(Cascading Style Sheets)는 HTML 요소의 색상, 크기, 위치, 여백과 같은 표현 방식을 정의하는 스타일시트 언어다.

```css
선택자 {
    속성: 값;
}
```

다음 코드는 모든 `h1` 요소의 글자색을 흰색으로 바꾸고 가운데 정렬한다.

```css
h1 {
    color: white;
    text-align: center;
}
```

- `h1`: 스타일을 적용할 요소를 찾는 선택자다.
- `color`: 변경할 CSS 속성이다.
- `white`: 속성에 적용할 값이다.
- 선언의 끝에는 세미콜론(`;`)을 작성한다.

---

## 9. CSS를 적용하는 세 가지 방법

### 인라인 스타일

HTML 요소의 `style` 속성에 CSS를 직접 작성한다.

```html
<p style="color: gold;">안녕하세요. CSS입니다.</p>
```

간단하게 테스트할 수 있지만 HTML과 CSS가 섞이고 재사용하기 어려워 규모가 큰 프로젝트에는 적합하지 않다.

### 내부 스타일

HTML 문서의 `head` 안에 `style` 태그를 작성한다.

```html
<head>
    <style>
        body {
            background-color: deepskyblue;
        }

        h1 {
            color: white;
            text-align: center;
        }
    </style>
</head>
```

현재 HTML 문서 하나에만 적용할 스타일을 작성할 때 사용할 수 있다.

### 외부 스타일

CSS를 별도의 `.css` 파일에 작성하고 `link` 태그로 연결한다.

```html
<link rel="stylesheet" href="./css/test.css">
```

```css
/* css/test.css */
body {
    background-color: deepskyblue;
}

h1 {
    color: white;
    text-align: center;
}
```

여러 HTML 문서에서 같은 스타일을 재사용할 수 있어 실무에서 가장 일반적으로 사용하는 방식이다.

### 적용 방식 비교

| 방식 | 작성 위치 | 장점 | 단점 |
| --- | --- | --- | --- |
| 인라인 | HTML 요소의 `style` 속성 | 빠르게 적용할 수 있다 | 재사용과 유지보수가 어렵다 |
| 내부 스타일 | HTML 문서의 `style` 태그 | 한 문서를 관리하기 편하다 | 여러 문서에서 재사용하기 어렵다 |
| 외부 스타일 | 별도의 CSS 파일 | 재사용성과 유지보수성이 좋다 | CSS 파일을 별도로 연결해야 한다 |

---

## 10. CSS 선택자

선택자는 스타일을 적용할 HTML 요소를 찾는 표현식이다.

### 10.1 태그 선택자

특정 태그 이름을 가진 모든 요소를 선택한다.

```css
h1 {
    color: deepskyblue;
    text-align: center;
}
```

```html
<h1>선택자</h1>
```

### 10.2 클래스 선택자

`class` 속성값 앞에 마침표(`.`)를 붙여 선택한다. 같은 클래스를 여러 요소에 재사용할 수 있다.

```css
.intro {
    font-weight: bold;
    color: deeppink;
}
```

```html
<p class="intro">이 문단은 첫 번째 문단이다.</p>
```

한 요소가 여러 클래스를 가질 때는 공백으로 구분한다.

```html
<li class="bluecolor highlight">반하나</li>
```

```css
.bluecolor {
    font-style: italic;
}

.highlight {
    color: gold;
}
```

위 요소에는 두 클래스의 스타일이 모두 적용된다.

### 10.3 아이디 선택자

`id` 속성값 앞에 `#`을 붙여 선택한다.

```css
#favorite-list {
    background-color: ivory;
    padding: 10px;
}
```

```html
<ul id="favorite-list">
    <li>김사과</li>
    <li>반하나</li>
</ul>
```

`id`는 문서 안에서 고유해야 하며 같은 값을 여러 요소에 반복해서 사용하지 않는다.

### 10.4 그룹 선택자

쉼표로 선택자를 구분하면 여러 종류의 요소에 같은 스타일을 적용할 수 있다.

```css
p,
li {
    font-size: 20px;
}
```

### 10.5 의사 클래스 선택자

요소의 상태나 위치를 기준으로 선택한다.

```css
a:hover {
    color: yellowgreen;
    text-decoration: none;
}
```

`:hover`는 사용자가 마우스 포인터를 요소 위에 올린 상태를 의미한다.

자주 사용하는 의사 클래스는 다음과 같다.

| 선택자 | 의미 |
| --- | --- |
| `:hover` | 마우스 포인터가 올라간 요소 |
| `:focus` | 키보드 입력 등의 초점을 가진 요소 |
| `:first-child` | 형제 요소 중 첫 번째 요소 |
| `:last-child` | 형제 요소 중 마지막 요소 |
| `:nth-child(n)` | 형제 요소 중 지정한 순서의 요소 |

### 10.6 속성 선택자

특정 속성이나 속성값을 가진 요소를 선택한다.

```css
h1[title="제목"] {
    background-color: ivory;
}
```

```html
<h1 title="제목">선택자</h1>
```

다음과 같은 방식도 사용할 수 있다.

```css
/* target 속성이 있는 모든 a 요소 */
a[target] {
    color: red;
}

/* href가 https로 시작하는 모든 a 요소 */
a[href^="https"] {
    font-weight: bold;
}
```

### 10.7 자식 선택자

`>`는 특정 요소의 바로 아래에 있는 직접 자식만 선택한다.

```css
ul#favorite-list > li {
    list-style-type: square;
}
```

```html
<ul id="favorite-list">
    <li>김사과</li>
    <li>반하나</li>
</ul>
```

### 10.8 자손 선택자

공백은 특정 요소 내부의 모든 하위 요소 중 조건에 맞는 요소를 선택한다.

```css
ul#favorite-list p {
    color: violet;
    font-weight: bold;
}
```

자식 선택자와 자손 선택자의 차이는 다음과 같다.

```html
<div class="box">
    <p>직접 자식</p>

    <section>
        <p>더 아래에 있는 자손</p>
    </section>
</div>
```

```css
/* 첫 번째 p만 선택한다 */
.box > p {
    color: red;
}

/* box 안에 있는 두 p를 모두 선택한다 */
.box p {
    font-weight: bold;
}
```

### 10.9 인접 형제 선택자

`+`는 기준 요소 바로 다음에 나오는 형제 요소 하나를 선택한다.

```css
p.intro + p {
    background-color: aqua;
}
```

```html
<p class="intro">첫 번째 문단</p>
<p>두 번째 문단</p>
```

두 번째 `p`가 첫 번째 `p`의 바로 다음 형제이므로 배경색이 적용된다.

### 10.10 일반 형제 선택자

`~`는 기준 요소 뒤에 있는 같은 부모의 형제 요소를 모두 선택한다.

```css
p.intro ~ p {
    color: blue;
}
```

---

## 11. 선택자 예제 정리

```html
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>다양한 선택자</title>
    <style>
        h1 {
            color: deepskyblue;
            text-align: center;
        }

        .intro {
            font-weight: bold;
            color: deeppink;
        }

        #favorite-list {
            background-color: ivory;
            padding: 10px;
        }

        p,
        li {
            font-size: 20px;
        }

        .highlight {
            color: gold;
        }

        .bluecolor {
            font-style: italic;
        }

        a:hover {
            color: yellowgreen;
            text-decoration: none;
        }

        h1[title="제목"] {
            background-color: ivory;
        }

        ul#favorite-list > li {
            list-style-type: square;
        }

        ul#favorite-list p {
            color: violet;
            font-weight: bold;
        }

        p.intro + p {
            background-color: aqua;
        }
    </style>
</head>

<body>
    <h1 title="제목">선택자</h1>

    <p class="intro">이 문단은 첫 번째 문단이다.</p>
    <p>이 문단은 두 번째 문단이다.</p>

    <ul id="favorite-list">
        <li class="bluecolor">김사과</li>
        <li class="bluecolor highlight">반하나</li>
        <li class="bluecolor">오렌지</li>
        <li class="bluecolor">
            <p>이메론</p>
        </li>
        <li>
            <p>출석부</p>
        </li>
    </ul>

    <a href="https://www.naver.com">외부 링크</a>
    <a href="#top">내부 링크</a>
    <a href="./5_하이퍼링크.html" class="intro">하이퍼링크</a>
</body>

</html>
```

---

## 12. CSS의 Cascading

CSS의 첫 번째 `C`는 Cascading을 의미한다. 하나의 요소에 여러 스타일 규칙이 적용되면 브라우저가 우선순위를 계산해 최종 스타일을 결정한다.

주요 판단 기준은 다음과 같다.

1. `!important` 여부
2. 인라인 스타일 여부
3. 선택자의 명시도
4. 코드가 작성된 순서

일반적인 선택자의 명시도는 다음 순서로 높아진다.

```text
태그 선택자 < 클래스·속성·의사 클래스 선택자 < 아이디 선택자
```

```html
<p id="message" class="notice">안녕하세요.</p>
```

```css
p {
    color: blue;
}

.notice {
    color: green;
}

#message {
    color: red;
}
```

위 예제에서는 아이디 선택자의 명시도가 가장 높으므로 글자색은 빨간색이 된다.

`!important`를 자주 사용하면 우선순위 관리가 어려워지므로 꼭 필요한 경우에만 사용한다.

---

## 13. 경로 정리

HTML에서 이미지와 다른 페이지, CSS 파일을 연결하려면 파일 경로를 정확히 이해해야 한다.

| 경로 | 의미 |
| --- | --- |
| `spring1.png` | 현재 파일과 같은 폴더 |
| `./spring1.png` | 현재 폴더의 `spring1.png` |
| `images/spring2.png` | 현재 폴더 아래 `images` 폴더 |
| `../spring1.png` | 한 단계 상위 폴더 |
| `https://example.com/image.png` | 외부 서버의 절대 URL |

개발자의 컴퓨터에만 존재하는 `/Users/...` 또는 `C:\...` 형식의 로컬 절대 경로는 배포 환경에서 사용할 수 없다.

---

## 14. 접근성과 시맨틱 HTML(Semantic HTML)

> Semantic HTML 은 컴퓨터(웹 브라우저, 검색 엔진)  HTML 문서의 구조와 의미를 명확하게 이해할 수 있도록 알맞은 태그를 사용하여 작성하는 개발 방식이다. 

HTML은 화면의 모양뿐 아니라 콘텐츠의 의미도 표현한다.

다음 내용을 지키면 검색 엔진, 화면 낭독기, 키보드 사용자에게 더 좋은 문서를 제공할 수 있다.

- 문서 언어에 맞는 `lang="ko"`를 사용한다.
- 제목은 `h1`부터 순서에 맞게 구성한다.
- 이미지는 목적을 설명하는 `alt`를 작성한다.
- 이동 기능에는 `a`, 동작 실행에는 `button`을 사용한다.
- 목록은 `ul`, `ol`, `li` 구조에 맞게 작성한다.
- 강조의 의미가 있다면 `strong`, `em`을 사용한다.
- 색상만으로 중요한 상태를 구분하지 않는다.

---

## 15. 핵심 정리

1. HTML은 웹 페이지의 구조와 콘텐츠의 의미를 표현한다.
2. `head`에는 문서 정보, `body`에는 화면에 표시할 내용을 작성한다.
3. 제목은 `h1`부터 `h6`, 문단은 `p`, 목록은 `ul`, `ol`, `li`를 사용한다.
4. 이미지는 `img`의 `src`로 경로를 지정하고 의미 있는 `alt`를 작성한다.
5. 링크는 `a`의 `href`로 이동할 주소를 지정한다.
6. 프로젝트 내부 파일은 배포 가능한 상대 경로로 연결한다.
7. CSS는 `선택자 { 속성: 값; }` 형식으로 작성한다.
8. CSS는 인라인, 내부, 외부 스타일 방식으로 적용할 수 있다.
9. 클래스는 반복 사용이 가능하고, 아이디는 한 문서에서 고유해야 한다.
10. 자식 선택자 `>`와 자손 선택자 공백의 범위는 서로 다르다.
11. 여러 CSS 규칙이 충돌하면 명시도와 작성 순서에 따라 최종 스타일이 결정된다.
12. 올바른 HTML 구조와 의미 있는 태그 사용은 접근성과 유지보수성을 높인다.

