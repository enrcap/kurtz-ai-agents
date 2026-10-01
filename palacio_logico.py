"""
Parte 1: El Palacio Lógico
Implementación del entorno y agente basado en lógica proposicional
"""

import random
from collections import deque
from utilidades_visuales import (EstilosConsola, pausar, panel_arcade, imprimir_tablero_arcade,
                                  interpretar_sensaciones_logicas)


class EscenarioPalacio:
    """Representa el palacio de 6x6 con todos sus elementos"""
    
    def __init__(self, dimension=6):
        self.dimension = dimension
        self.posicion_willard = (0, 0)  # Siempre inicia en esquina superior izquierda
        
        # Elementos del palacio
        self.ubicaciones_precipicios = []
        self.ubicacion_militar = None
        self.ubicacion_coronel = None
        self.ubicacion_escape = None
        
        # Estados de misión
        self.coronel_rescatado = False
        self.militar_eliminado = False
        self.partida_finalizada = False
        self.resultado_final = ""
        self.granada_disponible = True
        self.escuchar_grito = False
        
        self._construir_escenario()
    
    def _construir_escenario(self):
        """Genera aleatoriamente las posiciones de todos los elementos"""
        todas_celdas = [(fila, col) for fila in range(self.dimension) 
                        for col in range(self.dimension)]
        # Excluir la posición inicial del capitán
        todas_celdas.remove((0, 0))
        
        random.shuffle(todas_celdas)
        
        # Asignar elementos
        self.ubicaciones_precipicios = [todas_celdas.pop() for _ in range(3)]
        self.ubicacion_militar = todas_celdas.pop()
        self.ubicacion_coronel = todas_celdas.pop()
        self.ubicacion_escape = todas_celdas.pop()
    
    def obtener_sensaciones(self):
        """
        Retorna los perceptos del estado actual
        [Brisa, Ronquido, Resplandor, ParedNorte, ParedEste, ParedSur, ParedOeste, Grito]
        """
        fila, columna = self.posicion_willard
        celdas_vecinas = self._calcular_celdas_adyacentes(fila, columna)
        
        # Detectar brisa (precipicios adyacentes)
        hay_brisa = any(ubicacion in self.ubicaciones_precipicios 
                       for ubicacion in celdas_vecinas)
        
        # Detectar ronquido (militar adyacente y vivo)
        hay_ronquido = False
        if not self.militar_eliminado:
            hay_ronquido = any(ubicacion == self.ubicacion_militar 
                             for ubicacion in celdas_vecinas)
        
        # Detectar resplandor (salida adyacente o en la misma celda)
        zona_resplandor = celdas_vecinas + [(fila, columna)]
        hay_resplandor = any(ubicacion == self.ubicacion_escape 
                           for ubicacion in zona_resplandor)
        
        # Detectar paredes
        en_borde_norte = (fila == 0)
        en_borde_este = (columna == self.dimension - 1)
        en_borde_sur = (fila == self.dimension - 1)
        en_borde_oeste = (columna == 0)
        
        # Grito (se activa una vez después de matar al militar)
        hay_grito = self.escuchar_grito
        self.escuchar_grito = False
        
        return [hay_brisa, hay_ronquido, hay_resplandor, 
                en_borde_norte, en_borde_este, en_borde_sur, en_borde_oeste,
                hay_grito]
    
    def _calcular_celdas_adyacentes(self, fila, columna):
        """Retorna las celdas adyacentes válidas (Manhattan distancia 1)"""
        candidatas = [
            (fila - 1, columna),  # Norte
            (fila + 1, columna),  # Sur
            (fila, columna - 1),  # Oeste
            (fila, columna + 1)   # Este
        ]
        validas = []
        for f, c in candidatas:
            if 0 <= f < self.dimension and 0 <= c < self.dimension:
                validas.append((f, c))
        return validas
    
    def ejecutar_movimiento(self, comando):
        """
        Ejecuta una acción del capitán
        Comandos: 'w'=norte, 's'=sur, 'a'=oeste, 'd'=este, 'e'=escapar, 'g*'=granada
        Retorna: (sensaciones, terminado, mensaje)
        """
        if self.partida_finalizada:
            return self.obtener_sensaciones(), True, self.resultado_final
        
        fila_actual, col_actual = self.posicion_willard
        
        # --- LÓGICA GRANADA ---
        if comando.startswith('g'):
            if not self.granada_disponible:
                return self.obtener_sensaciones(), False, "¡No quedan granadas!"
            
            self.granada_disponible = False
            direccion = comando[1] if len(comando) > 1 else ''
            
            # Calcular objetivo
            fila_objetivo, col_objetivo = fila_actual, col_actual
            if direccion == 'w': fila_objetivo -= 1
            elif direccion == 's': fila_objetivo += 1
            elif direccion == 'a': col_objetivo -= 1
            elif direccion == 'd': col_objetivo += 1
            
            objetivo = (fila_objetivo, col_objetivo)
            
            # Verificar impacto
            if objetivo == self.ubicacion_militar:
                self.militar_eliminado = True
                self.escuchar_grito = True
                return self.obtener_sensaciones(), False, "¡EXPLOSIÓN! Un grito confirma el impacto mortal."
            else:
                return self.obtener_sensaciones(), False, "¡EXPLOSIÓN! Solo escuchas el eco del fracaso."
        
        # --- LÓGICA MOVIMIENTO ---
        nueva_fila, nueva_col = fila_actual, col_actual
        
        if comando == 'w' and fila_actual > 0:
            nueva_fila -= 1
        elif comando == 's' and fila_actual < self.dimension - 1:
            nueva_fila += 1
        elif comando == 'a' and col_actual > 0:
            nueva_col -= 1
        elif comando == 'd' and col_actual < self.dimension - 1:
            nueva_col += 1
        elif comando == 'e':
            # Intentar escapar
            if self.posicion_willard == self.ubicacion_escape:
                if self.coronel_rescatado:
                    self.partida_finalizada = True
                    self.resultado_final = "¡VICTORIA! Has completado la misión con éxito."
                    return self.obtener_sensaciones(), True, self.resultado_final
                else:
                    return self.obtener_sensaciones(), False, "¡Primero debes encontrar a Kurtz!"
            else:
                return self.obtener_sensaciones(), False, "Aquí no hay salida visible."
        
        # Actualizar posición
        self.posicion_willard = (nueva_fila, nueva_col)
        mensaje_accion = "Avanzas con precaución..."
        
        # Verificar muerte
        if self.posicion_willard in self.ubicaciones_precipicios:
            self.partida_finalizada = True
            self.resultado_final = "FRACASO: Caíste en un precipicio mortal."
        elif self.posicion_willard == self.ubicacion_militar and not self.militar_eliminado:
            self.partida_finalizada = True
            self.resultado_final = "FRACASO: El soldado enemigo te ha ejecutado."
        
        # Verificar rescate de Kurtz
        if self.posicion_willard == self.ubicacion_coronel and not self.coronel_rescatado:
            self.coronel_rescatado = True
            mensaje_accion = "¡OBJETIVO ALCANZADO! Has encontrado al Coronel Kurtz."
        
        resultado_mensaje = self.resultado_final if self.partida_finalizada else mensaje_accion
        return self.obtener_sensaciones(), self.partida_finalizada, resultado_mensaje


class CerebroLogico:
    """Agente que usa lógica proposicional para razonar sobre el entorno"""
    
    def __init__(self, dimension=6):
        self.dimension = dimension
        
        # Base de conocimiento
        self.celdas_exploradas = set()
        self.celdas_confirmadas_seguras = set()
        
        # Historial de sensaciones
        self.ubicaciones_con_brisa = set()
        self.ubicaciones_con_ronquido = set()
        self.ubicaciones_con_resplandor = set()
        self.resplandor_detectado = False
        
        # Inferencias sobre peligros
        self.precipicios_posibles = set()
        self.precipicios_confirmados = set()
        self.militar_posible = set()
        self.militar_confirmado = set()
        
        # Inferencias sobre salida
        self.salidas_posibles = set((f, c) for f in range(dimension) 
                                    for c in range(dimension))
        self.salida_confirmada = None
        
        # Estado de misión
        self.kurtz_localizado = False
        self.posicion_kurtz_conocida = None
    
    def procesar_informacion(self, posicion_actual, sensaciones):
        """Actualiza la base de conocimiento con nueva información"""
        fila, columna = posicion_actual
        self.celdas_exploradas.add(posicion_actual)
        self.celdas_confirmadas_seguras.add(posicion_actual)
        
        # Eliminar esta celda de peligros posibles
        self.precipicios_posibles.discard(posicion_actual)
        self.militar_posible.discard(posicion_actual)
        
        # Extraer sensaciones
        brisa, ronquido, resplandor = sensaciones[0], sensaciones[1], sensaciones[2]
        grito = sensaciones[7]
        
        vecinos = self._obtener_vecinos(fila, columna)
        
        # --- RAZONAMIENTO SOBRE SALIDA ---
        zona_influencia_salida = set(vecinos)
        zona_influencia_salida.add(posicion_actual)
        
        if resplandor:
            self.resplandor_detectado = True
            self.ubicaciones_con_resplandor.add(posicion_actual)
            # La salida DEBE estar en esta zona
            self.salidas_posibles &= zona_influencia_salida
        else:
            # La salida NO está en esta zona
            self.salidas_posibles -= zona_influencia_salida
        
        if len(self.salidas_posibles) == 1:
            self.salida_confirmada = list(self.salidas_posibles)[0]
        
        # --- RAZONAMIENTO SOBRE PELIGROS ---
        if grito:
            # Militar eliminado
            self.militar_posible.clear()
            self.militar_confirmado.clear()
        
        if brisa:
            self.ubicaciones_con_brisa.add(posicion_actual)
            for vecino in vecinos:
                if vecino not in self.celdas_confirmadas_seguras:
                    if vecino not in self.precipicios_confirmados:
                        self.precipicios_posibles.add(vecino)
        else:
            # Sin brisa = vecinos libres de precipicios
            for vecino in vecinos:
                self.precipicios_posibles.discard(vecino)
                self.precipicios_confirmados.discard(vecino)
        
        if ronquido and not grito:
            self.ubicaciones_con_ronquido.add(posicion_actual)
            for vecino in vecinos:
                if vecino not in self.celdas_confirmadas_seguras:
                    if vecino not in self.militar_confirmado:
                        self.militar_posible.add(vecino)
        elif not ronquido:
            # Sin ronquido = vecinos libres de militar
            for vecino in vecinos:
                self.militar_posible.discard(vecino)
                self.militar_confirmado.discard(vecino)
        
        # Inferencias avanzadas
        self._deducir_peligros_exactos(self.ubicaciones_con_brisa, 
                                       self.precipicios_confirmados, 
                                       self.precipicios_posibles)
        self._deducir_peligros_exactos(self.ubicaciones_con_ronquido,
                                       self.militar_confirmado,
                                       self.militar_posible)
        self._marcar_celdas_seguras(vecinos, brisa, ronquido)
    
    def _deducir_peligros_exactos(self, ubicaciones_sensacion, confirmados, posibles):
        """Si solo hay un candidato para una sensación, debe ser el culpable"""
        for ubicacion_sensacion in ubicaciones_sensacion:
            f, c = ubicacion_sensacion
            vecinos = self._obtener_vecinos(f, c)
            candidatos = [v for v in vecinos if v not in self.celdas_confirmadas_seguras]
            
            if len(candidatos) == 1:
                culpable = candidatos[0]
                confirmados.add(culpable)
                if culpable in posibles:
                    posibles.remove(culpable)
    
    def _marcar_celdas_seguras(self, vecinos, brisa, ronquido):
        """Si no hay sensaciones de peligro, los vecinos son seguros"""
        if not brisa and not ronquido:
            for vecino in vecinos:
                self.celdas_confirmadas_seguras.add(vecino)
    
    def _obtener_vecinos(self, fila, columna):
        """Retorna vecinos válidos"""
        candidatos = [(fila-1, columna), (fila+1, columna), 
                     (fila, columna-1), (fila, columna+1)]
        return [(f, c) for f, c in candidatos 
                if 0 <= f < self.dimension and 0 <= c < self.dimension]
    
    def decidir_movimiento_automatico(self, posicion_actual, algoritmo="BFS"):
        """
        Decide la siguiente acción usando búsqueda
        Retorna: comando ('w', 'a', 's', 'd', 'e', 'g*', o None)
        """
        # 1. Si hay militar confirmado adyacente, lanzar granada
        vecinos = self._obtener_vecinos(*posicion_actual)
        for vecino in vecinos:
            if vecino in self.militar_confirmado:
                diff_fila = vecino[0] - posicion_actual[0]
                diff_col = vecino[1] - posicion_actual[1]
                
                if diff_fila == -1: return 'gw'
                elif diff_fila == 1: return 'gs'
                elif diff_col == -1: return 'ga'
                elif diff_col == 1: return 'gd'
        
        # 2. Determinar objetivo
        objetivo = None
        if self.kurtz_localizado:
            if self.salida_confirmada:
                objetivo = self.salida_confirmada
        elif self.posicion_kurtz_conocida:
            objetivo = self.posicion_kurtz_conocida
        
        # 3. Ejecutar búsqueda
        siguiente_celda = None
        if algoritmo == "BFS":
            siguiente_celda = self._buscar_amplitud(posicion_actual, objetivo)
        elif algoritmo == "DFS":
            siguiente_celda = self._buscar_profundidad(posicion_actual, objetivo)
        
        # 4. Traducir a comando
        if siguiente_celda:
            if siguiente_celda == posicion_actual:
                if self.kurtz_localizado and posicion_actual == self.salida_confirmada:
                    return 'e'
                return 'e' if (posicion_actual == self.salida_confirmada 
                             and self.kurtz_localizado) else None
            
            diff_fila = siguiente_celda[0] - posicion_actual[0]
            diff_col = siguiente_celda[1] - posicion_actual[1]
            
            if diff_fila == -1: return 'w'
            if diff_fila == 1: return 's'
            if diff_col == -1: return 'a'
            if diff_col == 1: return 'd'
        
        if self.kurtz_localizado and self.salida_confirmada == posicion_actual:
            return 'e'
        
        return None
    
    def _buscar_amplitud(self, inicio, meta):
        """Búsqueda BFS por celdas seguras"""
        cola = deque([(inicio, [])])
        visitados = {inicio}
        
        while len(cola) > 0:
            actual, ruta = cola.popleft()
            
            # Verificar si es meta
            es_objetivo = False
            if meta:
                if actual == meta:
                    es_objetivo = True
            else:
                # Exploración: buscar celda segura no visitada
                if actual not in self.celdas_exploradas and actual in self.celdas_confirmadas_seguras:
                    es_objetivo = True
            
            if es_objetivo:
                if not ruta:
                    return actual
                return ruta[0]
            
            # Expandir
            for vecino in self._obtener_vecinos(*actual):
                if vecino not in visitados:
                    if vecino in self.celdas_confirmadas_seguras:
                        visitados.add(vecino)
                        cola.append((vecino, ruta + [vecino]))
        
        return None
    
    def _buscar_profundidad(self, inicio, meta):
        """Búsqueda DFS por celdas seguras"""
        pila = [(inicio, [])]
        visitados = {inicio}
        
        while len(pila) > 0:
            actual, ruta = pila.pop()
            
            es_objetivo = False
            if meta:
                if actual == meta:
                    es_objetivo = True
            else:
                if actual not in self.celdas_exploradas and actual in self.celdas_confirmadas_seguras:
                    es_objetivo = True
            
            if es_objetivo:
                if not ruta:
                    return actual
                return ruta[0]
            
            for vecino in self._obtener_vecinos(*actual):
                if vecino not in visitados:
                    if vecino in self.celdas_confirmadas_seguras:
                        visitados.add(vecino)
                        pila.append((vecino, ruta + [vecino]))
        
        return None
    
    def visualizar_conocimiento(self, posicion_capitan, tiene_kurtz):
        """Muestra el mapa mental del agente (estilo arcade)."""
        self.kurtz_localizado = tiene_kurtz
        if tiene_kurtz:
            self.posicion_kurtz_conocida = posicion_capitan

        leyenda = [
            f"{EstilosConsola.INFO}👾 LEYENDA{EstilosConsola.RESET}",
            f"{EstilosConsola.CAPITAN}CW{EstilosConsola.RESET} = Willard",
            f"{EstilosConsola.CAPITAN_KURTZ}CW+K{EstilosConsola.RESET} = Willard+Kurtz",
            f"{EstilosConsola.SALIDA}SAL!{EstilosConsola.RESET} = Salida",
            f"{EstilosConsola.TRAMPA}P!{EstilosConsola.RESET} = Precipicio",
            f"{EstilosConsola.SOLDADO}S!{EstilosConsola.RESET} = Soldado",
            f"{EstilosConsola.ADVERTENCIA}P/S/E?{EstilosConsola.RESET} = Sospecha",
            f"{EstilosConsola.SEGURO}OK{EstilosConsola.RESET} = Seguro",
            f"{EstilosConsola.DESCONOCIDO}??{EstilosConsola.RESET} = Desconocido",
            f"{EstilosConsola.MAGENTA}B/R/L{EstilosConsola.RESET} = Recuerdo (Brisa/Ronquido/Luz)",
        ]

        def celda_fn(fila, columna):
            celda = (fila, columna)
            simbolo = "??"
            color = EstilosConsola.DESCONOCIDO

            # 1) Posición del capitán
            if celda == posicion_capitan:
                simbolo = "CW+K" if self.kurtz_localizado else "CW"
                color = EstilosConsola.CAPITAN_KURTZ if self.kurtz_localizado else EstilosConsola.CAPITAN

            # 2) Certezas
            elif self.salida_confirmada == celda:
                simbolo = "SAL!"
                color = EstilosConsola.SALIDA
            elif celda in self.precipicios_confirmados:
                simbolo = "P!"
                color = EstilosConsola.TRAMPA
            elif celda in self.militar_confirmado:
                simbolo = "S!"
                color = EstilosConsola.SOLDADO

            # 3) Incertidumbres
            elif (celda in self.precipicios_posibles or
                  celda in self.militar_posible or
                  (self.resplandor_detectado and celda in self.salidas_posibles)):

                posibilidades = []
                if celda in self.precipicios_posibles: posibilidades.append("P")
                if celda in self.militar_posible: posibilidades.append("S")
                if self.resplandor_detectado and celda in self.salidas_posibles:
                    posibilidades.append("E")

                simbolo = "/".join(posibilidades) + "?"
                color = EstilosConsola.ADVERTENCIA

            # 4) Memoria
            elif celda in self.celdas_exploradas:
                info = []
                if celda in self.ubicaciones_con_brisa: info.append("B")
                if celda in self.ubicaciones_con_ronquido: info.append("R")
                if celda in self.ubicaciones_con_resplandor: info.append("L")

                if not info:
                    simbolo = "OK"
                    color = EstilosConsola.SEGURO
                else:
                    simbolo = "".join(info)
                    color = EstilosConsola.MAGENTA

            # 5) Seguras no exploradas
            elif celda in self.celdas_confirmadas_seguras:
                simbolo = "OK"
                color = EstilosConsola.SEGURO

            return simbolo, color

        imprimir_tablero_arcade(
            self.dimension,
            celda_fn,
            titulo_mapa="🧩 MAPA MENTAL (Deducción lógica)",
            leyenda=leyenda,
            cellw=6,
            ejes=True,
        )

        if self.salida_confirmada:
            print(f"{EstilosConsola.EXITO}🏁 Salida deducida en: {self.salida_confirmada}{EstilosConsola.RESET}\n")
        else:
            print()


class ControladorPalacioLogico:
    """Controlador del juego para la Parte 1"""
    
    def __init__(self, dimension=6, modo="MANUAL"):
        self.escenario = EscenarioPalacio(dimension)
        self.cerebro = CerebroLogico(dimension)
        self.modo = modo
    
    def iniciar_partida(self):
        """Loop principal del juego"""
        activo = True
        turno = 1
        
        while activo:
            #limpiar_pantalla()
            objetivo = "¡Lleva a Kurtz a la salida!" if self.escenario.coronel_rescatado else "Encuentra al Coronel Kurtz"
            estado = f"Turno {turno}  |  Pos {self.escenario.posicion_willard}  |  Granada {'✔' if self.escenario.granada_disponible else '✖'}"
            panel_arcade("PARTE 1 · PALACIO LÓGICO", f"🎯 {objetivo}   ·   {estado}")

            # Obtener estado actual
            sensaciones = self.escenario.obtener_sensaciones()
            
            # Procesar información
            self.cerebro.procesar_informacion(self.escenario.posicion_willard, sensaciones)
            self.cerebro.visualizar_conocimiento(self.escenario.posicion_willard,
                                                 self.escenario.coronel_rescatado)
            
            # Mostrar información
            print(f"{EstilosConsola.INFO}Sensaciones:{EstilosConsola.RESET} {interpretar_sensaciones_logicas(sensaciones)}")
            
            if self.escenario.coronel_rescatado:
                print(f"{EstilosConsola.ADVERTENCIA}>>> OBJETIVO: ¡Lleva a Kurtz a la salida! <<<{EstilosConsola.RESET}")
            else:
                print(f"{EstilosConsola.INFO}>>> OBJETIVO: Encuentra al Coronel Kurtz <<<{EstilosConsola.RESET}")
            
            comando = None
            
            if self.modo == "MANUAL":
                print(f"\n{EstilosConsola.GRIS}[WASD]=Mover [G]=Granada [E]=Salir [Q]=Abandonar{EstilosConsola.RESET}")
                entrada = input(f"{EstilosConsola.ENTRADA}Tu comando: {EstilosConsola.RESET}").lower().strip()
                
                if entrada == 'q':
                    break
                
                if entrada == 'g':
                    if not self.escenario.granada_disponible:
                        print(f"{EstilosConsola.ERROR}¡Sin munición!{EstilosConsola.RESET}")
                        continue
                    direccion = input("Dirección (w/a/s/d): ").strip()
                    if direccion in 'wasd':
                        comando = 'g' + direccion
                elif entrada in 'wasde':
                    comando = entrada
            else:
                print(f"{EstilosConsola.CYAN}El Capitán piensa ({self.modo})...{EstilosConsola.RESET}")
                pausar(0.7)
                
                comando = self.cerebro.decidir_movimiento_automatico(
                    self.escenario.posicion_willard, self.modo)
                
                if comando:
                    print(f"→ Decisión: {EstilosConsola.EXITO}{comando.upper()}{EstilosConsola.RESET}")
                else:
                    print(f"{EstilosConsola.ERROR}¡El Capitán está bloqueado!{EstilosConsola.RESET}")
                    break
            
            # Ejecutar
            if comando:
                _, terminado, mensaje = self.escenario.ejecutar_movimiento(comando)
                print(f"\n{EstilosConsola.BLANCO_BRILLO}» {mensaje} «{EstilosConsola.RESET}\n")
                pausar(0.3)
                
                if terminado:
                    activo = False
                else:
                    turno += 1
                    if "VICTORIA" in mensaje:
                        print(f"\n{EstilosConsola.EXITO}{'='*50}")
                        print("✓ MISIÓN CUMPLIDA ✓".center(50))
                        print(f"{'='*50}{EstilosConsola.RESET}\n")
                    
