import json
import urllib.request

class IntegracionIA:
    def __init__(self, modelo="qwen2.5-coder:latest"):
        self.modelo = modelo
        self.url = "http://localhost:11434/api/chat"

    def analizar_resultados(self, resultados_num):
        prompt = f"""
        Actúa como un Chief Technology Officer (CTO). Analiza la viabilidad de negocio de estos resultados:
        - Servidores: {resultados_num['servidores']}
        - Latencia de Red: {resultados_num['latencia']}ms
        - Marketing: {resultados_num['marketing']}
        Evalúa el riesgo técnico y el retorno de inversión.
        """
        
        data = {
            "model": self.modelo,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        
        req = urllib.request.Request(self.url, data=json.dumps(data).encode("utf-8"))
        req.add_header("Content-Type", "application/json")
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read())
                return result['message']['content']
        except Exception as e:
            return str(e)