from PIL import Image, ImageDraw, ImageFont
import textwrap, sys, os

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
BG = (22, 24, 28)
AMBER = (255, 176, 32)
WHITE = (245, 245, 245)
GREY = (170, 174, 182)
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(p, s): return ImageFont.truetype(p, s)

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def slide(n, total, title, body, tag, fname, title_size=84):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    # hazard stripe top
    for i in range(-2, 30):
        x = i * 60
        d.polygon([(x, 0), (x + 30, 0), (x + 10, 22), (x - 20, 22)], fill=AMBER)
    d.rectangle([0, 22, W, 26], fill=AMBER)
    m = 90
    d.text((m, 80), tag, font=font(B, 30), fill=AMBER)
    ft = font(B, title_size)
    y = 260
    for ln in wrap(d, title, ft, W - 2 * m):
        d.text((m, y), ln, font=ft, fill=WHITE)
        y += int(title_size * 1.22)
    d.rectangle([m, y + 20, m + 140, y + 28], fill=AMBER)
    y += 80
    fb = font(R, 44)
    for ln in wrap(d, body, fb, W - 2 * m):
        d.text((m, y), ln, font=fb, fill=GREY)
        y += 66
    d.text((m, H - 110), "@journeyofcoo", font=font(B, 32), fill=AMBER)
    d.text((W - m - 120, H - 110), f"{n}/{total}", font=font(B, 32), fill=GREY)
    im.save(os.path.join(OUT, fname))

S = [
 ("Every project runs late.", "The biggest lesson running operations has taught me. Swipe.", "A JOURNEY OF A COO", 96),
 ("Delays aren't the exception. They're the rule.", "Materials show up late. Other trades fall behind. Someone else is working in your space. It happens on every single job.", "LESSON #1", 78),
 ("Never price a job on the best case.", "Quote the work plus the delays. Nobody pays you to stand around, so build the cushion in before you say yes.", "LESSON #2", 78),
 ("Plan for the delay. Protect your people. Protect your margin.", "Real talk on running operations. No highlight reel. Follow along.", "THE TAKEAWAY", 72),
]
for i, (t, b, tag, sz) in enumerate(S, 1):
    slide(i, len(S), t, b, tag, f"coo_{i}.png", sz)
print("done")
