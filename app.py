from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import io
from fpdf import FPDF

# Importar la lógica existente
from programacion_dinamica import ProgramacionDinamica
from optimizacion_nolineal import OptimizacionNoLineal
from integracion_ia import IntegracionIA

app = FastAPI(title="Calculadora Estratégica Pro")
templates = Jinja2Templates(directory="templates")

# Ejemplos (Casos de Estudio)
EJEMPLO_SERVIDORES = [
    {"nombre": "Autenticación", "peso": 3, "valor": 5},
    {"nombre": "Matchmaking", "peso": 4, "valor": 7},
    {"nombre": "Sincronización", "peso": 7, "valor": 11},
    {"nombre": "Caché", "peso": 5, "valor": 8}
]

EJEMPLO_GRAFO = {
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

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Reporte de Optimización Estratégica', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/servidores", response_class=HTMLResponse)
async def get_servidores(request: Request):
    return templates.TemplateResponse(request, "servidores.html", {
        "ejemplo_servidores": json.dumps(EJEMPLO_SERVIDORES),
        "capacidad_default": 16
    })

@app.post("/servidores", response_class=HTMLResponse)
async def post_servidores(request: Request, capacidad: int = Form(...), servicios_json: str = Form(...)):
    servicios_raw = json.loads(servicios_json)
    # Convertir a formato esperado por la lógica: list of (nombre, peso, valor)
    microservicios = [(s['nombre'], int(s['peso']), int(s['valor'])) for s in servicios_raw]
    
    valor_optimo, seleccion = ProgramacionDinamica.optimizar_servidores(capacidad, microservicios)
    
    return templates.TemplateResponse(request, "servidores.html", {
        "resultado": {"valor": valor_optimo, "seleccion": seleccion},
        "ejemplo_servidores": servicios_json,
        "capacidad_default": capacidad,
        "raw_data": json.dumps({"capacidad": capacidad, "servicios": servicios_raw})
    })

@app.get("/ruta", response_class=HTMLResponse)
async def get_ruta(request: Request):
    return templates.TemplateResponse(request, "ruta.html", {
        "grafo_default": json.dumps(EJEMPLO_GRAFO, indent=2),
        "inicio_default": "A",
        "fin_default": "J"
    })

@app.post("/ruta", response_class=HTMLResponse)
async def post_ruta(request: Request, grafo_json: str = Form(...), inicio: str = Form(...), fin: str = Form(...)):
    grafo = json.loads(grafo_json)
    latencia, ruta = ProgramacionDinamica.ruta_minima_backward(grafo, inicio, fin)
    
    return templates.TemplateResponse(request, "ruta.html", {
        "resultado": {"latencia": latencia, "ruta": " -> ".join(ruta)},
        "grafo_default": grafo_json,
        "inicio_default": inicio,
        "fin_default": fin,
        "raw_data": json.dumps({"inicio": inicio, "fin": fin, "grafo": grafo})
    })

@app.get("/marketing", response_class=HTMLResponse)
async def get_marketing(request: Request):
    return templates.TemplateResponse(request, "marketing.html", {
        "presupuesto_default": 10
    })

@app.post("/marketing", response_class=HTMLResponse)
async def post_marketing(request: Request, presupuesto: float = Form(...)):
    roi, x1, x2 = OptimizacionNoLineal.maximizar_marketing(presupuesto)
    
    return templates.TemplateResponse(request, "marketing.html", {
        "resultado": {"roi": roi, "creadores": x1, "anuncios": x2},
        "presupuesto_default": presupuesto,
        "raw_data": json.dumps({"presupuesto": presupuesto})
    })

@app.post("/analizar-ia", response_class=HTMLResponse)
async def analizar_ia(request: Request, data: str = Form(...)):
    resultados = json.loads(data)
    ia = IntegracionIA()
    analisis = ia.analizar_resultados(resultados)
    # Devolver el análisis y un campo oculto para el PDF
    return HTMLResponse(content=f"""
        <div class='alert alert-info' id='ia-text-content'>{analisis}</div>
        <input type='hidden' id='ia-analisis-input' value='{analisis}'>
    """)

@app.post("/descargar-pdf")
async def descargar_pdf(
    tipo: str = Form(...),
    datos: str = Form(...),
    resultado: str = Form(...),
    ia_analisis: str = Form(...)
):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, f"Tipo de Ejercicio: {tipo}", ln=1)
    pdf.ln(5)

    # Formatear datos de entrada legibles
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Datos de Entrada:", ln=1)
    pdf.set_font("helvetica", size=10)
    
    try:
        raw_datos = json.loads(datos)
        if "Optimización de Servidores" in tipo:
            cap = raw_datos.get("capacidad", "N/A")
            servs = raw_datos.get("servicios", [])
            txt = f"Capacidad Maxima: {cap}\nServicios disponibles:\n"
            for s in servs:
                txt += f"- {s['nombre']} (Peso: {s['peso']}, Valor: {s['valor']})\n"
            pdf.multi_cell(0, 10, txt)
        elif "Ruta Mínima" in tipo:
            txt = f"Inicio: {raw_datos.get('inicio', 'N/A')}\nFin: {raw_datos.get('fin', 'N/A')}\nGrafo:\n"
            grafo = raw_datos.get("grafo", {})
            for nodo, conns in grafo.items():
                conns_str = ", ".join([f"{k}({v}ms)" for k, v in conns.items()])
                txt += f"- {nodo} conecta con: {conns_str}\n"
            pdf.multi_cell(0, 10, txt)
        else:
            pdf.multi_cell(0, 10, datos)
    except:
        pdf.multi_cell(0, 10, datos)
    
    pdf.ln(5)

    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Resultados Obtenidos:", ln=1)
    pdf.set_font("helvetica", size=10)
    pdf.multi_cell(0, 10, resultado)
    pdf.ln(5)

    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Análisis del CTO (IA):", ln=1)
    pdf.set_font("helvetica", size=10)
    # Limpiar texto para latin-1 (standard PDF font encoding)
    clean_ia = ia_analisis.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_ia)

    pdf_bytes = pdf.output()
    
    return Response(
        content=bytes(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Reporte_{tipo.replace(' ', '_')}.pdf"}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
