# -*- coding: utf-8 -*-
"""Contenido del sitio (fuente única). Todo lo que se afirma acá sale de lo que
ya muestra la landing y las capturas del producto. No se inventan métricas,
integraciones ni funciones. Si algo no está confirmado, se deriva a WhatsApp."""

SITE_URL = "https://www.tablero.uno"
SITE_NAME = "Tablero"
WA_NUMBER = "5491122699526"
PHONE_DISPLAY = "+54 9 11 2269-9526"
OG_IMAGE = "/assets/og-image.jpg"
LASTMOD = "2026-10-05"
# Pegá acá el token de verificación de Google Search Console (solo el valor de content="...").
# Si queda vacío no se emite la meta. Ver docs/search-console.md
GSC_TOKEN = ""


def wa(text="Hola! Quiero conocer Tablero para mi agencia."):
    from urllib.parse import quote
    return "https://wa.me/%s?text=%s" % (WA_NUMBER, quote(text, safe="!"))


ICONS = {
    "inventario": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 13l1.5-4.5A2 2 0 0 1 6.4 7h11.2a2 2 0 0 1 1.9 1.5L21 13"/><rect x="2" y="13" width="20" height="6" rx="1.5"/><circle cx="7" cy="19" r="1.5"/><circle cx="17" cy="19" r="1.5"/></svg>',
    "finanzas": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="2" y="6" width="20" height="14" rx="2"/><path d="M2 10h20"/><path d="M6 15h4"/></svg>',
    "gestoria": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 2h6l1 3h3v17H5V5h3l1-3z"/><path d="M9 11h6M9 15h6"/></svg>',
    "detailing": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M14.7 6.3a1 1 0 0 0-1.4 0l-6 6a1 1 0 0 0 0 1.4l3 3a1 1 0 0 0 1.4 0l6-6a1 1 0 0 0 0-1.4l-3-3z"/><path d="M17 3l4 4"/><path d="M3 21l4-1 8.5-8.5"/></svg>',
    "visitas": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
    "tareas": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>',
    "vitrina": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></svg>',
    "roles": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6.5 6.5-6.5s6.5 2.9 6.5 6.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14c2.2.7 3.5 2.6 3.5 6"/></svg>',
    "medida": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2"/><circle cx="8" cy="17" r="2"/></svg>',
    "moneda": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="9"/><path d="M14.5 9.2c-.4-.8-1.3-1.2-2.5-1.2-1.5 0-2.5.8-2.5 1.9 0 2.7 5.2 1.3 5.2 4 0 1.1-1.1 1.9-2.7 1.9-1.3 0-2.3-.5-2.7-1.4M12 6.5V8m0 8v1.5"/></svg>',
}

# ---------------------------------------------------------------- MODULOS
MODULES = [
    dict(
        key="inventario", slug="inventario-de-autos", name="Inventario", img="inventario", dark=True,
        badge="Stock en tiempo real",
        blurb="Cada auto o moto con su ficha completa: dominio, marca, modelo, año, km y precio en pesos o dólares, con historial de cambios de precio y galería de fotos.",
        alt="Panel de administración de Tablero con el listado de autos: dominio, marca, modelo, año, fecha de ingreso, vendedor y estado de cada unidad",
        alt_dark="Panel de administración de Tablero con el listado de autos de la agencia, en modo oscuro",
        title="Inventario de autos usados: control de stock | Tablero",
        desc="Controlá el stock de tu agencia: ficha de cada auto o moto con dominio, km, precio en USD o ARS, historial de precios, fotos y vendedor asignado.",
        h1="Inventario de autos usados para tu agencia",
        lead="Cada auto o moto con su ficha completa y su estado siempre al día, en un solo lugar y sin planillas sueltas.",
        short="Fichas de autos y motos, precios en USD o ARS y stock siempre al día.",
    ),
    dict(
        key="finanzas", slug="finanzas-agencia-de-autos", name="Finanzas", img="finanzas", dark=True,
        badge="Bimonetario USD / ARS",
        blurb="Ingresos y salidas con categoría, monto, moneda, medio de pago y comprobante. Cargás la cotización una vez y el sistema convierte todo solo.",
        alt="Inicio del módulo de finanzas de Tablero con ingresos, salidas y neto en pesos y en dólares, últimos movimientos y totales por medio de pago",
        alt_dark="Inicio del módulo de finanzas de Tablero con ingresos, salidas y neto en pesos y dólares, en modo oscuro",
        title="Finanzas para agencias de autos: USD y ARS | Tablero",
        desc="Ingresos y salidas con categoría, medio de pago y comprobante, en pesos y dólares. Cargás la cotización una vez y Tablero convierte todo solo.",
        h1="Control de finanzas para agencias de autos, en pesos y dólares",
        lead="Registrá cada ingreso y cada salida con su categoría, moneda, medio de pago y comprobante, y mirá el neto de tu agencia en ARS y en USD.",
        short="Ingresos y salidas en pesos y dólares, con medios de pago y comprobantes.",
    ),
    dict(
        key="gestoria", slug="gestoria-automotor", name="Gestoría", img="gestoria", dark=True,
        badge="Documentación al día",
        blurb="Checklist por auto: título, cédula, formulario 08, verificación policial e informe de dominio. Al marcar «Transferido», el auto cambia de estado solo.",
        alt="Pantalla de gestoría pendientes de Tablero con el checklist de documentación y pagos de cada vehículo y su estado",
        alt_dark="Pantalla de gestoría pendientes de Tablero con el checklist de documentación de cada vehículo, en modo oscuro",
        title="Gestoría de autos usados: checklist por unidad | Tablero",
        desc="Seguí la documentación de cada auto: título, cédula, formulario 08, verificación policial e informe de dominio. Al transferir, el estado cambia solo.",
        h1="Gestoría de autos usados: la documentación de cada unidad, al día",
        lead="Un checklist por auto para saber de un vistazo qué papeles tiene, cuáles faltan y cuáles están listos para transferir.",
        short="Checklist de documentación por auto y seguimiento hasta la transferencia.",
    ),
    dict(
        key="detailing", slug="detailing-de-autos", name="Detailing", img="detailing", dark=False,
        badge="Control de calidad",
        blurb="Catálogo de servicios de preparación con precio, asignados a cada auto con seguimiento de si ya se hicieron. Vuelve solo a Disponible al terminar.",
        alt="Lista de servicios de detailing disponibles en Tablero, con nombre y precio de cada servicio y un formulario para agregar uno nuevo",
        alt_dark="",
        title="Detailing de autos usados: servicios y seguimiento | Tablero",
        desc="Armá el catálogo de servicios de preparación con su precio, asignalos a cada auto y seguí cuáles ya se hicieron. Al terminar, vuelve a Disponible.",
        h1="Detailing y preparación de autos usados, con seguimiento",
        lead="Definí qué servicios ofrecés, asignalos a cada auto y controlá cuáles ya se hicieron antes de volver a ponerlo a la venta.",
        short="Catálogo de servicios de preparación asignados a cada auto.",
    ),
    dict(
        key="visitas", slug="visitas-y-agenda", name="Visitas", img="visitas", dark=True,
        badge="Agenda coordinada",
        blurb="Agenda de visitas con fecha, horario, vendedor asignado y soporte que coordina. Horarios por vendedor, con excepciones por fecha.",
        alt="Listado de visitas de Tablero con cliente, fecha, horario, vendedor, asesor, estado y comentarios, y un calendario de visitas debajo",
        alt_dark="Listado y calendario de visitas de Tablero, en modo oscuro",
        title="Agenda de visitas para agencias de autos | Tablero",
        desc="Agendá visitas con fecha, horario y vendedor asignado, con soporte que coordina y horarios por vendedor con excepciones por fecha.",
        h1="Agenda de visitas para tu agencia de autos",
        lead="Cada visita con su fecha, su horario y el vendedor que la atiende, coordinada por el equipo de soporte y visible en un calendario.",
        short="Agenda de visitas por vendedor, con calendario y horarios propios.",
    ),
    dict(
        key="tareas", slug="tareas-del-equipo", name="Tareas", img="tareas", dark=False,
        badge="Equipo sincronizado",
        blurb="Tareas internas asignadas entre el equipo, con urgencia, estado y comentarios. Nada se pierde en un chat: queda todo escrito y con responsable.",
        alt="Calendario de tareas de Tablero con urgencia baja, media y alta, y botones para crear una tarea o ver la lista",
        alt_dark="",
        title="Tareas del equipo para agencias de autos | Tablero",
        desc="Asigná tareas internas con urgencia, estado y comentarios. Todo queda escrito y con responsable, en lista o en calendario.",
        h1="Tareas del equipo: que nada se pierda en un chat",
        lead="Asigná tareas entre las personas de tu agencia, con urgencia, estado y comentarios, y dejá de depender de mensajes sueltos.",
        short="Tareas internas con responsable, urgencia, estado y comentarios.",
    ),
]
MOD = {m["key"]: m for m in MODULES}


def mod_url(key):
    return "/modulos/%s/" % MOD[key]["slug"]


# ------------------------------------------------------------------- FAQ
FAQ = {
    "que-es": (
        "¿Qué es Tablero?",
        "Tablero es un sistema de gestión para agencias de autos usados. Reúne en un solo lugar inventario, finanzas, gestoría, detailing, visitas y tareas, y se adapta a cómo trabaja tu agencia.",
    ),
    "para-quien": (
        "¿Para qué tipo de negocio sirve?",
        "Para agencias y concesionarias que compran y venden autos usados y motos. Para estructuras grandes o con varias sucursales existe el plan A Medida, donde roles, flujos e integraciones se definen en conjunto.",
    ),
    "precio": (
        "¿Cuánto cuesta Tablero?",
        "Hay tres planes: Esencial, Completo y A Medida. No publicamos precios fijos porque dependen de los módulos y de lo que necesite tu agencia; lo definimos juntos por WhatsApp, sin letra chica.",
    ),
    "monedas": (
        "¿Maneja pesos y dólares?",
        "Sí. Tablero tiene gestión bimonetaria (USD y ARS): los autos pueden tener precio en pesos o en dólares y, en finanzas, cargás la cotización una vez y el sistema convierte todo solo.",
    ),
    "vitrina": (
        "¿Qué es la vitrina pública sincronizada?",
        "Es la vitrina web de tu agencia conectada con Tablero. Cada vez que guardás un auto, un webhook automático actualiza la vitrina, y tus clientes pueden buscar por marca, carrocería y precio máximo en USD con el stock real.",
    ),
    "roles": (
        "¿Pueden trabajar varias personas con distintos permisos?",
        "Sí. Tablero tiene ocho roles: Administrador, Vendedor, Contadora, Visualizador, Gestor, Detailer, Gerente y Soporte. Cada uno ve y hace solo lo que le corresponde, y los permisos se ajustan a cómo se organiza tu equipo.",
    ),
    "gestoria": (
        "¿Cómo se lleva la documentación de cada auto?",
        "Con el módulo de Gestoría: un checklist por unidad con título, cédula, formulario 08, verificación policial e informe de dominio. Al marcar un auto como «Transferido», cambia de estado automáticamente.",
    ),
    "personalizar": (
        "¿Se puede adaptar a mi forma de trabajar?",
        "Sí, es el punto central de Tablero. Los roles, las categorías de finanzas y el checklist de gestoría se arman a tu medida, y el sistema se define con vos, hablando módulo por módulo.",
    ),
    "motos": (
        "¿Sirve también para motos?",
        "Sí. El inventario maneja autos y motos, y en detailing también se pueden definir servicios para motos.",
    ),
    "empezar": (
        "¿Cómo empiezo?",
        "Escribinos por WhatsApp al %s y pedí una demo. Te mostramos el sistema, hablamos de cómo trabaja tu agencia y armamos Tablero con vos, módulo por módulo." % PHONE_DISPLAY,
    ),
    "otro-pais": (
        "¿Y si mi agencia no está en Argentina?",
        "Tablero nació para el mercado argentino: trabaja con USD y ARS y su gestoría contempla trámites locales como el formulario 08. Si tu agencia está en otro país, escribinos y vemos juntos qué parte del sistema se adapta a tu mercado.",
    ),
}

HOME_FAQ = ["que-es", "precio", "monedas", "vitrina", "roles", "otro-pais"]

FAQ_PAGE_GROUPS = [
    ("Sobre Tablero", ["que-es", "para-quien", "precio", "empezar", "otro-pais"]),
    ("Funciones y módulos", ["monedas", "vitrina", "gestoria", "motos"]),
    ("Equipo y personalización", ["roles", "personalizar"]),
]

# FAQ propias de cada módulo (3 por página). (pregunta, respuesta)
MODULE_FAQ = {
    "inventario": [
        ("¿Puedo cargar precios en pesos y en dólares?",
         "Sí. Cada unidad puede tener su precio en pesos o en dólares, y Tablero guarda el historial de cambios de precio de cada auto."),
        ("¿Qué datos tiene la ficha de cada auto?",
         "Dominio, marca, modelo, año, kilómetros y precio, además de una galería de fotos y el vendedor asignado a la unidad."),
        ("¿Puedo cargar motos además de autos?",
         "Sí. El inventario completo incluye autos y motos en el mismo sistema, con listados separados."),
    ],
    "finanzas": [
        ("¿Cómo se registran los movimientos en dos monedas?",
         "Cada ingreso o salida se carga con su moneda (pesos o dólares). Cargás la cotización una vez y el sistema convierte todo solo, así ves el neto en ARS y en USD."),
        ("¿Quién puede ver y editar las finanzas?",
         "Depende del rol. La Contadora puede cargar, editar y borrar; el Visualizador solo lee; el Vendedor carga movimientos sin editar ni borrar; y el Gerente ve todo el negocio operativo menos la plata."),
        ("¿Puedo definir mis propias categorías y medios de pago?",
         "Sí. Las categorías de finanzas se arman a tu medida y el sistema permite crear categorías y medios de pago propios."),
    ],
    "gestoria": [
        ("¿Qué documentos se controlan por auto?",
         "El checklist base incluye título, cédula, formulario 08, verificación policial e informe de dominio, con un resumen de lo que falta en cada unidad."),
        ("¿Se puede adaptar el checklist a mi agencia?",
         "Sí. El checklist de gestoría se arma a tu medida, junto con tu gestor, para reflejar los trámites que hacés en la práctica."),
        ("¿Qué pasa cuando se transfiere un auto?",
         "Al marcar el auto como «Transferido», el sistema cambia su estado automáticamente. No hace falta actualizarlo en otro lado."),
    ],
    "detailing": [
        ("¿Puedo definir mis propios servicios y precios?",
         "Sí. El catálogo de servicios de preparación es tuyo: cada servicio tiene su nombre y su precio, y se pueden agregar nuevos cuando los necesites."),
        ("¿Qué pasa cuando termina la preparación de un auto?",
         "Cuando se completan los servicios asignados, el auto vuelve solo al estado Disponible."),
        ("¿Hay un rol específico para quien hace el detailing?",
         "Sí. El rol Detailer accede al módulo de preparación y detailing, sin necesidad de ver el resto del sistema."),
    ],
    "visitas": [
        ("¿Cada vendedor puede tener sus propios horarios?",
         "Sí. Los horarios se definen por vendedor, con excepciones por fecha para los días puntuales que lo necesiten."),
        ("¿Quién coordina las visitas?",
         "El rol Soporte coordina las visitas y se asigna a cada una junto con el vendedor que atiende al cliente."),
        ("¿Puedo ver las visitas en un calendario?",
         "Sí. Además del listado con filtros por fecha, vendedor y asesor, el módulo incluye un calendario con vista por mes, semana y día."),
    ],
    "tareas": [
        ("¿Se pueden asignar tareas a cualquier persona del equipo?",
         "Sí. Las tareas se asignan entre los integrantes del equipo y cada una queda con su responsable."),
        ("¿Qué niveles de urgencia tienen las tareas?",
         "Baja, media y alta, diferenciadas por color para que el equipo priorice de un vistazo."),
        ("¿Hay calendario de tareas?",
         "Sí. Podés ver las tareas en una lista o en un calendario por mes, semana y día."),
    ],
}

ROLES = [
    ("Administrador", "Acceso total al sistema."),
    ("Vendedor", "Gestiona autos y carga movimientos, sin editar ni borrar."),
    ("Contadora", "Finanzas completas: carga, edita y borra."),
    ("Visualizador", "Solo lectura de finanzas."),
    ("Gestor", "Módulo de gestoría y documentación legal."),
    ("Detailer", "Módulo de preparación y detailing."),
    ("Gerente", "Todo el negocio operativo, menos la plata."),
    ("Soporte", "Coordina visitas y se asigna a autos y movimientos."),
]
