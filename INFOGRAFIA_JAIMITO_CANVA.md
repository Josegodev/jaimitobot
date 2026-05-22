# ¿Cómo funciona Jaimito?

## Subtítulo
El asistente del curso de IA aplicada que ayuda a preparar la web del proyecto final

## Texto de apertura
Jaimito es un bot de Telegram que acompaña al alumnado cuando prepara su proyecto final. Recibe dudas, orienta paso a paso y, cuando hace falta, consulta IA para responder mejor.

---

## Flujo principal visual
Alumno en Telegram → Jaimito Bot → Railway 24/7 → Docker → OpenAI → Respuesta en Telegram

---

## Bloque 1. Alumno en Telegram

**Título corto:** El alumno escribe su duda

**Texto breve:** El alumno usa Telegram para pedir ayuda con su proyecto.

**Ejemplos visuales:**

```text
/pregunta ¿Cómo empiezo mi web?
/web Quiero hacer una idea sobre una tienda
```

**Iconos recomendados:** alumno, móvil, Telegram

---

## Bloque 2. Jaimito Bot

**Título corto:** Jaimito recibe el mensaje

**Texto breve:** Jaimito lee la duda y decide qué hacer. Si puede responder con ayuda preparada, lo hace. Si necesita elaborar una mejor respuesta, consulta IA.

**Iconos recomendados:** robot pequeño, burbuja de chat

---

## Bloque 3. Railway

**Título corto:** Jaimito está encendido 24/7

**Texto breve:** Railway es el servidor en la nube que mantiene el bot encendido aunque el ordenador esté apagado.

**Iconos recomendados:** nube, servidor, luz verde de "activo"

---

## Bloque 4. Docker

**Título corto:** Todo va dentro de una caja preparada

**Texto breve:** Docker es una caja con todo lo necesario para que funcione igual siempre.

**Iconos recomendados:** caja, contenedor, paquete

---

## Bloque 5. OpenAI

**Título corto:** Cuando hace falta, consulta IA

**Texto breve:** OpenAI ayuda a generar respuestas, pero Jaimito le indica que hable claro, sencillo y útil para el proyecto.

**Iconos recomendados:** cerebro IA, chispa, nube inteligente

---

## Bloque 6. Respuesta en Telegram

**Título corto:** El alumno recibe ayuda práctica

**Texto breve:** Jaimito devuelve una respuesta clara para que el alumno pueda avanzar en su web del proyecto final.

**Ejemplo de respuesta:**

> Tu web puede explicar el problema, a quién ayuda, cómo usarías IA y cuál sería el resultado esperado.

**Iconos recomendados:** mensaje de Telegram, check, documento web

---

## Sección extra: Por dentro de Jaimito

**Título de sección:** Los archivos que hacen funcionar al bot

### Tarjeta 1. `config.py`

**Texto simple:** Prepara la configuración del bot. Lee las claves y decide con qué modelo de IA trabajar.

**Ejemplo corto de código:**

```python
openai_model=os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
```

**Explicación visual corta:** "Busca la configuración necesaria para arrancar."

**Icono recomendado:** llave, engranaje, ajustes

### Tarjeta 2. `jaimito_bot.py`

**Texto simple:** Es el archivo principal. Recibe comandos de Telegram, llama a OpenAI cuando hace falta y envía la respuesta.

**Ejemplo corto de código:**

```python
application.add_handler(CommandHandler("web", web))
```

**Explicación visual corta:** "Conecta Telegram con la lógica del bot."

**Icono recomendado:** robot, flechas, centro de control

### Tarjeta 3. `logging_utils.py`

**Texto simple:** Guarda registros internos para revisar errores o saber qué ha pasado.

**Ejemplo corto de código:**

```python
def new_trace_id() -> str:
    return uuid4().hex
```

**Explicación visual corta:** "Anota información interna para depurar."

**Icono recomendado:** lupa, bloc de notas, historial

### Tarjeta 4. `prompts.py`

**Texto simple:** Define cómo debe hablar Jaimito y qué tipo de ayuda debe dar al alumnado.

**Ejemplo corto de código:**

```python
SYSTEM_PROMPT = "Eres Jaimito..."
```

**Explicación visual corta:** "Marca el tono, el estilo y la misión del bot."

**Icono recomendado:** bocadillo de texto, bombilla, documento

---

## Sección: Qué puede hacer Jaimito

### Título
Qué puede hacer Jaimito

- Ayudar a elegir una idea de proyecto
- Explicar las secciones de la web
- Redactar textos claros
- Dar una plantilla de web
- Explicar la rúbrica
- Resolver dudas durante el curso

---

## Sección: Cómo se controla

### Título
Cómo se controla

- Solo responde a comandos o menciones
- No responde a todos los mensajes del grupo
- Las claves se guardan como variables privadas
- Los errores se revisan en registros internos
- No se muestra información técnica al alumnado

---

## Mensaje final

**Jaimito no sustituye al profesor: ayuda al alumnado a avanzar paso a paso con su proyecto.**

---

## Paleta de colores

- Azul claro: `#D9EEFF`
- Azul principal: `#4A90E2`
- Blanco: `#FFFFFF`
- Gris oscuro: `#2F3A45`
- Gris suave: `#EEF3F7`
- Verde de estado activo: `#36B37E`

---

## Iconos recomendados

- Alumno o persona con móvil
- Logo de Telegram
- Robot pequeño amable
- Nube o servidor
- Caja Docker
- Cerebro o chispa IA
- Documento o mini web
- Llave o engranaje
- Lupa o historial
- Candado o escudo

---

## Distribución visual recomendada

### Opción 1. Infografía vertical

- Arriba: título, subtítulo y robot protagonista
- Centro: flujo principal en 6 bloques con flechas grandes
- Debajo: sección `Los archivos que hacen funcionar al bot` con 4 tarjetas
- Abajo: dos franjas
- `Qué puede hacer Jaimito`
- `Cómo se controla`
- Cierre final en una banda destacada

### Opción 2. Diapositiva 16:9

- Izquierda: flujo principal
- Derecha: 4 tarjetas de archivos
- Parte inferior: `Qué puede hacer Jaimito` y `Cómo se controla`
- Pie: mensaje final

---

## Nota importante de consistencia

En el repositorio hay una pequeña contradicción documental:

- existe `Dockerfile`
- pero el `README` también dice que Railway funciona "sin Docker"

Para la infografía puedes mantener Docker como "caja preparada", pero conviene revisar después qué versión quieres enseñar como explicación oficial.
