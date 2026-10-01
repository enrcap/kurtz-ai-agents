# Buscando al Coronel Kurtz · Agentes de IA en Python

Proyecto de **Fundamentos de Inteligencia Artificial** que explora cómo tomar decisiones con información parcial: deducir qué casillas son seguras, estimar riesgos y planificar movimientos en un entorno estocástico.

**Autor:** Enrique Capella · **Tecnologías:** Python, NumPy · **Técnicas:** razonamiento lógico, BFS, inferencia bayesiana, A* y Value Iteration.

El Capitán Willard debe localizar a Kurtz y escapar de un palacio peligroso. Un tercer escenario plantea el cruce de un río con corrientes e islas. La interfaz de consola muestra el conocimiento y las decisiones de los agentes durante la ejecución.

## ¿Cuál es el objetivo del proyecto?

La pregunta central es: **¿cómo puede un agente decidir qué hacer cuando no conoce todo lo que ocurre a su alrededor o no puede garantizar el resultado de sus acciones?** El proyecto permite observar tres maneras de resolver ese problema dentro de una simulación interactiva.

En los palacios, la misión consiste en encontrar a Kurtz, llegar con él a la salida y escapar con vida. El agente comienza en la esquina superior izquierda de un tablero 6 × 6, en la posición `(0, 0)`. El resto del mapa está oculto: explorar implica interpretar señales antes de entrar en una casilla que podría ser peligrosa. Encontrar a Kurtz lo rescata automáticamente; para ganar todavía hay que alcanzar la salida y ejecutar la acción de escape.

En el río, la misión es llevar la embarcación hasta la salida de la orilla derecha. El mapa y el modelo de la corriente están disponibles para el solucionador, pero una misma acción puede tener distintos resultados. Aquí el reto es escoger movimientos que compensen esa incertidumbre.

**Los tres escenarios se seleccionan por separado en el menú.** Aunque comparten la historia, el programa no encadena una partida de palacio con una de río ni traslada el estado de una a otra.

## Escenarios y algoritmos

| Escenario | Problema | Solución implementada | Visualización |
| --- | --- | --- | --- |
| Palacio lógico | Explorar una cuadrícula 6 × 6 sin conocer la ubicación de los peligros | Base de conocimiento con reglas de deducción y BFS sobre casillas consideradas seguras | Mapa mental con casillas exploradas, peligros posibles y confirmados |
| Palacio bayesiano | Estimar la ubicación de trampas, un enemigo y la salida a partir de estímulos | Actualización de distribuciones con Bayes y A* con penalización por riesgo | Mapa de probabilidades y riesgo |
| Cruce del río | Elegir movimientos cuando la corriente puede cambiar el destino | MDP con transiciones probabilísticas y Value Iteration para extraer una política | Tablero del río y política mediante flechas |

## ¿Cómo funciona una partida?

En los dos palacios, cada turno sigue este ciclo:

1. **Percibir:** el entorno informa de las sensaciones en la posición actual, como brisa, ronquidos, estímulos de trampas o resplandor de la salida.
2. **Actualizar el conocimiento:** el agente incorpora esas señales a su mapa mental o a sus probabilidades.
3. **Decidir:** en modo manual, eliges la acción viendo ese conocimiento; en modo automático, el agente calcula el siguiente paso.
4. **Actuar:** el entorno aplica el movimiento o la acción, comprueba si se ha encontrado a Kurtz, alcanzado un peligro o completado la misión, y muestra el resultado.

El tablero que ves en un palacio representa **lo que el agente cree o ha deducido**, no un mapa completo con todos los peligros revelados. Las coordenadas se escriben como `(fila, columna)`: moverse al sur aumenta la fila y moverse al este aumenta la columna.

### 1. Palacio lógico: deducir antes de avanzar

Este escenario contiene tres precipicios, un soldado, Kurtz y una salida. La **brisa** avisa de un precipicio en alguna casilla vecina; el **ronquido**, de un soldado vecino; y el **resplandor**, de una salida en la casilla actual o en una vecina. Los vecinos son las casillas al norte, sur, este y oeste, sin diagonales.

El agente conserva las observaciones de turnos anteriores y aplica reglas para marcar casillas seguras, posibles peligros y peligros confirmados. Por ejemplo, si no hay brisa ni ronquido, puede considerar seguras las casillas vecinas. Cuando hay una señal de peligro, debe reducir las posibilidades con la información que va acumulando.

El modo automático utiliza **BFS (búsqueda en anchura)**: explora rutas por casillas consideradas seguras y devuelve el primer paso de una ruta hacia el objetivo o hacia una casilla segura aún no explorada. Si confirma un soldado vecino, puede lanzar su única granada en esa dirección. Si no encuentra un movimiento que pueda planificar, la partida automática se detiene indicando que el agente está bloqueado.

**Ejemplo ilustrativo:** desde `(0, 0)`, si no se percibe brisa ni ronquido, `(0, 1)` y `(1, 0)` se consideran seguras. El agente puede avanzar a una de ellas. Si en la nueva posición aparece brisa, incorpora a las casillas vecinas no seguras como posibles ubicaciones de precipicios; la señal por sí sola no le dice cuál contiene uno.

### 2. Palacio bayesiano: decidir según el riesgo

Aquí hay tres tipos de trampas: fuego, pinchos y dardos, además de un soldado. Cada amenaza tiene un estímulo propio que puede percibirse en su casilla o en una vecina. Las trampas pueden coincidir entre sí; Kurtz, el soldado y la salida se generan en casillas sin trampas.

El agente mantiene una distribución de probabilidad para cada amenaza y para la salida. Empieza repartiendo la probabilidad entre las casillas candidatas y, al recibir una señal, **actualiza sus creencias con la regla de Bayes**: descarta posiciones incompatibles con la observación y normaliza las probabilidades restantes. Haber llegado vivo a una casilla también aporta información.

Para decidir, combina las probabilidades de las amenazas en un riesgo total estimado. El planificador usa **A***, priorizando movimientos según la distancia recorrida, una estimación de la distancia al objetivo y una penalización por riesgo. Primero busca por casillas con riesgo inferior al 5 %; si no encuentra ruta, vuelve a intentarlo con un umbral del 20 %. Si tampoco encuentra una, se detiene. Tras rescatar a Kurtz, intenta dirigirse a la casilla con mayor probabilidad de contener la salida.

Así, una casilla aparentemente cercana puede ser menos atractiva que otra más alejada si su riesgo estimado es mayor. Esas probabilidades son creencias del modelo: una etiqueta de riesgo bajo no garantiza que la casilla sea segura.

### 3. Río: planificar cuando la corriente cambia el movimiento

El río tiene una cuadrícula 6 × 6, dos islas y una salida. Las acciones disponibles son subir, bajar, ir a la izquierda, ir a la derecha y quedarse. En las columnas interiores, la corriente puede arrastrar la embarcación al sur en lugar de ejecutar el movimiento deseado; bajar es determinista. Intentar entrar en una isla o salir del tablero deja la embarcación en su posición actual.

El problema se representa como un **MDP (Proceso de Decisión de Markov)**: cada casilla es un estado, cada movimiento es una acción y cada posible destino tiene una probabilidad y una recompensa. Llegar a la salida da `+100`; las demás transiciones cuestan `-1`.

**Value Iteration** calcula repetidamente cuánto retorno puede esperarse desde cada casilla, considerando los posibles resultados de cada acción. A partir de esos valores extrae una **política**, es decir, una recomendación de movimiento para cada casilla, que se dibuja con flechas.

La simulación sigue esa política y sortea el destino de cada movimiento según las probabilidades de transición. Termina al llegar a la salida o al alcanzar 50 pasos, mostrando los pasos y la recompensa acumulada. La política es un plan para todos los estados; no es una ruta fija que la corriente vaya a respetar.

## Vista del proyecto

Capturas de ejecuciones incluidas en la memoria original.

### Palacio bayesiano

![Mapa de creencias del agente bayesiano](docs/images/palacio-bayesiano.png)

### Política del río

![Política calculada mediante Value Iteration](docs/images/politica-rio.png)

### Cómo interpretar los tableros

| Vista | Símbolos principales |
| --- | --- |
| Ambos palacios | `CW`: Willard; `CW+K`: Kurtz ya está rescatado |
| Palacio lógico | `??`: desconocido; `OK`: considerado seguro; `P!` / `S!`: precipicio / soldado confirmados; `P?` / `S?` / `E?`: posibilidades de peligro o salida; `SAL!`: salida deducida |
| Palacio bayesiano | `F`, `P`, `D`, `M`: fuego, pinchos, dardos y militar; `S`: salida probable; `R`: riesgo total. El número expresa un porcentaje estimado: `R16` equivale aproximadamente a un 16 % de riesgo. `OK` indica riesgo estimado inferior al 5 % |
| Río | `CW+K`: embarcación; `####`: isla; `EX`: salida; flechas: acción recomendada; `•`: quedarse |

Cada tablero incluye su propia leyenda. En el palacio bayesiano se muestra un resumen por casilla, no todas sus probabilidades a la vez.

## Ejecutar

Necesitas **Python 3.11 o posterior** y una terminal con soporte UTF-8. NumPy es la única dependencia externa.

```bash
git clone https://github.com/enrcap/kurtz-ai-agents.git
cd kurtz-ai-agents
python -m venv .venv
```

Activa el entorno virtual:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Instala la dependencia y abre el menú:

```bash
python -m pip install -r requirements.txt
python -X utf8 kurtz.py
```

En Windows se recomienda Windows Terminal para visualizar los colores y símbolos de la consola. Si PowerShell impide activar el entorno, puedes ejecutar directamente:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -X utf8 kurtz.py
```

### Menú y controles

- **1 → 1:** palacio lógico en modo manual.
- **1 → 2:** palacio lógico con agente automático BFS.
- **2 → 1 → 1/2:** palacio bayesiano en modo manual o automático con A*.
- **2 → 2:** cruce del río; calcula la política y simula su ejecución.
- **0:** salir del menú principal. **Ctrl+C:** interrumpir la ejecución.

En el modo manual de los palacios, introduce un comando y pulsa **Enter**:

| Comando | Acción |
| --- | --- |
| `w`, `a`, `s`, `d` | Moverse al norte, oeste, sur o este |
| `g` | Lanzar la granada; el programa pregunta después la dirección (`w`, `a`, `s` o `d`). Solo hay una granada por partida |
| `e` | Intentar escapar: debes estar en la salida y haber rescatado a Kurtz |
| `q` | Abandonar la partida y volver al menú |

En automático, los comandos como `gw` o `gd` que aparecen en pantalla representan la decisión del agente de lanzar la granada en una dirección; en manual se utiliza `g` y luego se responde a la pregunta de dirección.

### Primera ejecución recomendada

Para observar el funcionamiento sin tener que elegir cada movimiento:

1. Ejecuta `python -X utf8 kurtz.py`.
2. Selecciona **1** (Agente Lógico) y después **2** (Piloto Automático BFS).
3. Observa cómo cambian las sensaciones, el mapa mental y la decisión impresa en cada turno. La partida puede terminar por victoria, por un peligro o porque el agente quede bloqueado.
4. Al volver al menú, selecciona **2 → 2** para ver el río. Pulsa **Enter** cuando el programa lo solicite: primero calcula y muestra la política y después inicia el cruce.

Para explorar por tu cuenta, usa **1 → 1**. Para observar las probabilidades y el planificador A*, usa **2 → 1 → 2**. Cada nueva partida genera un mapa distinto.

## Organización

```text
kurtz-ai-agents/
├── kurtz.py                 # Menú y punto de entrada
├── palacio_logico.py        # Entorno, base de conocimiento y BFS
├── palacio_bayesiano.py     # Entorno, inferencia bayesiana y A*
├── river_mdp.py             # Modelo del río y Value Iteration
├── utilidades_visuales.py   # Tableros, colores y presentación
├── requirements.txt        # NumPy
└── docs/
    ├── memoria.pdf         # Memoria técnica original
    └── images/             # Capturas de la memoria
```

Cada escenario separa el entorno, el agente o solucionador y el controlador. El entorno mantiene el mapa real; los agentes de los palacios razonan a partir de los perceptos que reciben. Las funciones de presentación se comparten entre los módulos.

## Competencias que demuestra

- Modelado de estados, acciones, perceptos, transiciones y recompensas.
- Implementación de algoritmos de búsqueda con colas y colas de prioridad.
- Actualización de creencias probabilísticas con matrices NumPy.
- Planificación con la ecuación de Bellman y extracción de políticas.
- Diseño modular con clases y visualización de las decisiones del agente.

## Alcance y limitaciones

Es un proyecto académico de simulación. Los mapas se generan aleatoriamente y el resultado varía entre partidas; los agentes de los palacios no tienen garantizado completar cualquier mapa. El agente lógico utiliza reglas específicas del problema, y el agente bayesiano combina los riesgos asumiendo independencia entre amenazas.

El río usa `gamma = 0.9` y `epsilon = 0.001` en la ejecución del menú. La política optimiza el retorno esperado del modelo definido; una trayectoria concreta puede variar por las transiciones aleatorias.

El repositorio no presenta una evaluación estadística de éxito ni una comparación de rendimiento entre agentes. La [memoria técnica](docs/memoria.pdf) describe el modelado, los algoritmos y ejemplos de ejecución. En la memoria se menciona `rio_mdp.py`; el archivo entregado y usado por el programa se llama `river_mdp.py`.

## Contexto académico

Trabajo final de Fundamentos de Inteligencia Artificial, inspirado en *Apocalypse Now*. Esta publicación conserva el código y la memoria entregados y añade documentación para facilitar su revisión y ejecución. La bibliografía y las referencias originales figuran en la memoria.
