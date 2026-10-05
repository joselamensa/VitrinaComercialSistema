# -*- coding: utf-8 -*-
"""Generador del sitio estático de Tablero.

Uso:  python3 tools/build.py

- Genera las páginas internas (carpetas con index.html => URLs limpias con barra final).
- Rellena en index.html los bloques entre marcadores <!--@@NOMBRE-->...<!--@@/NOMBRE-->
  (NAV, SLIDES, FAQ, FOOTER, JSONLD). El resto de index.html se edita a mano.
- Genera sitemap.xml y robots.txt.
No hay dependencias externas.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import *  # noqa
import pages  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
esc = html.escape


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


# ---------------------------------------------------------------- piezas
def img_tag(m, dark=False, eager=False, sizes="(max-width:900px) 92vw, 640px"):
    name = m["img"] + ("dark" if dark else "")
    alt = m["alt_dark"] if dark else m["alt"]
    cls = ' class="shot__dark"' if dark else ""
    return (
        '<img%s src="/assets/modulos/%s-800.webp" '
        'srcset="/assets/modulos/%s-800.webp 800w, /assets/modulos/%s.webp 1900w" sizes="%s" '
        'width="1900" height="935" alt="%s" loading="%s" decoding="async" data-full="/assets/modulos/%s.webp">'
        % (cls, name, name, name, sizes, esc(alt, quote=True), "eager" if eager else "lazy", name)
    )


def shot(m, extra_cls="", sizes="(max-width:900px) 92vw, 640px"):
    cls = "shot" + (" shot--nodark" if not m["dark"] else "") + (" " + extra_cls if extra_cls else "")
    out = '<div class="%s">%s' % (cls, img_tag(m, sizes=sizes))
    if m["dark"]:
        out += img_tag(m, dark=True, sizes=sizes)
    return out + "</div>"


def nav_html():
    links = [
        ("/modulos/", "Módulos"),
        ("/#roles", "Roles"),
        ("/#personalizacion", "Personalización"),
        ("/#precios", "Precios"),
        ("/preguntas-frecuentes/", "Preguntas"),
        ("/#contacto", "Contacto"),
    ]
    a = "\n".join('      <a href="%s">%s</a>' % l for l in links)
    b = "\n".join('    <a href="%s">%s</a>' % l for l in links)
    return """<nav class="nav" id="nav" aria-label="Principal">
  <div class="nav__inner">
    <a href="/" class="nav__logo" aria-label="Tablero — inicio">
      <span class="nav__logo-badge"><img src="/assets/logo-96.webp" width="38" height="38" alt="Logo de Tablero"></span>
      <span class="nav__logo-text wordmark" aria-hidden="true">TABL<i class="wordmark__e"><span></span><span></span><span></span></i>RO</span>
    </a>
    <div class="nav__links">
%s
    </div>
    <a class="btn btn-primary nav__cta" href="%s" target="_blank" rel="noopener">Solicitar Demo</a>
    <button class="nav__toggle" id="navToggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="navMobile"><span></span><span></span><span></span></button>
  </div>
  <div class="nav__mobile" id="navMobile">
%s
    <a class="btn btn-primary" href="%s" target="_blank" rel="noopener">Solicitar Demo</a>
  </div>
</nav>""" % (a, wa(), b, wa())


def footer_html(brand_img=False):
    mods = "\n".join('      <a href="%s">%s</a>' % (mod_url(m["key"]), m["name"]) for m in MODULES)
    brand = ""
    if brand_img:
        brand = """  <div class="container">
    <div class="footer-brand-img">
      <img src="/assets/tablero.webp" width="680" height="453" loading="lazy" decoding="async" alt="Tablero, sistema de gestión para agencias de autos: logo sobre fondo oscuro con un panel de control y un auto">
    </div>
  </div>
"""
    return """<footer>
%s  <div class="container">
    <div class="footer-cols">
      <div>
        <a href="/" class="footer-logo" aria-label="Tablero — inicio">
          <span class="footer-logo-badge"><img src="/assets/logo-96.webp" width="32" height="32" loading="lazy" alt="Logo de Tablero"></span>
          <span class="footer-logo-text wordmark" aria-hidden="true">TABL<i class="wordmark__e"><span></span><span></span><span></span></i>RO</span>
        </a>
        <p>Sistema de gestión hecho a medida para agencias de autos usados en Argentina.</p>
      </div>
      <div>
        <h2>Módulos</h2>
%s
      </div>
      <div>
        <h2>Soluciones</h2>
        <a href="/sistema-de-gestion-para-agencia-de-autos-usados/">Sistema para agencias de autos usados</a>
        <a href="/software-para-concesionaria/">Software para concesionarias</a>
        <a href="/preguntas-frecuentes/">Preguntas frecuentes</a>
      </div>
      <div>
        <h2>Tablero</h2>
        <a href="/#precios">Precios</a>
        <a href="/#roles">Roles</a>
        <a href="%s" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>
  </div>
</footer>""" % (brand, mods, wa())


def faq_html(keys=None, items=None):
    if items is None:
        items = [FAQ[k] for k in keys]
    out = ['<div class="faq">']
    for q, a in items:
        out.append('  <details><summary>%s</summary><div class="answer"><p>%s</p></div></details>' % (esc(q), esc(a)))
    out.append("</div>")
    return "\n".join(out)


def faq_jsonld(items):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }


def slides_html():
    out = []
    for m in MODULES:
        out.append(
            """        <article class="slide reveal">
          <div class="slide__head">
            <span class="slide__icon" aria-hidden="true">%s</span>
            <h3>%s</h3>
          </div>
          %s
          <p>%s</p>
          <a class="slide__more" href="%s">Ver módulo de %s →</a>
          <div class="slide__badge">%s</div>
        </article>"""
            % (ICONS[m["key"]], m["name"], shot(m, sizes="(max-width:600px) 90vw, 700px"), esc(m["blurb"]), mod_url(m["key"]), m["name"].lower(), esc(m["badge"]))
        )
    return "\n\n".join(out)


def breadcrumb_html(trail):
    items = ['<li><a href="/">Inicio</a></li>']
    for i, (name, url) in enumerate(trail):
        if i == len(trail) - 1:
            items.append('<li aria-current="page">%s</li>' % esc(name))
        else:
            items.append('<li><a href="%s">%s</a></li>' % (url, esc(name)))
    return '<nav class="breadcrumb" aria-label="Migas de pan"><ol>%s</ol></nav>' % "".join(items)


def breadcrumb_jsonld(trail):
    els = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE_URL + "/"}]
    for i, (name, url) in enumerate(trail):
        els.append({"@type": "ListItem", "position": i + 2, "name": name, "item": SITE_URL + url})
    return {"@type": "BreadcrumbList", "itemListElement": els}


def org_jsonld():
    return {
        "@type": "Organization",
        "@id": SITE_URL + "/#organization",
        "name": SITE_NAME,
        "url": SITE_URL + "/",
        "logo": {"@type": "ImageObject", "url": SITE_URL + "/assets/logo.png", "width": 512, "height": 512},
        "description": "Sistema de gestión para agencias de autos usados.",
        "contactPoint": [{
            "@type": "ContactPoint",
            "contactType": "sales",
            "telephone": "+5491122699526",
            "availableLanguage": "es",
            "url": wa(),
        }],
    }


def software_jsonld():
    return {
        "@type": "SoftwareApplication",
        "@id": SITE_URL + "/#software",
        "name": SITE_NAME,
        "url": SITE_URL + "/",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web",
        "inLanguage": "es",
        "description": "Sistema de gestión para agencias de autos usados: inventario, finanzas en pesos y dólares, gestoría, detailing, visitas y tareas, con vitrina pública sincronizada.",
        "featureList": [
            "Inventario de autos y motos con historial de precios y galería de fotos",
            "Finanzas bimonetarias (USD y ARS) con medios de pago y comprobantes",
            "Gestoría con checklist de documentación por unidad",
            "Detailing: catálogo de servicios de preparación y seguimiento",
            "Agenda de visitas por vendedor",
            "Tareas internas con urgencia, estado y comentarios",
            "Ocho roles con permisos diferenciados",
            "Vitrina pública sincronizada en tiempo real",
        ],
        "screenshot": [SITE_URL + "/assets/modulos/%s.webp" % m["img"] for m in MODULES],
        "publisher": {"@id": SITE_URL + "/#organization"},
    }


def website_jsonld():
    return {
        "@type": "WebSite",
        "@id": SITE_URL + "/#website",
        "url": SITE_URL + "/",
        "name": SITE_NAME,
        "inLanguage": "es",
        "publisher": {"@id": SITE_URL + "/#organization"},
    }


def webpage_jsonld(path, title, desc):
    return {
        "@type": "WebPage",
        "@id": SITE_URL + path + "#webpage",
        "url": SITE_URL + path,
        "name": title,
        "description": desc,
        "inLanguage": "es",
        "isPartOf": {"@id": SITE_URL + "/#website"},
        "about": {"@id": SITE_URL + "/#software"},
    }


def jsonld_script(nodes):
    data = {"@context": "https://schema.org", "@graph": nodes}
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(data, ensure_ascii=False, indent=2)


def head_html(title, desc, path, jsonld_nodes, og_type="website", robots="index, follow"):
    url = SITE_URL + path
    t = esc(title, quote=True)
    d = esc(desc, quote=True)
    return """<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(t)s</title>
<meta name="description" content="%(d)s">
<meta name="robots" content="%(robots)s, max-image-preview:large">
<link rel="canonical" href="%(url)s">
<meta name="theme-color" content="#0052cc">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" href="/assets/icon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:type" content="%(og_type)s">
<meta property="og:site_name" content="Tablero">
<meta property="og:locale" content="es_AR">
<meta property="og:title" content="%(t)s">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="%(site)s%(og)s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Tablero, sistema de gestión para agencias de autos usados">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(t)s">
<meta name="twitter:description" content="%(d)s">
<meta name="twitter:image" content="%(site)s%(og)s">
<link rel="stylesheet" href="/assets/css/site.css">
%(ld)s""" % dict(t=t, d=d, url=url, robots=robots, og_type=og_type, site=SITE_URL, og=OG_IMAGE, ld=jsonld_script(jsonld_nodes))


NAV_JS = """<script>
  var nav = document.getElementById('nav');
  var navToggle = document.getElementById('navToggle');
  navToggle.addEventListener('click', function(){
    var open = nav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.querySelectorAll('.nav__mobile a').forEach(function(a){
    a.addEventListener('click', function(){ nav.classList.remove('is-open'); navToggle.setAttribute('aria-expanded','false'); });
  });
  var reveals = document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){ entry.target.classList.add('in'); io.unobserve(entry.target); }
      });
    }, {threshold:0.12});
    reveals.forEach(function(el){ io.observe(el); });
  } else { reveals.forEach(function(el){ el.classList.add('in'); }); }
</script>"""


def cta_html(h2, text, wa_text):
    return """<section class="cta cta--tight" id="contacto">
  <div class="container">
   <div class="cta__card">
    <h2>%s</h2>
    <p>%s</p>
    <a class="btn btn-wa" style="padding:18px 34px;font-size:14.5px;" href="%s" target="_blank" rel="noopener">Contactar por WhatsApp</a>
   </div>
  </div>
</section>""" % (esc(h2), esc(text), wa(wa_text))


# --------------------------------------------------------- bloques de página
def render_block(b):
    t = b[0]
    if t == "prose":
        _, h2, body, *opt = b
        cls = "content content--alt" if (opt and opt[0] == "alt") else ("content content--white" if (opt and opt[0] == "white") else "content")
        return '<section class="%s"><div class="container"><div class="prose">\n<h2>%s</h2>\n%s\n</div></div></section>' % (cls, esc(h2), render_body(body))
    if t == "split":
        _, h2, body, mkey, *opt = b
        cls = "content content--alt" if (opt and opt[0] == "alt") else ("content content--white" if (opt and opt[0] == "white") else "content")
        m = MOD[mkey]
        cap = "Pantalla del módulo de %s en Tablero%s." % (m["name"].lower(), " (pasá el mouse para verla en modo oscuro)" if m["dark"] else "")
        return ('<section class="%s"><div class="container"><div class="split">\n<div class="prose">\n<h2>%s</h2>\n%s\n</div>\n'
                '<figure class="figure">%s<figcaption>%s</figcaption></figure>\n</div></div></section>') % (cls, esc(h2), render_body(body), shot(m), esc(cap))
    if t == "features":
        _, h2, intro, feats, *opt = b
        cls = "content content--alt" if (opt and opt[0] == "alt") else ("content content--white" if (opt and opt[0] == "white") else "content")
        cards = []
        for icon, title, text, href in feats:
            h3 = '<a href="%s">%s</a>' % (href, esc(title)) if href else esc(title)
            cards.append('<div class="card feat"><div class="feat__icon" aria-hidden="true">%s</div><h3>%s</h3><p>%s</p></div>' % (ICONS[icon], h3, text))
        return ('<section class="%s"><div class="container"><div class="section-head"><h2>%s</h2>%s</div>\n<div class="feat-grid">\n%s\n</div></div></section>'
                % (cls, esc(h2), ("<p>%s</p>" % intro) if intro else "", "\n".join(cards)))
    if t == "links":
        _, h2, intro, links, *opt = b
        cls = "content content--alt" if (opt and opt[0] == "alt") else ("content content--white" if (opt and opt[0] == "white") else "content")
        cards = ['<a class="card link-card" href="%s"><h3>%s</h3><p>%s</p><span>Ver más →</span></a>' % (href, esc(title), esc(text)) for title, text, href in links]
        return ('<section class="%s"><div class="container"><div class="section-head"><h2>%s</h2>%s</div>\n<div class="link-grid">\n%s\n</div></div></section>'
                % (cls, esc(h2), ("<p>%s</p>" % intro) if intro else "", "\n".join(cards)))
    if t == "faq":
        _, h2, items, *opt = b
        cls = "content content--alt" if (opt and opt[0] == "alt") else ("content content--white" if (opt and opt[0] == "white") else "content")
        return '<section class="%s"><div class="container"><div class="section-head"><h2>%s</h2></div>\n%s\n</div></section>' % (cls, esc(h2), faq_html(items=items))
    if t == "faqgroups":
        out = []
        for i, (h2, items) in enumerate(b[1]):
            cls = "content content--alt" if i % 2 else "content"
            out.append('<section class="%s"><div class="container"><div class="section-head"><h2>%s</h2></div>\n%s\n</div></section>' % (cls, esc(h2), faq_html(items=items)))
        return "\n".join(out)
    raise ValueError(t)


def render_body(body):
    out = []
    for p in body:
        if isinstance(p, tuple) and p[0] == "ul":
            out.append('<ul class="bullets">\n' + "\n".join("  <li>%s</li>" % li for li in p[1]) + "\n</ul>")
        elif isinstance(p, tuple) and p[0] == "h3":
            out.append("<h3>%s</h3>" % esc(p[1]))
        else:
            out.append("<p>%s</p>" % p)
    return "\n".join(out)


def page_html(pg):
    path = pg["path"]
    trail = pg["trail"]
    blocks = [b for b in pg["blocks"]]
    faq_items = []
    for b in blocks:
        if b[0] == "faq":
            faq_items += b[2]
        elif b[0] == "faqgroups":
            for _, items in b[1]:
                faq_items += items
    nodes = [webpage_jsonld(path, pg["title"], pg["desc"]), breadcrumb_jsonld(trail)]
    if faq_items:
        nodes.append(faq_jsonld(faq_items))
    body = [render_block(b) for b in blocks]
    cta = pg.get("cta") or ("Pedí una demo de Tablero", "Te mostramos el sistema y lo armamos con vos, módulo por módulo.", "Hola! Quiero conocer Tablero para mi agencia.")
    return """<!DOCTYPE html>
<html lang="es">
<head>
%s
</head>
<body>
<a class="skip-link" href="#contenido">Saltar al contenido</a>

%s

<main id="contenido">
<header class="page-hero">
  <div class="container">
    %s
    <h1>%s</h1>
    <p class="lead">%s</p>
    <div class="hero__ctas">
      <a class="btn btn-wa" href="%s" target="_blank" rel="noopener">Hablar por WhatsApp</a>
      <a class="btn btn-outline" href="/#precios">Ver planes</a>
    </div>
  </div>
</header>

%s

%s
</main>

%s

<a class="float-wa" href="%s" target="_blank" rel="noopener" aria-label="Escribinos por WhatsApp">
  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.29-1.39c1.45.79 3.08 1.21 4.75 1.21h.01c5.46 0 9.9-4.45 9.9-9.91C21.96 6.45 17.5 2 12.04 2zm5.79 14.06c-.24.68-1.42 1.33-1.96 1.4-.5.07-1.12.1-1.81-.11-.42-.13-.95-.31-1.64-.6-2.88-1.24-4.76-4.14-4.9-4.33-.14-.19-1.17-1.55-1.17-2.96s.72-2.1.98-2.39c.26-.28.56-.35.75-.35h.53c.17 0 .4-.06.62.48.24.58.8 2 .87 2.14.07.14.12.31.02.5-.09.19-.14.31-.28.48-.14.16-.29.36-.42.48-.14.14-.28.29-.12.57.16.28.72 1.19 1.55 1.93 1.06.95 1.96 1.24 2.24 1.38.28.14.44.12.6-.07.16-.19.68-.79.87-1.06.18-.28.37-.23.62-.14.26.1 1.63.77 1.91.91.28.14.47.21.53.33.07.12.07.68-.17 1.36z"/></svg>
</a>

%s
</body>
</html>
""" % (
        head_html(pg["title"], pg["desc"], path, nodes),
        nav_html(),
        breadcrumb_html(trail),
        esc(pg["h1"]),
        esc(pg["lead"]),
        wa(pg.get("wa", "Hola! Quiero conocer Tablero para mi agencia.")),
        "\n\n".join(body),
        cta_html(*cta),
        footer_html(),
        wa(),
        NAV_JS,
    )


def page_404():
    t = "Página no encontrada | Tablero"
    d = "La página que buscás no existe. Volvé al inicio de Tablero, el sistema de gestión para agencias de autos usados."
    head = head_html(t, d, "/404.html", [], robots="noindex, follow").replace('<link rel="canonical" href="%s/404.html">' % SITE_URL, "")
    return """<!DOCTYPE html>
<html lang="es">
<head>
%s
</head>
<body>
%s
<main id="contenido">
<header class="page-hero">
  <div class="container">
    <h1>No encontramos esa página</h1>
    <p class="lead">Puede que el enlace haya cambiado. Probá desde el inicio o mirá los módulos de Tablero.</p>
    <div class="hero__ctas">
      <a class="btn btn-primary" href="/">Ir al inicio</a>
      <a class="btn btn-outline" href="/modulos/">Ver módulos</a>
    </div>
  </div>
</header>
</main>
%s
%s
</body>
</html>
""" % (head, nav_html(), footer_html(), NAV_JS)


# ----------------------------------------------------------------- salida
def write(path, text):
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def fill_markers(text, name, content):
    pat = re.compile(r"(<!--@@%s-->).*?(<!--@@/%s-->)" % (name, name), re.S)
    if not pat.search(text):
        raise SystemExit("Falta el marcador %s en index.html" % name)
    return pat.sub(lambda m: m.group(1) + "\n" + content + "\n" + m.group(2), text)


def build_home():
    p = os.path.join(ROOT, "index.html")
    text = open(p, encoding="utf-8").read()
    home_title = "Tablero | Sistema de gestión para agencias de autos usados"
    home_desc = "Tablero es el sistema de gestión para agencias de autos usados: inventario, finanzas en USD y ARS, gestoría, detailing, visitas y tareas, a tu medida."
    nodes = [org_jsonld(), website_jsonld(), software_jsonld(), webpage_jsonld("/", home_title, home_desc),
             faq_jsonld([FAQ[k] for k in HOME_FAQ])]
    text = fill_markers(text, "HEAD", head_html(home_title, home_desc, "/", nodes))
    text = fill_markers(text, "NAV", nav_html())
    text = fill_markers(text, "SLIDES", slides_html())
    text = fill_markers(text, "FAQ", faq_html(HOME_FAQ))
    text = fill_markers(text, "FOOTER", footer_html(brand_img=True))
    open(p, "w", encoding="utf-8").write(text)
    return home_title, home_desc


def build():
    all_pages = pages.all_pages()
    urls = [("/", "1.0")]
    home_title, home_desc = build_home()
    problems = []
    for pg in all_pages:
        write(pg["path"] + "index.html", page_html(pg))
        urls.append((pg["path"], pg.get("priority", "0.7")))
        if len(pg["title"]) > 62:
            problems.append("title largo (%d): %s" % (len(pg["title"]), pg["title"]))
        if not (110 <= len(pg["desc"]) <= 165):
            problems.append("description fuera de rango (%d): %s" % (len(pg["desc"]), pg["path"]))
    for t, d, n in [(home_title, home_desc, "home")]:
        if len(t) > 62:
            problems.append("title largo home (%d)" % len(t))
        if len(d) > 165:
            problems.append("description larga home (%d)" % len(d))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, prio in urls:
        sm.append("  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (SITE_URL, u, LASTMOD, prio))
    sm.append("</urlset>")
    write("/sitemap.xml", "\n".join(sm) + "\n")
    write("/robots.txt", "User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: %s/sitemap.xml\n" % SITE_URL)
    write("/404.html", page_404())
    print("Páginas generadas: %d (+ home)" % len(all_pages))
    for p in problems:
        print("AVISO:", p)


if __name__ == "__main__":
    build()
