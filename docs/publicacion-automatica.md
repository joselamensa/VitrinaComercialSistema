# Publicación automática en YouTube y en la página de LinkedIn

Objetivo: que una rutina de Claude pueda subir videos al canal **@Tablero-uno** y publicar en la página de LinkedIn
**Tablero**, con autorizaciones tuyas. Los programas están en `tools/social/`.

> Estado: los programas están escritos pero **sin probar contra las APIs reales** (hacen falta tus credenciales).
> Es normal que haya que ajustar detalles en la primera prueba.

**Reglas de seguridad**
- Los tokens y claves se guardan **solo** en el entorno de la nube (menú del entorno → Editar → Variables de entorno). **Nunca en un chat ni en el repositorio.**
- Las variables del entorno las puede ver cualquiera que use ese entorno; si lo compartís con alguien, avisá.
- Si una clave se filtra: revocala (Google: myaccount.google.com/permissions · LinkedIn: borrar/regenerar el secret de la app) y repetí la autorización.
- Los pasos de autorización (los que abren el navegador) se hacen **en tu computadora**, con Python 3 y este repositorio clonado.

Recomendación de orden: **empezá hoy por LinkedIn** (la aprobación de LinkedIn es manual y lenta) y avanzá YouTube en paralelo.

---

## Parte A — YouTube

### A1. Habilitar la API (proyecto de Google Cloud «Tablero Uno», el mismo que ya usás)
1. console.cloud.google.com → menú → **APIs y servicios → Biblioteca**.
2. Buscá **YouTube Data API v3** → **Habilitar**.

### A2. Pantalla de consentimiento de OAuth
1. **APIs y servicios → Pantalla de consentimiento de OAuth** (o «Google Auth Platform»).
2. Tipo de usuario: **Externo**. Nombre de la app: «Tablero publicador». Tu correo en soporte y contacto.
3. **Permisos (scopes)**: agregá `.../auth/youtube.upload` y `.../auth/youtube.readonly`.
4. **Usuarios de prueba**: agregá la cuenta de Google dueña del canal.
5. **MUY IMPORTANTE:** al terminar, pasá la app a **«En producción» (Publicar aplicación)**. Si queda en «Prueba», el refresh token **vence a los 7 días**. Al publicarla sin verificar, Google mostrará un aviso de «app no verificada» al autorizar: para uso propio es aceptable (límite de 100 usuarios).

### A3. Credencial de OAuth
1. **Credenciales → Crear credenciales → ID de cliente de OAuth**.
2. Tipo de aplicación: **Aplicación de escritorio**. Nombre: «Tablero publicador».
3. Copiá el **ID de cliente** y el **Secreto de cliente** (no los compartas).

### A4. Autorizar (en tu computadora)
```
git pull
python3 tools/social/oauth_youtube.py
```
Pegá el ID y el secreto (el secreto no se ve al escribirlo). Se abre el navegador: iniciá sesión con la cuenta dueña del canal
(si te pregunta qué canal, elegí **Tablero-uno**) y aceptá. En la terminal aparece el **refresh token**.

### A5. Variables en el entorno de la nube
- `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`
- **Acceso a la red → Personalizado**: permitir `www.googleapis.com` y `oauth2.googleapis.com`.
- Formato (una por línea): `YT_CLIENT_ID='...'`

### A6. Auditoría de la API (para publicar videos como públicos)
Google deja en **privado** los videos subidos por API desde proyectos nuevos **sin auditar**. Para quitar esa restricción:
completá el formulario **«YouTube API Services – Audit and Quota Extension»**: https://support.google.com/youtube/contact/yt_api_form
(uso: «subir videos propios al canal de mi empresa»). Puede tardar semanas.
Mientras tanto el flujo es: la rutina sube el video en privado y vos lo pasás a público (o lo programás) desde YouTube Studio con un clic.

Cuota: cada subida gasta 1.600 de las 10.000 unidades diarias, o sea unas 6 subidas por día.

### A7. Probar
```
python3 tools/social/youtube_upload.py video.mp4 --title "Prueba" --description "Prueba" --privacy private
```

---

## Parte B — LinkedIn (página de empresa)

LinkedIn solo permite publicar en páginas de empresa por API con el producto **Community Management API**, que requiere **aprobación manual**.
No puedo asegurar que la aprueben ni cuánto tarda.

### B1. Crear la app
> **Importante (comprobado):** LinkedIn exige que **Community Management API sea el ÚNICO producto de la app**. Si una app ya tiene otro producto
> (por ejemplo «Share on LinkedIn», que LinkedIn agrega solo al crearla), el botón *Request access* queda bloqueado. Hay que crear una **app dedicada**,
> con otro nombre (p. ej. «Tablero publicador»), y pedir ese producto **antes** de agregar cualquier otro. Si LinkedIn le puso «Share on LinkedIn», quitalo.
1. linkedin.com/developers/apps → **Create app**.
2. Nombre: «Tablero publicador». **LinkedIn Page:** elegí la página **Tablero**. Logo: `assets/logo.png`.
3. LinkedIn genera un enlace de **verificación**: el **super administrador** de la página debe abrirlo y aprobar la asociación.

### B2. Pedir el producto
1. En la app, pestaña **Products** → **Community Management API** → **Request access**.
2. Completá el formulario: uso = «publicar contenido propio de la empresa (artículos del blog y videos) en su página de LinkedIn»;
   empresa Tablero, sitio https://www.tablero.uno, contacto tuyo. Si piden un video demostrativo del flujo, describí el proceso: un script publica en la página propia.
3. Esperá la aprobación (puede aparecer por correo).

### B3. Configurar la redirección
- Pestaña **Auth** → **Authorized redirect URLs for your app** → agregar exactamente:
  `http://127.0.0.1:8977/callback`
- Copiá **Client ID** y **Primary Client Secret**.

### B4. Número de la página (`LI_ORG_ID`)
Entrá a la administración de la página de LinkedIn: la URL tiene la forma `linkedin.com/company/NÚMERO/admin/...`. Ese número es `LI_ORG_ID`.

### B5. Autorizar (en tu computadora, cuando el producto esté aprobado)
```
python3 tools/social/oauth_linkedin.py
```
Imprime `LI_ACCESS_TOKEN` (dura unos 60 días) y, solo si LinkedIn lo entrega, `LI_REFRESH_TOKEN`.
Sin refresh token habrá que repetir este paso cada ~60 días.

### B6. Variables y red en la nube
- `LI_ACCESS_TOKEN`, `LI_ORG_ID` (+ `LI_CLIENT_ID`, `LI_CLIENT_SECRET`, `LI_REFRESH_TOKEN` si hay refresh token)
- Red: permitir `api.linkedin.com` y `www.linkedin.com`.
- Si LinkedIn rechaza la versión de la API, definí `LI_API_VERSION` (formato AAAAMM) con una versión vigente.

### B7. Probar
```
python3 tools/social/linkedin_post.py --check
python3 tools/social/linkedin_post.py --text "Prueba" --link https://www.tablero.uno/blog/
```
(borrá la publicación de prueba desde la página).

---

## Parte C — Cuando ambas funcionen
Se crea una rutina semanal que publica desde una cola de contenido del repositorio (texto de LinkedIn + video/título/descripción de YouTube),
sin inventar datos y respetando las reglas editoriales de `docs/agente-seo.md`. Se define una vez que las dos autorizaciones estén probadas.

Pendiente conocido: subir videos a LinkedIn (la API de videos tiene varios pasos); por ahora se publican textos con enlace.
