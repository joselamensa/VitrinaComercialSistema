# Verificación y puesta en marcha de Google Search Console

Sitio: `https://www.tablero.uno/` · Sitemap: `https://www.tablero.uno/sitemap.xml`

> Search Console es gratis y es la única fuente confiable de lo que Google realmente ve de tu sitio
> (indexación, consultas, clics, errores). Nada de lo que sigue promete posiciones: Google decide
> si indexa y cómo rankea cada página.

## 1. Crear la propiedad

Entrá a <https://search.google.com/search-console> con la cuenta de Google que va a administrar el sitio.

**Opción recomendada: propiedad de dominio** (cubre `tablero.uno`, `www`, http y https).
1. «Añadir propiedad» → **Dominio** → escribí `tablero.uno`.
2. Google te da un registro **TXT**. Agregalo en el DNS del dominio (donde registraste `tablero.uno`
   o en Vercel → Domains, si ahí administrás el DNS).
3. Volvé a Search Console y tocá **Verificar**. El DNS puede tardar desde minutos hasta unas horas.

**Opción alternativa: prefijo de URL con etiqueta HTML** (si no podés tocar el DNS).
1. «Añadir propiedad» → **Prefijo de URL** → `https://www.tablero.uno/`.
2. Elegí el método **Etiqueta HTML** y copiá solo el valor de `content="..."`.
3. Pegalo en `tools/content.py`, en `GSC_TOKEN = "..."`.
4. Ejecutá `python3 tools/build.py`, commiteá y esperá a que Vercel despliegue.
5. Verificá en Search Console. **No borres la etiqueta** después: Google la vuelve a comprobar de forma periódica.

## 2. Enviar el sitemap
En **Sitemaps** → escribí `sitemap.xml` → Enviar. Debería decir «Correcto» y detectar las 22 URLs
(home, 2 páginas por intención, hub de módulos, 6 módulos, FAQ, blog y 10 artículos).
El sitemap se regenera con `python3 tools/build.py`.

## 3. Pedir indexación de las páginas clave
En la barra superior pegá cada URL → **Inspección de URLs** → «Solicitar indexación». Hay un cupo diario
limitado; empezá por estas, en este orden:

1. `https://www.tablero.uno/`
2. `https://www.tablero.uno/sistema-de-gestion-para-agencia-de-autos-usados/`
3. `https://www.tablero.uno/software-para-concesionaria/`
4. `https://www.tablero.uno/modulos/`
5. `https://www.tablero.uno/blog/`
6. Las 6 páginas de módulo y los artículos, a razón de unas pocas por día.

Pedir indexación **acelera el descubrimiento, no garantiza** que la página se indexe.

## 4. Revisar que el dominio esté bien configurado
- `https://tablero.uno/` debe redirigir con 301 a `https://www.tablero.uno/` (ya está en `vercel.json`;
  además el dominio sin www tiene que estar agregado al proyecto de Vercel).
- `http://` debe redirigir a `https://` (Vercel lo hace por defecto).
- Probá `https://www.tablero.uno/robots.txt` y `.../sitemap.xml`: tienen que abrir sin error.

## 5. Informes que importan (y qué mirar)
| Informe | Qué mirar | Cada cuánto |
|---|---|---|
| **Páginas** (Indexación) | Cuántas URLs están indexadas y por qué otras no. «Detectada, actualmente sin indexar» es normal en sitios nuevos al principio. | Semanal |
| **Rendimiento** | Consultas, páginas, clics, impresiones, CTR y posición media. Solo hay datos reales cuando Google empieza a mostrar el sitio. | Semanal |
| **Experiencia → Core Web Vitals** | Aparece cuando hay suficientes visitas reales. | Mensual |
| **Mejoras → Migas de pan / Datos estructurados** | Errores o advertencias en el JSON-LD. | Tras cada cambio de plantilla |
| **Acciones manuales / Seguridad** | Debe decir «Ninguna». | Mensual |

## 6. Complementos recomendados
- **Bing Webmaster Tools** (<https://www.bing.com/webmasters>): se puede importar la propiedad desde Search Console en un clic. Sirve también para otros buscadores.
- **PageSpeed Insights** (<https://pagespeed.web.dev/>): probá la home y una página de módulo en móvil.
- **Prueba de resultados enriquecidos** (<https://search.google.com/test/rich-results>): validá una página con JSON-LD.
- **Analítica de visitas**: el sitio no tiene ninguna instalada. Si querés medir visitas y clics a WhatsApp,
  agregá una herramienta liviana de analítica; Search Console solo mide lo que pasa en Google.

## 7. Qué esperar
- Un sitio nuevo suele tardar semanas en mostrar datos estables. No hay plazos garantizados.
- El tráfico orgánico depende del contenido útil, de la autoridad del sitio (enlaces de otros sitios) y de la competencia.
  Por eso el plan incluye blog constante y presencia en directorios: ver `docs/checklist-semanal.md` y `docs/difusion.md`.
