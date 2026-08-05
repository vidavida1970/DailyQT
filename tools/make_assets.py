#!/usr/bin/env python3
"""매일매일 큐티 당일 assets 생성 (로컬 macOS / 클라우드 Linux 공통).

background.jpg   1600x1000  새벽 산빛 플랫 그래픽
thumbnail-v1.png 1200x630   카카오/OG 공유 썸네일 (RGB, 알파 없음)

글꼴은 레포에 번들된 Noto Sans KR(OFL)을 쓴다. macOS 전용 폰트에 의존하지 않으므로
로컬과 클라우드 어디서 돌려도 결과가 동일하다.

사용 예:
  python3 tools/make_assets.py --out archive/2026-08-05/assets \
    --date 2026.08.05 \
    --title "맡겨진 자리에서," "회복의 반석을 붙들다" \
    --sub "충실히 섬기며 구원의 반석을 기억하십시오" \
    --refs "민수기 3:14–26 · 에스겔 36:1–15 · 이사야 17:1–14"

생성 후 반드시 PNG를 직접 열어 한글 깨짐·잘림·오탈자를 육안 검수할 것.
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "NotoSansKR-VF.ttf")

# 하우스 팔레트 (2026-08-04 판에서 실측)
THUMB_BG = (7, 29, 23)
C_EYEBROW = (190, 179, 139)
C_TITLE = (255, 255, 255)
C_SUB = (244, 221, 176)
C_REFS = (213, 224, 218)

SKY_TOP, SKY_MID, SKY_LOW = (22, 58, 74), (88, 101, 94), (150, 143, 114)
RIDGE_BACK, RIDGE_FRONT, RIDGE_FORE = (49, 90, 82), (17, 44, 37), (13, 35, 29)

# Noto 기준 좌표 — 참조판(2026-08-04) 텍스트 밴드에 맞춰 실측 보정한 값.
# 밴드 목표: 81-101 / 170-227 / 265-316 / 345-368 / 403-422
X = 92
Y_EYEBROW, Y_TITLE1, Y_TITLE2, Y_SUB, Y_REFS = 71, 146, 241, 336, 396
SZ_EYEBROW, SZ_TITLE, SZ_SUB, SZ_REFS = 23, 68, 27, 23
MAX_TEXT_W = 1150  # 이 폭을 넘으면 잘림 위험


def font(size, instance="Regular"):
    if not os.path.exists(FONT):
        sys.exit(f"글꼴을 찾을 수 없음: {FONT}\n레포의 tools/fonts/ 가 체크아웃됐는지 확인할 것.")
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_name(instance)
    return f


def make_background(out_dir):
    W, H, horizon = 1600, 1000, 620
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)

    for y in range(H):
        t = min(y / horizon, 1.0)
        if t < 0.5:
            a, b, k = SKY_TOP, SKY_MID, t / 0.5
        else:
            a, b, k = SKY_MID, SKY_LOW, (t - 0.5) / 0.5
        d.line([(0, y), (W, y)], fill=tuple(round(p + (q - p) * k) for p, q in zip(a, b)))

    d.polygon([(-120, 700), (260, 410), (500, 620), (720, 355),
               (940, 600), (1190, 385), (1720, 720), (1720, H), (-120, H)], fill=RIDGE_BACK)
    d.polygon([(-120, 820), (260, 575), (520, 715), (805, 512),
               (1085, 700), (1345, 555), (1720, 830), (1720, H), (-120, H)], fill=RIDGE_FRONT)
    d.polygon([(-120, 900), (320, 735), (610, 800), (925, 745),
               (1265, 828), (1720, 905), (1720, H), (-120, H)], fill=RIDGE_FORE)

    im.save(os.path.join(out_dir, "background.jpg"), "JPEG", quality=88, optimize=True)
    print(f"background.jpg   {im.size}")


def make_thumbnail(out_dir, date, title, sub, refs):
    im = Image.new("RGB", (1200, 630), THUMB_BG)
    d = ImageDraw.Draw(im)
    warn = []

    f = font(SZ_EYEBROW)
    x = X
    for ch in f"DAILY QT · {date}":
        d.text((x, Y_EYEBROW), ch, font=f, fill=C_EYEBROW)
        x += d.textlength(ch, font=f) + 0.4
    if x > MAX_TEXT_W:
        warn.append("eyebrow")

    ft = font(SZ_TITLE, "Light")
    for line, y in zip(title, (Y_TITLE1, Y_TITLE2)):
        d.text((X, y), line, font=ft, fill=C_TITLE)
        if X + d.textlength(line, font=ft) > MAX_TEXT_W:
            warn.append(f"title:{line}")

    for text, y, size, color in ((sub, Y_SUB, SZ_SUB, C_SUB), (refs, Y_REFS, SZ_REFS, C_REFS)):
        f = font(size)
        d.text((X, y), text, font=f, fill=color)
        if X + d.textlength(text, font=f) > MAX_TEXT_W:
            warn.append(text[:20])

    im.save(os.path.join(out_dir, "thumbnail-v1.png"), "PNG", optimize=True)
    print(f"thumbnail-v1.png {im.size} mode={im.mode}")
    if warn:
        print("WARNING: 1200px 폭을 넘어 잘릴 수 있음 -> " + ", ".join(warn), file=sys.stderr)
        return 1
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True, help="assets 출력 디렉터리")
    p.add_argument("--date", required=True, help="썸네일 표기용 날짜, 예: 2026.08.05")
    p.add_argument("--title", required=True, nargs=2, metavar=("LINE1", "LINE2"),
                   help="제목 2줄. 각 12자 내외 권장")
    p.add_argument("--sub", required=True, help="부제 한 줄")
    p.add_argument("--refs", required=True, help="본문 장절 3개, ' · ' 구분")
    a = p.parse_args()

    os.makedirs(a.out, exist_ok=True)
    make_background(a.out)
    rc = make_thumbnail(a.out, a.date, a.title, a.sub, a.refs)
    print("\n생성 완료. thumbnail-v1.png를 열어 육안 검수할 것.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
