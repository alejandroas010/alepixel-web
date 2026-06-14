from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080

BLUE_DARK  = (13,  45, 110)
BLUE_MID   = (26,  90, 170)
TEAL       = (0,  188, 196)
WHITE      = (255, 255, 255)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def draw_centered(draw, y, text, font, fill, spacing=10):
    """Draw single-line centered text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]  # return height


def draw_centered_block(draw, y, lines, font, fill, spacing=12):
    """Draw multiple lines centered."""
    fh = draw.textbbox((0, 0), "Ag", font=font)[3]
    for line in lines:
        draw_centered(draw, y, line, font, fill)
        y += fh + spacing
    return y


# --- Fondo degradado ---
img = Image.new("RGBA", (W, H))
draw = ImageDraw.Draw(img)

for y in range(H):
    t = y / H
    r = int(BLUE_DARK[0] + (BLUE_MID[0] - BLUE_DARK[0]) * t)
    g = int(BLUE_DARK[1] + (BLUE_MID[1] - BLUE_DARK[1]) * t)
    b = int(BLUE_DARK[2] + (BLUE_MID[2] - BLUE_DARK[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

# --- Círculos decorativos ---
for layer_data in [
    ((700, 650, 1250, 1200), (0, 188, 196, 40)),
    ((780, 720, 1180, 1120), (0, 188, 196, 22)),
    ((-200, -200, 400, 400), (26, 90, 170, 50)),
]:
    cl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(cl).ellipse(layer_data[0], fill=layer_data[1])
    img = Image.alpha_composite(img, cl)

draw = ImageDraw.Draw(img)

# --- Logo ---
logo = Image.open(
    "/root/.claude/uploads/4429211d-2678-5ac4-878e-30396e595de5/280683d0-IMG_0816.png"
).convert("RGBA")
logo_size = 260
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, ((W - logo_size) // 2, 90), logo)

# --- Línea teal ---
lw = 80
draw.rounded_rectangle([(W - lw) // 2, 400, (W + lw) // 2, 406], radius=3, fill=TEAL)

# --- Titular ---
f_title = ImageFont.truetype(FONT_BOLD, 56)
title_lines = [
    "A veces, cobrar lo que te deben",
    "solo necesita el enfoque correcto.",
]
draw_centered_block(draw, 430, title_lines, f_title, WHITE, spacing=14)

# --- Separador ---
draw.rounded_rectangle([360, 610, 720, 613], radius=2, fill=(255, 255, 255, 50))

# --- Subtítulo ---
f_sub = ImageFont.truetype(FONT_REG, 33)
sub_lines = [
    "Gestionamos tus deudas pendientes de forma",
    "cercana, profesional y siempre amistosa. ✅",
]
draw_centered_block(draw, 635, sub_lines, f_sub, (200, 230, 255), spacing=12)

# --- CTA pill ---
pill_y = 820
pill_h = 74
pill_x1, pill_x2 = 250, 830
draw.rounded_rectangle([pill_x1, pill_y, pill_x2, pill_y + pill_h], radius=37, fill=TEAL)
f_cta = ImageFont.truetype(FONT_BOLD, 31)
cta_text = "Primera consulta gratuita  →"
bbox = draw.textbbox((0, 0), cta_text, font=f_cta)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
draw.text(((W - tw) // 2, pill_y + (pill_h - th) // 2), cta_text, font=f_cta, fill=BLUE_DARK)

# --- Web ---
f_web = ImageFont.truetype(FONT_REG, 27)
draw_centered(draw, 930, "sendacreditgroup.com", f_web, (180, 220, 255))

# --- Hashtags ---
f_hash = ImageFont.truetype(FONT_REG, 21)
draw_centered(
    draw, 978,
    "#SendacreditGroup   #RecobrosAmistosos   #GestiónDeImpagados",
    f_hash, (110, 170, 215)
)

# --- Guardar ---
img.convert("RGB").save("/home/user/alepixel-web/sendacredit_post.jpg", "JPEG", quality=95)
print("Imagen generada correctamente.")
