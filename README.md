# Tablero — sitio web (tablero.uno)

Sitio estático (HTML + CSS + JS sin dependencias), desplegado tal cual en Vercel.

## Estructura
- `index.html` — home. Los bloques entre `<!--@@NOMBRE-->…<!--@@/NOMBRE-->` los genera `tools/build.py`; el resto se edita a mano.
- `assets/` — CSS (`css/site.css`), imágenes WebP, video del hero, favicons.
- Carpetas con `index.html` (`modulos/`, `blog/`, etc.) — generadas; **no editar a mano**.
- `tools/` — generador: `content.py` (módulos y FAQ), `pages.py` (páginas), `blog.py` (artículos), `build.py`.
- `docs/` — Search Console, checklist semanal SEO, textos de difusión y publicación automática (no se despliegan).
- `tools/social/` — autorización y publicación en YouTube y en la página de LinkedIn (ver `docs/publicacion-automatica.md`).

## Flujo de trabajo
```
python3 tools/build.py   # regenera páginas, sitemap.xml, robots.txt, feed del blog
git add -A && git commit && git push
```
Para sumar un artículo: agregarlo a `POSTS` en `tools/blog.py` y ejecutar el build.
