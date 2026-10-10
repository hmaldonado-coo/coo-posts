import json, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = sys.argv[1]  # repo root
W, H = 1080, 1350
BG = (22, 24, 28); AMBER = (255, 176, 32); WHITE = (245, 245, 245); GREY = (170, 174, 182)
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F = lambda p, s: ImageFont.truetype(p, s)
M = 90

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def render(path, tag, title, body, counter, tsize):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    for i in range(-2, 30):
        x = i * 60
        d.polygon([(x, 0), (x + 30, 0), (x + 10, 22), (x - 20, 22)], fill=AMBER)
    d.rectangle([0, 22, W, 26], fill=AMBER)
    d.text((M, 80), tag, font=F(B, 30), fill=AMBER)
    # auto-fit title (max 6 lines) and body (max 7 lines)
    while True:
        ft = F(B, tsize)
        tl = wrap(d, title, ft, W - 2 * M)
        if len(tl) <= 6 or tsize <= 56: break
        tsize -= 4
    y = 250
    for ln in tl:
        d.text((M, y), ln, font=ft, fill=WHITE); y += int(tsize * 1.22)
    d.rectangle([M, y + 20, M + 140, y + 28], fill=AMBER)
    y += 80
    fb = F(R, 44)
    for ln in wrap(d, body, fb, W - 2 * M):
        d.text((M, y), ln, font=fb, fill=GREY); y += 66
    assert y < H - 170, f"overflow {path}"
    d.text((M, H - 110), "@journeyofcoo", font=F(B, 32), fill=AMBER)
    if counter: d.text((W - M - 120, H - 110), counter, font=F(B, 32), fill=GREY)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)

TAGS = ["A JOURNEY OF A COO", "LESSON #1", "LESSON #2", "THE TAKEAWAY"]
CAL = json.load(open(os.path.join(ROOT, "posts", "week1.json")))
for p in CAL:
    folder = os.path.join(ROOT, "posts", p["folder"])
    if p["type"] == "carousel":
        n = len(p["slides"])
        for i, (t, b) in enumerate(p["slides"], 1):
            render(os.path.join(folder, f"slide_{i}.png"), TAGS[i - 1], t, b, f"{i}/{n}", 96 if i == 1 else 78)
    else:
        t, b = p["slides"][0]
        render(os.path.join(folder, "slide_1.png"), "REAL TALK", t, b, None, 88)
print("generated", len(CAL))
