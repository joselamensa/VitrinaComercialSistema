# Agente SEO semanal de Tablero

Un agente de Claude que, una vez por semana, revisa el sitio y propone mejoras **mediante un pull request**.
Este archivo es su instrucción permanente y sus reglas. Si cambia la estrategia, se edita acá.

## Por qué semanal y con PR (y no «todos los días, solo»)
- Google tarda días en reflejar cambios y los datos de Search Console van con 2–3 días de demora: mirar todos los días es ruido.
- Un agente que edita producción sin revisión puede degradar el sitio o publicar algo falso sin que nadie se entere. El PR es la red de seguridad.
- Nada de lo que haga el agente garantiza posiciones. Su trabajo es aplicar buenas prácticas con constancia.

## Qué hace en cada ejecución
1. `git pull` de `main`; crear rama `seo/AAAA-MM-DD`.
2. `python3 tools/gsc_report.py` → si dice `SIN_DATOS`, seguir con los pasos 3–5 sin datos.
3. `python3 tools/build.py && python3 tools/check_site.py` → debe terminar sin problemas. Arreglar lo que falle (enlaces rotos, `alt`, JSON-LD, títulos/descripciones fuera de rango).
4. Elegir **una** mejora, por orden de prioridad:
   1. Corrección técnica detectada en el paso 3.
   2. Mejora de `title`/`description` de una página con muchas impresiones y CTR bajo (datos reales).
   3. **Un artículo nuevo** para la mejor oportunidad: una consulta con impresiones y posición 8–30, o una pregunta pendiente de `docs/checklist-semanal.md`.
   4. Ampliar un artículo existente que ya recibe impresiones.
5. Registrar en `docs/seo-log.md` la fecha, los números reales del reporte y qué se cambió.
6. `python3 tools/build.py` → commit → push de la rama → **abrir PR hacia `main`** con: datos usados, qué cambió y por qué, y qué debe revisar una persona.

## Reglas editoriales (no negociables)
- **No inventar** cifras, estudios, porcentajes, clientes, testimonios, premios, precios ni funciones. Sobre Tablero solo se afirma lo que ya está en `tools/content.py` y en el sitio.
- Trámites y temas legales: explicar lo general, avisar que los requisitos varían y remitir al gestor o al Registro.
- Un artículo responde **una** pregunta real de una agencia de autos usados, en español rioplatense, 600–900 palabras, con H2 claros, enlaces a al menos un módulo y a dos artículos existentes, y CTA a WhatsApp.
- No duplicar: si ya existe un artículo sobre esa consulta, ampliarlo en lugar de crear otro.
- Fechas: `PUBLISHED` y `LASTMOD` solo con la fecha real de la edición.

## Prohibido
- Relleno de palabras clave, texto oculto, páginas masivas casi iguales, comprar o intercambiar enlaces, reseñas falsas.
- Tocar diseño general, precios/planes, datos de contacto, textos legales o `vercel.json` sin pedirlo antes a una persona.
- Hacer push directo a `main` (salvo que una persona lo habilite por escrito).
- Pedir o imprimir credenciales en el chat o en el PR.

## Credenciales de Search Console (opcional pero recomendado)
Sin ellas el agente solo hace chequeos técnicos y artículos de la lista de pendientes. Con ellas decide con datos reales.
1. En Google Cloud: crear un proyecto, habilitar **Google Search Console API** y crear una **cuenta de servicio**; descargar su clave JSON.
2. En Search Console → Configuración → Usuarios y permisos: agregar el email de la cuenta de servicio con permiso **Restringido** (solo lectura).
3. En el entorno de la nube (menú del entorno en la barra del título → Editar): guardar
   - `GSC_SERVICE_ACCOUNT_JSON` = contenido completo del JSON
   - `GSC_SITE` = `sc-domain:tablero.uno` (propiedad de dominio) o `https://www.tablero.uno/`
4. En **Acceso a la red** del entorno: permitir `searchconsole.googleapis.com`, `oauth2.googleapis.com` y mantener la lista de gestores de paquetes (para `pip install google-auth requests`).
5. **Nunca pegues la clave en el chat.**
