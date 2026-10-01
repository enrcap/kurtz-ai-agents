"""
Proyecto: Buscando al Coronel Kurtz
Fundamentos de Inteligencia Artificial
Implementación completa Parte 1 y Parte 2
"""

import sys
import os
from time import sleep
from utilidades_visuales import EstilosConsola #limpiar_pantalla
from palacio_logico import ControladorPalacioLogico
from palacio_bayesiano import ControladorPalacioBayesiano  
from river_mdp import ControladorRioMDP


def mostrar_portada():
    """Muestra la presentación inicial del juego"""
    print(f"\n{EstilosConsola.TITULO}")
    print("=" * 60)
    print("    BUSCANDO AL CORONEL KURTZ".center(60))
    print("    Fundamentos de Inteligencia Artificial".center(60))
    print("=" * 60)
    print(EstilosConsola.RESET)
    print(f"\n{EstilosConsola.SUBTITULO}Misión del Capitán Willard:{EstilosConsola.RESET}")
    print("  1. Infiltrarse en el palacio")
    print("  2. Localizar al Coronel Kurtz")
    print("  3. Escapar con vida\n")


def ejecutar_parte_uno():
    """Ejecuta la Parte 1: Agente Lógico"""
    #limpiar_pantalla()
    print(f"\n{EstilosConsola.TITULO}=== PARTE 1: EL PALACIO DEL TERROR ==={EstilosConsola.RESET}\n")
    
    print("El Capitán Willard debe usar la lógica proposicional")
    print("para deducir la ubicación de trampas y enemigos.\n")
    
    print(f"{EstilosConsola.PREGUNTA}Selecciona el modo de juego:{EstilosConsola.RESET}")
    print(f"  {EstilosConsola.OPCION}[1]{EstilosConsola.RESET} Control Manual (Tú decides cada movimiento)")
    print(f"  {EstilosConsola.OPCION}[2]{EstilosConsola.RESET} Piloto Automático BFS")
    #print(f"  {EstilosConsola.OPCION}[3]{EstilosConsola.RESET} Piloto Automático DFS")
    
    eleccion = input(f"\n{EstilosConsola.ENTRADA}Tu elección: {EstilosConsola.RESET}").strip()
    
    modo_juego = "MANUAL"
    if eleccion == "2":
        modo_juego = "BFS"
    
    controlador = ControladorPalacioLogico(dimension=6, modo=modo_juego)
    controlador.iniciar_partida()


def ejecutar_parte_dos():
    """Ejecuta la Parte 2: Incertidumbre"""
    #limpiar_pantalla()
    print(f"\n{EstilosConsola.TITULO}=== PARTE 2: EL REINO DE LA INCERTIDUMBRE ==={EstilosConsola.RESET}\n")
    
    print("Willard debe adaptarse a nuevos desafíos:")
    print("  • Trampas con estímulos específicos")
    print("  • Inferencia Bayesiana para actualizar creencias")
    print("  • Proceso de Decisión de Markov en el río\n")
    
    print(f"{EstilosConsola.PREGUNTA}Elige tu escenario:{EstilosConsola.RESET}")
    print(f"  {EstilosConsola.OPCION}[1]{EstilosConsola.RESET} Palacio con Inferencia Bayesiana")
    print(f"  {EstilosConsola.OPCION}[2]{EstilosConsola.RESET} Cruce del Río (MDP)")
    
    escenario = input(f"\n{EstilosConsola.ENTRADA}Tu elección: {EstilosConsola.RESET}").strip()
    
    if escenario == "1":
        ejecutar_escenario_bayesiano()
    elif escenario == "2":
        ejecutar_escenario_rio()
    else:
        print(f"{EstilosConsola.ERROR}Opción inválida{EstilosConsola.RESET}")


def ejecutar_escenario_bayesiano():
    """Ejecuta el escenario del palacio con inferencia bayesiana"""
    #limpiar_pantalla()
    print(f"\n{EstilosConsola.SUBTITULO}--- PALACIO BAYESIANO ---{EstilosConsola.RESET}\n")
    
    print(f"{EstilosConsola.PREGUNTA}Modo de control:{EstilosConsola.RESET}")
    print(f"  {EstilosConsola.OPCION}[1]{EstilosConsola.RESET} Manual (Tú interpretas probabilidades)")
    print(f"  {EstilosConsola.OPCION}[2]{EstilosConsola.RESET} Automático (A* con evaluación de riesgo)")
    
    eleccion = input(f"\n{EstilosConsola.ENTRADA}Modo: {EstilosConsola.RESET}").strip()
    
    auto = (eleccion == "2")
    
    controlador = ControladorPalacioBayesiano(dimension=6, automatico=auto)
    controlador.iniciar_partida()


def ejecutar_escenario_rio():
    """Ejecuta el escenario del río con MDP"""
    #limpiar_pantalla()
    print(f"\n{EstilosConsola.SUBTITULO}--- CRUCE DEL RÍO (MDP) ---{EstilosConsola.RESET}\n")
    
    print("El Capitán debe cruzar un río traicionero.")
    print("Usaremos Value Iteration para encontrar la política óptima.\n")
    
    input(f"{EstilosConsola.ENTRADA}Presiona Enter para continuar...{EstilosConsola.RESET}")
    
    controlador = ControladorRioMDP(filas=6, columnas=6)
    controlador.iniciar_simulacion()


def menu_principal():
    """Menú principal del programa"""
    while True:
        mostrar_portada()
        
        print(f"{EstilosConsola.PREGUNTA}Selecciona la parte del proyecto:{EstilosConsola.RESET}")
        print(f"  {EstilosConsola.OPCION}[1]{EstilosConsola.RESET} Parte 1: Agente Lógico")
        print(f"  {EstilosConsola.OPCION}[2]{EstilosConsola.RESET} Parte 2: Incertidumbre")
        print(f"  {EstilosConsola.OPCION}[0]{EstilosConsola.RESET} Salir")
        
        opcion = input(f"\n{EstilosConsola.ENTRADA}Opción: {EstilosConsola.RESET}").strip()
        
        if opcion == "1":
            ejecutar_parte_uno()
        elif opcion == "2":
            ejecutar_parte_dos()
        elif opcion == "0":
            print(f"\n{EstilosConsola.EXITO}¡Hasta pronto, Capitán!{EstilosConsola.RESET}\n")
            break
        else:
            print(f"\n{EstilosConsola.ERROR}Opción no válida{EstilosConsola.RESET}")
            sleep(1)


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(f"\n\n{EstilosConsola.ERROR}Misión abortada.{EstilosConsola.RESET}\n")
        sys.exit(0)
