class ProgramacionDinamica:
    @staticmethod
    def optimizar_servidores(capacidad_max, microservicios):
        n = len(microservicios)
        dp = [[0 for _ in range(capacidad_max + 1)] for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            nombre, peso, valor = microservicios[i-1]
            for w in range(1, capacidad_max + 1):
                if peso <= w:
                    dp[i][w] = max(valor + dp[i-1][w-peso], dp[i-1][w])
                else:
                    dp[i][w] = dp[i-1][w]
                    
        res, w = dp[n][capacidad_max], capacidad_max
        seleccion = []
        for i in range(n, 0, -1):
            if res <= 0: break
            if res != dp[i-1][w]:
                seleccion.append(microservicios[i-1][0])
                res -= microservicios[i-1][2]
                w -= microservicios[i-1][1]
                
        return dp[-1][-1], seleccion

    @staticmethod
    def ruta_minima_backward(grafo, inicio, fin):
        memo = {fin: 0}
        rutas = {fin: [fin]}
        
        def calcular_dp(nodo):
            if nodo in memo: return memo[nodo]
            min_costo = float('inf')
            mejor_ruta = []
            
            for vecino, peso in grafo.get(nodo, {}).items():
                costo = peso + calcular_dp(vecino)
                if costo < min_costo:
                    min_costo = costo
                    mejor_ruta = [nodo] + rutas[vecino]
                    
            memo[nodo] = min_costo
            rutas[nodo] = mejor_ruta
            return min_costo
            
        latencia_minima = calcular_dp(inicio)
        return latencia_minima, rutas.get(inicio, [])