"""
Parte 2.1: Palacio Bayesiano
Implementación con trampas específicas e inferencia bayesiana
"""

import random
import numpy as np
import heapq
from utilidades_visuales import (EstilosConsola, pausar, panel_arcade, imprimir_tablero_arcade,
                                  interpretar_sensaciones_bayesianas, bloque_prob)


class EscenarioPalacioBayesiano:
    """Palacio con trampas específicas: Fuego, Pinchos, Dardos"""
    
    def __init__(self, dimension=6):
        self.dimension = dimension
        self.posicion_willard = (0, 0)
        
        # Elementos específicos
        self.ubicacion_trampa_fuego = None
        self.ubicacion_trampa_pinchos = None
        self.ubicacion_trampa_dardos = None
        self.ubicacion_militar = None
        self.ubicacion_coronel = None
        self.ubicacion_escape = None
        
        # Estados
        self.coronel_rescatado = False
        self.militar_eliminado = False
        self.partida_finalizada = False
        self.resultado_final = ""
        self.granada_disponible = True
        self.escuchar_grito = False
        
        self._construir_escenario()
    
    def _construir_escenario(self):
        """
        Genera el escenario aleatorio:
        - Trampas (F, P, D) pueden coincidir entre sí
        - Militar, Kurtz y Salida no están en trampas pero pueden coincidir entre ellos
        """
        todas = [(f, c) for f in range(self.dimension) for c in range(self.dimension)]
        todas.remove((0, 0))
        
        # 1. Colocar trampas (pueden solaparse)
        self.ubicacion_trampa_fuego = random.choice(todas)
        self.ubicacion_trampa_pinchos = random.choice(todas)
        self.ubicacion_trampa_dardos = random.choice(todas)
        
        # 2. Identificar celdas con trampas
        celdas_con_trampas = {self.ubicacion_trampa_fuego, 
                             self.ubicacion_trampa_pinchos,
                             self.ubicacion_trampa_dardos}
        
        # 3. Celdas limpias para NPCs
        celdas_limpias = [pos for pos in todas if pos not in celdas_con_trampas]
        
        if len(celdas_limpias) < 1:
            # Muy improbable, pero regeneramos
            self._construir_escenario()
            return
        
        # 4. Colocar Militar, Kurtz y Salida (pueden coincidir entre ellos)
        self.ubicacion_militar = random.choice(celdas_limpias)
        self.ubicacion_coronel = random.choice(celdas_limpias)
        self.ubicacion_escape = random.choice(celdas_limpias)
    
    def obtener_sensaciones(self):
        """
        Retorna: [eF, eP, eD, eM, eS, ParedN, ParedE, ParedS, ParedO, Grito]
        """
        fila, columna = self.posicion_willard
        vecinos = self._calcular_vecinos(fila, columna)
        zona_completa = vecinos + [(fila, columna)]
        
        # Estímulos de trampas (se sienten en vecinos + propia celda)
        estimulo_fuego = any(pos == self.ubicacion_trampa_fuego for pos in zona_completa)
        estimulo_pinchos = any(pos == self.ubicacion_trampa_pinchos for pos in zona_completa)
        estimulo_dardos = any(pos == self.ubicacion_trampa_dardos for pos in zona_completa)
        
        # Estímulo militar
        estimulo_militar = False
        if not self.militar_eliminado:
            estimulo_militar = any(pos == self.ubicacion_militar for pos in zona_completa)
        
        # Estímulo salida
        estimulo_salida = any(pos == self.ubicacion_escape for pos in zona_completa)
        
        # Paredes
        pared_norte = (fila == 0)
        pared_este = (columna == self.dimension - 1)
        pared_sur = (fila == self.dimension - 1)
        pared_oeste = (columna == 0)
        
        # Grito
        hay_grito = self.escuchar_grito
        self.escuchar_grito = False
        
        return [estimulo_fuego, estimulo_pinchos, estimulo_dardos,
                estimulo_militar, estimulo_salida,
                pared_norte, pared_este, pared_sur, pared_oeste,
                hay_grito]
    
    def _calcular_vecinos(self, fila, columna):
        """Vecinos adyacentes válidos"""
        candidatos = [(fila-1, columna), (fila+1, columna),
                     (fila, columna-1), (fila, columna+1)]
        return [(f, c) for f, c in candidatos 
                if 0 <= f < self.dimension and 0 <= c < self.dimension]
    
    def ejecutar_movimiento(self, comando):
        """Ejecuta acción del capitán"""
        if self.partida_finalizada:
            return self.obtener_sensaciones(), True, self.resultado_final
        
        fila_actual, col_actual = self.posicion_willard
        
        # --- GRANADA ---
        if comando.startswith('g'):
            if not self.granada_disponible:
                return self.obtener_sensaciones(), False, "¡Sin munición!"
            
            self.granada_disponible = False
            direccion = comando[1] if len(comando) > 1 else ''
            
            fila_obj, col_obj = fila_actual, col_actual
            if direccion == 'w': fila_obj -= 1
            elif direccion == 's': fila_obj += 1
            elif direccion == 'a': col_obj -= 1
            elif direccion == 'd': col_obj += 1
            
            objetivo = (fila_obj, col_obj)
            
            if objetivo == self.ubicacion_militar:
                self.militar_eliminado = True
                self.escuchar_grito = True
                return self.obtener_sensaciones(), False, "¡IMPACTO! El soldado ha sido neutralizado."
            else:
                return self.obtener_sensaciones(), False, "¡EXPLOSIÓN! Has fallado el objetivo."
        
        # --- MOVIMIENTO ---
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
            if self.posicion_willard == self.ubicacion_escape:
                if self.coronel_rescatado:
                    self.partida_finalizada = True
                    self.resultado_final = "¡VICTORIA! Misión completada con Kurtz a salvo."
                    return self.obtener_sensaciones(), True, self.resultado_final
                else:
                    return self.obtener_sensaciones(), False, "¡Primero rescata a Kurtz!"
            else:
                return self.obtener_sensaciones(), False, "No hay salida aquí."
        
        # Actualizar posición
        self.posicion_willard = (nueva_fila, nueva_col)
        mensaje = "Avanzas cautelosamente..."
        
        # Verificar muertes
        causas_muerte = []
        if self.posicion_willard == self.ubicacion_trampa_fuego:
            causas_muerte.append("QUEMADO por trampa de fuego")
        if self.posicion_willard == self.ubicacion_trampa_pinchos:
            causas_muerte.append("EMPALADO por pinchos")
        if self.posicion_willard == self.ubicacion_trampa_dardos:
            causas_muerte.append("ENVENENADO por dardos")
        if self.posicion_willard == self.ubicacion_militar and not self.militar_eliminado:
            causas_muerte.append("EJECUTADO por el soldado")
        
        if causas_muerte:
            self.partida_finalizada = True
            self.resultado_final = f"FRACASO: {' + '.join(causas_muerte)}"
            return self.obtener_sensaciones(), True, self.resultado_final
        
        # Verificar rescate
        if self.posicion_willard == self.ubicacion_coronel and not self.coronel_rescatado:
            self.coronel_rescatado = True
            mensaje = "¡OBJETIVO! Has encontrado al Coronel Kurtz."
        
        return self.obtener_sensaciones(), False, mensaje


class MotorInferenciaBayesiana:
    """Agente que usa inferencia bayesiana para actualizar creencias"""
    
    def __init__(self, dimension=6):
        self.dimension = dimension
        
        # Prior uniforme: 1/(N-1) excluyendo la celda inicial
        probabilidad_inicial = 1.0 / ((dimension * dimension) - 1)
        
        # Matrices de probabilidad para cada elemento
        self.prob_fuego = np.full((dimension, dimension), probabilidad_inicial)
        self.prob_pinchos = np.full((dimension, dimension), probabilidad_inicial)
        self.prob_dardos = np.full((dimension, dimension), probabilidad_inicial)
        self.prob_militar = np.full((dimension, dimension), probabilidad_inicial)
        self.prob_salida = np.full((dimension, dimension), probabilidad_inicial)
        
        # La celda (0,0) es segura inicialmente
        for matriz in [self.prob_fuego, self.prob_pinchos, self.prob_dardos,
                      self.prob_militar, self.prob_salida]:
            matriz[0, 0] = 0.0
        
        # Estado
        self.kurtz_localizado = False
        self.celdas_exploradas = set()
    
    def actualizar_probabilidades(self, posicion_actual, sensaciones):
        """Actualiza todas las distribuciones usando el teorema de Bayes"""
        self.celdas_exploradas.add(posicion_actual)
        
        estimulo_fuego = sensaciones[0]
        estimulo_pinchos = sensaciones[1]
        estimulo_dardos = sensaciones[2]
        estimulo_militar = sensaciones[3]
        estimulo_salida = sensaciones[4]
        grito = sensaciones[9]
        
        # 1. Actualizar militar
        if grito:
            self.prob_militar = np.zeros((self.dimension, self.dimension))
        else:
            self._aplicar_regla_bayes(self.prob_militar, posicion_actual, estimulo_militar)
        
        # 2. Actualizar trampas
        self._aplicar_regla_bayes(self.prob_fuego, posicion_actual, estimulo_fuego)
        self._aplicar_regla_bayes(self.prob_pinchos, posicion_actual, estimulo_pinchos)
        self._aplicar_regla_bayes(self.prob_dardos, posicion_actual, estimulo_dardos)
        
        # 3. Actualizar salida
        self._aplicar_regla_bayes(self.prob_salida, posicion_actual, estimulo_salida)
        
        # 4. Evidencia implícita: estamos vivos en esta celda
        fila, columna = posicion_actual
        self.prob_fuego[fila, columna] = 0
        self.prob_pinchos[fila, columna] = 0
        self.prob_dardos[fila, columna] = 0
        if not grito:
            self.prob_militar[fila, columna] = 0
        
        # 5. Normalizar
        self._normalizar_distribucion(self.prob_fuego)
        self._normalizar_distribucion(self.prob_pinchos)
        self._normalizar_distribucion(self.prob_dardos)
        if not grito:
            self._normalizar_distribucion(self.prob_militar)
        self._normalizar_distribucion(self.prob_salida)
    
    def _aplicar_regla_bayes(self, matriz_prob, posicion_observador, percibe_estimulo):
        """
        P(Elemento_ij | Evidencia) = α * P(Evidencia | Elemento_ij) * P(Elemento_ij)
        
        Modelo determinista:
        - Si percibimos estímulo: P(estímulo | elemento_ij) = 1 si ij en zona, 0 si no
        - Si NO percibimos: P(¬estímulo | elemento_ij) = 0 si ij en zona, 1 si no
        """
        fila, columna = posicion_observador
        zona_influencia = self._obtener_zona_influencia(fila, columna)
        
        for i in range(self.dimension):
            for j in range(self.dimension):
                esta_en_zona = (i, j) in zona_influencia
                
                if percibe_estimulo:
                    # Solo las celdas en la zona pueden ser culpables
                    verosimilitud = 1.0 if esta_en_zona else 0.0
                else:
                    # Las celdas en la zona NO pueden ser culpables
                    verosimilitud = 0.0 if esta_en_zona else 1.0
                
                matriz_prob[i, j] *= verosimilitud
    
    def _normalizar_distribucion(self, matriz):
        """Normaliza para que sume 1"""
        suma_total = np.sum(matriz)
        if suma_total > 0:
            matriz /= suma_total
    
    def _obtener_zona_influencia(self, fila, columna):
        """Retorna vecinos + celda propia"""
        vecinos = self._obtener_vecinos(fila, columna)
        vecinos.append((fila, columna))
        return vecinos
    
    def _obtener_vecinos(self, fila, columna):
        """Vecinos adyacentes"""
        candidatos = [(fila-1, columna), (fila+1, columna),
                     (fila, columna-1), (fila, columna+1)]
        return [(f, c) for f, c in candidatos
                if 0 <= f < self.dimension and 0 <= c < self.dimension]
    
    def calcular_riesgo_total(self, fila, columna):
        """Calcula P(muerte) en una celda"""
        pf = self.prob_fuego[fila, columna]
        pp = self.prob_pinchos[fila, columna]
        pd = self.prob_dardos[fila, columna]
        pm = self.prob_militar[fila, columna]
        
        # Asumiendo independencia: P(vivir) = (1-pf)*(1-pp)*(1-pd)*(1-pm)
        prob_sobrevivir = (1 - pf) * (1 - pp) * (1 - pd) * (1 - pm)
        return 1.0 - prob_sobrevivir
    
    def decidir_movimiento_automatico(self, posicion_actual):
        """
        Decide acción basada en riesgos usando A*
        """
        # 1. Amenaza inmediata de militar
        vecinos = self._obtener_vecinos(*posicion_actual)
        for vecino in vecinos:
            if self.prob_militar[vecino] > 0.5:
                diff_fila = vecino[0] - posicion_actual[0]
                diff_col = vecino[1] - posicion_actual[1]
                
                if diff_fila == -1: return 'gw'
                if diff_fila == 1: return 'gs'
                if diff_col == -1: return 'ga'
                if diff_col == 1: return 'gd'
        
        # 2. Determinar objetivo
        objetivo = None
        if self.kurtz_localizado:
            # Buscar celda con mayor P(salida)
            idx_maximo = np.argmax(self.prob_salida)
            objetivo = np.unravel_index(idx_maximo, self.prob_salida.shape)
            
            if self.prob_salida[objetivo] < 0.1:
                objetivo = None
        
        # 3. Planificar ruta (A* con umbral de riesgo)
        umbral_riesgo = 0.05
        siguiente = self._buscar_a_estrella(posicion_actual, objetivo, umbral_riesgo)
        
        if not siguiente:
            # Aumentar tolerancia al riesgo
            umbral_riesgo = 0.20
            siguiente = self._buscar_a_estrella(posicion_actual, objetivo, umbral_riesgo)
        
        # 4. Traducir a comando
        if siguiente:
            if siguiente == posicion_actual:
                return 'e'
            
            diff_fila = siguiente[0] - posicion_actual[0]
            diff_col = siguiente[1] - posicion_actual[1]
            
            if diff_fila == -1: return 'w'
            if diff_fila == 1: return 's'
            if diff_col == -1: return 'a'
            if diff_col == 1: return 'd'
        
        return None
    
    def _buscar_a_estrella(self, inicio, objetivo, umbral_riesgo):
        """
        A* considerando riesgo como obstáculo
        """
        # Cola de prioridad: (f, g, posicion, ruta)
        cola_prioridad = []
        heapq.heappush(cola_prioridad, (0, 0, inicio, []))
        visitados = {inicio}
        
        while len(cola_prioridad) > 0:
            f_actual, g_actual, posicion, ruta = heapq.heappop(cola_prioridad)
            
            # Verificar meta
            es_meta = False
            if objetivo:
                if posicion == objetivo:
                    es_meta = True
            else:
                # Modo exploración: celda no explorada
                if posicion not in self.celdas_exploradas:
                    es_meta = True
            
            if es_meta:
                if not ruta:
                    return posicion
                return ruta[0]
            
            # Expandir vecinos
            for vecino in self._obtener_vecinos(*posicion):
                if vecino in visitados:
                    continue
                
                riesgo = self.calcular_riesgo_total(*vecino)
                
                # Solo transitamos si es seguro
                if riesgo < umbral_riesgo:
                    visitados.add(vecino)
                    
                    nuevo_g = g_actual + 1
                    
                    # Heurística
                    h = 0
                    if objetivo:
                        h = abs(vecino[0] - objetivo[0]) + abs(vecino[1] - objetivo[1])
                    
                    # Penalización por riesgo
                    penalizacion_riesgo = riesgo * 10
                    
                    nuevo_f = nuevo_g + h + penalizacion_riesgo
                    
                    heapq.heappush(cola_prioridad, (nuevo_f, nuevo_g, vecino, ruta + [vecino]))
        
        return None
    
    def visualizar_heatmap(self, posicion_capitan):
        """Muestra el mapa de probabilidades (estilo arcade con intensidad)."""
        leyenda = [
            f"{EstilosConsola.INFO}👾 LEYENDA{EstilosConsola.RESET}",
            f"{EstilosConsola.CAPITAN}CW{EstilosConsola.RESET} = Willard",
            f"{EstilosConsola.CAPITAN_KURTZ}CW+K{EstilosConsola.RESET} = Willard+Kurtz",
            f"{EstilosConsola.SALIDA}█Sxx{EstilosConsola.RESET} = Salida probable",
            f"{EstilosConsola.FUEGO}█Fxx{EstilosConsola.RESET} = Fuego",
            f"{EstilosConsola.PINCHOS}█Pxx{EstilosConsola.RESET} = Pinchos",
            f"{EstilosConsola.DARDOS}█Dxx{EstilosConsola.RESET} = Dardos",
            f"{EstilosConsola.SOLDADO}█Mxx{EstilosConsola.RESET} = Militar",
            f"{EstilosConsola.ADVERTENCIA}█Rxx{EstilosConsola.RESET} = Riesgo total",
            f"{EstilosConsola.SEGURO}OK{EstilosConsola.RESET} = Seguro (<5%)",
            f"xx = porcentaje (00–99)",
            f"Escala: ░▒▓█ (bajo→alto)",
        ]

        def celda_fn(fila, columna):
            if (fila, columna) == posicion_capitan:
                if self.kurtz_localizado:
                    return "CW+K", EstilosConsola.CAPITAN_KURTZ
                return "CW", EstilosConsola.CAPITAN
            return self._analizar_celda(fila, columna)

        imprimir_tablero_arcade(
            self.dimension,
            celda_fn,
            titulo_mapa="🔥 MAPA DE PROBABILIDADES (Inferencia bayesiana)",
            leyenda=leyenda,
            cellw=6,
            ejes=True,
        )

    def _analizar_celda(self, fila, columna):
        """Determina símbolo y color para una celda"""
        pf = self.prob_fuego[fila, columna]
        pp = self.prob_pinchos[fila, columna]
        pd = self.prob_dardos[fila, columna]
        pm = self.prob_militar[fila, columna]
        ps = self.prob_salida[fila, columna]
        
        riesgo = self.calcular_riesgo_total(fila, columna)
        
        # Prioridad 1: Salida
        if ps > 0.50:
            return f"{bloque_prob(ps)}S{int(ps*100):02d}", EstilosConsola.SALIDA
        
        # Prioridad 2: Seguro
        if riesgo < 0.05:
            return "OK", EstilosConsola.SEGURO
        
        # Prioridad 3: Amenaza dominante
        amenazas = {'F': pf, 'P': pp, 'D': pd, 'M': pm}
        tipo_dom = max(amenazas, key=amenazas.get)
        prob_dom = amenazas[tipo_dom]
        
        if prob_dom > 0.50:
            texto = f"{bloque_prob(prob_dom)}{tipo_dom}{int(prob_dom*100):02d}"
            color = EstilosConsola.RESET
            
            if tipo_dom == 'F': color = EstilosConsola.FUEGO
            elif tipo_dom == 'P': color = EstilosConsola.PINCHOS
            elif tipo_dom == 'D': color = EstilosConsola.DARDOS
            elif tipo_dom == 'M': color = EstilosConsola.SOLDADO
            
            return texto, color
        
        # Prioridad 4: Riesgo genérico
        texto = f"{bloque_prob(riesgo)}R{int(riesgo*100):02d}"
        color = EstilosConsola.PELIGRO if riesgo > 0.50 else EstilosConsola.ADVERTENCIA
        return texto, color


class ControladorPalacioBayesiano:
    """Controlador del juego bayesiano"""
    
    def __init__(self, dimension=6, automatico=False):
        self.escenario = EscenarioPalacioBayesiano(dimension)
        self.cerebro = MotorInferenciaBayesiana(dimension)
        self.automatico = automatico
    
    def iniciar_partida(self):
        """Loop principal"""
        activo = True
        turno = 1
        
        while activo:
            #limpiar_pantalla()
            objetivo = "¡Lleva a Kurtz a la salida!" if self.escenario.coronel_rescatado else "Encuentra al Coronel Kurtz"
            estado = f"Turno {turno}  |  Pos {self.escenario.posicion_willard}"
            panel_arcade("PARTE 2 · INCERTIDUMBRE", f"🎯 {objetivo}   ·   {estado}")

            # Estado actual
            sensaciones = self.escenario.obtener_sensaciones()
            
            # Actualizar creencias
            self.cerebro.actualizar_probabilidades(self.escenario.posicion_willard, sensaciones)
            self.cerebro.kurtz_localizado = self.escenario.coronel_rescatado
            
            # Visualizar
            self.cerebro.visualizar_heatmap(self.escenario.posicion_willard)
            print(f"{EstilosConsola.INFO}Sensaciones:{EstilosConsola.RESET} {interpretar_sensaciones_bayesianas(sensaciones)}")
            
            if self.escenario.coronel_rescatado:
                print(f"{EstilosConsola.ADVERTENCIA}>>> OBJETIVO: Localiza la salida (S) <<<{EstilosConsola.RESET}")
            else:
                print(f"{EstilosConsola.INFO}>>> OBJETIVO: Encuentra a Kurtz (explora zonas seguras) <<<{EstilosConsola.RESET}")
            
            comando = None
            
            if not self.automatico:
                print(f"\n{EstilosConsola.GRIS}[WASD]=Mover [G]=Granada [E]=Salir [Q]=Abandonar{EstilosConsola.RESET}")
                entrada = input(f"{EstilosConsola.ENTRADA}Comando: {EstilosConsola.RESET}").lower().strip()
                
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
                print(f"{EstilosConsola.CYAN}Calculando riesgos...{EstilosConsola.RESET}")
                pausar(0.8)
                
                comando = self.cerebro.decidir_movimiento_automatico(self.escenario.posicion_willard)
                
                if comando:
                    print(f"→ Decisión: {EstilosConsola.EXITO}{comando.upper()}{EstilosConsola.RESET}")
                else:
                    print(f"{EstilosConsola.ERROR}¡Sin ruta segura! Riesgo excesivo.{EstilosConsola.RESET}")
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
                        print("✓ MISIÓN CUMPLIDA (Bayes) ✓".center(50))
                        print(f"{'='*50}{EstilosConsola.RESET}\n")
                    else:
                        print(f"\n{EstilosConsola.PELIGRO}{'='*50}")
                        print("✗ MUERTE ✗".center(50))
                        print(f"{'='*50}{EstilosConsola.RESET}\n")
