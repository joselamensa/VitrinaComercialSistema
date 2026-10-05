# -*- coding: utf-8 -*-
"""Artículos del blog. Reglas editoriales:
- Responden preguntas reales de una agencia de usados, con consejo práctico de oficio.
- No hay estadísticas, estudios ni comparaciones con competidores inventados.
- Lo que se dice de Tablero sale de la landing y de las capturas del producto.
- En trámites y temas legales se explica lo general y se remite al gestor / Registro.
Cuerpo: str = párrafo (HTML permitido); ("ul"|"ol", [items]); ("h3", t); ("callout", t).
"""

PUBLISHED = "2026-10-05"

POSTS = [
    dict(
        slug="como-llevar-el-stock-de-una-agencia-de-autos-usados",
        title="Cómo llevar el stock de una agencia de autos usados",
        desc="Guía práctica para ordenar el stock de tu agencia de autos usados: qué datos cargar, cómo registrar precios y estados y cómo evitar versiones duplicadas.",
        h1="Cómo llevar el stock de una agencia de autos usados sin perder el control",
        lead="El stock cambia todos los días: entran autos, se baja un precio, se vende una unidad, otra queda en preparación. Esta guía explica cómo registrarlo para que cualquiera del equipo vea lo mismo.",
        modules=["inventario"],
        sections=[
            ("Por qué el stock se desordena", [
                "En casi todas las agencias el stock empieza igual: una planilla. Funciona mientras hay pocas unidades y una sola persona que la actualiza. El problema aparece cuando el equipo crece: el vendedor tiene su lista, el gerente otra, la vitrina web una tercera, y nadie está seguro de cuál es la correcta.",
                "El resultado es el de siempre: autos que figuran como disponibles y ya se vendieron, precios distintos según quién responda y tiempo perdido preguntando «¿este sigue?».",
            ]),
            ("Qué datos tiene que tener la ficha de cada unidad", [
                "Una buena ficha no necesita ser larga, pero sí completa y igual para todos los autos y motos. Como mínimo:",
                ("ul", [
                    "<strong>Identificación:</strong> dominio, marca, modelo y año.",
                    "<strong>Estado físico:</strong> kilómetros y fotos actuales.",
                    "<strong>Precio y moneda:</strong> si está en pesos o en dólares, y desde cuándo.",
                    "<strong>Responsable:</strong> el vendedor asignado a la unidad.",
                    "<strong>Fecha de ingreso:</strong> te permite saber cuánto tiempo lleva cada auto en el lote.",
                    "<strong>Estado:</strong> en qué punto del circuito está (más abajo).",
                ]),
            ]),
            ("Los estados: la pieza que más se subestima", [
                "Casi todo lo demás se ordena si los estados están bien definidos. La regla es tener pocos, con un significado claro y sin zonas grises. Por ejemplo: disponible, vendido, transferido y baja. Cada estado responde una pregunta distinta: ¿se puede mostrar?, ¿ya se cobró?, ¿ya se hizo el trámite?, ¿salió del stock?",
                "Lo ideal es que el estado cambie por el trabajo mismo del equipo y no por una tarea extra de actualización. Si marcar un auto como transferido en gestoría ya actualiza su estado, nadie tiene que acordarse de hacerlo dos veces.",
            ]),
            ("Precio en pesos o en dólares, con historial", [
                "En el mercado de usados argentino es normal que unas unidades se publiquen en dólares y otras en pesos. Registrá siempre la moneda junto con el precio, y guardá cada cambio con su fecha. Ese historial sirve para entender cuánto tardó en venderse un auto después de bajarle el precio y evita discusiones del tipo «yo lo tenía a otro valor».",
            ]),
            ("Una sola fuente de verdad, también para la vitrina web", [
                "Si tu agencia tiene vitrina web, la peor práctica es cargar cada auto dos veces: una en la planilla y otra en la web. Tarde o temprano se desfasan. Lo recomendable es que la vitrina se alimente del mismo lugar donde se carga el stock, de modo que al guardar un auto la web se actualice sola.",
            ]),
            ("Cuándo conviene pasar de la planilla a un sistema", [
                "Si ya tenés más de una persona editando, si perdés tiempo conciliando versiones o si el stock tiene que reflejarse en una web, es momento de dar el salto. Podés leer más sobre eso en %s." % '<a href="/blog/excel-o-sistema-de-gestion-agencia-de-autos/">Excel o sistema de gestión: cuándo dar el salto</a>',
                "En Tablero, el %s guarda la ficha de cada auto o moto con su precio en pesos o dólares, el historial de cambios de precio, la galería de fotos y el vendedor asignado, y mantiene la vitrina pública sincronizada." % '<a href="/modulos/inventario-de-autos/">módulo de inventario</a>',
            ]),
            ("callout", "Resumen: ficha igual para todas las unidades, pocos estados bien definidos, precio con su moneda y su historial, y una única fuente para la vitrina."),
        ],
    ),
    dict(
        slug="caja-en-pesos-y-dolares-agencia-de-autos",
        title="Cómo manejar la caja en pesos y dólares en una agencia",
        desc="Cómo registrar ingresos y salidas en pesos y dólares en una agencia de autos usados sin perder el control: categorías, medios de pago y cotización.",
        h1="Cómo manejar la caja en pesos y dólares en una agencia de autos",
        lead="Cuando una parte de la operación se mueve en dólares y otra en pesos, la caja se complica rápido. Estos son los criterios que ordenan el manejo de dos monedas sin hacer cuentas a mano.",
        modules=["finanzas"],
        sections=[
            ("El problema de trabajar con dos monedas", [
                "En una agencia de usados es habitual comprar un auto en dólares, pagar un gasto fijo en pesos, cobrar una seña en efectivo y recibir una transferencia el mismo día. Si todo se anota en una única columna, el total no dice nada: mezcla monedas distintas.",
            ]),
            ("Principios para ordenar la caja", [
                ("ol", [
                    "<strong>Registrá cada movimiento en su moneda original.</strong> Si se pagó en dólares, se anota en dólares; no conviertas antes de guardar.",
                    "<strong>Definí un único criterio de cotización</strong> y aplicalo siempre igual, para que los totales sean comparables entre sí.",
                    "<strong>Separá ingresos de salidas</strong> y calculá el neto de cada moneda por separado.",
                    "<strong>Usá categorías estables.</strong> Si hoy una compra se llama «Compra» y mañana «Adquisición», no vas a poder comparar períodos.",
                    "<strong>Anotá el medio de pago:</strong> efectivo en pesos, efectivo en dólares, cuenta bancaria. Es lo que permite saber dónde está realmente la plata.",
                    "<strong>Guardá el comprobante</strong> de cada movimiento, o al menos dónde está.",
                ]),
            ]),
            ("Errores comunes", [
                ("ul", [
                    "Convertir a mano cada fila y que dos personas usen cotizaciones distintas.",
                    "Llevar una planilla para pesos y otra para dólares sin un resumen que las junte.",
                    "No registrar los gastos chicos, que sumados pesan.",
                    "Dar a todo el equipo acceso a editar la caja.",
                ]),
            ]),
            ("Quién debería poder ver y editar la caja", [
                "No todas las personas de la agencia necesitan ver el dinero. Una buena práctica es que quien registra y quien controla sean roles distintos, y que haya perfiles de solo lectura. Hablamos de esto con más detalle en %s." % '<a href="/blog/permisos-y-roles-quien-debe-ver-la-caja-agencia-de-autos/">Roles y permisos: quién debería ver la caja</a>',
            ]),
            ("Cómo se resuelve en Tablero", [
                "El %s registra ingresos y salidas con categoría, monto, moneda, medio de pago y comprobante. La gestión es bimonetaria: cargás la cotización una vez y el sistema convierte todo solo, y el resumen muestra ingresos, salidas y neto en pesos y en dólares, por período y por medio de pago." % '<a href="/modulos/finanzas-agencia-de-autos/">módulo de finanzas</a>',
            ]),
            ("callout", "Resumen: cada movimiento en su moneda, una cotización de referencia, categorías estables, medio de pago y comprobante, y permisos distintos para cargar y para controlar."),
        ],
    ),
    dict(
        slug="documentacion-para-vender-un-auto-usado-argentina",
        title="Documentación para vender un auto usado en Argentina",
        desc="Checklist de la documentación que suele pedirse para transferir un auto usado: título, cédula, formulario 08, verificación policial e informe de dominio.",
        h1="Documentación para vender un auto usado en Argentina: checklist para la agencia",
        lead="Un auto no está realmente listo para vender hasta que su documentación está completa. Este es un checklist general para que ninguna unidad se frene por un papel que faltaba.",
        modules=["gestoria"],
        sections=[
            ("callout", "Este artículo es informativo y general. Los requisitos exactos pueden variar según la jurisdicción, el tipo de vehículo y el trámite; confirmalos siempre con tu gestor o con el Registro del Automotor."),
            ("Por qué conviene un checklist por unidad", [
                "Reunir la documentación de un auto suele involucrar a varias personas y varios momentos: lo que trae el vendedor anterior, lo que se solicita en el Registro, lo que se verifica antes de entregar. Si esa información vive en la memoria del gestor o en mensajes sueltos, es fácil que una unidad quede frenada por un papel que nadie sabía que faltaba.",
            ]),
            ("Los documentos que suelen controlarse", [
                ("ul", [
                    "<strong>Título del automotor:</strong> el documento que acredita la titularidad del vehículo.",
                    "<strong>Cédula de identificación del automotor:</strong> la «cédula verde», que identifica el vehículo y a sus autorizados.",
                    "<strong>Formulario 08:</strong> el formulario que se utiliza para solicitar la transferencia; conviene revisar que los datos coincidan con los del título y la cédula.",
                    "<strong>Verificación policial:</strong> constata que los datos identificatorios del vehículo (por ejemplo, chasis y motor) coinciden con los registrados.",
                    "<strong>Informe de dominio:</strong> muestra la situación registral del vehículo, como su titular y si tiene medidas o inscripciones.",
                    "<strong>Otros según el caso:</strong> estado de deudas de patentes e infracciones, verificación técnica o la oblea de GNC cuando corresponde.",
                ]),
            ]),
            ("Cómo organizar el seguimiento", [
                ("ol", [
                    "<strong>Un checklist igual para todas las unidades</strong>, con los documentos que tu agencia controla siempre.",
                    "<strong>Un estado por documento:</strong> pendiente, en trámite o listo.",
                    "<strong>Una vista de pendientes</strong> para el gestor, en lugar de reconstruir la lista cada vez.",
                    "<strong>Una lista de «listos para transferir»</strong>, para saber qué autos pueden cerrarse hoy.",
                    "<strong>Un estado final claro</strong> cuando la transferencia se completó.",
                ]),
            ]),
            ("Cómo lo resuelve Tablero", [
                "El %s mantiene un checklist por auto (título, cédula, formulario 08, verificación policial e informe de dominio), una vista de gestoría pendientes con filtros y listas de «Listos para transferir» y «Transferidos». Al marcar un auto como «Transferido», cambia de estado solo. El checklist se arma a la medida de cada agencia." % '<a href="/modulos/gestoria-automotor/">módulo de gestoría</a>',
                "Para entender mejor uno de los documentos más consultados, mirá %s." % '<a href="/blog/formulario-08-que-es-y-para-que-sirve/">Formulario 08: qué es y para qué sirve</a>',
            ]),
        ],
    ),
    dict(
        slug="formulario-08-que-es-y-para-que-sirve",
        title="Formulario 08: qué es y para qué sirve en una venta",
        desc="Qué es el formulario 08, cuándo se usa en la transferencia de un auto usado y qué conviene controlar antes de firmarlo y guardarlo en la agencia.",
        h1="Formulario 08: qué es y para qué sirve en la venta de un auto usado",
        lead="Es uno de los papeles que más se nombran en una agencia. Esta es una explicación general de qué es, cuándo aparece y qué conviene controlar.",
        modules=["gestoria"],
        sections=[
            ("callout", "Este artículo es informativo y general. Para el trámite concreto, los requisitos y los costos vigentes, consultá con tu gestor o con el Registro del Automotor."),
            ("Qué es el formulario 08", [
                "El formulario 08 es el formulario del Registro del Automotor que se utiliza para solicitar la transferencia de un vehículo. En él figuran los datos del vehículo, del vendedor y del comprador, y se firma por las partes.",
                "En una agencia aparece en el momento de la venta, cuando el auto pasa de un titular a otro, y es una de las piezas centrales del trámite de transferencia.",
            ]),
            ("Qué conviene controlar antes de firmarlo", [
                ("ul", [
                    "Que los datos del vehículo coincidan con el título y la cédula.",
                    "Que los datos de las personas estén completos y sean correctos.",
                    "Que las firmas se hayan hecho donde corresponde.",
                    "Que el resto de la documentación de la unidad esté completa (podés ver el checklist en %s)." % '<a href="/blog/documentacion-para-vender-un-auto-usado-argentina/">Documentación para vender un auto usado</a>',
                ]),
            ]),
            ("Qué conviene registrar en la agencia", [
                "Más allá del papel en sí, es útil que la agencia sepa en todo momento, para cada unidad, si el formulario ya está firmado, si falta, quién lo tiene y en qué etapa del trámite está el auto. Eso evita que una venta cerrada quede trabada por un documento que nadie encuentra.",
                "En Tablero, el formulario 08 es parte del checklist de gestoría de cada auto, junto con el título, la cédula, la verificación policial y el informe de dominio. Más información en el %s." % '<a href="/modulos/gestoria-automotor/">módulo de gestoría</a>',
            ]),
        ],
    ),
    dict(
        slug="como-organizar-las-visitas-en-una-agencia-de-autos",
        title="Cómo organizar las visitas de clientes en una agencia",
        desc="Cómo organizar la agenda de visitas de una agencia de autos usados: qué datos registrar, horarios por vendedor, excepciones y seguimiento.",
        h1="Cómo organizar las visitas de clientes en una agencia de autos",
        lead="Cuando las visitas se arreglan por mensajes sueltos, se cruzan clientes y los vendedores no están. Una agenda simple y compartida resuelve casi todo.",
        modules=["visitas"],
        sections=[
            ("Los problemas típicos de coordinar visitas por chat", [
                ("ul", [
                    "Dos clientes citados a la misma hora con el mismo vendedor.",
                    "Un vendedor que no sabía que tenía una visita.",
                    "Clientes que llegan y nadie tiene anotado qué auto querían ver.",
                    "Nadie recuerda si una visita se concretó o se canceló.",
                ]),
            ]),
            ("Qué datos registrar de cada visita", [
                ("ul", [
                    "<strong>Cliente</strong> y forma de contacto.",
                    "<strong>Fecha y horario.</strong>",
                    "<strong>Vendedor asignado</strong> que lo va a atender.",
                    "<strong>Quién coordina</strong> la visita, si hay un equipo de soporte.",
                    "<strong>Estado:</strong> pendiente, realizada o cancelada.",
                    "<strong>Comentarios:</strong> qué busca el cliente o qué auto quiere ver.",
                ]),
            ]),
            ("Horarios por vendedor y excepciones", [
                "No todos los vendedores trabajan los mismos días y horarios. Definir los horarios de cada uno evita agendar visitas en momentos en que no está. Y como siempre hay días puntuales en los que alguien no puede, conviene poder cargar excepciones por fecha sin tocar el horario habitual.",
            ]),
            ("Una vista de calendario", [
                "El listado sirve para buscar y filtrar, pero el calendario es lo que permite ver la semana de un vistazo. Lo ideal es poder mirar por mes, por semana y por día.",
            ]),
            ("Cómo lo resuelve Tablero", [
                "El %s tiene una agenda con cliente, fecha, horario, vendedor asignado, asesor, estado y comentarios, con filtros por fecha, vendedor y asesor, un calendario por mes, semana y día, y horarios por vendedor con excepciones por fecha." % '<a href="/modulos/visitas-y-agenda/">módulo de visitas</a>',
            ]),
        ],
    ),
    dict(
        slug="detailing-autos-usados-preparacion-para-la-venta",
        title="Detailing de autos usados: cómo ordenar la preparación",
        desc="Cómo organizar el detailing y la preparación de autos usados antes de la venta: catálogo de servicios, asignación por unidad y seguimiento.",
        h1="Detailing de autos usados: cómo ordenar la preparación antes de la venta",
        lead="Un auto bien presentado se muestra mejor. Pero preparar unidades también implica coordinar servicios, precios y tiempos. Así se ordena.",
        modules=["detailing"],
        sections=[
            ("La preparación es parte de la venta", [
                "Entre que un auto ingresa al stock y se pone a la venta, suele pasar por algún tipo de preparación: lavado, detailing, repasos, trabajos de chapa. Si no hay un registro, es difícil saber qué se le hizo a cada unidad y qué falta.",
            ]),
            ("Paso 1: armar un catálogo de servicios con precio", [
                "Definí qué servicios ofrece o contrata tu agencia y cuánto cuesta cada uno: por ejemplo lavado simple, detailing completo, repaso para entrega o trabajos de chapa. Con un catálogo, todos hablan de lo mismo y el costo de preparar cada unidad es claro.",
            ]),
            ("Paso 2: asignar los servicios a cada auto", [
                "Cada unidad que lo necesite debería tener sus servicios asignados. Así existe una lista de pendientes de preparación y se evita que un auto salga a mostrarse a medias.",
            ]),
            ("Paso 3: marcar lo que ya se hizo", [
                "Cada servicio debería poder marcarse como realizado. Ese registro permite saber qué se hizo, cuándo y en qué unidad, y evita repetir trabajos.",
            ]),
            ("Paso 4: que el auto vuelva solo a estar disponible", [
                "Cuando se completan los servicios asignados, el auto debería volver al estado de disponible sin que nadie tenga que acordarse de actualizarlo.",
            ]),
            ("Cómo lo resuelve Tablero", [
                "El %s incluye un catálogo de servicios con precio, la asignación a cada auto, listas de pendientes de preparación, de vehículos con servicios y de servicios realizados, y el rol Detailer para quien hace el trabajo. Al terminar, el auto vuelve solo a Disponible." % '<a href="/modulos/detailing-de-autos/">módulo de detailing</a>',
            ]),
        ],
    ),
    dict(
        slug="vitrina-web-agencia-de-autos-stock-real",
        title="Vitrina web de una agencia: cómo mostrar el stock real",
        desc="Cómo lograr que la vitrina web de tu agencia de autos usados muestre siempre el stock real, sin cargar cada auto dos veces ni dejar vendidos publicados.",
        h1="Vitrina web de una agencia de autos: cómo mostrar siempre el stock real",
        lead="Nada molesta más a un cliente que consultar por un auto que ya se vendió. Esto es lo que ayuda a que la web diga siempre la verdad.",
        modules=["inventario"],
        sections=[
            ("El problema: dos listas que se desfasan", [
                "Cuando el stock se lleva en un lugar y la web se actualiza a mano en otro, tarde o temprano hay diferencias: autos vendidos que siguen publicados, precios viejos, unidades nuevas que todavía no aparecen. Cada diferencia es una consulta perdida o un cliente molesto.",
            ]),
            ("Qué buscan los clientes en una vitrina", [
                "Por lo general, quien navega la vitrina de una agencia quiere filtrar rápido. Los filtros que más valor aportan son la marca, el tipo de carrocería y el precio máximo, que es justamente lo que permite descartar opciones sin abrir cada ficha.",
            ]),
            ("La solución: que la web se actualice sola", [
                "La forma más confiable de mostrar el stock real es que la vitrina se actualice automáticamente cada vez que se guarda un auto en el sistema de gestión. Técnicamente suele hacerse con un <em>webhook</em>: cuando se guarda un cambio, el sistema avisa a la web, y la web se actualiza. Para el equipo es transparente: cargan el auto una vez y listo.",
            ]),
            ("Buenas prácticas para cada ficha", [
                ("ul", [
                    "Fotos recientes y de buena calidad.",
                    "Precio con su moneda a la vista.",
                    "Datos completos: año, kilómetros, marca y modelo.",
                    "Baja inmediata de las unidades vendidas (que sea automática, no una tarea).",
                ]),
            ]),
            ("Cómo lo resuelve Tablero", [
                "En Tablero la vitrina pública está sincronizada en tiempo real: cada vez que guardás un auto, un webhook automático actualiza la vitrina, y tus clientes buscan por marca, carrocería y precio máximo en USD, siempre con el stock real. Más en el %s." % '<a href="/modulos/inventario-de-autos/">módulo de inventario</a>',
            ]),
        ],
    ),
    dict(
        slug="permisos-y-roles-quien-debe-ver-la-caja-agencia-de-autos",
        title="Roles y permisos: quién debería ver la caja de la agencia",
        desc="Cómo definir roles y permisos en una agencia de autos usados: quién carga, quién edita, quién solo mira y quién no debería ver la plata.",
        h1="Roles y permisos en una agencia de autos: quién debería ver la caja",
        lead="No todas las personas del equipo necesitan ver o editar lo mismo. Definir roles evita errores, protege la información y hace que cada uno trabaje sobre lo suyo.",
        modules=["finanzas", "inventario"],
        sections=[
            ("El principio: cada persona, lo que necesita", [
                "La regla más útil para definir permisos es dar a cada persona el acceso mínimo que necesita para hacer bien su trabajo. Un vendedor necesita gestionar autos; un detailer, ver la preparación; un gestor, la documentación. Ninguno necesita, por lo general, editar la caja.",
            ]),
            ("Preguntas para definir los roles de tu agencia", [
                ("ol", [
                    "¿Quién carga movimientos de dinero y quién los controla? Conviene que sean personas o roles distintos.",
                    "¿Quién puede editar o borrar? Eso debería ser más restringido que cargar.",
                    "¿Hay personas que solo necesitan mirar? Un perfil de solo lectura es muy útil.",
                    "¿Hay personas que necesitan ver todo lo operativo, pero no el dinero?",
                    "¿Quién coordina agenda y visitas?",
                ]),
            ]),
            ("Los ocho roles de Tablero", [
                ("ul", [
                    "<strong>Administrador:</strong> acceso total al sistema.",
                    "<strong>Vendedor:</strong> gestiona autos y carga movimientos, sin editar ni borrar.",
                    "<strong>Contadora:</strong> finanzas completas; carga, edita y borra.",
                    "<strong>Visualizador:</strong> solo lectura de finanzas.",
                    "<strong>Gestor:</strong> módulo de gestoría y documentación legal.",
                    "<strong>Detailer:</strong> módulo de preparación y detailing.",
                    "<strong>Gerente:</strong> todo el negocio operativo, menos la plata.",
                    "<strong>Soporte:</strong> coordina visitas y se asigna a autos y movimientos.",
                ]),
                "Y como cada agencia se organiza distinto, los permisos se ajustan a cómo trabaja tu equipo.",
            ]),
            ("Errores comunes", [
                ("ul", [
                    "Dar a todos el rol de administrador «para simplificar».",
                    "Compartir una misma cuenta entre varias personas.",
                    "Dejar permisos de edición a quien solo debería cargar.",
                ]),
            ]),
            ("Para seguir", [
                "Mirá cómo se aplican estos permisos en el %s y en el %s." % ('<a href="/modulos/finanzas-agencia-de-autos/">módulo de finanzas</a>', '<a href="/modulos/inventario-de-autos/">módulo de inventario</a>'),
            ]),
        ],
    ),
    dict(
        slug="como-elegir-sistema-de-gestion-agencia-de-autos-usados",
        title="Cómo elegir un sistema de gestión para tu agencia de autos",
        desc="Las preguntas que conviene hacer antes de contratar un sistema de gestión para una agencia de autos usados: ciclo completo, monedas, trámites y permisos.",
        h1="Cómo elegir un sistema de gestión para tu agencia de autos usados",
        lead="No alcanza con comparar listas de funciones. Estas son las preguntas que ayudan a decidir si un sistema realmente encaja con tu forma de trabajar.",
        modules=["inventario", "gestoria", "finanzas"],
        sections=[
            ("1. ¿Cubre todo el ciclo del auto o solo el stock?", [
                "El stock es el punto de partida, pero una agencia también prepara autos, agenda visitas, cobra, paga gastos y hace trámites. Cuanto más del ciclo cubre el sistema, menos herramientas sueltas vas a tener.",
            ]),
            ("2. ¿Entiende el negocio local?", [
                "Preguntá si maneja pesos y dólares, y si contempla trámites propios del mercado argentino, como el formulario 08, la verificación policial o el informe de dominio. Un software genérico adaptado suele quedarse corto en estos puntos.",
            ]),
            ("3. ¿Cada persona ve lo que le corresponde?", [
                "Revisá si hay roles diferenciados y qué tan finos son. Especialmente: quién puede ver y editar la caja.",
            ]),
            ("4. ¿La vitrina web muestra el stock real?", [
                "Si tenés web, fijate que se sincronice sola con el sistema. Cargar cada auto dos veces no escala.",
            ]),
            ("5. ¿Se adapta a tu forma de trabajar?", [
                "Cada agencia tiene sus categorías, sus controles y su manera de organizar al equipo. Preguntá qué se puede personalizar y cómo se hace.",
            ]),
            ("6. ¿Quién te acompaña en la implementación?", [
                "Un buen sistema mal implementado no sirve. Preguntá cómo es el proceso de arranque y quién te acompaña.",
            ]),
            ("7. ¿Cómo es la contratación?", [
                "Pedí que te expliquen planes y condiciones antes de decidir, y que te muestren el sistema funcionando. Si es posible, probalo con casos reales de tu agencia.",
            ]),
            ("Dónde encaja Tablero", [
                "Tablero está pensado alrededor de estos puntos: cubre inventario, finanzas, gestoría, detailing, visitas y tareas, trabaja en pesos y dólares, tiene ocho roles, sincroniza la vitrina pública y se arma con cada agencia, módulo por módulo. Podés ver más en la página del %s o %s." % ('<a href="/sistema-de-gestion-para-agencia-de-autos-usados/">sistema de gestión para agencia de autos usados</a>', '<a href="https://wa.me/5491122699526?text=Hola!%20Quiero%20una%20demo%20de%20Tablero." target="_blank" rel="noopener">pedir una demo por WhatsApp</a>'),
            ]),
        ],
    ),
    dict(
        slug="excel-o-sistema-de-gestion-agencia-de-autos",
        title="Excel o sistema de gestión: cuándo dar el salto en tu agencia",
        desc="Cuándo una planilla deja de alcanzar para una agencia de autos usados, qué señales indican que conviene un sistema de gestión y cómo hacer la transición.",
        h1="Excel o sistema de gestión: cuándo conviene dar el salto en tu agencia de autos",
        lead="Las planillas sirven y mucho. Pero llega un momento en que cuestan más de lo que ayudan. Estas son las señales y una forma ordenada de hacer el cambio.",
        modules=["inventario"],
        sections=[
            ("Lo que las planillas hacen bien", [
                "Son flexibles, rápidas de armar y conocidas por todos. Para empezar, o para una agencia muy chica con una sola persona a cargo, pueden ser suficientes.",
            ]),
            ("Señales de que la planilla quedó chica", [
                ("ul", [
                    "Hay más de una persona editando y existen varias versiones del mismo archivo.",
                    "Perdés tiempo conciliando datos entre stock, caja y gestoría.",
                    "Tu vitrina web no coincide con el stock real.",
                    "No podés darle a cada persona acceso solo a lo que le corresponde.",
                    "Cuesta saber en qué etapa está cada auto: preparación, documentación, visita, transferencia.",
                    "La caja en pesos y dólares requiere cuentas manuales.",
                ]),
            ]),
            ("Cómo hacer la transición sin frenar la operación", [
                ("ol", [
                    "<strong>Empezá por el inventario.</strong> Es el módulo que más ordena y el que todos usan.",
                    "<strong>Sumá la vitrina web</strong> para dejar de cargar autos dos veces.",
                    "<strong>Después sumá finanzas</strong>, y luego gestoría, detailing, visitas y tareas, a medida que el equipo se acostumbra.",
                    "<strong>Definí los roles</strong> desde el principio, para que cada persona tenga acceso a lo suyo.",
                ]),
                "Esta lógica es la de los planes de Tablero: el plan Esencial arranca con inventario y vitrina, y el plan Completo suma finanzas, gestoría, detailing, visitas y tareas.",
            ]),
            ("Qué hacer con las planillas actuales", [
                "Contanos qué planillas usás hoy y cómo llevás cada área, y lo vemos juntos. Podés escribirnos por %s." % '<a href="https://wa.me/5491122699526?text=Hola!%20Hoy%20uso%20planillas%20y%20quiero%20ver%20Tablero." target="_blank" rel="noopener">WhatsApp</a>',
                "Para ordenar el stock desde cero, empezá por %s." % '<a href="/blog/como-llevar-el-stock-de-una-agencia-de-autos-usados/">Cómo llevar el stock de una agencia de autos usados</a>',
            ]),
        ],
    ),
]

POST = {p["slug"]: p for p in POSTS}


def post_url(slug):
    return "/blog/%s/" % slug


def words(p):
    import re
    n = len(re.sub(r"<[^>]+>", " ", p["lead"]).split())
    for h2, body in p["sections"]:
        if h2 == "callout":
            n += len(body.split())
            continue
        n += len(h2.split())
        for b in body:
            if isinstance(b, str):
                n += len(re.sub(r"<[^>]+>", " ", b).split())
            elif b[0] in ("ul", "ol"):
                for i in b[1]:
                    n += len(re.sub(r"<[^>]+>", " ", i).split())
    return n


def minutes(p):
    return max(2, round(words(p) / 200))
