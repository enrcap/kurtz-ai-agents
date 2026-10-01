"""
Parte 2.2: Cruce del Río
Implementación de MDP y Value Iteration
"""

import random
import numpy as np
from time import sleep
from utilidades_visuales import EstilosConsola, panel_arcade, imprimir_tablero_arcade_rc, barra_corriente


class EscenarioRio:
    """
    Representa el río como un MDP estocástico
    con corrientes, islas y una salida
    """
    
    def __init__(self, filas=6, columnas=6):
        self.filas = filas
        self.columnas = columnas
        self.posicion_inicio = (0, 0)
        self.posicion_salida = None
        self.islas = []
        self.fuerzas_corriente = np.zeros(columnas)
        
        self._generar_rio()
    
    def _generar_rio(self):
        """Genera el río con islas, salida y corrientes aleatorias"""
        # 1. Salida en la última columna (orilla derecha)
        fila_salida = random.randint(1, self.filas - 2)
        self.posicion_salida = (fila_salida, self.columnas - 1)
        
        # 2. Fuerzas de corriente por columna
        for col in range(self.columnas):
            if col == 0 or col == self.columnas - 1:
                # Orillas sin corriente
                self.fuerzas_corriente[col] = 0.0
            else:
                # Columnas interiores: fuerza aleatoria [0.06, 0.94]
                self.fuerzas_corriente[col] = round(random.uniform(0.06, 0.94), 2)
        
        # 3. Generar 2 islas
        # No en primera/última fila, no superpuestas, no en inicio/salida
        posibles = []
        for f in range(1, self.filas - 1):
            for c in range(1, self.columnas - 1):
                if (f, c) != self.posicion_inicio and (f, c) != self.posicion_salida:
                    posibles.append((f, c))
        
        if len(posibles) >= 2:
            self.islas = random.sample(posibles, 2)
        else:
            self.islas = []
    
    def obtener_estados(self):
        """Retorna todos los estados posibles"""
        return [(f, c) for f in range(self.filas) for c in range(self.columnas)]
    
    def obtener_acciones(self):
        """Retorna todas las acciones posibles"""
        return ['up', 'down', 'left', 'right', 'stay']
    
    def obtener_transiciones(self, estado, accion):
        """
        Calcula las transiciones estocásticas desde un estado dada una acción.
        
        Retorna: lista de tuplas (probabilidad, estado_siguiente, recompensa)
        
        Física del río:
        - Si accion == 'down': P(ir hacia abajo) = 1.0 (la corriente ayuda)
        - Si accion != 'down': 
            P(dirección deseada) = 1 - river_strength
            P(arrastrado al sur) = river_strength
        """
        if estado == self.posicion_salida:
            # Estado terminal
            return []
        
        fila, columna = estado
        fuerza = self.fuerzas_corriente[columna]
        transiciones = []
        
        def obtener_destino_valido(f_objetivo, c_objetivo):
            """Verifica límites e islas. Si inválido, devuelve estado actual (rebote)"""
            if not (0 <= f_objetivo < self.filas and 0 <= c_objetivo < self.columnas):
                return estado
            if (f_objetivo, c_objetivo) in self.islas:
                return estado
            return (f_objetivo, c_objetivo)
        
        # --- CASO 1: Acción DOWN ---
        if accion == 'down':
            destino = obtener_destino_valido(fila + 1, columna)
            recompensa = 100 if destino == self.posicion_salida else -1
            transiciones.append((1.0, destino, recompensa))
        
        # --- CASO 2: Acción STAY ---
        elif accion == 'stay':
            # Intenta quedarse pero la corriente puede arrastrar
            destino_intentado = estado
            destino_deriva = obtener_destino_valido(fila + 1, columna)
            
            p_quedarse = 1.0 - fuerza
            p_deriva = fuerza
            
            rew_quedarse = -1
            rew_deriva = 100 if destino_deriva == self.posicion_salida else -1
            
            if p_quedarse > 0:
                transiciones.append((p_quedarse, destino_intentado, rew_quedarse))
            if p_deriva > 0:
                transiciones.append((p_deriva, destino_deriva, rew_deriva))
        
        # --- CASO 3: Acciones UP, LEFT, RIGHT ---
        else:
            # Calcular destino deseado
            f_destino, c_destino = fila, columna
            if accion == 'up':
                f_destino -= 1
            elif accion == 'left':
                c_destino -= 1
            elif accion == 'right':
                c_destino += 1
            
            destino_deseado = obtener_destino_valido(f_destino, c_destino)
            destino_deriva = obtener_destino_valido(fila + 1, columna)
            
            p_deseado = 1.0 - fuerza
            p_deriva = fuerza
            
            rew_deseado = 100 if destino_deseado == self.posicion_salida else -1
            rew_deriva = 100 if destino_deriva == self.posicion_salida else -1
            
            if p_deseado > 0:
                transiciones.append((p_deseado, destino_deseado, rew_deseado))
            if p_deriva > 0:
                transiciones.append((p_deriva, destino_deriva, rew_deriva))
        
        return transiciones
    
    def visualizar_rio(self, posicion_agente=None):
        """Muestra el mapa del río en consola (estilo arcade)."""
        # HUD de corriente
        maxf = max(float(x) for x in self.fuerzas_corriente) if len(self.fuerzas_corriente) else 1.0
        maxf = max(maxf, 0.01)
        barras = " ".join(barra_corriente(float(x) / maxf) for x in self.fuerzas_corriente)
        nums = " ".join(f"{float(x):.2f}" for x in self.fuerzas_corriente)

        print(f"{EstilosConsola.INFO}🌊 Corriente:{EstilosConsola.RESET} {barras}")
        print(f"{EstilosConsola.GRIS}   Fuerza:   {nums}{EstilosConsola.RESET}")

        leyenda = [
            f"{EstilosConsola.INFO}👾 LEYENDA{EstilosConsola.RESET}",
            f"{EstilosConsola.CAPITAN_KURTZ}CW+K{EstilosConsola.RESET} = Embarcación",
            f"{EstilosConsola.SALIDA}EX{EstilosConsola.RESET} = Salida",
            f"{EstilosConsola.GRIS}####{EstilosConsola.RESET} = Isla",
            f"{EstilosConsola.CYAN}~~~~{EstilosConsola.RESET} = Agua",
        ]

        def celda_fn(f, c):
            celda = (f, c)
            if celda == posicion_agente:
                return "CW+K", EstilosConsola.CAPITAN_KURTZ
            if celda == self.posicion_salida:
                return "EX", EstilosConsola.SALIDA
            if celda in self.islas:
                return "####", EstilosConsola.GRIS
            return "~~~~", EstilosConsola.CYAN

        imprimir_tablero_arcade_rc(
            self.filas,
            self.columnas,
            celda_fn,
            titulo_mapa="🌊 MAPA DEL RÍO",
            leyenda=leyenda,
            cellw=6,
            ejes=True,
        )


class SolucionadorMDP:
    """
    Implementa Value Iteration para resolver el MDP del río
    """
    
    def __init__(self, entorno_mdp):
        self.mdp = entorno_mdp
        self.valores = {}  # V(s)
        self.politica = {}  # π(s) -> mejor acción
        
        # Inicializar
        for estado in self.mdp.obtener_estados():
            self.valores[estado] = 0.0
            self.politica[estado] = 'stay'
    
    def iterar_valores(self, gamma=0.9, epsilon=0.001):
        """
        Ejecuta Value Iteration hasta convergencia
        
        Ecuación de Bellman:
        V(s) = max_a Σ P(s'|s,a) * [R(s,a,s') + γ * V(s')]
        """
        estados = self.mdp.obtener_estados()
        acciones = self.mdp.obtener_acciones()
        
        iteracion = 0
        
        while True:
            delta_maximo = 0
            nuevos_valores = self.valores.copy()
            
            for estado in estados:
                if estado == self.mdp.posicion_salida:
                    # Estado terminal
                    nuevos_valores[estado] = 0.0
                    continue
                
                # Calcular Q-values para todas las acciones
                valores_acciones = []
                
                for accion in acciones:
                    q_valor = 0
                    transiciones = self.mdp.obtener_transiciones(estado, accion)
                    
                    for (probabilidad, estado_siguiente, recompensa) in transiciones:
                        # Ecuación de Bellman
                        q_valor += probabilidad * (recompensa + gamma * self.valores[estado_siguiente])
                    
                    valores_acciones.append(q_valor)
                
                # Actualizar con el máximo
                mejor_valor = max(valores_acciones)
                delta_maximo = max(delta_maximo, abs(mejor_valor - self.valores[estado]))
                nuevos_valores[estado] = mejor_valor
            
            self.valores = nuevos_valores
            iteracion += 1
            
            # Condición de parada
            if delta_maximo < epsilon:
                print(f"{EstilosConsola.EXITO}Value Iteration convergió en {iteracion} iteraciones.{EstilosConsola.RESET}")
                break
        
        # Extraer política óptima
        self._extraer_politica(gamma)
    
    def _extraer_politica(self, gamma):
        """Extrae la mejor acción para cada estado basándose en V(s)"""
        estados = self.mdp.obtener_estados()
        acciones = self.mdp.obtener_acciones()
        
        for estado in estados:
            if estado == self.mdp.posicion_salida:
                self.politica[estado] = 'EXIT'
                continue
            
            mejor_accion = None
            mejor_q = -float('inf')
            
            for accion in acciones:
                q_valor = 0
                transiciones = self.mdp.obtener_transiciones(estado, accion)
                
                for (prob, siguiente, rew) in transiciones:
                    q_valor += prob * (rew + gamma * self.valores[siguiente])
                
                if q_valor > mejor_q:
                    mejor_q = q_valor
                    mejor_accion = accion
            
            self.politica[estado] = mejor_accion
    
    def obtener_mejor_accion(self, estado):
        """Retorna la mejor acción según la política calculada"""
        return self.politica.get(estado, 'stay')
    
    def visualizar_politica(self):
        """Muestra la política óptima en el mapa (estilo arcade)."""
        leyenda = [
            f"{EstilosConsola.INFO}👾 LEYENDA{EstilosConsola.RESET}",
            f"{EstilosConsola.SALIDA}EX{EstilosConsola.RESET} = Salida",
            f"{EstilosConsola.GRIS}####{EstilosConsola.RESET} = Isla",
            f"{EstilosConsola.CYAN}↑ ↓ ← → •{EstilosConsola.RESET} = Acción",
        ]

        def celda_fn(f, c):
            estado = (f, c)
            if estado == self.mdp.posicion_salida:
                return "EX", EstilosConsola.SALIDA
            if estado in self.mdp.islas:
                return "####", EstilosConsola.GRIS

            accion = self.politica.get(estado, 'stay')
            if accion == 'up':
                simbolo = "↑"
            elif accion == 'down':
                simbolo = "↓"
            elif accion == 'left':
                simbolo = "←"
            elif accion == 'right':
                simbolo = "→"
            else:
                simbolo = "•"

            return simbolo, EstilosConsola.CYAN

        imprimir_tablero_arcade_rc(
            self.mdp.filas,
            self.mdp.columnas,
            celda_fn,
            titulo_mapa="🧠 POLÍTICA ÓPTIMA (Value Iteration)",
            leyenda=leyenda,
            cellw=6,
            ejes=True,
        )


class ControladorRioMDP:
    """Controlador de la simulación del río"""
    
    def __init__(self, filas=6, columnas=6):
        self.rio = EscenarioRio(filas, columnas)
        self.solucionador = SolucionadorMDP(self.rio)
    
    def iniciar_simulacion(self):
        """Ejecuta la simulación completa"""
        #limpiar_pantalla()
        panel_arcade("PARTE 2.2 · CRUCE DEL RÍO (MDP)", "🌊 Corrientes estocásticas · 🧠 Value Iteration")

        # 1. Mostrar río
        self.rio.visualizar_rio(self.rio.posicion_inicio)
        
        # 2. Resolver MDP
        print(f"\n{EstilosConsola.ADVERTENCIA}Calculando política óptima...{EstilosConsola.RESET}")
        sleep(1)
        self.solucionador.iterar_valores(gamma=0.9, epsilon=0.001)
        
        # 3. Mostrar política
        #limpiar_pantalla()
        panel_arcade("PARTE 2.2 · CRUCE DEL RÍO (MDP)", "🧠 Política óptima calculada")
        self.solucionador.visualizar_politica()
        
        # 4. Simular partida
        print(f"\n{EstilosConsola.TITULO}--- INICIANDO CRUCE DEL RÍO ---{EstilosConsola.RESET}")
        input(f"{EstilosConsola.ENTRADA}Presiona Enter para comenzar...{EstilosConsola.RESET}")
        
        self._simular_cruce()
    
    def _simular_cruce(self):
        """Simula el cruce del río siguiendo la política óptima"""
        estado_actual = self.rio.posicion_inicio
        pasos = 0
        recompensa_acumulada = 0
        max_pasos = 50
        
        while estado_actual != self.rio.posicion_salida and pasos < max_pasos:
            # Limpiar y mostrar estado
            #limpiar_pantalla()
            print(f"\n{EstilosConsola.INFO}Paso: {pasos} | Recompensa acumulada: {recompensa_acumulada}{EstilosConsola.RESET}")
            self.rio.visualizar_rio(estado_actual)
            
            # Decidir acción
            accion = self.solucionador.obtener_mejor_accion(estado_actual)
            print(f"{EstilosConsola.CYAN}El Capitán decide: {accion.upper()}{EstilosConsola.RESET}")
            
            sleep(0.8)
            
            # Ejecutar transición estocástica
            transiciones = self.rio.obtener_transiciones(estado_actual, accion)
            
            # Seleccionar resultado según probabilidades
            probs = [t[0] for t in transiciones]
            idx_elegido = np.random.choice(len(transiciones), p=probs)
            
            prob_elegida, estado_siguiente, recompensa = transiciones[idx_elegido]
            
            # Feedback narrativo
            if estado_siguiente != estado_actual:
                if estado_siguiente[0] > estado_actual[0] and accion != 'down':
                    print(f"{EstilosConsola.ADVERTENCIA}¡La corriente arrastra el bote hacia el sur!{EstilosConsola.RESET}")
                elif estado_siguiente == estado_actual:
                    print(f"{EstilosConsola.GRIS}El bote rebota contra un obstáculo.{EstilosConsola.RESET}")
            
            estado_actual = estado_siguiente
            recompensa_acumulada += recompensa
            pasos += 1
            
            sleep(0.6)
        
        # Resultado final
        #limpiar_pantalla()
        self.rio.visualizar_rio(estado_actual)
        
        if estado_actual == self.rio.posicion_salida:
            print(f"\n{EstilosConsola.EXITO}{'='*60}")
            print("✓ ¡ÉXITO! Willard y Kurtz han cruzado el río".center(60))
            print(f"{'='*60}{EstilosConsola.RESET}")
            print(f"\n{EstilosConsola.INFO}Pasos totales: {pasos}")
            print(f"Recompensa final: {recompensa_acumulada}{EstilosConsola.RESET}\n")
        else:
            print(f"\n{EstilosConsola.PELIGRO}{'='*60}")
            print("✗ FRACASO: El tiempo se agotó".center(60))
            print(f"{'='*60}{EstilosConsola.RESET}\n")
