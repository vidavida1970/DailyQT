# 매일매일 큐티 페이지 템플릿

`{{DATE}}` = `YYYY-MM-DD`, `{{NO}}` = `MMDD`, `{{PAGE_URL}}` = 파일별 canonical/og:url (SKILL.md 4장 표 참조).

공용 스타일은 `assets/site.css`에 있고 **수정하지 않는다**. 페이지가 갖는 인라인 `<style>`은 hero 배경과 몇 개 유틸 클래스뿐이다.

---

## head

```html
<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>매일매일 큐티｜{{YYYY년 M월 D일 요일}}</title><meta name="description" content="{{한 줄 요약}} {{YYYY년 M월 D일}} 큐티">
<link rel="canonical" href="{{PAGE_URL}}"><link rel="image_src" href="{{BASE}}/archive/{{DATE}}/assets/thumbnail-v1.png"><meta name="thumbnail" content="{{BASE}}/archive/{{DATE}}/assets/thumbnail-v1.png">
<meta property="og:title" content="매일매일 큐티｜{{제목 2줄을 이은 문구}}"><meta property="og:description" content="{{YYYY년 M월 D일}}｜소망교회·생명의 삶·매일성경 공식 영상과 오늘의 묵상"><meta property="og:type" content="article"><meta property="og:locale" content="ko_KR"><meta property="og:url" content="{{PAGE_URL}}"><meta property="og:image" content="{{BASE}}/archive/{{DATE}}/assets/thumbnail-v1.png"><meta property="og:image:url" content="…"><meta property="og:image:secure_url" content="…"><meta property="og:image:type" content="image/png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="매일매일 큐티 {{YYYY년 M월 D일}} {{제목}}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="…"><meta name="twitter:description" content="{{YYYY년 M월 D일}} 공식 영상과 오늘의 묵상"><meta name="twitter:image" content="…"><link rel="stylesheet" href="{{CSS_PATH}}">
<style>.hero{position:relative;background:#17382a url("{{BG_PATH}}") center 48%/cover no-repeat}.hero::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,27,23,.92) 0%,rgba(8,27,23,.66) 56%,rgba(8,27,23,.18) 100%)}.hero-inner{position:relative;z-index:1}.today-word{margin:26px 0 0;padding:18px 22px;border-left:4px solid #d8c89c;background:rgba(255,255,255,.1);border-radius:0 12px 12px 0;max-width:700px}.today-word strong{display:block;color:#f4ddb0}.source-note{margin-top:18px;color:#718078;font-size:.83rem}</style></head>
```

`{{BASE}}` = `https://vidavida1970.github.io/DailyQT`

경로 변형:

| 파일 | `<base>` | `{{CSS_PATH}}` | `{{BG_PATH}}` | `archive/` 링크 | `source/` 링크 |
|---|---|---|---|---|---|
| `archive/{{DATE}}/index.html` | `<base href="../../">` (charset 뒤) | `assets/site.css` | `archive/{{DATE}}/assets/background.jpg` | `archive/` | `source/{{DATE}}.md` |
| `archive/{{DATE}}/kakao-v1.html` | 없음 | `../../assets/site.css` | `assets/background.jpg` | `../` | `../../source/{{DATE}}.md` |
| `index.html` (루트) | 없음 | `assets/site.css` | `archive/{{DATE}}/assets/background.jpg` | `archive/` | `source/{{DATE}}.md` |

---

## body

```html
<body><main><header class="hero"><div class="hero-inner"><p class="eyebrow">DAILY DEVOTIONAL LETTER · NO. {{NO}}</p><h1>매일매일 큐티</h1><p class="date">{{YYYY년 M월 D일 요일}} <span>AUGUST 05</span></p><p class="intro">오늘의 말씀을 정확하게 확인하고, 짧게 묵상하고, 한 가지를 살아냅니다.</p><p class="today-word"><strong>오늘 읽을 말씀</strong>{{장절1}} · {{장절2}} · {{장절3}}</p></div></header>
<div class="content"><nav class="top-links"><a href="{{ARCHIVE}}">지난 QT 보기</a><a href="{{SOURCE}}">오늘 원문</a></nav><aside class="toc"><span>오늘의 순서</span><a href="#s01">01 소망교회 새벽기도</a><a href="#s02">02 CGN 생명의 삶</a><a href="#s03">03 성서유니온 매일성경</a></aside>
```

### 섹션 (01/02/03 동일 구조)

```html
<article id="s01" class="letter"><div class="section-head"><span>01</span><div><p>{{소스명}}</p><h2>{{영상 제목}}</h2><strong>{{본문 장절}} · {{설교자}}</strong><a class="bible-link" href="https://www.godpia.com/read/reading.asp?chap={{장}}&amp;goSec=gae_{{권}}_{{장}}_{{절}}&amp;sec={{절}}&amp;ver=gae&amp;vol={{권}}" target="_blank" rel="noopener noreferrer">GODpia에서 {{권}} {{장}}장 {{절}}절부터 읽기 ↗</a></div></div>
<section><h3>핵심 요약</h3><ul><li>…</li><li>…</li><li>…</li><li>…</li></ul></section>
<div class="two-col"><section><h3>묵상 포인트</h3><p>{{질문 한 문장}}</p></section><section><h3>오늘의 적용</h3><p>{{행동 한 문장}}</p></section></div>
<blockquote><span>짧은 기도</span>{{기도 한 문장}} 아멘.</blockquote>
<section class="video"><h3>오늘의 영상</h3><div class="frame"><iframe src="https://www.youtube-nocookie.com/embed/{{VIDEO_ID}}?rel=0&amp;playsinline=1" title="{{소스명}} {{영상 제목}}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div><a href="https://www.youtube.com/watch?v={{VIDEO_ID}}" target="_blank" rel="noopener noreferrer">YouTube에서 크게 보기 ↗</a></section>
<p class="source-note">확인 근거: {{제목·본문·설교자·날짜 표기 근거}}</p></article>
```

GODpia `vol` 코드: 민수기 `num`, 이사야 `isa`, 에스겔 `ezk`. 다른 권은 GODpia에서 확인 후 사용한다.

### footer

```html
<footer><p>오늘의 한 문장</p><h2>{{3개 소스를 아우르는 한 문장}}</h2><label><input type="checkbox"> {{오늘 실천할 세 가지를 한 문장으로}}</label><small>{{YYYY년 M월 D일}} 공식 회차 정보만 사용했습니다. 배경: DailyQT 자체 제작 새벽 산빛 그래픽</small></footer></div></main></body></html><!-- published {{DATE}} -->
```

---

## source/{{DATE}}.md

```markdown
# 매일매일 큐티｜{{YYYY년 M월 D일 요일}}

## 오늘의 한 문장
{{footer와 동일}}

## 1. 소망교회 새벽기도
- 제목: / 본문: / 설교: / 공개일: / 공식 영상: / 확인 근거:

{{2~3문장 요약}}

## 2. CGN 생명의 삶
## 3. 성서유니온 매일성경
## 오늘의 적용
## 검증 메모
- 영상 ID: `…`, `…`, `…`
- 정정 사항: {{있을 경우 반드시 기록}}
```
