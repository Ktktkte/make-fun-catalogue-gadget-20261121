#!/usr/bin/env python3
"""Draw the ToastMail 3000 catalogue photograph (1024x1024 PNG).

Everything is drawn from scratch with Pillow: no downloaded photos, no
copied images. A chrome two-slot toaster that toasts your unread emails
onto bread, shot as a studio catalogue product photo: clean seamless
background, soft shadow, faint reflection, one accessory (a butter knife).
"""
import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1024, 1024
HORIZON = 720  # surface line

FDIR = "/usr/share/fonts/truetype/dejavu/"
SANS = "DejaVuSans.ttf"
SANSB = "DejaVuSans-Bold.ttf"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


random.seed(7)

# ---------------------------------------------------------------- background
# Vertical gradient: slightly darker warm grey at the top, lighter at the
# bottom, with a barely darker surface below the horizon line.
top = (214, 209, 200)
bottom = (238, 235, 228)
surf_top = (228, 224, 214)
surf_bottom = (240, 236, 229)

img = Image.new("RGB", (W, H))
px = img.load()
for y in range(H):
    if y < HORIZON:
        t = y / HORIZON
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    else:
        t = (y - HORIZON) / (H - HORIZON)
        c = tuple(int(surf_top[i] + (surf_bottom[i] - surf_top[i]) * t) for i in range(3))
    for x in range(W):
        px[x, y] = c

d = ImageDraw.Draw(img, "RGBA")

# Warm key light from the upper left: a very soft bright wash.
wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
wd = ImageDraw.Draw(wash)
wd.ellipse((-350, -350, 700, 550), fill=(255, 244, 220, 34))
wash = wash.filter(ImageFilter.GaussianBlur(180))
img.paste(Image.alpha_composite(img.convert("RGBA"), wash).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# ------------------------------------------------------------------ toaster
# Front face: x 250..774, y 420..700. Slight three-quarter angle: a thin
# right side face and a slanted top face.
FX0, FX1, FY0, FY1 = 250, 774, 420, 700
SIDE_DX, TOP_DY = 26, 28  # side face width, top face depth


def rounded_rect(draw, box, r, **kw):
    draw.rounded_rectangle(box, radius=r, **kw)


# --- chrome front face: horizontal brushed-metal gradient
grad = Image.new("RGB", (FX1 - FX0, 1))
stops = [(0.00, (176, 181, 188)), (0.18, (238, 241, 244)), (0.38, (196, 201, 208)),
         (0.55, (150, 155, 162)), (0.72, (228, 231, 235)), (0.88, (164, 169, 176)),
         (1.00, (210, 214, 219))]
gx = grad.load()
gw = FX1 - FX0
for x in range(gw):
    t = x / gw
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0) if t1 > t0 else 0
            gx[x, 0] = tuple(int(c0[j] + (c1[j] - c0[j]) * f) for j in range(3))
            break
grad = grad.resize((gw, FY1 - FY0))
mask = Image.new("L", (gw, FY1 - FY0), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle((0, 0, gw - 1, FY1 - FY0 - 1), radius=26, fill=255)
img.paste(grad, (FX0, FY0), mask)
d = ImageDraw.Draw(img, "RGBA")

# Brushed-metal vertical streaks on the front face.
for _ in range(240):
    x = random.randint(FX0 + 4, FX1 - 4)
    y0 = random.randint(FY0 + 8, FY1 - 60)
    ln = random.randint(20, 120)
    a = random.randint(6, 16)
    col = (255, 255, 255, a) if random.random() < 0.5 else (90, 95, 105, a)
    d.line((x, y0, x, min(y0 + ln, FY1 - 6)), fill=col, width=1)

# Soft diagonal highlight band across the front face.
hl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(hl)
hd.polygon([(300, FY0), (430, FY0), (330, FY1), (200, FY1)], fill=(255, 255, 255, 26))
hl = hl.filter(ImageFilter.GaussianBlur(18))
img.paste(Image.alpha_composite(img.convert("RGBA"), hl).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# Front face outline (thin, dark) + black base strip.
d.rounded_rectangle((FX0, FY0, FX1, FY1), radius=26, outline=(70, 76, 84, 255), width=2)
d.rounded_rectangle((FX0 + 6, FY1 - 26, FX1 - 6, FY1), radius=10, fill=(28, 30, 34, 255))

# --- right side face (parallelogram) and top face
side = [(FX1, FY0), (FX1 + SIDE_DX, FY0 - TOP_DY), (FX1 + SIDE_DX, FY1 - TOP_DY - 8),
        (FX1, FY1 - 8)]
d.polygon(side, fill=(148, 153, 160, 255), outline=(70, 76, 84, 255))
topf = [(FX0, FY0), (FX1, FY0), (FX1 + SIDE_DX, FY0 - TOP_DY), (FX0 + SIDE_DX, FY0 - TOP_DY)]
d.polygon(topf, fill=(188, 193, 200, 255), outline=(70, 76, 84, 255))

# --- slots on the top face (dark, skewed to match the top face)
for sx0, sx1 in ((330, 470), (560, 700)):
    # skew: +8 px over the slot height
    d.polygon([(sx0, FY0 - 20), (sx1, FY0 - 20), (sx1 + 8, FY0 - 8), (sx0 + 8, FY0 - 8)],
              fill=(24, 24, 28, 255))

# --- toast slices rising from the slots
BREAD = (232, 196, 130)
CRUST = (146, 94, 42)
TOASTED = (122, 74, 30)


def toast_slice(x0, x1, y0, y1, r=22):
    """A slice of toast: crust border, lighter crumb, toasted top edge."""
    d.rounded_rectangle((x0, y0, x1, y1), radius=r, fill=CRUST)
    d.rounded_rectangle((x0 + 9, y0 + 9, x1 - 9, y1 - 4), radius=r - 8, fill=BREAD)
    # light toasting blotches
    for _ in range(26):
        bx = random.randint(x0 + 16, x1 - 16)
        by = random.randint(y0 + 16, y1 - 20)
        br = random.randint(4, 12)
        d.ellipse((bx - br, by - br, bx + br, by + br),
                  fill=(196, 150, 88, 70))
    d.rounded_rectangle((x0, y0, x1, y1), radius=r, outline=(120, 76, 32, 255), width=2)


# Left slice pops high: envelope + UNREAD count toasted on it.
toast_slice(332, 478, 246, 424)
# envelope glyph
ex0, ey0, ex1, ey1 = 362, 282, 448, 332
d.rectangle((ex0, ey0, ex1, ey1), outline=TOASTED, width=4)
d.line((ex0, ey0, (ex0 + ex1) // 2, (ey0 + ey1) // 2 + 8), fill=TOASTED, width=4)
d.line((ex1, ey0, (ex0 + ex1) // 2, (ey0 + ey1) // 2 + 8), fill=TOASTED, width=4)
f_unread = font(SANSB, 19)
for i, line in enumerate(("UNREAD:", "12,402")):
    lw = d.textlength(line, font=f_unread)
    d.text(((332 + 478) / 2 - lw / 2, 348 + i * 24), line, font=f_unread, fill=TOASTED)

# Right slice sits lower: a single toasted "@".
toast_slice(562, 708, 306, 424)
f_at = font(SANSB, 54)
at = "@"
aw = d.textlength(at, font=f_at)
d.text(((562 + 708) / 2 - aw / 2, 330), at, font=f_at, fill=TOASTED)

# --- lever on the right side face, pushed down
d.polygon([(FX1 + 2, 520), (FX1 + SIDE_DX - 2, 520 - 4), (FX1 + SIDE_DX - 2, 532 - 4),
           (FX1 + 2, 532)], fill=(90, 94, 102, 255))
d.ellipse((FX1 + SIDE_DX - 12, 512, FX1 + SIDE_DX + 6, 540), fill=(30, 32, 36, 255))

# --- browning dial on the front face
cx, cy, r = 700, 596, 27
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(38, 40, 44, 255),
          outline=(220, 224, 228, 255), width=2)
for k in range(7):
    ang = math.radians(-120 + k * 40)
    x0 = cx + (r - 8) * math.cos(ang)
    y0 = cy + (r - 8) * math.sin(ang)
    x1 = cx + (r - 2) * math.cos(ang)
    y1 = cy + (r - 2) * math.sin(ang)
    d.line((x0, y0, x1, y1), fill=(220, 224, 228, 255), width=2)
ang = math.radians(-40)
d.line((cx, cy, cx + (r - 6) * math.cos(ang), cy + (r - 6) * math.sin(ang)),
       fill=(240, 120, 60, 255), width=3)

# --- brand on the front face: product text only
f_brand = font(SANSB, 30)
brand = "TOASTMAIL"
# manual letter spacing
letters = list(brand)
widths = [d.textlength(ch, font=f_brand) for ch in letters]
gap = 4
total_w = sum(widths) + gap * (len(letters) - 1)
x = (FX0 + FX1) / 2 - total_w / 2
for ch, wch in zip(letters, widths):
    d.text((x, 622), ch, font=f_brand, fill=(52, 58, 66, 255))
    x += wch + gap
f_model = font(SANS, 18)
d.text(((FX0 + FX1) / 2 - d.textlength("3000", font=f_model) / 2, 656),
       "3000", font=f_model, fill=(92, 98, 106, 255))

# ------------------------------------------------------------------- shadow
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sh)
sd.ellipse((236, 688, 812, 736), fill=(60, 55, 48, 110))
sh = sh.filter(ImageFilter.GaussianBlur(14))
img.paste(Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# --------------------------------------------------------------- reflection
# Faint flipped copy of the toaster body below the surface line, fading out.
body = img.crop((FX0, FY0, FX1 + SIDE_DX, FY1)).transpose(Image.FLIP_TOP_BOTTOM)
body = body.convert("RGBA")
fade = Image.new("L", body.size, 0)
fd = ImageDraw.Draw(fade)
for y in range(body.size[1]):
    a = int(58 * (1 - y / body.size[1]))
    fd.line((0, y, body.size[0], y), fill=a)
body.putalpha(Image.composite(body.split()[3], Image.new("L", body.size, 0), fade))
refl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
refl.paste(body, (FX0, FY1 - 2), body)
refl = refl.filter(ImageFilter.GaussianBlur(3))
img.paste(Image.alpha_composite(img.convert("RGBA"), refl).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# ------------------------------------------------------------- butter knife
# The ONE accessory: a single butter knife lying flat on the surface to the
# right of the toaster, blade catching a highlight. Slight diagonal.
kx, ky, klen, kwid, kang = 812, 758, 190, 18, -8
rad = math.radians(kang)
ux, uy = math.cos(rad), math.sin(rad)
vx, vy = -uy, ux
base = (kx, ky)
tip = (kx + klen * ux, ky + klen * uy)


def pt(t, s):
    return (base[0] + t * ux + s * vx, base[1] + t * uy + s * vy)


# handle (dark) + blade (bright steel)
d.polygon([pt(0, -kwid // 2), pt(52, -kwid // 2), pt(52, kwid // 2), pt(0, kwid // 2)],
          fill=(44, 44, 48, 255))
d.polygon([pt(52, -kwid // 2), pt(klen - 14, -kwid // 2), pt(klen, 0), pt(klen - 14, kwid // 2),
           pt(52, kwid // 2)], fill=(214, 218, 224, 255), outline=(120, 126, 134, 255))
d.line([pt(56, -kwid // 2 + 3), pt(klen - 20, -kwid // 2 + 3)], fill=(255, 255, 255, 200), width=2)
# tiny shadow under the knife
d.line([pt(2, kwid // 2 + 4), pt(klen - 2, kwid // 2 + 4)], fill=(90, 84, 76, 90), width=3)

img.save("entry.png", "PNG")
print("saved entry.png", img.size)
