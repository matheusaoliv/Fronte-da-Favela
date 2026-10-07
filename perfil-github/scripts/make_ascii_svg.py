"""Gera matheus-ascii.svg: arte ASCII que se digita linha por linha.

    python scripts/make_ascii_svg.py                      # monograma "M"
    python scripts/make_ascii_svg.py source-prepped.png   # retrato a partir de foto

Para foto, rode antes scripts/prep_photo.py (remove fundo e aumenta contraste).
Cada linha é revelada por uma "tampa" da cor do fundo que desliza para a
direita em passos de um caractere, com um cursor verde na borda. Toca uma vez
ao carregar e congela.
"""
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

from svgkit import ACCENT, BG, TEXT, TITLE_H, esc, window, write

RAMP = " .`:-=+*cs#%@"  # claro -> escuro; o espaço some no fundo

WIDTH, HEIGHT = 370, 400
PAD_X, PAD_Y = 22, 18
COLS = 56
ROW_H = 11

ART_W = WIDTH - 2 * PAD_X
CELL_W = ART_W / COLS
ROWS = int((HEIGHT - TITLE_H - 2 * PAD_Y) // ROW_H)
ART_H = ROWS * ROW_H
TOP = TITLE_H + (HEIGHT - TITLE_H - ART_H) / 2

FONTS = ["DejaVuSans-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf", "LiberationSans-Bold.ttf"]


def load_font(size):
    for name in FONTS:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def monogram(text="M"):
    """Letras grossas com degradê e sombra em 3D, sobre fundo branco."""
    scale = 4
    w, h = int(ART_W * scale), int(ART_H * scale)
    depth = int(h * 0.05)
    # Maior fonte que cabe na caixa contando a extrusão.
    probe = load_font(100)
    left, top, right, bottom = ImageDraw.Draw(Image.new("L", (1, 1))).textbbox((0, 0), text, font=probe)
    size = 100 * min((w * 0.92 - depth) / (right - left), (h * 0.9 - depth) / (bottom - top))
    font = load_font(int(size))
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    x = (w - (right - left) - depth) / 2 - left
    y = (h - (bottom - top) - depth) / 2 - top
    draw.text((x, y), text, fill=255, font=font)

    # Extrusão para baixo/direita: vira os caracteres médios (= + *).
    extrude = Image.new("L", (w, h), 0)
    for i in range(1, depth + 1, 2):
        extrude = ImageChops.lighter(extrude, ImageChops.offset(mask, i, i))

    # Face com degradê diagonal: escuro embaixo à esquerda, mais claro no topo.
    gradient = Image.linear_gradient("L").rotate(35, expand=False).resize((w, h))
    face = ImageOps.invert(gradient).point(lambda v: 10 + v * 0.45)

    img = Image.new("L", (w, h), 255)
    img.paste(170, mask=extrude)
    img.paste(face, mask=mask)
    # Contorno claro separa a face da extrusão.
    edge = mask.filter(ImageFilter.FIND_EDGES).point(lambda v: 255 if v > 40 else 0)
    edge = edge.filter(ImageFilter.MaxFilter(3))
    img.paste(235, mask=edge)
    return img


def from_photo(path):
    img = ImageOps.grayscale(Image.open(path))
    target = (int(ART_W * 4), int(ART_H * 4))
    return ImageOps.pad(img, target, color=255, centering=(0.5, 1.0))


def to_ascii(img):
    # Cada célula do terminal é ~2x mais alta que larga: reduz direto para COLS x ROWS.
    small = ImageOps.autocontrast(img.resize((COLS, ROWS), Image.Resampling.BOX), cutoff=1)
    px = small.load()
    return [
        "".join(RAMP[min(len(RAMP) - 1, (255 - px[x, y]) * len(RAMP) // 256)] for x in range(COLS))
        for y in range(ROWS)
    ]


def main():
    img = from_photo(sys.argv[1]) if len(sys.argv) > 1 else monogram()
    lines = to_ascii(img)

    css = f"""
.art {{ font-size: {CELL_W / 0.6:.2f}px; white-space: pre; }}
.cv {{ animation: wipe .6s steps({COLS + 1}, end) both; }}
@keyframes wipe {{ from {{ transform: translateX(0); }} to {{ transform: translateX({ART_W + CELL_W:.2f}px); }} }}
.cur {{ opacity: 0; animation: on .6s step-end; }}
@keyframes on {{ from, to {{ opacity: 1; }} }}
@media (prefers-reduced-motion: reduce) {{ .cv {{ display: none; }} }}
"""
    rows, covers = [], []
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        y = TOP + i * ROW_H
        delay = f"animation-delay:{0.2 + i * 0.075:.3f}s"
        rows.append(
            f'<text x="{PAD_X}" y="{y + ROW_H - 2.5:.2f}" textLength="{ART_W}" '
            f'lengthAdjust="spacing" xml:space="preserve">{esc(line)}</text>'
        )
        covers.append(
            f'<g class="cv" style="{delay}">'
            f'<rect x="{PAD_X - 1}" y="{y:.2f}" width="{ART_W + 2}" height="{ROW_H}" fill="{BG}"/>'
            f'<rect class="cur" style="{delay}" x="{PAD_X}" y="{y + 1:.2f}" width="{CELL_W:.2f}" height="{ROW_H - 2}" fill="{ACCENT}"/>'
            f"</g>"
        )

    defs = (
        f'<clipPath id="art"><rect x="{PAD_X - 1}" y="{TOP:.2f}" width="{ART_W + 2}" height="{ART_H}"/></clipPath>'
        f'<linearGradient id="ink" gradientUnits="userSpaceOnUse" x1="0" y1="{TOP:.2f}" x2="0" y2="{TOP + ART_H:.2f}">'
        f'<stop offset="0" stop-color="{TEXT}"/><stop offset="1" stop-color="#7d8590"/></linearGradient>'
    )
    body = (
        f'<g clip-path="url(#art)"><g class="art" fill="url(#ink)">{"".join(rows)}</g>'
        f'{"".join(covers)}</g>'
    )
    label = "Monograma M em arte ASCII" if len(sys.argv) == 1 else "Retrato em arte ASCII"
    write("matheus-ascii.svg", window(WIDTH, HEIGHT, "matheus@github: ~", label, body, css, defs))


if __name__ == "__main__":
    main()
