from programacion_dinamica import ProgramacionDinamica
from optimizacion_nolineal import OptimizacionNoLineal
from integracion_ia import IntegracionIA

def main():
    # 1. Optimización de Servidores
    microservicios = [
        ("Autenticación", 3, 5),
        ("Matchmaking", 4, 7),
        ("Sincronización", 7, 11),
        ("Caché", 5, 8)
    ]
    valor_optimo, seleccion = ProgramacionDinamica.optimizar_servidores(16, microservicios)

    # 2. Ruta Mínima
    grafo = {
        'A': {'B': 4, 'C': 6, 'D': 3},
        'B': {'E': 7, 'F': 5},
        'C': {'E': 3, 'F': 8, 'G': 4},
        'D': {'F': 6, 'G': 9},
        'E': {'H': 5, 'I': 6},
        'F': {'H': 3, 'I': 5},
        'G': {'H': 8, 'I': 2},
        'H': {'J': 4},
        'I': {'J': 7}
    }
    latencia, ruta = ProgramacionDinamica.ruta_minima_backward(grafo, 'A', 'J')

    # 3. Optimización de Marketing
    roi, x1, x2 = OptimizacionNoLineal.maximizar_marketing(10)

    # 4. Integración con Ollama
    resultados = {
        'servidores': f"Valor: {valor_optimo}, Seleccionados: {seleccion}",
        'latencia': latencia,
        'marketing': f"ROI: {roi}, Creadores: {x1}, Anuncios: {x2}"
    }
    
    ia = IntegracionIA(modelo="qwen2.5-coder:latest")
    analisis = ia.analizar_resultados(resultados)
    
    print("--- Conclusiones Estratégicas del Asistente de IA ---")
    print(analisis)

if __name__ == "__main__":
    main()