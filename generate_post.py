from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

W, H = 1080, 1080

NAVY      = (6, 14, 40)
NAVY_MID  = (10, 28, 75)
TEAL      = (0, 195, 200)
TEAL_DARK = (0, 150, 158)
WHITE     = (255, 255, 255)

FONT_BOLD  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG   = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

SPLIT = 530   # Y where navy ends / teal begins
LOGO_SIZE = 240
LOGO_Y = SPLIT - LOGO_SIZE // 2   # logo centered on split line


def cx(draw, y, text, font, fill):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    draw.text(((W - tw) // 2, y), text, font=font, fill=fill)
    return th


# ── 1. BASE: navy top + teal bottom ──────────────────────────────────────────
img = Image.new("RGBA", (W, H), NAVY + (255,))
draw = ImageDraw.Draw(img)

# Navy gradient (top half)
for y in range(SPLIT):
    t = y / SPLIT
    r = int(NAVY[0] + (NAVY_MID[0] - NAVY[0]) * t)
    g = int(NAVY[1] + (NAVY_MID[1] - NAVY[1]) * t)
    b = int(NAVY[2] + (NAVY_MID[2] - NAVY[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

# Teal gradient (bottom half)
for y in range(SPLIT, H):
    t = (y - SPLIT) / (H - SPLIT)
    r = int(TEAL[0] + (TEAL_DARK[0] - TEAL[0]) * t)
    g = int(TEAL[1] + (TEAL_DARK[1] - TEAL[1]) * t)
    b = int(TEAL[2] + (TEAL_DARK[2] - TEAL[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b, 255))


# ── 2. DECORATIVE WAVES (faint, top area — eco del logo) ─────────────────────
for i, (amp, period, base_y, alpha) in enumerate([
    (16, 310, 370, 45),
    (12, 280, 415, 32),
    (18, 340, 460, 22),
]):
    wl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wl)
    for x in range(W - 1):
        y1 = base_y + int(amp * math.sin(x * 2 * math.pi / period + i * 1.1))
        y2 = base_y + int(amp * math.sin((x+1) * 2 * math.pi / period + i * 1.1))
        wd.line([(x, y1), (x+1, y2)], fill=(255, 255, 255, alpha), width=3)
    img = Image.alpha_composite(img, wl)


# ── 3. HEADLINE (top / navy area) ────────────────────────────────────────────
draw = ImageDraw.Draw(img)

f90 = ImageFont.truetype(FONT_BOLD, 92)
f38 = ImageFont.truetype(FONT_REG, 38)
f34 = ImageFont.truetype(FONT_BOLD, 34)
f26 = ImageFont.truetype(FONT_REG, 26)
f22 = ImageFont.truetype(FONT_REG, 22)

# Small label above
label = "S E N D A C R E D I T   G R O U P"
f20b = ImageFont.truetype(FONT_BOLD, 20)
bb = draw.textbbox((0,0), label, font=f20b)
tw = bb[2] - bb[0]
lx = (W - tw) // 2
# Teal pill behind label
draw.rounded_rectangle([lx - 18, 62, lx + tw + 18, 62 + 36], radius=18,
                        fill=(0, 195, 200, 60))
draw.text((lx, 65), label, font=f20b, fill=TEAL)

# Big headline
h1 = cx(draw, 118, "Tu dinero", f90, WHITE)
cx(draw, 118 + h1 + 4, "merece volver.", f90, TEAL)

# Sub-headline
cx(draw, 330, "Gestionamos tus deudas pendientes de forma", f38, (200, 225, 255))
cx(draw, 330 + 48, "cercana, profesional y siempre amistosa.", f38, (200, 225, 255))


# ── 4. LOGO (centered on the split) ──────────────────────────────────────────
# Soft white halo behind logo
halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(halo)
hr = LOGO_SIZE // 2 + 24
hd.ellipse(
    [(W//2 - hr, LOGO_Y - 24), (W//2 + hr, LOGO_Y + LOGO_SIZE + 24)],
    fill=(255, 255, 255, 30)
)
img = Image.alpha_composite(img, halo.filter(ImageFilter.GaussianBlur(18)))

logo = Image.open(
    "/root/.claude/uploads/4429211d-2678-5ac4-878e-30396e595de5/280683d0-IMG_0816.png"
).convert("RGBA").resize((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)
img.paste(logo, ((W - LOGO_SIZE) // 2, LOGO_Y), logo)

draw = ImageDraw.Draw(img)


# ── 5. BOTTOM TEAL AREA ──────────────────────────────────────────────────────
# Three benefit pills
pills = ["Sin cuotas fijas", "Vía amistosa", "Sin compromiso"]
pill_colors = [(255, 255, 255, 50), (255, 255, 255, 50), (255, 255, 255, 50)]
f_pill = ImageFont.truetype(FONT_BOLD, 26)

total_pills_w = 0
pill_sizes = []
for p in pills:
    bb = draw.textbbox((0,0), p, font=f_pill)
    pw = bb[2] - bb[0] + 40
    pill_sizes.append(pw)
    total_pills_w += pw
gap = (W - total_pills_w - 60) // (len(pills) - 1)
px = 30
PILL_Y = SPLIT + 74

for p, pw in zip(pills, pill_sizes):
    pill_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pill_layer)
    pd.rounded_rectangle([px, PILL_Y, px + pw, PILL_Y + 46], radius=23,
                          fill=(255, 255, 255, 55))
    img = Image.alpha_composite(img, pill_layer)
    draw = ImageDraw.Draw(img)
    bb = draw.textbbox((0,0), p, font=f_pill)
    tx = px + (pw - (bb[2]-bb[0])) // 2
    ty = PILL_Y + (46 - (bb[3]-bb[1])) // 2
    draw.text((tx, ty), p, font=f_pill, fill=NAVY)
    px += pw + gap

# Divider
draw.line([(120, PILL_Y + 68), (W - 120, PILL_Y + 69)], fill=(255, 255, 255, 50), width=1)

# CTA button (white, navy text)
CTA_Y = PILL_Y + 90
CTA_H = 76
cta_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(cta_layer)
cd.rounded_rectangle([200, CTA_Y, W - 200, CTA_Y + CTA_H], radius=38, fill=WHITE + (255,))
img = Image.alpha_composite(img, cta_layer)
draw = ImageDraw.Draw(img)
cta_txt = "Solicita tu consulta gratuita  →"
bb = draw.textbbox((0,0), cta_txt, font=f34)
tw, th = bb[2]-bb[0], bb[3]-bb[1]
draw.text(((W-tw)//2, CTA_Y + (CTA_H - th)//2), cta_txt, font=f34, fill=NAVY)

# Web
cx(draw, CTA_Y + CTA_H + 28, "sendacreditgroup.com", f26, (10, 40, 90))

# Hashtags
cx(draw, CTA_Y + CTA_H + 68,
   "#SendacreditGroup   #RecobrosAmistosos   #GestiónDeImpagados",
   f22, (8, 35, 75))


# ── 6. SAVE ───────────────────────────────────────────────────────────────────
img.convert("RGB").save("/home/user/alepixel-web/sendacredit_post_v2.jpg", "JPEG", quality=96)
print("Done.")
