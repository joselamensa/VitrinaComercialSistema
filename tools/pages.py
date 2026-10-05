# -*- coding: utf-8 -*-
"""Definición de las páginas internas. Ver content.py para la regla de contenido:
solo se afirma lo que Tablero ya muestra en su landing y en sus capturas."""
from content import *  # noqa


def L(href, text):
    return '<a href="%s">%s</a>' % (href, text)


def feat_mod(key, text=None):
    m = MOD[key]
    return (key, m["name"], text or m["short"], mod_url(key))


HUB = "/modulos/"
URL_SISTEMA = "/sistema-de-gestion-para-agencia-de-autos-usados/"
URL_CONC = "/software-para-concesionaria/"
URL_FAQ = "/preguntas-frecuentes/"

ROLES_UL = ("ul", ["<strong>%s:</strong> %s" % r for r in ROLES])


# ============================================================ INTENCIÓN 1
def page_sistema():
    return dict(
        path=URL_SISTEMA,
        title="Sistema de gestión para agencia de autos usados | Tablero",
        desc="Tablero es el sistema de gestión para agencias de autos usados: inventario, finanzas en USD y ARS, gestoría, detailing, visitas y tareas en un solo lugar.",
        h1="Sistema de gestión para agencia de autos usados",
        lead="Todo el ciclo de vida de tus autos —stock, preparación, visitas, cobros y transferencia— en un único sistema, armado a la medida de tu agencia.",
        trail=[("Sistema de gestión para agencia de autos usados", URL_SISTEMA)],
        priority="0.9",
        blocks=[
            ("prose", "Qué tiene que resolver un sistema de gestión para una agencia de usados", [
                "Una agencia de usados maneja muchas cosas a la vez: un stock que cambia todos los días, precios en pesos y en dólares, documentación que hay que reunir para cada transferencia, autos que pasan por preparación, clientes que vienen a ver unidades y un equipo que tiene que coordinarse. Cuando cada una de esas cosas vive en una planilla, un cuaderno o un chat distinto, la información se duplica, se desactualiza y se pierde.",
                "Un <strong>sistema de gestión para agencias de autos usados</strong> junta todo eso en un único lugar, con una sola versión de los datos. Eso es Tablero: acompaña a cada unidad durante todo su ciclo de vida, desde que entra al stock hasta que se transfiere.",
            ]),
            ("features", "Seis módulos para todo el ciclo del auto",
             "Cada módulo resuelve una parte del trabajo diario y se conecta con los demás.",
             [feat_mod(m["key"]) for m in MODULES], "alt"),
            ("prose", "El recorrido de un auto dentro de Tablero", [
                "Así se ve el trabajo de la agencia cuando todo está conectado:",
                ("ul", [
                    "<strong>Ingresa al inventario.</strong> Se carga la ficha con dominio, marca, modelo, año, kilómetros, precio y fotos, y se asigna un vendedor. Ver %s." % L(mod_url("inventario"), "módulo de inventario"),
                    "<strong>Se prepara.</strong> Los servicios de detailing se asignan al auto y se marcan a medida que se hacen; al terminar, vuelve solo a Disponible. Ver %s." % L(mod_url("detailing"), "módulo de detailing"),
                    "<strong>Se muestra.</strong> Cada vez que guardás el auto, la vitrina pública se actualiza sola, y las visitas se agendan con fecha, horario y vendedor. Ver %s." % L(mod_url("visitas"), "módulo de visitas"),
                    "<strong>Se vende y se cobra.</strong> Los ingresos y las salidas se registran en pesos o dólares, con su medio de pago y comprobante. Ver %s." % L(mod_url("finanzas"), "módulo de finanzas"),
                    "<strong>Se transfiere.</strong> El checklist de gestoría controla la documentación y, al marcar «Transferido», el auto cambia de estado solo. Ver %s." % L(mod_url("gestoria"), "módulo de gestoría"),
                ]),
                "Nadie copia datos de un lado a otro: lo que se carga en un módulo queda disponible para el resto.",
            ]),
            ("split", "Stock y vitrina web: una sola fuente de verdad", [
                "El inventario de Tablero es la base de todo. Cada auto o moto tiene su ficha, su precio en pesos o dólares, su galería de fotos y su vendedor asignado.",
                "Además, la <strong>vitrina pública de tu agencia está sincronizada en tiempo real</strong>: cuando guardás un auto, un webhook automático actualiza la vitrina y tus clientes pueden buscar por marca, carrocería y precio máximo en USD, siempre con el stock real.",
                "Conocé más en la página del %s." % L(mod_url("inventario"), "inventario de autos usados"),
            ], "inventario", "white"),
            ("prose", "Pensado para cómo se trabaja en Argentina", [
                "Tablero no es un software genérico al que se le cambió el nombre. Está armado alrededor del flujo real de una agencia de usados argentina:",
                ("ul", [
                    "<strong>Gestión bimonetaria (USD / ARS):</strong> cargás la cotización una vez y el sistema convierte todo solo.",
                    "<strong>Gestoría con la documentación local:</strong> título, cédula, formulario 08, verificación policial e informe de dominio.",
                    "<strong>Estados que se actualizan solos:</strong> «Transferido» en gestoría o «Disponible» al terminar el detailing.",
                ]),
            ], "alt"),
            ("prose", "Cada persona ve lo que le corresponde", [
                "Tu equipo no necesita ver lo mismo. Tablero trabaja con ocho roles, cada uno con una interfaz y permisos acordes:",
                ROLES_UL,
                "Los permisos se ajustan a cómo se organiza tu equipo. Más detalle en la sección de %s." % L("/#roles", "roles"),
            ]),
            ("prose", "Se adapta a tu agencia, no al revés", [
                "Tablero se arma con vos, hablando módulo por módulo: los roles y permisos, las categorías de finanzas y el checklist de gestoría se definen a tu medida. No te pedimos que cambies cómo vendés; te ayudamos a hacerlo de forma más eficiente.",
                "Hay tres planes —Esencial, Completo y A Medida— y el precio se define por consulta. Mirá el detalle en %s." % L("/#precios", "planes"),
            ], "alt"),
            ("faq", "Preguntas frecuentes sobre el sistema", [FAQ[k] for k in ("que-es", "precio", "personalizar", "empezar")]),
            ("links", "Seguí explorando", None, [
                ("Software para concesionaria", "Cómo se usa Tablero en una concesionaria con equipo, caja y varias personas.", URL_CONC),
                ("Todos los módulos", "Inventario, finanzas, gestoría, detailing, visitas y tareas en detalle.", HUB),
                ("Preguntas frecuentes", "Respuestas sobre precios, monedas, vitrina, roles y más.", URL_FAQ),
            ], "alt"),
        ],
        cta=("Pedí una demo del sistema", "Contanos cómo trabaja tu agencia y te mostramos Tablero.", "Hola! Quiero conocer el sistema de gestión Tablero para mi agencia de autos usados."),
        wa="Hola! Quiero conocer el sistema de gestión Tablero para mi agencia de autos usados.",
    )


# ============================================================ INTENCIÓN 2
def page_concesionaria():
    return dict(
        path=URL_CONC,
        title="Software para concesionaria de autos usados | Tablero",
        desc="Software para concesionarias de autos usados: stock, finanzas en USD y ARS, gestoría, visitas y equipo con roles y permisos, todo conectado en Tablero.",
        h1="Software para concesionaria de autos usados",
        lead="Ordená stock, caja, trámites, visitas y equipo en un solo sistema, con permisos por rol y la posibilidad de crecer a varias sucursales.",
        trail=[("Software para concesionaria", URL_CONC)],
        priority="0.9",
        blocks=[
            ("prose", "Qué buscar en un software para concesionaria", [
                "Elegir un software para tu concesionaria no es solo comparar listas de funciones. Estos son los criterios que más conviene mirar:",
                ("ul", [
                    "<strong>Que cubra el ciclo completo del auto</strong>, no solo el stock: preparación, visitas, venta, cobro y transferencia.",
                    "<strong>Que entienda el negocio local:</strong> precios y caja en pesos y dólares, y trámites como el formulario 08.",
                    "<strong>Que cada persona vea lo que le corresponde:</strong> el gerente no necesita acceso a la plata y el detailer solo trabaja en preparación.",
                    "<strong>Que la vitrina web muestre el stock real</strong>, sin cargar cada auto dos veces.",
                    "<strong>Que se adapte a tu forma de trabajar</strong> y no al revés.",
                ]),
                "Tablero está armado alrededor de estos criterios.",
            ]),
            ("features", "Lo que cubre Tablero en una concesionaria", None, [
                feat_mod("inventario", "Fichas de autos y motos con precio en USD o ARS, historial de precios, fotos y vendedor asignado."),
                ("moneda", "Finanzas en dos monedas", "Ingresos y salidas con medio de pago y comprobante; cotización cargada una vez y conversión automática.", mod_url("finanzas")),
                ("roles", "Equipo con permisos", "Ocho roles —de Administrador a Detailer— para que cada persona vea y haga solo lo que le toca.", "/#roles"),
                ("vitrina", "Vitrina web sincronizada", "Cada auto que guardás actualiza tu vitrina pública con el stock real.", mod_url("inventario")),
            ], "alt"),
            ("split", "Stock, precios y vitrina en el mismo lugar", [
                "El corazón de una concesionaria es su stock. En Tablero cada unidad tiene su ficha completa, con precio en pesos o en dólares, historial de cambios de precio y galería de fotos.",
                "Los clientes ven esa información en tu vitrina web, que se actualiza sola cada vez que guardás un auto. Buscan por marca, carrocería y precio máximo en USD.",
                "Más detalle en el módulo de %s." % L(mod_url("inventario"), "inventario"),
            ], "inventario", "white"),
            ("prose", "Roles y permisos para equipos con varias personas", [
                "En una concesionaria trabajan vendedores, gerentes, administración, gestoría y preparación. Tablero separa los accesos para que cada uno use solo lo que necesita:",
                ("ul", [
                    "El <strong>Vendedor</strong> gestiona autos y carga movimientos, sin editar ni borrar.",
                    "La <strong>Contadora</strong> tiene finanzas completas: carga, edita y borra.",
                    "El <strong>Gerente</strong> maneja todo el negocio operativo, menos la plata.",
                    "El <strong>Gestor</strong> y el <strong>Detailer</strong> acceden a gestoría y a preparación, respectivamente.",
                    "El <strong>Visualizador</strong> solo lee las finanzas y <strong>Soporte</strong> coordina las visitas.",
                ]),
                "Los permisos se ajustan a cómo se organiza tu concesionaria.",
            ], "alt"),
            ("prose", "Crecer a varias sucursales", [
                "Si tu estructura es grande o tenés más de una sucursal, existe el plan <strong>A Medida</strong>: módulos y campos personalizados, multi-sucursal y acompañamiento en la implementación. Los roles, los flujos y las integraciones se definen en conjunto, en una conversación inicial por WhatsApp.",
            ]),
            ("prose", "¿Concesionaria o agencia de usados?", [
                "En el negocio automotor argentino los dos términos se usan casi como sinónimos. Tablero está pensado para la <strong>compraventa de autos usados y motos</strong>. Si tu concesionaria trabaja además con otro tipo de operación, contanos cómo y vemos juntos qué parte del sistema se adapta.",
                "Si querés una mirada más general, leé la página del %s." % L(URL_SISTEMA, "sistema de gestión para agencia de autos usados"),
            ], "alt"),
            ("faq", "Preguntas frecuentes sobre el software para concesionarias", [
                ("¿Sirve para una concesionaria con varios vendedores?",
                 "Sí. Cada unidad tiene un vendedor asignado y existen roles diferenciados, de modo que cada persona accede solo a lo que le corresponde."),
                ("¿Puede usarse en más de una sucursal?",
                 "Sí, con el plan A Medida, que incluye multi-sucursal. Cómo se organiza cada caso se define en conjunto."),
                FAQ["precio"],
            ]),
        ],
        cta=("Mirá Tablero en tu concesionaria", "Pedí una demo y vemos cómo se adapta a tu operación.", "Hola! Quiero conocer Tablero para mi concesionaria."),
        wa="Hola! Quiero conocer Tablero para mi concesionaria.",
    )


# =============================================================== MÓDULOS
MODULE_BODY = {
    "inventario": dict(
        h2="Qué incluye el módulo de inventario",
        bullets=[
            "<strong>Ficha completa por unidad:</strong> dominio, marca, modelo, año, kilómetros y precio.",
            "<strong>Precio en pesos o en dólares</strong>, con historial de cambios de precio.",
            "<strong>Galería de fotos</strong> de cada auto o moto.",
            "<strong>Autos y motos</strong> en el mismo sistema, con listados separados.",
            "<strong>Vendedor asignado</strong> por unidad.",
            "<strong>Panel con contadores por estado</strong> (disponibles, vendidos, transferidos y bajas) y filtros por vendedor, estado y días en sistema.",
        ],
        extra=[
            ("prose", "Un stock que se actualiza solo en tu vitrina web", [
                "La vitrina pública de tu agencia está sincronizada en tiempo real con Tablero. Cada vez que guardás un auto, un webhook automático actualiza la vitrina; tus clientes buscan por marca, carrocería y precio máximo en USD, siempre con el stock real.",
                "Así no hay que cargar el mismo auto dos veces ni acordarse de bajar el que ya se vendió.",
            ], "alt"),
            ("prose", "Para qué sirve tener el inventario ordenado", [
                "Saber qué tenés, a qué precio y en qué estado es la base de todo lo demás. Con la ficha de cada unidad en un solo lugar, el vendedor encuentra los datos sin preguntar, el gerente ve cuánto stock hay en cada estado y se pueden detectar los autos que llevan más días en el sistema con el filtro correspondiente.",
                "El historial de cambios de precio deja registro de cada modificación, para que no dependa de la memoria de nadie.",
            ]),
            ("prose", "Quién usa el inventario", [
                "El <strong>Administrador</strong> tiene acceso total; el <strong>Vendedor</strong> gestiona autos y carga movimientos, sin editar ni borrar; el <strong>Gerente</strong> maneja todo el negocio operativo y <strong>Soporte</strong> se asigna a autos y movimientos. Mirá todos los %s." % L("/#roles", "roles de Tablero"),
            ], "alt"),
        ],
        related=[
            ("gestoria", "Cuando un auto se marca como «Transferido» en gestoría, cambia de estado solo."),
            ("detailing", "Los servicios de preparación se asignan a cada unidad; al terminar, el auto vuelve a Disponible."),
            ("visitas", "Las visitas se agendan con fecha, horario y vendedor asignado."),
        ],
    ),
    "finanzas": dict(
        h2="Qué incluye el módulo de finanzas",
        bullets=[
            "<strong>Ingresos y salidas</strong> con categoría, monto, moneda, medio de pago y comprobante.",
            "<strong>Gestión bimonetaria USD / ARS:</strong> cargás la cotización una vez y el sistema convierte todo solo.",
            "<strong>Resumen de ingresos, salidas y neto</strong> en pesos y en dólares.",
            "<strong>Períodos:</strong> hoy, esta semana, este mes, este año, histórico o un rango de fechas a elección.",
            "<strong>Últimos movimientos</strong> y totales por medio de pago (por ejemplo, efectivo en pesos, efectivo en dólares o una cuenta bancaria).",
            "<strong>Categorías y medios de pago propios</strong>, armados a tu medida.",
        ],
        extra=[
            ("prose", "Por qué importa manejar dos monedas", [
                "En una agencia de usados argentina es habitual que los autos se coticen en dólares y que parte de la operación se cobre y se pague en pesos. Llevar eso en una planilla obliga a hacer cuentas aparte para ver cuánto se ganó o se gastó en cada moneda.",
                "En Tablero cargás la cotización una vez y el sistema convierte todo solo, así los netos en ARS y en USD quedan a la vista en el mismo resumen.",
            ], "alt"),
            ("prose", "Permisos pensados para el manejo del dinero", [
                "No todo el equipo tiene que ver la plata. Por eso Tablero separa los accesos:",
                ("ul", [
                    "La <strong>Contadora</strong> tiene finanzas completas: carga, edita y borra.",
                    "El <strong>Visualizador</strong> solo tiene lectura de finanzas.",
                    "El <strong>Vendedor</strong> carga movimientos, sin editar ni borrar.",
                    "El <strong>Gerente</strong> ve todo el negocio operativo, menos la plata.",
                    "El <strong>Administrador</strong> tiene acceso total.",
                ]),
            ]),
        ],
        related=[
            ("inventario", "Cada unidad tiene su precio en pesos o en dólares, con historial de cambios."),
            ("gestoria", "Los trámites de cada auto se siguen en un checklist por unidad."),
            ("tareas", "Las tareas pendientes del equipo, con responsable y urgencia."),
        ],
    ),
    "gestoria": dict(
        h2="Qué incluye el módulo de gestoría",
        bullets=[
            "<strong>Checklist por auto:</strong> título, cédula, formulario 08, verificación policial e informe de dominio.",
            "<strong>Vista de gestoría pendientes</strong> con los vehículos, su estado y la documentación de cada uno, con filtros.",
            "<strong>Listas «Listos para transferir» y «Transferidos»</strong>, y un resumen de ventas.",
            "<strong>Cambio de estado automático:</strong> al marcar «Transferido», el auto actualiza su estado solo.",
            "<strong>Checklist a tu medida</strong>, para reflejar los trámites que hace tu agencia.",
            "<strong>Rol Gestor</strong> con acceso al módulo de gestoría y documentación legal.",
        ],
        extra=[
            ("prose", "Menos papeles perdidos, menos autos frenados", [
                "Cuando la documentación de cada unidad se lleva en carpetas, mensajes y memoria, es fácil que un auto quede frenado por un papel que nadie sabía que faltaba. Con un checklist por unidad, cualquiera del equipo ve de un vistazo qué está completo y qué falta.",
                "El gestor trabaja sobre una lista de pendientes en lugar de reconstruirla cada vez, y los autos listos para transferir quedan identificados en su propia lista.",
            ], "alt"),
            ("prose", "Quién usa la gestoría", [
                "El rol <strong>Gestor</strong> accede al módulo de gestoría y documentación legal. El <strong>Administrador</strong> tiene acceso total y el <strong>Gerente</strong> maneja todo el negocio operativo. El resto del equipo trabaja sin ver este módulo si no lo necesita.",
            ]),
        ],
        related=[
            ("inventario", "El estado de cada unidad se actualiza solo cuando se marca como «Transferido»."),
            ("finanzas", "Ingresos y salidas en pesos y dólares, con medio de pago y comprobante."),
            ("tareas", "Asigná pendientes al equipo con responsable y urgencia."),
        ],
    ),
    "detailing": dict(
        h2="Qué incluye el módulo de detailing",
        bullets=[
            "<strong>Catálogo de servicios</strong> con nombre y precio, que podés ampliar cuando quieras.",
            "<strong>Servicios asignados a cada auto</strong>, con seguimiento de cuáles ya se hicieron.",
            "<strong>Pendientes de preparación</strong> y vehículos con servicios, en listas separadas.",
            "<strong>Servicios realizados:</strong> queda registro de lo que se hizo.",
            "<strong>Vuelta automática a Disponible</strong> cuando se completan los servicios.",
            "<strong>Rol Detailer</strong> con acceso al módulo de preparación.",
        ],
        extra=[
            ("prose", "Que ningún auto salga a la venta a medias", [
                "La preparación es parte de la venta: un auto bien presentado se muestra mejor. Con el catálogo de servicios y el seguimiento por unidad, la agencia sabe qué trabajos tiene cada auto, cuáles están pendientes y cuáles ya se hicieron.",
                "Al completar los servicios, el auto vuelve solo a Disponible, sin que nadie tenga que acordarse de actualizarlo.",
            ], "alt"),
            ("prose", "Un catálogo que armás vos", [
                "Cada agencia tiene sus propios servicios y sus propios precios. En Tablero los definís vos: por ejemplo lavado, detailing completo, repaso para entrega o trabajos de chapa, cada uno con su valor, y los asignás a las unidades que los necesitan.",
            ]),
        ],
        related=[
            ("inventario", "Cada servicio se asigna a una unidad del inventario."),
            ("gestoria", "Después de la preparación, el seguimiento de la documentación hasta la transferencia."),
            ("tareas", "Tareas internas con responsable, urgencia y comentarios."),
        ],
    ),
    "visitas": dict(
        h2="Qué incluye el módulo de visitas",
        bullets=[
            "<strong>Agenda de visitas</strong> con cliente, fecha, horario y vendedor asignado.",
            "<strong>Soporte que coordina:</strong> cada visita tiene también al asesor que la gestiona.",
            "<strong>Horarios por vendedor</strong>, con excepciones por fecha.",
            "<strong>Estado y comentarios</strong> en cada visita, para dejar anotado qué busca el cliente.",
            "<strong>Listado con filtros</strong> por fecha, vendedor y asesor.",
            "<strong>Calendario</strong> con vista por mes, semana y día.",
        ],
        extra=[
            ("prose", "Coordinar visitas sin pisarse", [
                "Cuando las visitas se arreglan por mensajes sueltos, es fácil que dos clientes se crucen o que el vendedor no esté. Con una agenda donde cada visita tiene fecha, horario y responsable, y con horarios definidos por vendedor, el equipo sabe quién atiende a quién y cuándo.",
                "Las excepciones por fecha permiten reflejar los días puntuales en que un vendedor no está disponible, sin tocar el resto de su horario.",
            ], "alt"),
            ("prose", "Quién usa las visitas", [
                "El <strong>Vendedor</strong> recibe las visitas asignadas, el rol <strong>Soporte</strong> las coordina, y el <strong>Administrador</strong> y el <strong>Gerente</strong> tienen una vista general de la agenda.",
            ]),
        ],
        related=[
            ("inventario", "Cada visita se apoya en las unidades que tenés en stock."),
            ("tareas", "Tareas internas con responsable, urgencia y calendario."),
            ("finanzas", "El resultado de la venta, registrado en pesos o dólares."),
        ],
    ),
    "tareas": dict(
        h2="Qué incluye el módulo de tareas",
        bullets=[
            "<strong>Tareas asignadas</strong> a cualquier integrante del equipo, cada una con su responsable.",
            "<strong>Urgencia baja, media o alta</strong>, con colores para priorizar de un vistazo.",
            "<strong>Estado y comentarios</strong> en cada tarea.",
            "<strong>Lista y calendario</strong>, con vista por mes, semana y día.",
            "<strong>Todo queda escrito:</strong> nada depende de un mensaje que se pierde en un chat.",
        ],
        extra=[
            ("prose", "Del «avisale a…» a una tarea con responsable", [
                "En una agencia hay muchos pedidos chicos que se resuelven por chat: «revisá la documentación de este auto», «llamá a este cliente», «avisale al detailer». El problema es que nadie sabe después si se hicieron.",
                "Con el módulo de tareas cada pedido queda registrado, con quién lo tiene que hacer, qué tan urgente es, en qué estado está y con los comentarios del equipo.",
            ], "alt"),
        ],
        related=[
            ("visitas", "Agenda de visitas con vendedor asignado y horarios por vendedor."),
            ("gestoria", "Documentación de cada auto, con checklist por unidad."),
            ("detailing", "Servicios de preparación asignados a cada auto."),
        ],
    ),
}


def page_module(m):
    b = MODULE_BODY[m["key"]]
    path = mod_url(m["key"])
    blocks = [
        ("bulletcards", b["h2"], None, b["bullets"], "white"),
    ]
    blocks += b["extra"]
    blocks.append(("features", "Se conecta con otros módulos",
                   "Tablero funciona como un solo sistema: lo que pasa en un módulo se refleja en los demás.",
                   [feat_mod(k, txt) for k, txt in b["related"]], "alt"))
    blocks.append(("faq", "Preguntas frecuentes sobre %s" % m["name"].lower(), MODULE_FAQ[m["key"]]))
    others = [x for x in MODULES if x["key"] != m["key"]]
    blocks.append(("links", "Más módulos de Tablero", "Conocé el resto de las herramientas para tu agencia.",
                   [(x["name"], x["short"], mod_url(x["key"])) for x in others[:3]] , "alt"))
    return dict(
        path=path, title=m["title"], desc=m["desc"], h1=m["h1"], lead=m["lead"],
        trail=[("Módulos", HUB), (m["name"], path)],
        priority="0.8", blocks=blocks, hero_mod=m["key"],
        cta=("Pedí una demo de Tablero",
             "Te mostramos el módulo de %s y cómo se conecta con el resto del sistema." % m["name"].lower(),
             "Hola! Quiero conocer el módulo de %s de Tablero." % m["name"].lower()),
        wa="Hola! Quiero conocer el módulo de %s de Tablero." % m["name"].lower(),
    )


def page_hub():
    return dict(
        path=HUB,
        title="Módulos de Tablero para agencias de autos usados",
        desc="Conocé los seis módulos de Tablero: inventario, finanzas, gestoría, detailing, visitas y tareas, conectados entre sí para toda la operación de tu agencia.",
        h1="Módulos de Tablero para agencias de autos usados",
        lead="Seis módulos pensados para el flujo real de una agencia de usados, no funciones genéricas. Elegí los que necesitás hoy y sumá el resto cuando quieras.",
        trail=[("Módulos", HUB)],
        priority="0.8",
        blocks=[
            ("features", "Todo lo que necesitás en un solo lugar", None, [feat_mod(m["key"]) for m in MODULES]),
            ("prose", "Cómo trabajan juntos", [
                "Los módulos no son islas. Cuando guardás un auto en el inventario, tu vitrina web se actualiza sola. Al marcar un auto como «Transferido» en gestoría, cambia de estado automáticamente. Al terminar los servicios de detailing, el auto vuelve solo a Disponible.",
                "Cada persona del equipo ve los módulos que le corresponden según su rol, de modo que el gestor, el detailer, la contadora o el vendedor trabajan sobre la misma información sin pisarse.",
            ], "alt"),
            ("prose", "Elegí los módulos que necesitás", [
                "Tablero se ofrece en tres planes: <strong>Esencial</strong>, con inventario completo, vendedor asignado por unidad y vitrina pública sincronizada; <strong>Completo</strong>, con finanzas, gestoría, detailing, visitas, tareas y todos los roles; y <strong>A Medida</strong>, para estructuras grandes o multi-sucursal.",
                "El precio se define por consulta. Mirá el detalle en la sección de %s o escribinos por WhatsApp." % L("/#precios", "planes"),
            ]),
            ("faq", "Preguntas frecuentes", [FAQ[k] for k in ("que-es", "precio", "personalizar")], "alt"),
        ],
    )


# ================================================================== FAQ
def page_faq():
    return dict(
        path=URL_FAQ,
        title="Preguntas frecuentes sobre Tablero | Sistema para agencias",
        desc="Respuestas sobre Tablero: qué es, para quién sirve, precios, manejo de pesos y dólares, vitrina pública, roles, gestoría y cómo empezar.",
        h1="Preguntas frecuentes sobre Tablero",
        lead="Lo que más nos preguntan las agencias de autos usados sobre el sistema. Si no encontrás tu duda, escribinos por WhatsApp.",
        trail=[("Preguntas frecuentes", URL_FAQ)],
        priority="0.7",
        blocks=[("faqgroups", [(g, [FAQ[k] for k in keys]) for g, keys in FAQ_PAGE_GROUPS])]
        + [("links", "Seguí explorando", None, [
            ("Sistema para agencias de autos usados", "El ciclo completo del auto en un solo sistema.", URL_SISTEMA),
            ("Software para concesionaria", "Equipo, caja, trámites y vitrina conectados.", URL_CONC),
            ("Módulos", "Inventario, finanzas, gestoría, detailing, visitas y tareas.", HUB),
        ], "alt")],
    )


def all_pages():
    pgs = [page_sistema(), page_concesionaria(), page_hub()]
    pgs += [page_module(m) for m in MODULES]
    pgs.append(page_faq())
    return pgs
