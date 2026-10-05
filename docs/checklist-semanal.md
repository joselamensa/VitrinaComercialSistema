# Checklist semanal de SEO para tablero.uno

Dedicale 45–60 minutos por semana, siempre el mismo día. Anotá lo que veas en la tabla del final:
**solo datos reales**, tal como los muestra Search Console.

## Cada semana
### 1. Search Console (15 min)
- [ ] **Páginas**: ¿hay URLs con error o «excluidas» que no esperabas? Abrí el detalle y anotá el motivo.
- [ ] **Páginas**: ¿las URLs nuevas de la semana ya figuran como indexadas? Si no, usá Inspección de URLs → «Solicitar indexación».
- [ ] **Sitemaps**: sigue en «Correcto» y con la cantidad de URLs esperada.
- [ ] **Rendimiento** (últimos 28 días, comparar con el período anterior): anotá clics, impresiones, CTR y posición media.
- [ ] **Rendimiento → Consultas**: ¿qué búsquedas traen impresiones? Anotá 3 que no habías contemplado: pueden ser artículos nuevos.
- [ ] **Rendimiento → Páginas**: ¿qué páginas tienen muchas impresiones y poco CTR? Mejorá su título y descripción.

### 2. Contenido (20–30 min)
- [ ] Publicar o programar **1 artículo nuevo** del blog (ver ideas abajo).
- [ ] Revisar **1 artículo existente**: ¿responde la pregunta en los primeros párrafos? ¿Tiene enlaces internos a módulos y a otros artículos?
- [ ] Cada artículo nuevo debe: enlazar al menos a 1 módulo, ser enlazado desde 2 artículos existentes y sumarse con `python3 tools/build.py` (el sitemap, el RSS y el footer se actualizan solos).
- [ ] No repetir la misma consulta en dos artículos: si ya hay uno, ampliarlo.

### 3. Salud técnica (5 min)
- [ ] La home y un módulo cargan bien en el celular.
- [ ] Ningún enlace roto nuevo (revisá que los artículos nuevos enlacen a URLs existentes).
- [ ] Probar el botón de WhatsApp: abre el chat con el mensaje esperado.

### 4. Difusión (10 min)
- [ ] Compartir el artículo de la semana en LinkedIn (textos en `docs/difusion.md`).
- [ ] Responder consultas o comentarios recibidos en LinkedIn y YouTube.
- [ ] Avanzar con **1 directorio** pendiente de la lista.

## Cada mes
- [ ] **PageSpeed Insights** (móvil) de la home y de una página de módulo; anotar problemas nuevos.
- [ ] **Core Web Vitals** en Search Console (si ya hay datos).
- [ ] **Datos estructurados** sin errores nuevos.
- [ ] Actualizar `LASTMOD` en `tools/content.py` y `PUBLISHED`/fechas de los artículos que se hayan revisado de verdad.
- [ ] Preguntarle a cada cliente o contacto nuevo **cómo llegó a Tablero** y anotar la respuesta: es la medición más confiable hoy.
- [ ] Revisar quién enlaza al sitio (Search Console → Enlaces) y agradecer / reforzar.

## Ideas de artículos pendientes (todas son preguntas reales de una agencia)
Priorizá las que aparezcan como consultas en Search Console o las que más te pregunten los clientes.
- Cómo calcular cuánto tiempo lleva cada auto en stock y qué hacer con los que más tardan.
- Cómo registrar una seña y una reserva sin perder el rastro de la plata.
- Qué datos conviene pedir al cliente en una visita.
- Cómo armar el checklist de recepción de un auto usado (compra o toma en parte de pago).
- Cómo organizar un equipo de ventas: roles y responsabilidades.
- Gastos fijos y variables de una agencia de autos: cómo categorizarlos.
- Cómo sacar buenas fotos de un auto usado para la vitrina.

## Tabla de seguimiento (completar con datos reales)
| Semana | Clics | Impresiones | CTR | Posición media | URLs indexadas | Consultas nuevas | Qué hice | Qué haré |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |
