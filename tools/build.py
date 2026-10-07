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
import math
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import *  # noqa
from content import GSC_TOKEN, PRICE_ESENCIAL_USD, PRICE_COMPLETO_USD, LINKEDIN_URL, FOUNDER  # noqa
import pages  # noqa
import blog  # noqa

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


def shot(m, extra_cls="", sizes="(max-width:900px) 92vw, 640px", eager=False):
    cls = "shot" + (" shot--nodark" if not m["dark"] else "") + (" " + extra_cls if extra_cls else "")
    out = '<div class="%s">%s' % (cls, img_tag(m, sizes=sizes, eager=eager))
    if m["dark"]:
        out += img_tag(m, dark=True, sizes=sizes)
    return out + "</div>"


CHEV = '<svg class="nav__chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'

SOLUTIONS = [
    ("Sistema para agencias de autos usados", "El ciclo completo del auto en un solo lugar", "/sistema-de-gestion-para-agencia-de-autos-usados/"),
    ("Software para concesionarias", "Equipo, caja, trámites y vitrina conectados", "/software-para-concesionaria/"),
]


def nav_active(path):
    if path.startswith("/modulos/"):
        return "modulos"
    if path in [u for _, _, u in SOLUTIONS]:
        return "soluciones"
    if path.startswith("/blog/"):
        return "blog"
    if path.startswith("/preguntas-frecuentes/"):
        return "faq"
    return ""


def nav_html(path=""):
    act = nav_active(path)

    def cls(k):
        return ' class="is-active" aria-current="true"' if act == k else ""

    mods_sub = "".join(
        '<a href="%s" role="menuitem">%s<small>%s</small></a>' % (mod_url(m["key"]), m["name"], esc(m["short"])) for m in MODULES
    ) + '<a class="nav__sub-all" href="/modulos/" role="menuitem">Ver todos los módulos →</a>'
    sol_sub = "".join('<a href="%s" role="menuitem">%s<small>%s</small></a>' % (u, esc(t), esc(d)) for t, d, u in SOLUTIONS)
    desktop = """      <div class="nav__item"><a href="/modulos/"%s>Módulos %s</a><div class="nav__sub" role="menu">%s</div></div>
      <div class="nav__item"><a href="%s"%s>Soluciones %s</a><div class="nav__sub" role="menu">%s</div></div>
      <a href="/#precios">Precios</a>
      <a href="/blog/"%s>Blog</a>
      <a href="/preguntas-frecuentes/"%s>Preguntas</a>
      <a href="/#contacto">Contacto</a>""" % (cls("modulos"), CHEV, mods_sub, SOLUTIONS[0][2], cls("soluciones"), CHEV, sol_sub, cls("blog"), cls("faq"))
    mobile = ['    <span class="nav__group">Módulos</span>']
    mobile += ['    <a class="sub" href="%s">%s</a>' % (mod_url(m["key"]), m["name"]) for m in MODULES]
    mobile += ['    <span class="nav__group">Soluciones</span>']
    mobile += ['    <a class="sub" href="%s">%s</a>' % (u, esc(t)) for t, d, u in SOLUTIONS]
    mobile += ['    <span class="nav__group">Más</span>', '    <a class="sub" href="/#precios">Precios</a>', '    <a class="sub" href="/blog/">Blog</a>',
               '    <a class="sub" href="/preguntas-frecuentes/">Preguntas frecuentes</a>', '    <a class="sub" href="/#contacto">Contacto</a>']
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
    <button class="nav__toggle" id="navToggle" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="navMobile"><span></span><span></span><span></span></button>
  </div>
  <div class="nav__mobile" id="navMobile">
%s
    <a class="btn btn-primary" href="%s" target="_blank" rel="noopener">Solicitar Demo</a>
  </div>
</nav>""" % (desktop, wa(), "\n".join(mobile), wa())


WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.29-1.39c1.45.79 3.08 1.21 4.75 1.21h.01c5.46 0 9.9-4.45 9.9-9.91C21.96 6.45 17.5 2 12.04 2zm5.79 14.06c-.24.68-1.42 1.33-1.96 1.4-.5.07-1.12.1-1.81-.11-.42-.13-.95-.31-1.64-.6-2.88-1.24-4.76-4.14-4.9-4.33-.14-.19-1.17-1.55-1.17-2.96s.72-2.1.98-2.39c.26-.28.56-.35.75-.35h.53c.17 0 .4-.06.62.48.24.58.8 2 .87 2.14.07.14.12.31.02.5-.09.19-.14.31-.28.48-.14.16-.29.36-.42.48-.14.14-.28.29-.12.57.16.28.72 1.19 1.55 1.93 1.06.95 1.96 1.24 2.24 1.38.28.14.44.12.6-.07.16-.19.68-.79.87-1.06.18-.28.37-.23.62-.14.26.1 1.63.77 1.91.91.28.14.47.21.53.33.07.12.07.68-.17 1.36z"/></svg>'


def footer_html(brand_img=False):
    mods = "\n".join('        <a href="%s">%s</a>' % (mod_url(m["key"]), m["name"]) for m in MODULES)
    recents = "\n".join('        <a href="%s">%s</a>' % (blog.post_url(p["slug"]), esc(p["title"])) for p in [q for q in blog.POSTS if "argentina" not in q["slug"] and "formulario-08" not in q["slug"]][:4])
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
        <p>Sistema de gestión hecho a medida para agencias de autos usados.</p>
        <a class="footer-wa" href="%s" target="_blank" rel="noopener">%s Hablar por WhatsApp</a>
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
        <h2>Blog</h2>
%s
        <a href="/blog/">Ver todos los artículos →</a>
      </div>
      <div>
        <h2>Tablero</h2>
        <a href="/sobre-tablero/">Sobre Tablero</a>
        <a href="/#roles">Roles</a>
        <a href="/#personalizacion">Personalización</a>
        <a href="/#precios">Precios</a>
        <a href="/#contacto">Contacto</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Tablero.</span>
      <span>Tel. <a href="%s" target="_blank" rel="noopener">%s</a></span>
    </div>
  </div>
</footer>""" % (brand, wa(), WA_SVG, mods, recents, wa(), PHONE_DISPLAY)


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


def person_jsonld():
    return {
        "@type": "Person",
        "@id": SITE_URL + "/#founder",
        "name": FOUNDER,
        "jobTitle": "Creador de Tablero",
        "url": SITE_URL + "/sobre-tablero/",
        "sameAs": [LINKEDIN_URL],
        "worksFor": {"@id": SITE_URL + "/#organization"},
    }


def org_jsonld():
    return {
        "@type": "Organization",
        "@id": SITE_URL + "/#organization",
        "name": SITE_NAME,
        "url": SITE_URL + "/",
        "logo": {"@type": "ImageObject", "url": SITE_URL + "/assets/logo.png", "width": 512, "height": 512},
        "description": "Sistema de gestión para agencias de autos usados.",
        "foundingDate": "2025",
        "areaServed": "Worldwide",
        "founder": {"@id": SITE_URL + "/#founder"},
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
        "description": "Sistema de gestión para agencias de autos usados: inventario, finanzas en tu moneda local y en dólares, gestoría, detailing, visitas y tareas, con vitrina pública sincronizada.",
        "featureList": [
            "Inventario de autos y motos con historial de precios y galería de fotos",
            "Finanzas bimonetarias (moneda local y USD) con medios de pago y comprobantes",
            "Gestoría con checklist de documentación por unidad",
            "Detailing: catálogo de servicios de preparación y seguimiento",
            "Agenda de visitas por vendedor",
            "Tareas internas con urgencia, estado y comentarios",
            "Ocho roles con permisos diferenciados",
            "Vitrina pública sincronizada en tiempo real",
        ],
        "screenshot": [SITE_URL + "/assets/modulos/%s.webp" % m["img"] for m in MODULES],
        "publisher": {"@id": SITE_URL + "/#organization"},
        "offers": [
            {"@type": "Offer", "name": "Esencial", "price": str(PRICE_ESENCIAL_USD), "priceCurrency": "USD",
             "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(PRICE_ESENCIAL_USD), "priceCurrency": "USD", "unitCode": "MON", "billingDuration": 1}},
            {"@type": "Offer", "name": "Completo", "price": str(PRICE_COMPLETO_USD), "priceCurrency": "USD",
             "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(PRICE_COMPLETO_USD), "priceCurrency": "USD", "unitCode": "MON", "billingDuration": 1}},
        ],
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


def css_version():
    import hashlib
    with open(os.path.join(ROOT, "assets/css/site.css"), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


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
<meta property="og:locale" content="es_LA">
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
<link rel="alternate" type="application/rss+xml" title="Blog de Tablero" href="/blog/feed.xml">
%(gsc)s<link rel="stylesheet" href="/assets/css/site.css?v=%(cssv)s">
%(ld)s""" % dict(cssv=css_version(), gsc=('<meta name="google-site-verification" content="%s">\n' % GSC_TOKEN) if GSC_TOKEN else "", t=t, d=d, url=url, robots=robots, og_type=og_type, site=SITE_URL, og=OG_IMAGE, ld=jsonld_script(jsonld_nodes))


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
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' && nav.classList.contains('is-open')){ nav.classList.remove('is-open'); navToggle.setAttribute('aria-expanded','false'); navToggle.focus(); }
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
    <a class="btn btn-wa" href="%s" target="_blank" rel="noopener">@@WA@@Contactar por WhatsApp</a>
   </div>
  </div>
</section>""".replace("@@WA@@", WA_SVG) % (esc(h2), esc(text), wa(wa_text))


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
    if t == "bulletcards":
        _, h2, intro, bullets, *opt = b
        cls = "content content--alt" if (opt and opt[0] == "alt") else ("content content--white" if (opt and opt[0] == "white") else "content")
        tick = '<span class="tick" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M20 6L9 17l-5-5"/></svg></span>'
        cards = []
        for item in bullets:
            m_ = re.match(r"^<strong>(.*?)</strong>[:,]?\s*(.*)$", item, re.S)
            title, rest = (m_.group(1).rstrip(":"), m_.group(2)) if m_ else (item, "")
            rest = (rest[:1].upper() + rest[1:]) if rest else ""
            cards.append('<div class="card feat feat--check">%s<div><h3>%s</h3>%s</div></div>' % (tick, title, ("<p>%s</p>" % rest) if rest else ""))
        return ('<section class="%s"><div class="container"><div class="section-head"><h2>%s</h2>%s</div>\n<div class="feat-grid">\n%s\n</div></div></section>'
                % (cls, esc(h2), ("<p>%s</p>" % intro) if intro else "", "\n".join(cards)))
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


def hero_html(pg):
    ctas = """<div class="hero__ctas">
      <a class="btn btn-wa" href="%s" target="_blank" rel="noopener">@@WA@@Hablar por WhatsApp</a>
      <a class="btn btn-outline" href="/#precios">Ver planes</a>
    </div>""".replace("@@WA@@", WA_SVG) % wa(pg.get("wa", "Hola! Quiero conocer Tablero para mi agencia."))
    text = '%s<h1>%s</h1>\n    <p class="lead">%s</p>\n    %s' % (breadcrumb_html(pg["trail"]), esc(pg["h1"]), esc(pg["lead"]), ctas)
    if pg.get("hero_mod"):
        m = MOD[pg["hero_mod"]]
        cap = "Pantalla del módulo de %s en Tablero%s." % (m["name"].lower(), " (pasá el mouse para verla en modo oscuro)" if m["dark"] else "")
        return ('<header class="page-hero"><div class="container"><div class="page-hero__grid">\n  <div>%s</div>\n  <figure class="page-hero__fig">%s<figcaption>%s</figcaption></figure>\n</div></div></header>'
                % (text, shot(m, sizes="(max-width:960px) 92vw, 560px", eager=True), esc(cap)))
    return '<header class="page-hero"><div class="container">\n    %s\n  </div></header>' % text


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
    if pg.get("page_type"):
        nodes[0]["@type"] = pg["page_type"]
        nodes.append(person_jsonld())
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
%s

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
        nav_html(path),
        hero_html(pg),
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
""" % (head, nav_html("/404.html"), footer_html(), NAV_JS)



# ------------------------------------------------------------------- blog
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def fecha_es(iso):
    y, m, d = iso.split("-")
    return "%d de %s de %s" % (int(d), MESES[int(m) - 1], y)


def slugify(t):
    import unicodedata
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def render_post_body(sections):
    out, toc, seen = [], [], set()
    for h2, body in sections:
        if h2 == "callout":
            out.append('<div class="callout"><p>%s</p></div>' % body)
            continue
        sid = slugify(h2)
        while sid in seen:
            sid += "-2"
        seen.add(sid)
        toc.append((sid, h2))
        out.append('<h2 id="%s">%s</h2>\n%s' % (sid, esc(h2), render_body_blog(body)))
    return "\n".join(out), toc


def render_body_blog(body):
    out = []
    for b in body:
        if isinstance(b, tuple) and b[0] in ("ul", "ol"):
            cls = ' class="bullets"' if b[0] == "ul" else ""
            out.append("<%s%s>\n%s\n</%s>" % (b[0], cls, "\n".join("  <li>%s</li>" % li for li in b[1]), b[0]))
        elif isinstance(b, tuple) and b[0] == "h3":
            out.append("<h3>%s</h3>" % esc(b[1]))
        elif isinstance(b, tuple) and b[0] == "callout":
            out.append('<div class="callout"><p>%s</p></div>' % b[1])
        else:
            out.append("<p>%s</p>" % b)
    return "\n".join(out)


def post_card(p, tag="h3"):
    return ('<a class="card post-card" href="%s"><div class="meta">%s · %d min de lectura</div><%s>%s</%s><p>%s</p><span class="more">Leer artículo →</span></a>'
            % (blog.post_url(p["slug"]), fecha_es(blog.PUBLISHED), blog.minutes(p), tag, esc(p["title"]), tag, esc(p["desc"])))


def post_page(p):
    path = blog.post_url(p["slug"])
    trail = [("Blog", "/blog/"), (p["title"], path)]
    body_html, toc = render_post_body(p["sections"])
    toc_html = '<aside class="card toc" aria-label="En este artículo"><h2>En este artículo</h2><ol>%s</ol></aside>' % "".join('<li><a href="#%s">%s</a></li>' % (i, esc(t)) for i, t in toc)
    nodes = [
        webpage_jsonld(path, p["title"], p["desc"]),
        breadcrumb_jsonld([("Blog", "/blog/"), (p["title"], path)]),
        {
            "@type": "BlogPosting",
            "@id": SITE_URL + path + "#article",
            "headline": p["h1"][:110],
            "description": p["desc"],
            "inLanguage": "es",
            "datePublished": blog.PUBLISHED,
            "dateModified": blog.PUBLISHED,
            "image": SITE_URL + OG_IMAGE,
            "mainEntityOfPage": SITE_URL + path,
            "author": {"@id": SITE_URL + "/#organization"},
            "publisher": {"@id": SITE_URL + "/#organization"},
            "wordCount": blog.words(p),
        },
    ]
    rel_mods = [feat_link(MOD[k]) for k in p["modules"]]
    others = [q for q in blog.POSTS if q["slug"] != p["slug"]]
    # los más cercanos: los que comparten módulo primero
    others.sort(key=lambda q: -len(set(q["modules"]) & set(p["modules"])))
    more = "".join(post_card(q) for q in others[:3])
    mod_names = " y ".join(MOD[k]["name"].lower() for k in p["modules"][:2])
    cta = """<div class="post-cta">
  <h2>¿Querés resolver esto en tu agencia?</h2>
  <p>Tablero reúne %s y el resto de la operación en un solo sistema, armado a tu medida.</p>
  <a class="btn btn-wa" href="%s" target="_blank" rel="noopener">Pedir una demo por WhatsApp</a>
</div>""" % (mod_names, wa("Hola! Leí un artículo del blog y quiero conocer Tablero."))
    head = head_html(p["title"] + " | Tablero", p["desc"], path, nodes, og_type="article")
    # el título del <title> no debe pasar de ~62: se reemplaza si es largo
    if len(p["title"] + " | Tablero") > 62:
        head = head_html(p["title"], p["desc"], path, nodes, og_type="article")
    return """<!DOCTYPE html>
<html lang="es">
<head>
%s
</head>
<body>
<a class="skip-link" href="#contenido">Saltar al contenido</a>

%s

<main id="contenido">
<header class="page-hero"><div class="container">
  %s
  <h1>%s</h1>
  <p class="lead">%s</p>
  <p class="post-meta"><span>Publicado el <strong>%s</strong></span><span>%d min de lectura</span><span>Por el equipo de Tablero</span></p>
</div></header>

<section class="content"><div class="container">
<div class="post-layout">
<article class="prose post-body">
%s
%s
</article>
%s
</div>
</div></section>

<section class="content content--alt"><div class="container">
  <div class="section-head"><h2>Módulos relacionados</h2></div>
  <div class="link-grid">%s</div>
</div></section>

<section class="content"><div class="container">
  <div class="section-head"><h2>Seguí leyendo</h2></div>
  <div class="post-grid">%s</div>
</div></section>
</main>

%s

%s
%s
</body>
</html>
""" % (head, nav_html(path), breadcrumb_html(trail), esc(p["h1"]), esc(p["lead"]), fecha_es(blog.PUBLISHED), blog.minutes(p), body_html, cta, toc_html,
       "".join(rel_mods), more, footer_html(), float_wa(), NAV_JS)


def feat_link(m):
    return '<a class="card link-card" href="%s"><h3>Módulo de %s</h3><p>%s</p><span>Ver módulo →</span></a>' % (mod_url(m["key"]), esc(m["name"].lower()), esc(m["short"]))


def float_wa():
    return """<a class="float-wa" href="%s" target="_blank" rel="noopener" aria-label="Escribinos por WhatsApp">
  %s
</a>""" % (wa(), WA_SVG)


def blog_index_page():
    path = "/blog/"
    title = "Blog de Tablero: gestión de agencias de autos usados"
    desc = "Guías prácticas para agencias de autos usados: stock, caja en tu moneda local y en dólares, documentación, visitas, detailing, vitrina web y cómo elegir un sistema."
    nodes = [webpage_jsonld(path, title, desc), breadcrumb_jsonld([("Blog", path)]),
             {"@type": "Blog", "@id": SITE_URL + path + "#blog", "name": "Blog de Tablero", "url": SITE_URL + path, "inLanguage": "es",
              "publisher": {"@id": SITE_URL + "/#organization"},
              "blogPost": [{"@type": "BlogPosting", "headline": q["title"], "url": SITE_URL + blog.post_url(q["slug"]), "datePublished": blog.PUBLISHED} for q in blog.POSTS]}]
    cards = "".join(post_card(q, "h2") for q in blog.POSTS)
    return """<!DOCTYPE html>
<html lang="es">
<head>
%s
</head>
<body>
<a class="skip-link" href="#contenido">Saltar al contenido</a>

%s

<main id="contenido">
<header class="page-hero"><div class="container">
  %s
  <h1>Blog de Tablero</h1>
  <p class="lead">Guías prácticas para agencias de autos usados: cómo ordenar el stock, la caja en tu moneda local y en dólares, la documentación, las visitas y el equipo.</p>
</div></header>

<section class="content"><div class="container">
  <div class="post-grid">%s</div>
</div></section>
</main>

%s

%s
%s
</body>
</html>
""" % (head_html(title, desc, path, nodes), nav_html(path), breadcrumb_html([("Blog", path)]), cards,
       cta_html("Pedí una demo de Tablero", "Te mostramos el sistema y lo armamos con vos, módulo por módulo.", "Hola! Quiero conocer Tablero para mi agencia."),
       footer_html() + "\n\n" + float_wa(), NAV_JS)


def rss_xml():
    from email.utils import format_datetime
    import datetime
    dt = datetime.datetime.strptime(blog.PUBLISHED + " 09:00", "%Y-%m-%d %H:%M").replace(tzinfo=datetime.timezone(datetime.timedelta(hours=-3)))
    items = []
    for q in blog.POSTS:
        items.append("<item><title>%s</title><link>%s%s</link><guid>%s%s</guid><pubDate>%s</pubDate><description>%s</description></item>"
                     % (esc(q["title"]), SITE_URL, blog.post_url(q["slug"]), SITE_URL, blog.post_url(q["slug"]), format_datetime(dt), esc(q["desc"])))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Blog de Tablero</title><link>%s/blog/</link>'
            "<description>Guías para agencias de autos usados.</description><language>es</language>\n%s\n</channel></rss>\n" % (SITE_URL, "\n".join(items)))

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


# ----------------------------------------------------------------- precios
FLAG_US = '<svg class="flag" viewBox="0 0 24 16" aria-hidden="true"><rect width="24" height="16" fill="#fff"/><g fill="#b22234"><rect y="0" width="24" height="1.23"/><rect y="2.46" width="24" height="1.23"/><rect y="4.92" width="24" height="1.23"/><rect y="7.38" width="24" height="1.23"/><rect y="9.85" width="24" height="1.23"/><rect y="12.3" width="24" height="1.23"/><rect y="14.77" width="24" height="1.23"/></g><rect width="10" height="8.6" fill="#3c3b6e"/></svg>'
def _flag(inner):
    return '<svg class="flag" viewBox="0 0 24 16" aria-hidden="true">%s</svg>' % inner


FLAG_AR = _flag('<rect width="24" height="16" fill="#74acdf"/><rect y="5.33" width="24" height="5.34" fill="#fff"/><circle cx="12" cy="8" r="1.7" fill="#f6b40e"/>')
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 6L9 17l-5-5"/></svg>'

# Moneda alternativa opcional a USD (los precios son en USD; el peso argentino es solo una comodidad).
CURRENCIES = [("ARS", "peso argentino", FLAG_AR, 1000)]


def load_rates():
    """Devuelve ({código: unidades por 1 USD}, fecha). Admite el formato viejo {"venta": ...} (solo ARS)."""
    try:
        with open(os.path.join(ROOT, "tools", "rate.json"), encoding="utf-8") as f:
            r = json.load(f)
        rates = {k: float(v) for k, v in r.get("rates", {}).items()}
        if "venta" in r and "ARS" not in rates:
            rates["ARS"] = float(r["venta"])
        return rates, r.get("fecha", "")
    except Exception:
        return {}, ""


def fmt_money(code, n):
    return "%s %s" % (code, "{:,.0f}".format(n).replace(",", "."))


def local_amount(usd, code, rate, step):
    return int(usd * rate / float(step) + 0.5) * step


def price_span(usd, rates):
    out = '<span class="cur" data-c="USD">USD %d</span>' % usd
    for code, _n, _f, step in CURRENCIES:
        if code in rates:
            out += '<span class="cur" data-c="%s" hidden>%s</span>' % (code, fmt_money(code, local_amount(usd, code, rates[code], step)))
    return out + '<span class="plan__per"> / mes</span>'


def pricing_html():
    rates, fecha = load_rates()
    avail = [c for c in CURRENCIES if c[0] in rates]
    if avail:
        code, name, flag, step = avail[0]
        f = "/".join(reversed(fecha.split("-"))) if fecha else ""
        switch = ('<div class="cur-switch" role="group" aria-label="Moneda de los precios">'
                  '<button type="button" class="cur-btn is-on" data-cur="USD" aria-pressed="true">%s<span>USD</span></button>'
                  '<button type="button" class="cur-btn" data-cur="%s" aria-pressed="false">%s<span>%s</span></button></div>' % (FLAG_US, code, flag, code))
        note = ('<p class="cur-note"><span class="cur" data-c="USD">Precios en dólares (USD) por mes.</span>'
                '<span class="cur" data-c="%s" hidden>Valor en %s calculado con el dólar oficial (venta) de %s%s. Se actualiza cada semana.</span></p>'
                % (code, name + "s", ("$ " + "{:,.0f}".format(rates[code]).replace(",", ".")), (", al " + f) if f else ""))
    else:
        switch, note = "", '<p class="cur-note">Precios en dólares (USD) por mes.</p>'

    def li(t):
        return "<li>%s%s</li>" % (CHECK, t)

    def wa_link(txt):
        return wa(txt)

    return """    <div class="section-head reveal">
      <h2>Planes pensados para tu crecimiento</h2>
      <p>Elegí la potencia que tu agencia necesita hoy. Precios claros, sin letra chica; el plan A Medida lo definimos juntos por WhatsApp.</p>
      %s
      %s
    </div>
    <div class="pricing-grid">
      <div class="card plan reveal">
        <h3>Esencial</h3>
        <p class="plan__desc">Para agencias que arrancan a digitalizar el lote.</p>
        <div class="plan__price">%s</div>
        <div class="plan__price-note">Ideal para empezar con inventario y vitrina</div>
        <ul>%s%s%s</ul>
        <a class="btn btn-outline" href="%s" target="_blank" rel="noopener">Elegir Esencial</a>
      </div>
      <div class="card plan featured reveal">
        <span class="plan__badge">Más recomendado</span>
        <h3>Completo</h3>
        <p class="plan__desc">El sistema de punta a punta, como lo pediste.</p>
        <div class="plan__price">%s</div>
        <div class="plan__price-note">Gestión bimonetaria (moneda local + USD)</div>
        <ul>%s%s%s%s</ul>
        <a class="btn btn-primary" href="%s" target="_blank" rel="noopener">Elegir Completo</a>
      </div>
      <div class="card plan reveal">
        <h3>A Medida</h3>
        <p class="plan__desc">Para estructuras grandes o multi-sucursal.</p>
        <div class="plan__price">A consultar</div>
        <div class="plan__price-note">Roles, flujos e integraciones a definir juntos</div>
        <ul>%s%s%s</ul>
        <a class="btn btn-outline" href="%s" target="_blank" rel="noopener">Contactar</a>
      </div>
    </div>""" % (
        switch, note,
        price_span(PRICE_ESENCIAL_USD, rates),
        li("Inventario completo de autos y motos"), li("Vendedor asignado por unidad"), li("Vitrina pública sincronizada"),
        wa_link("Hola! Quiero el plan Esencial de Tablero."),
        price_span(PRICE_COMPLETO_USD, rates),
        li("Todo lo del plan Esencial"), li("Finanzas, Gestoría y Detailing"), li("Visitas y Tareas de equipo"), li("Todos los roles del sistema"),
        wa_link("Hola! Quiero el plan Completo de Tablero."),
        li("Módulos y campos personalizados"), li("Multi-sucursal"), li("Acompañamiento en la implementación"),
        wa_link("Hola! Quiero consultar por el plan A Medida de Tablero."),
    )



def heroshot_html():
    front, back = MOD["inventario"], MOD["finanzas"]
    sz = "(max-width:900px) 92vw, 600px"
    return """        <div class="hv-card hv-card--back">%s</div>
        <div class="hv-card hv-card--front">%s<span class="hv-bar" aria-hidden="true"></span></div>
        <span class="hv-chip hv-chip--a"><b aria-hidden="true">✓</b> Auto transferido: el estado cambia solo</span>
        <span class="hv-chip hv-chip--b"><b aria-hidden="true">$</b> Moneda local y dólares</span>
        <span class="hv-chip hv-chip--c"><b aria-hidden="true">●</b> Vitrina actualizada</span>""" % (
        shot(back, sizes=sz), shot(front, sizes=sz, eager=True))


def build_home():
    p = os.path.join(ROOT, "index.html")
    text = open(p, encoding="utf-8").read()
    home_title = "Tablero | Sistema de gestión para agencias de autos usados"
    home_desc = "Tablero es el sistema de gestión para agencias de autos usados: inventario, finanzas en moneda local y USD, gestoría, detailing, visitas y tareas, a tu medida."
    nodes = [org_jsonld(), person_jsonld(), website_jsonld(), software_jsonld(), webpage_jsonld("/", home_title, home_desc),
             faq_jsonld([FAQ[k] for k in HOME_FAQ])]
    text = fill_markers(text, "HEAD", head_html(home_title, home_desc, "/", nodes))
    text = fill_markers(text, "NAV", nav_html())
    text = fill_markers(text, "SLIDES", slides_html())
    text = fill_markers(text, "FAQ", faq_html(HOME_FAQ))
    text = fill_markers(text, "FOOTER", footer_html(brand_img=True))
    text = fill_markers(text, "HEROSHOT", heroshot_html())
    text = fill_markers(text, "PRICING", pricing_html())
    open(p, "w", encoding="utf-8").write(text)
    return home_title, home_desc


def llms_txt():
    L = ["# Tablero", "",
         "> Tablero es un sistema de gestión hecho a medida para agencias de autos usados. Sirve a agencias de cualquier país. Reúne inventario de autos y motos, finanzas en tu moneda local y en dólares, gestoría con checklist de documentación, detailing, agenda de visitas y tareas del equipo, con ocho roles de usuario y una vitrina web sincronizada con el stock. Planes: Esencial USD 100 por mes, Completo USD 150 por mes y A Medida por consulta.", "",
         "Contacto: WhatsApp %s · %s/" % (PHONE_DISPLAY, SITE_URL), "",
         "## Qué es y para quién", "",
         "- [Sistema de gestión para agencia de autos usados](%s/sistema-de-gestion-para-agencia-de-autos-usados/): el ciclo completo del auto, del stock a la transferencia." % SITE_URL,
         "- [Software para concesionaria](%s/software-para-concesionaria/): equipo con roles, caja en dos monedas, trámites y vitrina conectados." % SITE_URL,
         "- [Preguntas frecuentes](%s/preguntas-frecuentes/): precios, monedas, vitrina, roles y cómo empezar." % SITE_URL,
         "- [Sobre Tablero](%s/sobre-tablero/): quién lo hace y desde cuándo funciona." % SITE_URL, "",
         "## Módulos", ""]
    for m in MODULES:
        L.append("- [%s](%s%s): %s" % (m["name"], SITE_URL, mod_url(m["key"]), m["short"]))
    L += ["", "## Guías del blog", ""]
    for q in blog.POSTS:
        L.append("- [%s](%s%s): %s" % (q["title"], SITE_URL, blog.post_url(q["slug"]), q["desc"]))
    return "\n".join(L) + "\n"


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
    write("/blog/index.html", blog_index_page())
    urls.append(("/blog/", "0.8"))
    for q in blog.POSTS:
        write(blog.post_url(q["slug"]) + "index.html", post_page(q))
        urls.append((blog.post_url(q["slug"]), "0.6"))
        full = q["title"]
        if len(full) > 62:
            problems.append("title de post largo (%d): %s" % (len(full), full))
        if not (110 <= len(q["desc"]) <= 165):
            problems.append("desc de post fuera de rango (%d): %s" % (len(q["desc"]), q["slug"]))
    write("/blog/feed.xml", rss_xml())
    write("/llms.txt", llms_txt())
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, prio in urls:
        sm.append("  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (SITE_URL, u, LASTMOD, prio))
    sm.append("</urlset>")
    write("/sitemap.xml", "\n".join(sm) + "\n")
    write("/robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL)
    write("/404.html", page_404())
    print("Páginas generadas: %d (+ home, blog y %d artículos)" % (len(all_pages), len(blog.POSTS)))
    for p in problems:
        print("AVISO:", p)


if __name__ == "__main__":
    build()
