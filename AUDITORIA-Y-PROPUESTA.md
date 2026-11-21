# Auditoría y propuesta de reestructuración

Estado: análisis previo a la implementación. Las capacidades y proyectos profesionales que no cuenten con evidencia o confirmación quedan pendientes, no se presentan como hechos.

## 1. Auditoría del portfolio actual

El sitio es una única página estática en inglés, sin framework, compilación, gestor de paquetes, pruebas ni CI visibles en el repositorio. `index.html` concentra contenido y parte del JavaScript; `css/style.css` agrupa estilos, media queries y animaciones; `js/script.js` controla navegación y animación. Los recursos incluyen imágenes, CV y bibliotecas cargadas desde CDN. El README propone abrir el HTML directamente. No se ha verificado el despliegue.

**Narrativa.** El hero presenta únicamente frontend y UX/UI. La biografía conserva un origen personal interesante en Río Ceballos y el paso desde marketing hacia el desarrollo; necesita una transición honesta al posicionamiento actual. La cifra de dos años puede haber caducado. Las descripciones de servicios son largas, repetitivas y no reflejan las prioridades actuales.

**Proyectos.** Deben conservarse los seis: Restaurant, Tech Company, Encryption Program, E-commerce, Courses y Mobile App. Los tres primeros tienen enlaces; los otros figuran como próximos. Courses contiene texto de relleno y un enlace vacío. Comprobar destinos y no inventar resultados ni convertir proyectos pendientes en casos terminados.

**Experiencia de uso y accesibilidad.** El menú y el cierre son elementos genéricos, hay enlaces de iconos sin nombre accesible y fotografías sin alternativas útiles. El viewport deshabilita el zoom. Las tarjetas de proyecto dependen del hover para mostrar información. El formulario no tiene envío implementado pese a la afirmación del README. Revisar también el selector `.scroll-button a` usado en el cierre del menú y los listeners añadidos repetidamente al hacer scroll.

**Visual y rendimiento.** La identidad actual combina azul, fondos claros, fotografía y abundante animación. El footer tiene una superficie azul con burbujas, filtro SVG y un gato animado: es un rasgo propio que debe mantenerse como base. Las burbujas animan tamaño y posición de forma infinita; requieren medición, reducción de coste y alternativa de movimiento reducido. Hay tres versiones de Font Awesome y varias fuentes externas, Hammer y FastClick; no eliminarlas sin verificar sus usos. No se han medido Core Web Vitals.

**SEO y calidad.** Título genérico, estructura de encabezados mejorable y ausencia de una descripción editorial clara. El README describe incorrectamente el formulario. No hay pruebas automatizadas ni flujo CI en el repositorio. La revisión visual y funcional en navegador debe ampliarse durante la implementación.

## 2. Referencia visual

La [referencia publicada](https://fede3500.github.io/demo-mundose-practica-1-Github/) se ha abierto en navegador y contrastado con su `index.html` local. Propone una página en español con hero, biografía, habilidades, proyectos y contacto. Usa fondo `#0e0e10`, superficies `#1a1a1e` y `#232328`, texto `#f0f0f5` y `#b0b0c0`, azul `#4070f4`, radio de 16 px y contenedor máximo de 1120 px. La familia declarada empieza por Inter con alternativas de sistema, pero no hay una carga de Inter en ese archivo. Las tarjetas elevan y cambian borde al hover; el CSS adapta grids bajo 768 px y contacto bajo 480 px. La iconografía usa emoji; las animaciones observadas en código son principalmente transiciones de hover y scroll suave.

**Decisiones aprovechables:** contraste oscuro/azul, ancho de lectura limitado, títulos claros y organización por bloques. **Evolución:** una composición editorial más diferenciada, iconos consistentes, mayor protagonismo de proyectos reales y una navegación accesible. Los tres proyectos de Kubernetes, CI/CD e infraestructura como código de la referencia tienen enlaces `#`; no hay evidencia suficiente para incorporarlos como logros propios finalizados. La referencia aporta dirección visual, no un inventario profesional verificado. No se dispone de capturas visuales exportadas ni mediciones de interacción de la referencia.

## 3. Inventario de contenido

| Tratamiento | Contenido | Decisión |
|---|---|---|
| Mantener | Seis proyectos, enlaces reales, CV, contacto, identidad y footer animado | Conservar destino y estado; validar enlaces y CV. |
| Mantener y reescribir | Trayectoria personal, frontend, UX y aprendizaje | Conectar con los roles actuales sin inventar fechas ni logros. |
| Sustituir | Fotografías personales actuales | Usar el avatar adjunto; no borrar archivos históricos sin necesidad. |
| Fusionar | Skills, servicios y herramientas | Organizar por áreas de trabajo y evitar listas de marcas sin contexto. |
| Retirar de la interfaz | Lorem ipsum, enlace vacío, cifra temporal sin confirmar y formulario que aparenta enviar | Sustituir el contacto por enlaces reales; conservar proyectos pendientes identificados. |
| Ampliar cuando haya evidencia | Experiencia, certificaciones, homelab, cloud, DevOps e IA | Incorporar empresa, fechas, tecnologías, resultados y enlaces solo con información confirmada. |

## 4. Posicionamiento y dirección

Federico combina infraestructura y sistemas con desarrollo frontend, automatización e interés por IA. El sitio debe permitir a reclutadores comprender sus áreas de interés, revisar trabajo real y contactar sin obligarles a leer una larga lista de tecnologías. Voz directa, cercana y concreta, evitando superlativos, métricas inventadas y promesas de dominio.

Propuesta visual: base carbón de la referencia, azul como acento y cian moderado que dialogue con el avatar; superficies oscuras con bordes sutiles, tipografía legible y espacios generosos. Evitar la imitación literal de terminales, dashboards o marcas de inspiración. Conservar el footer líquido y el gato como firma personal, adaptando su transición con el resto de la página. El avatar es una ilustración, por lo que su alternativa debe describirlo como tal.

## 5. Arquitectura de información y sitemap

Una página accesible por anclas evita dividir contenido escaso en rutas vacías:

```text
Inicio / #home
├── Perfil y resumen / #about
├── Áreas de trabajo / #expertise
│   ├── Infraestructura y cloud
│   ├── Sistemas y automatización
│   ├── Frontend y experiencia
│   └── IA y aprendizaje
├── Proyectos / #projects
├── Trayectoria y aprendizaje / #journey (solo con datos suficientes)
├── Contacto / #contact
└── Footer animado
```

Experiencia, certificaciones, homelab y testimonios no necesitan secciones vacías; se añadirán con pruebas reales. La navegación debe conservar equivalencias con las anclas anteriores cuando sea posible.

## 6. Secciones y wireframes conceptuales

| Sección | Propósito y contenido | Componentes, jerarquía y adaptación | Movimiento e iconos |
|---|---|---|---|
| Hero | Identidad, posicionamiento y acción principal; avatar adjunto | Nombre y propuesta primero, acciones y avatar; dos columnas en escritorio, una en móvil | Entrada discreta opcional; iconos funcionales coherentes. |
| Perfil | Trayectoria humana y resumen profesional | Texto breve con enlace al CV; ancho de lectura limitado | Sin movimiento necesario. |
| Expertise | Explicar cloud, sistemas, frontend, automatización e interés en IA sin exagerar experiencia | Bloques con título y descripción; columnas que se apilan en móvil | Iconos lineales discretos; foco visible y hover ligero. |
| Proyectos | Evidencia concreta: los seis proyectos actuales, estados y enlaces disponibles | Tres proyectos enlazados y tres pendientes, con imagen, texto visible y etiquetas; grid a lista en móvil | Transición breve de borde o imagen; nunca ocultar información tras hover. |
| Trayectoria y aprendizaje | Experiencia, certificaciones y laboratorios verificables | Cronología o lista solo cuando existan datos; sin huecos ficticios | Sin animación imprescindible. |
| Contacto | Facilitar conversación con reclutadores y empresas | Correo y enlaces profesionales reales, CV secundario; accesibles en móvil | Feedback de foco y hover. Sin formulario no funcional. |
| Footer | Mantener firma visual personal | Superficie líquida, burbujas y gato; contenido legible en ambas anchuras | Preservar animación con alternativa reducida y coste medido. |

```text
DESKTOP                           MÓVIL
[marca] [perfil proyectos contacto] [marca] [menú]
[nombre y propuesta | avatar]      [nombre y propuesta]
[acciones            |       ]      [acciones] [avatar]
[perfil breve                ]      [perfil]
[infra] [automatización]            [infra]
[frontend] [IA]                     [automatización] …
[proyecto] [proyecto]               [proyecto]
[proyecto] [pendientes]             [proyecto] …
[contacto                    ]      [contacto]
[footer líquido + gato       ]      [footer líquido + gato]
```

## 7. Arquitectura técnica y migración

Mantener inicialmente HTML/CSS/JS nativos para conservar el despliegue estático y evitar complejidad. Separar secciones semánticas, tokens, componentes CSS y comportamiento de navegación; extraer datos a un módulo solo si simplifica la edición sin ocultar contenido a buscadores o romper apertura local. Componentes conceptuales: Header, Hero, Profile, Expertise, ProjectCard, Contact y AnimatedFooter. No implica un framework.

```text
index.html
css/  base.css  components.css  style.css
js/   script.js
images/  profile/  projects/
resume/
README.md
```

La división exacta se decidirá al implementar; evitar archivos vacíos y preservar rutas existentes. Fases: 1) inventariar contenido y recursos; 2) documentar hechos confirmados; 3) establecer tokens y estructura semántica; 4) migrar contenido y seis proyectos; 5) integrar avatar y footer; 6) probar paridad de enlaces, interacción, móvil y accesibilidad; 7) medir rendimiento y revisar SEO; 8) actualizar documentación y preparar despliegue solo cuando esté autorizado. Mantener una vía de reversión mediante Git.

## 8. Estrategias de calidad

- **SEO:** título y descripción específicos, un H1, jerarquía semántica, texto descriptivo para proyectos, Open Graph con recursos reales y URL canónica solo tras confirmar dominio. No inventar datos estructurados. Comprobar indexabilidad y enlaces en el despliegue real.
- **Rendimiento:** medir antes/después en condiciones comparables; dimensionar y comprimir imágenes, cargar las inferiores de forma diferida, limitar fuentes y eliminar dependencias solo tras confirmar usos. Medir especialmente el filtro y la animación del footer; no prometer puntuaciones.
- **Accesibilidad:** landmarks, encabezados ordenados, controles nativos, nombres accesibles, foco visible, contraste, zoom, navegación por teclado, textos alternativos y movimiento reducido. Probar a 200 % de zoom, con teclado y en móvil; complementar herramientas automáticas con revisión manual.
- **Marca personal:** priorizar roles indicados por Federico y evidencias frente a adjetivos; conservar el origen personal y un tono conversacional; diferenciar conocimientos, aprendizaje y experiencia. Solicitar hechos antes de afirmar certificaciones, logros o tecnologías específicas.
- **DevOps y mantenimiento:** documentar ejecución y verificación; introducir pruebas de enlaces y HTML o CI únicamente si aportan valor y se ajustan al hosting. No configurar publicación o servicios externos sin autorización.

## 9. Pendientes para la implementación

Confirmar idioma, acción principal, experiencia, certificaciones, laboratorios y proyectos de infraestructura/cloud/DevOps/IA. Revisar vigencia del CV y datos de contacto. La imagen adjunta está disponible para integrarse. Las propuestas de contenido no deben interpretarse como credenciales verificadas.
