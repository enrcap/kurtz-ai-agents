"""
Utilidades para visualización en consola
Colores ANSI y funciones de presentación
"""

import os
import sys


class EstilosConsola:
    """Códigos ANSI para colores y estilos"""
    
    # Colores básicos
    RESET = "\033[0m"
    NEGRO = "\033[30m"
    ROJO = "\033[31m"
    VERDE = "\033[32m"
    AMARILLO = "\033[33m"
    AZUL = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    BLANCO = "\033[37m"
    GRIS = "\033[90m"
    
    # Colores brillantes
    ROJO_BRILLO = "\033[91m"
    VERDE_BRILLO = "\033[92m"
    AMARILLO_BRILLO = "\033[93m"
    AZUL_BRILLO = "\033[94m"
    MAGENTA_BRILLO = "\033[95m"
    CYAN_BRILLO = "\033[96m"
    BLANCO_BRILLO = "\033[97m"
    
    # Estilos semánticos
    TITULO = "\033[1;96m"  # Cyan brillante + negrita
    SUBTITULO = "\033[1;95m"  # Magenta brillante + negrita
    PELIGRO = "\033[1;91m"  # Rojo brillante + negrita
    EXITO = "\033[1;92m"  # Verde brillante + negrita
    ADVERTENCIA = "\033[1;93m"  # Amarillo brillante + negrita
    INFO = "\033[1;94m"  # Azul brillante + negrita
    
    # Específicos del juego
    CAPITAN = "\033[1;36m"  # Cyan para Willard
    CAPITAN_KURTZ = "\033[1;33m"  # Amarillo para Willard+Kurtz
    KURTZ = "\033[35m"  # Magenta para Kurtz
    SOLDADO = "\033[31m"  # Rojo para soldado
    SALIDA = "\033[1;37m"  # Blanco brillante para salida
    TRAMPA = "\033[91m"  # Rojo brillante para trampas
    SEGURO = "\033[92m"  # Verde brillante para seguro
    DESCONOCIDO = "\033[90m"  # Gris para desconocido
    
    # Trampas específicas (Parte 2)
    FUEGO = "\033[31m"  # Rojo para fuego
    PINCHOS = "\033[90m"  # Gris oscuro para pinchos
    DARDOS = "\033[35m"  # Magenta para dardos
    
    # Interacción
    ENTRADA = "\033[1;32m"  # Verde brillante para input
    OPCION = "\033[1;33m"  # Amarillo brillante para opciones
    PREGUNTA = "\033[1;96m"  # Cyan brillante para preguntas
    ERROR = "\033[1;91m"  # Rojo brillante para errores

    # Estilos extra (UI arcade)
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    # Fondos (background)
    BG_NEGRO = "\033[40m"
    BG_ROJO = "\033[41m"
    BG_VERDE = "\033[42m"
    BG_AMARILLO = "\033[43m"
    BG_AZUL = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_BLANCO = "\033[47m"
    BG_GRIS = "\033[100m"

    # Combinaciones útiles
    HUD = "\033[1;30;46m"        # Negro sobre fondo cyan (marcadores)
    HUD_WARN = "\033[1;30;43m"   # Negro sobre amarillo
    HUD_DANGER = "\033[1;37;41m" # Blanco sobre rojo



def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    #Finalmente he decidido no utilizar esta función, ya que al hacerlo, aunque se veía mas claro en terminal, se perdía información sobre pasos previos.
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar(segundos=0.5):
    """Pausa la ejecución"""
    from time import sleep
    sleep(segundos)


def dibujar_borde(texto, ancho=60, caracter="="):
    """Dibuja un texto con borde"""
    borde = caracter * ancho
    print(borde)
    print(texto.center(ancho))
    print(borde)


def mostrar_leyenda_parte1():
    """Muestra la leyenda para el mapa de la Parte 1"""
    print(f"\n{EstilosConsola.INFO}LEYENDA DEL MAPA:{EstilosConsola.RESET}")
    print(f"  {EstilosConsola.CAPITAN}[CW]{EstilosConsola.RESET} = Capitán Willard")
    print(f"  {EstilosConsola.CAPITAN_KURTZ}[CW+K]{EstilosConsola.RESET} = Willard con Kurtz")
    print(f"  {EstilosConsola.SALIDA}[SAL!]{EstilosConsola.RESET} = Salida confirmada")
    print(f"  {EstilosConsola.TRAMPA}[P!]{EstilosConsola.RESET} = Precipicio confirmado")
    print(f"  {EstilosConsola.SOLDADO}[S!]{EstilosConsola.RESET} = Soldado confirmado")
    print(f"  {EstilosConsola.ADVERTENCIA}[?]{EstilosConsola.RESET} = Posible peligro")
    print(f"  {EstilosConsola.SEGURO}[OK]{EstilosConsola.RESET} = Zona segura")
    print(f"  {EstilosConsola.DESCONOCIDO}[##]{EstilosConsola.RESET} = Desconocido")
    print()


def mostrar_leyenda_parte2():
    """Muestra la leyenda para el mapa de la Parte 2"""
    print(f"\n{EstilosConsola.INFO}LEYENDA DEL MAPA BAYESIANO:{EstilosConsola.RESET}")
    print(f"  {EstilosConsola.CAPITAN}CW{EstilosConsola.RESET} = Capitán Willard")
    print(f"  {EstilosConsola.CAPITAN_KURTZ}CW+K{EstilosConsola.RESET} = Con Kurtz")
    print(f"  {EstilosConsola.FUEGO}F##{EstilosConsola.RESET} = Prob. Fuego (%)")
    print(f"  {EstilosConsola.PINCHOS}P##{EstilosConsola.RESET} = Prob. Pinchos (%)")
    print(f"  {EstilosConsola.DARDOS}D##{EstilosConsola.RESET} = Prob. Dardos (%)")
    print(f"  {EstilosConsola.SOLDADO}M##{EstilosConsola.RESET} = Prob. Militar (%)")
    print(f"  {EstilosConsola.ADVERTENCIA}R##{EstilosConsola.RESET} = Riesgo total (%)")
    print(f"  {EstilosConsola.SEGURO}OK{EstilosConsola.RESET} = Seguro (<5%)")
    print()


def interpretar_sensaciones_logicas(sensaciones):
    """
    Convierte los perceptos booleanos de Parte 1 en texto legible
    
    Args:
        sensaciones: Lista [Brisa, Ronquido, Resplandor, ParedN, ParedE, ParedS, ParedW, Grito]
    
    Returns:
        String con descripción coloreada
    """
    elementos = []
    
    if sensaciones[0]:  # Brisa
        elementos.append(f"{EstilosConsola.CYAN}Brisa{EstilosConsola.RESET}")
    if sensaciones[1]:  # Ronquido
        elementos.append(f"{EstilosConsola.AMARILLO}Ronquido{EstilosConsola.RESET}")
    if sensaciones[2]:  # Resplandor
        elementos.append(f"{EstilosConsola.BLANCO_BRILLO}Resplandor{EstilosConsola.RESET}")
    if sensaciones[7]:  # Grito
        elementos.append(f"{EstilosConsola.PELIGRO}¡GRITO!{EstilosConsola.RESET}")
    
    # Paredes
    muros = []
    if sensaciones[3]: muros.append("N")
    if sensaciones[4]: muros.append("E")
    if sensaciones[5]: muros.append("S")
    if sensaciones[6]: muros.append("W")
    
    if muros:
        elementos.append(f"{EstilosConsola.GRIS}(Muros: {','.join(muros)}){EstilosConsola.RESET}")
    
    return ", ".join(elementos) if elementos else f"{EstilosConsola.GRIS}Silencio absoluto{EstilosConsola.RESET}"


def interpretar_sensaciones_bayesianas(sensaciones):
    """
    Convierte los perceptos de Parte 2 en texto legible
    
    Args:
        sensaciones: Lista [eF, eP, eD, eM, eS, ParedN, ParedE, ParedS, ParedW, Grito]
    
    Returns:
        String con descripción coloreada
    """
    elementos = []
    
    if sensaciones[0]:  # Estímulo Fuego
        elementos.append(f"{EstilosConsola.FUEGO}Olor a queroseno{EstilosConsola.RESET}")
    if sensaciones[1]:  # Estímulo Pinchos
        elementos.append(f"{EstilosConsola.PINCHOS}Suelo crujiente{EstilosConsola.RESET}")
    if sensaciones[2]:  # Estímulo Dardos
        elementos.append(f"{EstilosConsola.DARDOS}Cables visibles{EstilosConsola.RESET}")
    if sensaciones[3]:  # Estímulo Militar
        elementos.append(f"{EstilosConsola.AMARILLO}Ronquido{EstilosConsola.RESET}")
    if sensaciones[4]:  # Estímulo Salida
        elementos.append(f"{EstilosConsola.BLANCO_BRILLO}Resplandor{EstilosConsola.RESET}")
    if sensaciones[9]:  # Grito
        elementos.append(f"{EstilosConsola.PELIGRO}¡GRITO DE MUERTE!{EstilosConsola.RESET}")
    
    return ", ".join(elementos) if elementos else f"{EstilosConsola.GRIS}Nada destacable{EstilosConsola.RESET}"


# ============================================================
# UI ARCADE
# ============================================================

import re as _re

_ANSI_RE = _re.compile(r"\x1b\[[0-9;]*m")

def soporta_color() -> bool:
    """Detecta si la terminal soporta ANSI y el usuario no ha desactivado colores."""
    return sys.stdout.isatty() and not os.getenv("NO_COLOR")

def _strip_ansi(s: str) -> str:
    return _ANSI_RE.sub("", s)

def panel_arcade(titulo: str, estado: str = "", ancho: int = 76):
    """Panel superior estilo arcade (HUD)."""
    use_color = soporta_color()
    tcol = EstilosConsola.TITULO if use_color else ""
    scol = EstilosConsola.SUBTITULO if use_color else ""
    reset = EstilosConsola.RESET if use_color else ""

    print("╔" + "═"*ancho + "╗")
    print("║" + f"{tcol}🕹️  {titulo}{reset}".center(ancho) + "║")
    if estado:
        print("║" + f"{scol}{estado}{reset}".center(ancho) + "║")
    print("╚" + "═"*ancho + "╝")

def imprimir_tablero_arcade(
    n: int,
    celda_fn,
    titulo_mapa: str = "",
    leyenda: list[str] | None = None,
    cellw: int = 6,
    ejes: bool = True,
):
    """Renderiza una rejilla con bordes y leyenda lateral."""
    use_color = soporta_color()
    RESET = EstilosConsola.RESET if use_color else ""

    if titulo_mapa:
        col = EstilosConsola.INFO if use_color else ""
        print(f"\n{col}{titulo_mapa}{RESET}\n")

    ley = leyenda or []
    if not use_color:
        ley = [_strip_ansi(x) for x in ley]
    def ley_line(i: int) -> str:
        return ley[i] if i < len(ley) else ""

    # Eje X
    if ejes:
        header = "    " + "".join(f"{c:^{cellw}}" for c in range(n))
        # La leyenda se imprime SOLO en líneas "de contenido" (cabecera,
        # borde superior, filas, borde inferior). Si la imprimimos también en las líneas
        # separadoras (mid), se duplican entradas (mismo índice cae en separador y fila).
        print(header + ("   " + ley_line(0) if ley else ""))

    top = "   ┏" + "┳".join(["━"*cellw]*n) + "┓"
    mid = "   ┣" + "╋".join(["━"*cellw]*n) + "┫"
    bot = "   ┗" + "┻".join(["━"*cellw]*n) + "┛"

    print(top + ("   " + ley_line(1) if ley else ""))

    for f in range(n):
        pref = f"{f:>2} ┃" if ejes else "   ┃"
        row = pref
        for c in range(n):
            tok, col = celda_fn(f, c)
            tok = str(tok)
            tok = tok[:cellw].center(cellw)
            col = col if use_color else ""
            row += f"{col}{tok}{RESET}┃"
        extra = "   " + ley_line(f+2) if ley else ""
        print(row + extra)

        if f != n-1:
            # Sin leyenda en separadores para evitar duplicados.
            print(mid)

    # Última línea de leyenda (si existe)
    print(bot + ("   " + ley_line(n+2) if ley else ""))
    print()



def imprimir_tablero_arcade_rc(
    filas: int,
    columnas: int,
    celda_fn,
    titulo_mapa: str = "",
    leyenda: list[str] | None = None,
    cellw: int = 6,
    ejes: bool = True,
):
    """Versión rectangular (filas x columnas) del renderer arcade."""
    use_color = soporta_color()
    RESET = EstilosConsola.RESET if use_color else ""

    if titulo_mapa:
        col = EstilosConsola.INFO if use_color else ""
        print(f"\n{col}{titulo_mapa}{RESET}\n")

    ley = leyenda or []
    if not use_color:
        ley = [_strip_ansi(x) for x in ley]
    def ley_line(i: int) -> str:
        return ley[i] if i < len(ley) else ""

    if ejes:
        header = "    " + "".join(f"{c:^{cellw}}" for c in range(columnas))
        # Misma estrategia que en la versión cuadrada: no imprimir leyenda en separadores.
        print(header + ("   " + ley_line(0) if ley else ""))

    top = "   ┏" + "┳".join(["━"*cellw]*columnas) + "┓"
    mid = "   ┣" + "╋".join(["━"*cellw]*columnas) + "┫"
    bot = "   ┗" + "┻".join(["━"*cellw]*columnas) + "┛"

    print(top + ("   " + ley_line(1) if ley else ""))

    for f in range(filas):
        pref = f"{f:>2} ┃" if ejes else "   ┃"
        row = pref
        for c in range(columnas):
            tok, col = celda_fn(f, c)
            tok = str(tok)[:cellw].center(cellw)
            col = col if use_color else ""
            row += f"{col}{tok}{RESET}┃"
        extra = "   " + ley_line(f+2) if ley else ""
        print(row + extra)

        if f != filas - 1:
            print(mid)

    print(bot + ("   " + ley_line(filas+2) if ley else ""))
    print()
_BLOQUES = "░▒▓█"

def bloque_prob(p: float) -> str:
    """Mapea 0..1 a un bloque ░▒▓█ (arcade heatmap)."""
    if p <= 0:
        return _BLOQUES[0]
    if p >= 1:
        return _BLOQUES[-1]
    return _BLOQUES[min(3, int(p * 4))]

_BARRA = "▁▂▃▄▅▆▇█"

def barra_corriente(x: float) -> str:
    """Normaliza 0..1 a ▁▂▃▄▅▆▇█."""
    x = max(0.0, min(1.0, float(x)))
    return _BARRA[min(7, int(x * 8))]
