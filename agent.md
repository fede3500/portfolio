# Ecosistema de agentes del portfolio

Catálogo operativo de roles, no agentes registrados automáticamente. Una persona o asistente puede asumir varios; delegar solo si el entorno y la petición lo permiten. Aplicar las instrucciones vigentes y leer las skills pertinentes antes de usarlas. El usuario tiene prioridad.

## Diagnóstico del repositorio

- Portfolio estático de una página, con `index.html`, `css/style.css`, `js/script.js`, imágenes y CV. Utiliza HTML, CSS y JavaScript nativos, Flexbox y media queries. Los logotipos de React y otras tecnologías son contenido, no prueba de que el sitio las utilice.
- Hay JavaScript externo e inline, navegación por anclas, menú móvil, tarjeta interactiva y animaciones CSS. `css/reset.css` y `js/fastclick.js` existen, pero la página carga normalize y FastClick desde CDN: comprobar usos antes de retirarlos.
- Dependencias externas: Google Fonts, normalize, tres versiones de Font Awesome, Hammer.js y FastClick. Hammer declara integridad en su etiqueta. No hay manifiesto ni lockfile; evaluar necesidad, versión, procedencia y fallos de carga antes de cambiar dependencias.
- El README propone abrir `index.html` directamente; la configuración de VS Code asigna el puerto 5502 a Live Server. Hay remoto GitHub, pero no evidencia en el repositorio de un despliegue configurado. No se encontraron framework, backend, build, pruebas automatizadas, linter ni CI/CD. No asumirlos ni incorporar infraestructura por defecto.
- Riesgos observados que requieren reproducción: el README afirma que el formulario recibe consultas, pero el formulario usa `action="#"` y no se observa implementación de envío; hay enlaces de proyecto vacíos, imágenes sin alternativa útil, controles no semánticos y un viewport que impide el zoom. El cierre del menú referencia `.scroll-button a`; comprobar si existe. El manejador de scroll añade listeners repetidamente. La tarjeta y enlaces sociales dependen de Hammer/FastClick. Hay animaciones infinitas y `transition: all`, sin regla de movimiento reducido localizada en la hoja principal.

## Coordinación y reglas comunes

1. Leer los archivos afectados y establecer el comportamiento actual antes de editar. Activar el mínimo de roles; para tareas pequeñas combinar responsabilidades. Prioridad habitual: Frontend, UX/UI y Calidad.
2. Preservar identidad, contenido, enlaces y rutas salvo petición contraria. No inventar cifras, experiencia, proyectos, testimonios ni datos de contacto; no alterar datos personales o CV por inferencia.
3. Preferir soluciones pequeñas en la pila existente. No introducir framework, build, servicios, dependencias o automatizaciones persistentes sin necesidad demostrada y autorización correspondiente.
4. Verificar según el cambio: escritorio y móvil, teclado, foco, zoom, movimiento reducido, enlaces y consola. Indicar lo no probado; una inspección estática no equivale a una prueba en navegador. En revisión, citar archivo y línea, priorizar defectos y separar hipótesis de hechos.
5. Hallmark corresponde a páginas nuevas o a un rediseño/auditoría solicitados explícitamente con Hallmark; no aplicar su flujo completo a cambios ordinarios. Taste requiere una referencia concreta y herramientas de captura: no inventar evidencia. Impeccable orienta trabajo de interfaz. Seleccionar las skills de Emil según la tarea y leer sus instrucciones vigentes. Ninguna skill autoriza por sí sola delegación o acciones externas.

## 1. Frontend y arquitectura

**Mission:** mantener y desarrollar el sitio con una estructura comprensible y proporcional a su tamaño.

**Responsibilities:** HTML semántico, CSS responsive, JavaScript, límites entre presentación y comportamiento y refactorización justificada. Preservar anclas, recursos relativos y apertura local.

**Activation Criteria:** nueva sección o interacción, corrección funcional, refactor o decisión estructural.

**Workflow:** inspeccionar usos y comportamiento; definir alcance; aplicar cambios incrementales; comprobar rutas, navegación, consola y estados afectados; comunicar riesgos.

**Best Practices:** mantener la pila nativa salvo motivo demostrado; evitar listeners duplicados y estados globales innecesarios; usar controles semánticos y mejora progresiva. Extraer código inline cuando mejore el mantenimiento y se preserve el orden de carga.

**Related Skills:** Impeccable; Emil `emil-design-eng` para interacción; Hallmark en su ámbito indicado.

**Inputs:** petición, archivos, comportamiento actual y restricciones. **Tools:** búsqueda, editor, Git y navegador o servidor local. **Deliverables:** cambios, decisiones y comprobaciones con limitaciones.

## 2. UX/UI, accesibilidad y movimiento

**Mission:** mejorar claridad y usabilidad preservando identidad y contenido real.

**Responsibilities:** jerarquía, responsive, contraste, semántica, foco, teclado, zoom, textos alternativos, estados y movimiento; estudiar referencias cuando se solicite.

**Activation Criteria:** diseño, rediseño, auditoría visual o de accesibilidad, interacción táctil o animación.

**Workflow:** identificar objetivo y contexto; inspeccionar y, si es posible, renderizar; documentar evidencia; resolver y comprobar tamaños, teclado, zoom y movimiento reducido; señalar compromisos.

**Best Practices:** no inventar contenido ni copiar una estética sin petición; asegurar acciones utilizables sin hover; respetar `prefers-reduced-motion`; utilizar movimiento con propósito y propiedades eficientes. No imponer retroactivamente todas las reglas visuales de Hallmark.

**Related Skills:** Impeccable; Hallmark para nuevas páginas o rediseño/auditoría explícitos; Taste para una referencia concreta; Emil `animate`, `animation-performance`, `gestures`, `mobile-native` y `emil-design-eng` según corresponda.

**Inputs:** objetivo, contenido, restricciones y referencia si existe. **Tools:** navegador, DOM/CSS, capturas y herramientas de accesibilidad disponibles. **Deliverables:** implementación o hallazgos priorizados con evidencia y pruebas.

## 3. Calidad, debugging y code review

**Mission:** detectar y prevenir regresiones con comprobaciones proporcionadas.

**Responsibilities:** reproducir errores, investigar causas, revisar cambios y verificar menú, tarjeta, enlaces, formulario y recursos según el alcance. Mantener la revisión separada de la implementación cuando solo se pida revisar.

**Activation Criteria:** bug, revisión solicitada, comportamiento incierto o cambio con riesgo de regresión.

**Workflow:** registrar pasos y resultado esperado/real; aislar la causa; corregir cuando esté dentro del encargo; repetir el caso y comprobar escenarios vecinos; comunicar hallazgos y límites.

**Best Practices:** no afirmar que existen suites o CI; utilizar pruebas manuales pertinentes y añadir automatizadas significativas cuando aporten valor. No instalar herramientas sin justificación ni presentar conjeturas como defectos confirmados. Considerar fallo de CDN y JavaScript deshabilitado cuando afecten al cambio.

**Related Skills:** Emil `break-ui` para datos extremos y `review-animations` para movimiento; Impeccable para UX.

**Inputs:** fallo o diff, pasos, navegador y resultado esperado. **Tools:** Git diff, búsqueda, consola, navegador y validadores disponibles. **Deliverables:** causa y corrección verificada o revisión priorizada con archivo/línea, reproducción y riesgos.

## 4. Rendimiento, seguridad y dependencias

**Mission:** reducir riesgos y costes de carga sin complejidad innecesaria.

**Responsibilities:** revisar imágenes, fuentes, scripts, animaciones, scroll y recursos externos; evaluar versiones, integridad y necesidad de CDN, incluyendo duplicados de Font Awesome y uso de Hammer/FastClick.

**Activation Criteria:** lentitud, problema de seguridad o red, actualización de dependencias o integración externa.

**Workflow:** establecer comportamiento y medir si es posible; identificar causa; evaluar compatibilidad; aplicar cambio mínimo; comparar resultados y comprobar recursos e interacciones afectados.

**Best Practices:** no atribuir vulnerabilidades sin evidencia ni retirar librerías solo por su antigüedad; verificar procedencia y licencias; no exponer secretos o datos personales. Aplicar integridad y políticas de seguridad compatibles con el despliegue real; no inventar métricas.

**Related Skills:** Emil `animation-performance`, `remove-animations` o `review-animations`; Impeccable para impacto en experiencia.

**Inputs:** síntomas, recursos, mediciones y navegadores objetivo. **Tools:** DevTools, búsqueda, documentación oficial y auditorías disponibles. **Deliverables:** hallazgos reproducibles, cambios justificados, validación y riesgos de compatibilidad.

## 5. Integraciones, DevOps y automatización

**Mission:** conectar y entregar el sitio de manera fiable cuando exista una necesidad concreta.

**Responsibilities:** investigar formulario, enlaces, hosting y despliegue; diseñar integraciones, validación y errores; proponer CI o automatización proporcionada al flujo real.

**Activation Criteria:** solicitud de formulario funcional, servicio externo, publicación, despliegue o automatización. No asumir proveedor ni credenciales.

**Workflow:** identificar contrato y restricciones; revisar privacidad y configuración; preparar implementación y pruebas locales; documentar pasos; verificar en entorno autorizado antes de declarar éxito.

**Best Practices:** no enviar mensajes de prueba a terceros sin autorización; no subir secretos; no prometer entrega de formularios sin comprobar el servicio. No publicar ni configurar servicios externos por una mera recomendación. Mantener CI pequeña y reproducible; seguir las autorizaciones vigentes para despliegue y automatizaciones persistentes.

**Related Skills:** Impeccable para formularios y errores; Emil `emil-design-eng` para feedback.

**Inputs:** proveedor y contrato autorizados, entorno, datos y criterios de éxito. **Tools:** configuración del repositorio, documentación del proveedor, navegador y CI disponible. **Deliverables:** integración o propuesta verificable, configuración, pruebas y limitaciones.

## 6. Documentación y contenido

**Mission:** mantener instrucciones y contenido fieles al funcionamiento y a los datos del propietario.

**Responsibilities:** actualizar README, ejecución, verificación, dependencias y estado de integraciones; revisar coherencia y enlaces; documentar decisiones sin duplicar instrucciones.

**Activation Criteria:** cambio de comportamiento, dependencias o flujo; solicitud de documentación; discrepancia como la descripción actual del formulario.

**Workflow:** contrastar documentación con código y pruebas; actualizar lo afectado; comprobar rutas y comandos; señalar información que requiere confirmación.

**Best Practices:** escribir instrucciones concretas; distinguir capacidades actuales de propuestas; no modificar hechos profesionales, contacto o CV por inferencia ni prometer capacidades no verificadas.

**Related Skills:** Impeccable para claridad de interfaz; Taste solo para una referencia realmente analizada.

**Inputs:** cambios, evidencia, decisiones y datos proporcionados. **Tools:** editor, búsqueda, Git y navegador para enlaces cuando sea posible. **Deliverables:** documentación actualizada, comprobaciones y cuestiones pendientes.
