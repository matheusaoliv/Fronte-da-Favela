"""Visual compartilhado pelos SVGs do perfil: janela de terminal, cores e fontes.

O GitHub remove <script> e quase todo CSS do README, mas renderiza SVGs
embutidos via <img> e executa as animações CSS que estão *dentro* deles.
Por isso toda a animação mora nos arquivos .svg gerados por estes scripts.
"""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

# Imagens carregadas via <img> não podem baixar fontes externas: usamos a
# melhor monoespaçada disponível no sistema de quem está visitando.
FONT = ("'SFMono-Regular', ui-monospace, Menlo, Consolas, "
        "'Liberation Mono', 'DejaVu Sans Mono', monospace")

BG = "#0d1117"
BAR = "#161b22"
BORDER = "#30363d"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
ACCENT = "#39d353"
YELLOW = "#e3b341"
BLUE = "#58a6ff"

TITLE_H = 32
RADIUS = 10

# Quem pede menos movimento no sistema vê direto o quadro final.
REDUCED_MOTION = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def esc(text):
    return escape(str(text), {'"': "&quot;"})


def window(width, height, title, label, body, css="", defs=""):
    """Envolve `body` numa janela de terminal (barra de título + bolinhas)."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t">
<title id="t">{esc(label)}</title>
<style>
text {{ font-family: {FONT}; }}
{css}
{REDUCED_MOTION}
</style>
<defs>
<clipPath id="win"><rect width="{width}" height="{height}" rx="{RADIUS}"/></clipPath>
{defs}
</defs>
<g clip-path="url(#win)">
<rect width="{width}" height="{height}" fill="{BG}"/>
<rect width="{width}" height="{TITLE_H}" fill="{BAR}"/>
<line x1="0" y1="{TITLE_H}.5" x2="{width}" y2="{TITLE_H}.5" stroke="{BORDER}"/>
<circle cx="18" cy="16" r="6" fill="#ff5f57"/>
<circle cx="38" cy="16" r="6" fill="#febc2e"/>
<circle cx="58" cy="16" r="6" fill="#28c840"/>
<text x="{width / 2:g}" y="20.5" fill="{MUTED}" font-size="12" text-anchor="middle">{esc(title)}</text>
{body}
</g>
<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="{RADIUS}" fill="none" stroke="{BORDER}"/>
</svg>
"""


def write(name, svg):
    path = ROOT / name
    path.write_text(svg, encoding="utf-8")
    print(f"ok: {path.relative_to(ROOT)} ({len(svg.encode()) / 1024:.1f} KB)")
