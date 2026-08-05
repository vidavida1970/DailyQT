---
name: daily-qt
description: "매일매일 큐티 뉴스레터 최종 완료본을 제작·배포하는 스킬. 소망교회 새벽기도·CGN 생명의 삶·성서유니온 매일성경 3개 소스의 당일 공식 영상을 검증하고, 자체 제작 배경/썸네일과 함께 반응형 레터 페이지를 만들어 GitHub vidavida1970/DailyQT에 올린 뒤 공개 링크까지 검증해 공유한다. Triggers on '매일매일 큐티', '오늘 큐티 만들어', '큐티 레터 제작', 'DailyQT 오늘 날짜로 발행', '오늘의 QT 뉴스레터', or any request to build/publish today's QT newsletter."
---

# 매일매일 큐티 (Daily QT Newsletter)

3개 공식 소스의 **당일** 큐티를 검증해 하나의 레터 페이지로 만들고, `vidavida1970/DailyQT`에 발행한 뒤 공개 링크를 검증해 공유한다.

**완료 기준**: 당일 자료 검증 → 페이지 제작 → GitHub 푸시 → 공개 링크 HTTP 검증 → 링크 공유. 이 중 하나라도 실패하면 "완료"라고 말하지 말고 실패 지점과 필요한 조치를 정확히 알린다.

이 스킬은 **로컬 macOS와 클라우드 Linux 양쪽에서 동일하게** 동작하도록 작성돼 있다. macOS 전용 경로·폰트·브라우저에 의존하지 않는다.

---

## 0. 실행일과 작업 위치 확정

```bash
TZ=Asia/Seoul date "+%Y-%m-%d %A"
```
이 출력의 날짜(`YYYY-MM-DD`)를 이후 모든 경로·메타데이터·검증에 쓴다. 시스템 컨텍스트에 적힌 날짜가 아니라 **이 명령의 출력**을 기준으로 한다.

레포 위치를 잡는다. 클라우드 세션은 이미 체크아웃돼 있고, 로컬은 스크래치 클론을 쓴다.
```bash
REPO=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO" ] || [ ! -f "$REPO/tools/make_assets.py" ]; then
  REPO=/Users/vida/.gemini/antigravity/scratch/DailyQT
  if [ -d "$REPO" ]; then (cd "$REPO" && git fetch -q && git checkout main -q && git pull -q)
  else git clone -q https://github.com/vidavida1970/DailyQT "$REPO"; fi
  command -v gh >/dev/null && gh auth setup-git 2>/dev/null
  [ -x /opt/homebrew/bin/gh ] && /opt/homebrew/bin/gh auth setup-git 2>/dev/null
fi
cd "$REPO" && git pull -q && echo "REPO=$REPO"
```

레포 구조:
```
index.html                     # 당일 레터 전문 (사이트 루트, <base> 없음)
archive/index.html             # 날짜별 목록
archive/YYYY-MM-DD/index.html  # 당일 레터 (<base href="../../"> 사용)
archive/YYYY-MM-DD/kakao-v1.html
archive/YYYY-MM-DD/assets/{background.jpg,thumbnail-v1.png}
assets/site.css                # 공용 스타일 (수정 금지)
source/YYYY-MM-DD.md           # 원문·검증 근거 기록
tools/make_assets.py           # assets 생성기
tools/fonts/NotoSansKR-VF.ttf  # 번들 글꼴 (OFL)
```

---

## 1. 당일 공식 영상 검증 (가장 실패하기 쉬운 단계)

> **YouTube 재생목록/채널 페이지는 WebFetch로 파싱되지 않는다** (푸터만 반환됨). 반드시 RSS를 쓴다.

### CGN 생명의 삶
```bash
curl -s "https://www.youtube.com/feeds/videos.xml?playlist_id=PLrH3J2Hst9zSfUE5jmSkGmOfHQ6V_k0aK" \
  | grep -Eo '<title>[^<]*</title>|<yt:videoId>[^<]*</yt:videoId>|<published>[^<]*</published>' | sed 's/<[^>]*>//g' | head -12
```
제목 끝의 `YYMMDDQT` 코드가 실행일과 일치해야 한다. 예: `260805QT`.

### 성서유니온 매일성경
```bash
curl -s "https://www.youtube.com/feeds/videos.xml?channel_id=UCJUQfTt8Qnava39rNHcFp-Q" \
  | grep -Eo '<title>[^<]*</title>|<yt:videoId>[^<]*</yt:videoId>|<published>[^<]*</published>' | sed 's/<[^>]*>//g' | head -12
```
제목이 `[M월 D일 묵상]`으로 시작한다. **게시 시각은 전날 21시(KST)라 published 날짜와 묵상 날짜가 다르다 — 반드시 제목의 날짜로 판단한다.**

> 실제 사고 사례: published 기준으로 고르는 바람에 **다음 날 회차**를 실은 적이 있다. 본문 범위까지 통째로 틀린다.

### 소망교회 새벽기도
재생목록 RSS는 404다. 후보 영상 ID를 확보한 뒤 watch 페이지를 WebFetch로 제목만 확인한다.
```
https://www.youtube.com/watch?v=<ID>
```
제목 형식: `[소망교회] <강해 제목> / <본문> / 새벽기도회 / <설교자> / YYYYMMDD`. 끝의 `YYYYMMDD`가 실행일과 일치해야 한다.

### 검증 게이트
3개 영상 각각에 대해 **영상 ID · 제목 · 본문 범위 · 설교자 · 날짜 근거**를 확보하기 전에는 다음 단계로 넘어가지 않는다. 이전 날짜 영상, 다음 날짜 영상, 비공식 재업로드는 사용 금지.

아직 미게시인 소스가 있으면 **추측으로 채우거나 나머지만으로 발행하지 말 것.** 중단하고 어떤 소스가 미게시인지 보고한다.

---

## 2. 자체 제작 assets

```bash
python3 tools/make_assets.py \
  --out archive/YYYY-MM-DD/assets \
  --date YYYY.MM.DD \
  --title "<1줄>" "<2줄>" \
  --sub "<부제 한 줄>" \
  --refs "<장절1> · <장절2> · <장절3>"
```

`Pillow`가 없으면 `pip install --quiet Pillow` 후 재시도한다. 글꼴은 레포 번들(`tools/fonts/NotoSansKR-VF.ttf`)을 쓰므로 시스템 폰트 설치가 필요 없다.

생성 후 **PNG를 Read 툴로 직접 열어** 한글 깨짐·잘림·오탈자를 육안 검수한다. 제목 2줄은 각 12자 내외로 유지해야 1200px 폭을 넘지 않는다(넘으면 스크립트가 stderr로 경고한다).

외부 이미지(특히 `i.ytimg.com`)를 썸네일로 쓰지 않는다 — 4장 참조.

---

## 3. 페이지 제작

`references/page-template.md`의 구조를 그대로 따른다. **직전 날짜 폴더를 레이아웃 기준으로 삼는다.**

3개 파일을 만든다:

| 파일 | `<base>` | canonical / og:url |
|---|---|---|
| `archive/YYYY-MM-DD/index.html` | `<base href="../../">` | `.../archive/YYYY-MM-DD/` |
| `archive/YYYY-MM-DD/kakao-v1.html` | **없음** (4장 참조) | `.../archive/YYYY-MM-DD/kakao-v1.html` |
| `index.html` (루트) | 없음 | `https://vidavida1970.github.io/DailyQT/` |

세 파일의 본문은 동일하고 위 두 컬럼만 다르다. 루트 `index.html`은 리다이렉트 스텁이 아니라 **당일 레터 전문**이어야 한다.

각 섹션(01 소망교회 / 02 CGN / 03 성서유니온)은 동일 구성: 핵심 요약 4개 · 묵상 포인트 · 오늘의 적용 · 짧은 기도 · 16:9 iframe · "YouTube에서 크게 보기" 링크 · 확인 근거 한 줄.

성경 번역문은 장문 전재하지 않는다. 요약·묵상 문장으로 쓰고 장절만 정확히 표기한다.

`archive/index.html` 목록 맨 위에 당일 항목을 추가하고, `source/YYYY-MM-DD.md`에 영상 ID·본문·설교자·확인 근거를 기록한다.

구조가 흔들리지 않았는지 직전 날짜와 대조한다(출력이 비어야 정상):
```bash
diff <(grep -o '<[a-z][a-z0-9]*\( class="[^"]*"\)\?' archive/<직전날짜>/index.html | sed 's/ class=/./') \
     <(grep -o '<[a-z][a-z0-9]*\( class="[^"]*"\)\?' archive/YYYY-MM-DD/index.html | sed 's/ class=/./')
```

---

## 4. 카카오톡 썸네일 규칙 (반드시 지킬 것)

과거에 실제로 썸네일이 안 뜬 원인과 대책이다.

1. **`og:image`는 반드시 레포에 올린 자체 호스팅 이미지**를 절대 HTTPS 주소로 쓴다. `i.ytimg.com` 등 유튜브 CDN은 카카오 스크래퍼 요청을 차단하므로 절대 쓰지 않는다.
2. **카카오 OG 캐시는 자동 갱신되지 않는다.** URL이 잘못된 og:image로 한 번 스크랩되면 그 상태가 고착된다. 이미 공유한 URL을 고쳐야 하면 `kakao-v2.html`처럼 **새 URL을 발행**하거나, 사용자가 직접 https://developers.kakao.com/tool/clear/og 에서 캐시를 초기화해야 한다(카카오 로그인 필요 — 대신 해줄 수 없다).
3. 공유용 페이지에는 **`<base href>`를 넣지 않는다.** 스크래퍼가 상대경로를 잘못 해석할 수 있다. 경로는 페이지 기준 상대경로(`assets/background.jpg`, `../../assets/site.css`)로 쓴다.
4. **`<meta charset="utf-8">`을 `<head>` 최상단**에 둔다. 한글 OG 값 오파싱 방지.
5. 썸네일은 **1200×630 PNG(알파 없음, RGB)**, `og:image:width`/`height`/`type`/`alt` 명시.

필수 메타: `og:title`, `og:description`, `og:type=article`, `og:url`, `og:image`(+`:url`/`:secure_url`/`:type`/`:width`/`:height`/`:alt`), `og:locale=ko_KR`, `og:site_name`, `twitter:card=summary_large_image`, `twitter:title`/`description`/`image`, `link rel=canonical`, `link rel=image_src`, `meta name=thumbnail`.

---

## 5. 렌더 검수

브라우저가 있으면 직전 날짜와 나란히 렌더해 비교한다. **없으면 이 단계를 건너뛰고 6장의 정적 검사로 대체한다** (클라우드 환경에는 보통 없다).

```bash
CHROME=""
for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
         "$(command -v google-chrome)" "$(command -v chromium)" "$(command -v chromium-browser)"; do
  [ -n "$c" ] && [ -x "$c" ] && CHROME="$c" && break
done
if [ -n "$CHROME" ]; then
  (nohup python3 -m http.server 8765 >/tmp/qt-server.log 2>&1 &) ; sleep 1
  "$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars --window-size=1280,700 \
    --screenshot=/tmp/qt-new.png "http://localhost:8765/archive/YYYY-MM-DD/" 2>/dev/null
  pkill -f "http.server 8765"
  echo "Read 툴로 /tmp/qt-new.png 확인"
else
  echo "브라우저 없음 - 6장 정적 검사로 대체"
fi
```
(Browser pane은 localhost가 정책상 차단되므로 headless를 쓴다.)

정적 검사는 브라우저 유무와 무관하게 항상 수행한다:
```bash
for f in archive/YYYY-MM-DD/index.html archive/YYYY-MM-DD/kakao-v1.html index.html; do
  echo "--- $f"
  grep -c '<base' "$f" | sed 's/^/  base tags: /'
  grep -o 'og:image" content="[^"]*"\|embed/[A-Za-z0-9_-]*' "$f" | sort -u | sed 's/^/  /'
done
```
공유용 파일(`kakao-v1.html`, 루트 `index.html`)의 base tags는 `0`이어야 하고, og:image에 `ytimg`가 있으면 안 된다.

---

## 6. 커밋 & 푸시

```bash
git add -A && git status --short
git commit -m "DailyQT YYYY-MM-DD

<변경 요약 — 정정 사항이 있으면 반드시 명시>

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
git push origin main
git rev-list --left-right --count origin/main...main   # 0  0 이어야 함
```

푸시가 인증 문제로 실패하면 **조용히 넘어가지 말고** 실패 사실과 원인을 그대로 보고한다.

---

## 7. 배포 후 검증

Pages 반영을 기다린 뒤(폴링) 전 항목을 확인한다.

```bash
B=https://vidavida1970.github.io/DailyQT
until curl -s "$B/archive/YYYY-MM-DD/kakao-v1.html" | grep -q '<영상ID>'; do sleep 5; done
for u in "$B/archive/YYYY-MM-DD/kakao-v1.html" "$B/archive/YYYY-MM-DD/" "$B/" \
         "$B/archive/YYYY-MM-DD/assets/thumbnail-v1.png" "$B/archive/YYYY-MM-DD/assets/background.jpg" \
         "$B/source/YYYY-MM-DD.md" "$B/archive/"; do
  printf "%-52s " "${u#$B}"; curl -s -o /dev/null -w "%{http_code} %{content_type}\n" "$u"
done

UA='kakaotalk-scrap/1.0 (+https://devtalk.kakao.com/t/scrap/33984)'
curl -sI -A "$UA" "$B/archive/YYYY-MM-DD/assets/thumbnail-v1.png" | head -4
curl -s -A "$UA" "$B/archive/YYYY-MM-DD/kakao-v1.html" | grep -Eo '<meta property="og:[a-z:]*" content="[^"]*"'
```

체크리스트: HTTP 200 · 실행일 날짜 표기 · 3개 본문 장절 · 3개 iframe · YouTube 링크 · 배경 이미지 · OG 메타 · 썸네일 1200×630 · 공유용 `<base>` 없음 · 잘못된 날짜 영상 ID 미포함.

---

## 8. 최종 공유

간결하게 다음만 제공한다:

- 3개 소스별 **본문 장절 + 영상 제목/URL** (표)
- **카카오 공유용 링크** (`kakao-v1.html`) — 검증 완료 표시
- 기본 페이지 · 사이트 루트 링크
- GitHub 폴더 링크 · HTML 파일 링크 · 커밋 링크

검증에 실패한 항목이 있으면 완료라고 쓰지 말고 실패 지점과 사용자가 해야 할 조치를 명시한다.
