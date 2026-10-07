<div align="center">

<h3><code>matheus@github ~ $ ./contribuicoes.sh</code></h3>

<img src="./contrib-heatmap.svg" width="98.5%" alt="Gráfico de contribuições do último ano, atualizado todo dia"/>

<br><br>

<h3><code>matheus@github ~ $ neofetch</code></h3>

<img src="./matheus-ascii.svg" width="42.38%" alt="Monograma M em arte ASCII"/>
<img src="./info-card.svg" width="56.12%" alt="Matheus de Andrade Oliveira — Desenvolvedor Full Stack na Prefeitura Municipal de Japeri. Stack: TypeScript, React, Node.js, React Native, Flutter, PostgreSQL, AWS"/>

<br><br>

<h3><code>matheus@github ~ $ ls ~/projetos</code></h3>

<a href="https://github.com/matheusaoliv/Portfolio---Matheus-Oliveira"><code>portfolio/</code></a>&nbsp;
<a href="https://github.com/matheusaoliv/bicicletario-frontend"><code>bicicletario-frontend/</code></a>&nbsp;
<a href="https://github.com/matheusaoliv/Pokedex-2.0"><code>pokedex-2.0/</code></a>&nbsp;
<a href="https://github.com/matheusaoliv/Megapokedex"><code>megapokedex/</code></a>

</div>

<!--
Como funciona
- Toda a animação mora dentro dos .svg (o GitHub remove JS e CSS do README, mas anima SVG carregado via <img>).
- scripts/make_ascii_svg.py   -> matheus-ascii.svg  (gerado localmente; aceita foto: veja scripts/prep_photo.py)
- scripts/make_info_card.py   -> info-card.svg      (edite INFO no script)
- scripts/fetch_contributions.py + render_heatmap_svg.py -> contrib-heatmap.svg
- .github/workflows/update-profile-art.yml roda tudo isso todo dia e faz commit se algo mudou.
-->
