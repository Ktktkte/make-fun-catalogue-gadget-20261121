#!/usr/bin/env python3
"""Draw entry.png: a studio catalogue photograph of the ToastMail 3000 —
a chrome two-slot toaster that toasts your unread emails onto bread.
Everything is drawn from scratch with Pillow. No photo, no copied image."""

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))


def font(size, bold=False):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def vgrad(size, top, bottom):
    """Vertical gradient image."""
    w, h = size
    base = Image.new("RGB", (1, h))
    px = base.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return base.resize((w, h))


def rounded(draw, box, radius, **kw):
    draw.rounded_rectangle(box, radius=radius, **kw)


img = vgrad((W, H), (224, 219, 209), (246, 242, 233))
d = ImageDraw.Draw(img, "RGBA")

# ---- studio floor: surface line + soft contact shadow under the toaster ----
floor_y = 742
d.rectangle([0, floor_y, W, H], fill=(238, 233, 224, 255))
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([225, 700, 845, 790], fill=(60, 52, 40, 90))
shadow = shadow.filter(ImageFilter.GaussianBlur(16))
img.paste(Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# ---- faint reflection of the toaster on the floor ----
refl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(refl)
rd.rectangle([262, floor_y, 812, 800], fill=(150, 148, 142, 38))
refl = refl.filter(ImageFilter.GaussianBlur(6))
img.paste(Image.alpha_composite(img.convert("RGBA"), refl).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# ---- toaster body (front face): brushed chrome ----
body = [262, 430, 812, 742]
chrome = vgrad((body[2] - body[0], body[3] - body[1]), (228, 230, 232), (178, 182, 186))
img.paste(chrome, (body[0], body[1]))
d = ImageDraw.Draw(img, "RGBA")
# brushed-metal streaks: faint vertical lines
for x in range(body[0] + 8, body[2] - 8, 7):
    shade = 205 + ((x * 37) % 23)
    d.line([x, body[1] + 6, x, body[3] - 6], fill=(shade, shade + 2, shade + 4, 40), width=1)
# soft highlight band from the upper-left key light
hl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(hl)
hd.polygon([(300, 430), (470, 430), (400, 742), (290, 742)], fill=(255, 255, 255, 42))
hl = hl.filter(ImageFilter.GaussianBlur(12))
img.paste(Image.alpha_composite(img.convert("RGBA"), hl).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")
d.rounded_rectangle(body, radius=26, outline=(120, 124, 128, 255), width=3)

# ---- top face + slots ----
d.polygon([(262, 430), (812, 430), (838, 402), (288, 402)], fill=(196, 198, 202, 255))
d.polygon([(262, 430), (812, 430), (838, 402), (288, 402)], outline=(120, 124, 128, 255))
d.rounded_rectangle([330, 406, 500, 430], radius=8, fill=(38, 36, 34, 255))
d.rounded_rectangle([574, 406, 744, 430], radius=8, fill=(38, 36, 34, 255))

# ---- three-quarter side face (right) ----
d.polygon([(812, 430), (838, 402), (838, 700), (812, 742)], fill=(158, 161, 165, 255))
d.polygon([(812, 430), (838, 402), (838, 700), (812, 742)], outline=(110, 114, 118, 255))
# side lever, pushed down
d.rounded_rectangle([824, 560, 852, 606], radius=10, fill=(52, 54, 58, 255))
d.ellipse([828, 588, 850, 610], fill=(210, 212, 214, 255))

# ---- black base ----
d.rounded_rectangle([262, 700, 812, 742], radius=22, fill=(28, 28, 30, 255))
d.rectangle([262, 700, 812, 716], fill=(28, 28, 30, 255))

# ---- toast slice 1: popped up, envelope + UNREAD count ----
t1 = [338, 238, 492, 424]
d.rounded_rectangle(t1, radius=22, outline=(146, 96, 34, 255), width=7)
d.rounded_rectangle([t1[0] + 7, t1[1] + 7, t1[2] - 7, t1[3] - 7], radius=16,
                    fill=(232, 184, 110, 255))
# toast speckle
import random
random.seed(3000)
for _ in range(90):
    x = random.randint(t1[0] + 14, t1[2] - 14)
    y = random.randint(t1[1] + 14, t1[3] - 14)
    r = random.randint(2, 6)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(206, 150, 74, 90))
# envelope glyph
ex0, ey0, ex1, ey1 = 372, 268, 458, 316
d.rectangle([ex0, ey0, ex1, ey1], outline=(122, 74, 22, 255), width=4)
d.line([ex0, ey0, 415, ey0 + 26], fill=(122, 74, 22, 255), width=4)
d.line([ex1, ey0, 415, ey0 + 26], fill=(122, 74, 22, 255), width=4)
# toasted text on the slice
f_small = font(24, bold=True)
d.text((415, 352), "UNREAD:", font=f_small, fill=(122, 74, 22, 255), anchor="ma")
d.text((415, 382), "12,402", font=f_small, fill=(122, 74, 22, 255), anchor="ma")

# ---- toast slice 2: second slot, toasted "@" ----
t2 = [582, 292, 700, 424]
d.rounded_rectangle(t2, radius=18, outline=(146, 96, 34, 255), width=6)
d.rounded_rectangle([t2[0] + 6, t2[1] + 6, t2[2] - 6, t2[3] - 6], radius=13,
                    fill=(226, 178, 104, 255))
for _ in range(60):
    x = random.randint(t2[0] + 12, t2[2] - 12)
    y = random.randint(t2[1] + 12, t2[3] - 12)
    r = random.randint(2, 5)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(200, 146, 72, 90))
f_big = font(64, bold=True)
d.text((641, 348), "@", font=f_big, fill=(122, 74, 22, 255), anchor="mm")

# ---- browning dial ----
cx, cy, r = 706, 612, 34
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 30, 32, 255),
          outline=(200, 202, 204, 255), width=2)
for k in range(7):
    import math
    a = math.radians(-120 + k * 40)
    x0 = cx + (r - 4) * math.cos(a); y0 = cy + (r - 4) * math.sin(a)
    x1 = cx + (r - 12) * math.cos(a); y1 = cy + (r - 12) * math.sin(a)
    d.line([x0, y0, x1, y1], fill=(220, 222, 224, 255), width=2)
a = math.radians(-30)
d.line([cx, cy, cx + (r - 8) * math.cos(a), cy + (r - 8) * math.sin(a)],
       fill=(232, 120, 40, 255), width=4)
d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(220, 222, 224, 255))

# ---- brand: product text only ----
f_brand = font(34, bold=True)
d.text((520, 640), "TOASTMAIL", font=f_brand, fill=(44, 48, 52, 255), anchor="ma")
f_model = font(20)
d.text((520, 678), "3000", font=f_model, fill=(90, 94, 98, 255), anchor="ma")

# ---- the ONE accessory: a butter knife, lying flat to the right ----
knife = Image.new("RGBA", (260, 60), (0, 0, 0, 0))
kd = ImageDraw.Draw(knife)
kd.rounded_rectangle([8, 22, 96, 40], radius=8, fill=(40, 40, 42, 255))      # handle
kd.polygon([(96, 20), (232, 16), (252, 30), (232, 44), (96, 40)],           # blade
           fill=(208, 210, 212, 255))
kd.line([100, 24, 228, 21], fill=(255, 255, 255, 200), width=3)              # blade highlight
kd = ImageDraw.Draw(knife)
knife = knife.rotate(-14, expand=True, resample=Image.BICUBIC)
kshadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ksd = ImageDraw.Draw(kshadow)
ksd.ellipse([740, 770, 890, 800], fill=(60, 52, 40, 70))
kshadow = kshadow.filter(ImageFilter.GaussianBlur(8))
img.paste(Image.alpha_composite(img.convert("RGBA"), kshadow).convert("RGB"), (0, 0))
img.paste(knife, (720, 748), knife)

img = img.convert("RGB")
img.save(os.path.join(HERE, "entry.png"), "PNG")
print("wrote entry.png", img.size, os.path.getsize(os.path.join(HERE, "entry.png")), "bytes")
