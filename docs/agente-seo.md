# Agente SEO semanal de Tablero

Un agente de Claude que, una vez por semana (lunes por la mañana, hora de Argentina), revisa el sitio y publica **una mejora** directamente en `main`, solo si las verificaciones pasan.
Este archivo es su instrucción permanente y sus reglas. Si cambia la estrategia, se edita acá.

## Por qué semanal y con una sola mejora por vez
- Google tarda días en reflejar cambios y los datos de Search Console van con 2–3 días de demora: mirar todos los días es ruido.
- El dueño autorizó publicar directo a `main`. La red de seguridad es: verificaciones obligatorias antes de publicar, **un solo cambio pequeño por semana** (fácil de revertir con `git revert`) y una bitácora.
- Nada de lo que haga el agente garantiza posiciones. Su trabajo es aplicar buenas prácticas con constancia.

## Qué hace en cada ejecución
1. Asegurar el repo `joselamensa/VitrinaComercialSistema` (si no está clonado, `add_repo` con acceso `push`) y hacer `git pull` de `main`.
2. `python3 tools/gsc_report.py` → si dice `SIN_DATOS`, seguir con los pasos 3–5 sin datos.
2b. `python3 tools/gsc_inspect.py` → tabla de cómo ve Google cada URL del sitemap. «Descubierta/Rastreada: sin indexar» en páginas nuevas es normal las primeras semanas; si una página sigue así tras ~4 semanas, mejorarla (más enlaces internos, contenido más útil). Las variantes http/sin-www con «Página con redirección» son correctas (apuntan a la canónica www).
2c. `python3 tools/update_rate.py` → actualiza las cotizaciones en `tools/rate.json` para el switch de moneda de los planes (ARS: dólar oficial venta; UYU, CLP, MXN, COP, PEN, BRL y EUR: referencia). Si falla, se conserva el valor anterior y se anota en la bitácora. Cada lunes, aunque no haya otro cambio, se publica la cotización nueva.
3. `python3 tools/build.py && python3 tools/check_site.py` → debe terminar sin problemas. Arreglar lo que falle (enlaces rotos, `alt`, JSON-LD, títulos/descripciones fuera de rango).
4. Elegir **una** mejora, por orden de prioridad:
   1. Corrección técnica detectada en el paso 3.
   2. Mejora de `title`/`description` de una página con muchas impresiones y CTR bajo (datos reales).
   3. **Un artículo nuevo** para la mejor oportunidad: una consulta con impresiones y posición 8–30, o una pregunta pendiente de `docs/checklist-semanal.md`.
   4. Ampliar un artículo existente que ya recibe impresiones.
5. Registrar en `docs/seo-log.md` la fecha, los números reales del reporte y qué se cambió.
6. `python3 tools/build.py && python3 tools/check_site.py`. **Si falla, no publicar**: revertir el cambio y dejar el motivo en `docs/seo-log.md`.
7. Commit con mensaje claro (qué cambió y qué dato lo motivó) y push a `main`.
8. Esperar ~2 minutos a que Vercel despliegue y correr `python3 tools/indexnow.py --changed` para avisar a Bing y otros buscadores (Google no usa IndexNow). Si falla por red, anotarlo en la bitácora y seguir.

## Reglas editoriales (no negociables)
- **No inventar** cifras, estudios, porcentajes, clientes, testimonios, premios, precios ni funciones. Sobre Tablero solo se afirma lo que ya está en `tools/content.py` y en el sitio.
- Trámites y temas legales: explicar lo general, avisar que los requisitos varían y remitir al gestor o al Registro.
- Un artículo responde **una** pregunta real de una agencia de autos usados, en español rioplatense, 600–900 palabras, con H2 claros, enlaces a al menos un módulo y a dos artículos existentes, y CTA a WhatsApp.
- No duplicar: si ya existe un artículo sobre esa consulta, ampliarlo en lugar de crear otro.
- Fechas: `PUBLISHED` y `LASTMOD` solo con la fecha real de la edición.

## Prohibido
- Relleno de palabras clave, texto oculto, páginas masivas casi iguales, comprar o intercambiar enlaces, reseñas falsas.
- Tocar diseño general, los precios en USD de los planes (la conversión a pesos sí se actualiza sola), datos de contacto, textos legales o `vercel.json` sin pedirlo antes a una persona.
- Publicar más de una mejora por ejecución, o publicar con las verificaciones en rojo.
- Pedir o imprimir credenciales en el chat o en el PR.

## Credenciales de Search Console (opcional pero recomendado)
Sin ellas el agente solo hace chequeos técnicos y artículos de la lista de pendientes. Con ellas decide con datos reales.
1. En Google Cloud: crear un proyecto, habilitar **Google Search Console API** y crear una **cuenta de servicio**; descargar su clave JSON.
2. En Search Console → Configuración → Usuarios y permisos: agregar el email de la cuenta de servicio con permiso **Restringido** (solo lectura).
3. En el entorno de la nube (menú del entorno en la barra del título → Editar): guardar
   - `GSC_SERVICE_ACCOUNT_JSON` = contenido completo del JSON
   - `GSC_SITE` = `sc-domain:tablero.uno` (propiedad de dominio) o `https://www.tablero.uno/`
4. En **Acceso a la red** del entorno: permitir `api.indexnow.org` (IndexNow), `dolarapi.com` y `open.er-api.com` (cotizaciones),  `searchconsole.googleapis.com`, `oauth2.googleapis.com` y mantener la lista de gestores de paquetes (para `pip install google-auth requests`).
5. **Nunca pegues la clave en el chat.**
