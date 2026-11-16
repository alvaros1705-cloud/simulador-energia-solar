import io
import math
import zipfile
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage

st.set_page_config(
    page_title="Solar Lab – Integral Insights",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
TEAM = [
    "Sara Gáfaro Salamanca",
    "Leidy Stephania Delgado Galvis",
    "Angel David Carrascal Claro",
    "Samuel David Jaimes Estrada",
]

TEXT = {
    "es": {
        "subtitle": "Laboratorio de modelación y análisis de energía solar",
        "course": "INGENIERÍA MULTIMEDIA  /  CÁLCULO INTEGRAL",
        "nav": ["Resumen", "Mediciones", "Cálculo integral", "Hipótesis", "Historial", "Informes"],
        "model": "Parámetros del modelo",
        "panels": "Número de paneles",
        "peak": "Potencia máxima por panel",
        "start": "Hora inicial",
        "end": "Hora final",
        "intro": "Explora el comportamiento de la potencia solar, calcula la energía acumulada mediante integrales y contrasta el modelo con mediciones experimentales.",
        "power": "Potencia máxima total",
        "energy": "Energía estimada",
        "average": "Potencia promedio",
        "period": "Intervalo analizado",
        "curve_title": "Curva de potencia estimada",
        "curve_desc": "Modelo cuadrático de referencia para una jornada solar. Ajusta los parámetros desde el panel lateral.",
        "scenario": "Comparación de escenarios",
        "scenario_desc": "Observa cómo cambia la energía acumulada cuando la potencia máxima varía.",
        "scenario_name": "Escenario",
        "scenario_power": "Potencia máxima (W)",
        "scenario_energy": "Energía (kWh)",
        "measurement_title": "Mediciones experimentales",
        "measurement_desc": "Carga un archivo CSV para contrastar el modelo con datos registrados. Se requieren las columnas hora y potencia_w.",
        "template": "Descargar plantilla CSV",
        "upload": "Seleccionar archivo CSV",
        "quality": "Resumen de calidad de datos",
        "valid": "Registros válidos",
        "incomplete": "Filas incompletas",
        "duplicates": "Horas duplicadas",
        "negative": "Potencias negativas",
        "outliers": "Posibles atípicos",
        "score": "Indicador orientativo",
        "measured_energy": "Energía integrada desde las mediciones",
        "curve_fit": "Ajuste cuadrático de las mediciones",
        "r2": "Coeficiente de determinación R²",
        "measurement_curve": "Potencia medida y curva ajustada",
        "no_measurements": "Todavía no hay mediciones cargadas. Usa la plantilla o sube tu propio CSV.",
        "integral_title": "Análisis mediante cálculo integral",
        "integral_desc": "La energía acumulada corresponde al área bajo la curva de potencia en el intervalo de tiempo seleccionado.",
        "function": "Función de potencia",
        "antiderivative": "Antiderivada",
        "analytic": "Integración analítica",
        "numeric": "Regla del trapecio",
        "difference": "Diferencia absoluta",
        "steps": "Subintervalos de integración",
        "geometry": "Aplicación geométrica",
        "length_panel": "Largo del panel (m)",
        "width_panel": "Ancho del panel (m)",
        "panel_area": "Área total de paneles",
        "radius": "Radio inicial (m)",
        "slope": "Pendiente del radio (m/m)",
        "length": "Longitud (m)",
        "volume": "Volumen del sólido de revolución",
        "hyp_title": "Laboratorio de hipótesis",
        "hyp_desc": "Modifica la potencia máxima para explorar escenarios y comparar su efecto sobre la energía acumulada.",
        "variation": "Variación de potencia máxima",
        "base": "Modelo base",
        "hypothesis": "Hipótesis",
        "save": "Guardar escenario",
        "saved": "Escenario guardado en el historial de esta sesión.",
        "history_title": "Historial de escenarios",
        "history_desc": "Los escenarios guardados se conservan durante esta sesión de la aplicación.",
        "empty_history": "Aún no has guardado escenarios.",
        "clear": "Limpiar historial",
        "report_title": "Informe del laboratorio",
        "report_desc": "Genera un reporte con los parámetros actuales, resultados de integración y datos del proyecto.",
        "pdf": "Descargar informe PDF",
        "csv": "Descargar datos CSV",
        "zip": "Descargar paquete completo ZIP",
        "team": "Equipo de trabajo",
        "institution": "Universidad Simón Bolívar · Ingeniería Multimedia · Cálculo Integral",
        "note": "Nota metodológica",
        "caution": "El modelo de potencia es una aproximación académica. El indicador de calidad es orientativo y no sustituye la calibración de instrumentos. No extrapoles el ajuste cuadrático fuera del intervalo medido.",
        "hour": "Hora",
        "watts": "Potencia (W)",
        "area_note": "El área física de los paneles es una magnitud geométrica y no debe confundirse con el área bajo la curva potencia-tiempo, que representa energía.",
        "invalid_csv": "El CSV debe contener las columnas hora y potencia_w.",
        "invalid_time": "No fue posible interpretar una o más horas. Usa valores decimales (8.5) o formato HH:MM.",
        "negative_warning": "Se encontraron potencias negativas. Revisa las mediciones; no se integraron datos con valores negativos.",
        "need_rows": "Se necesitan al menos dos horas distintas con potencia numérica no negativa.",
        "quality_note": "La puntuación resume faltantes, duplicados y posibles atípicos; úsala como señal de revisión, no como certificación.",
        "date": "Fecha",
        "variation_col": "Variación (%)",
        "count_col": "Paneles",
        "energy_col": "Energía (kWh)",
        "interval": "Intervalo",
    },
    "en": {
        "subtitle": "Solar energy modelling and analysis laboratory",
        "course": "MULTIMEDIA ENGINEERING  /  INTEGRAL CALCULUS",
        "nav": ["Overview", "Measurements", "Integral calculus", "Hypotheses", "History", "Reports"],
        "model": "Model parameters",
        "panels": "Number of panels",
        "peak": "Maximum power per panel",
        "start": "Start time",
        "end": "End time",
        "intro": "Explore solar power behaviour, calculate accumulated energy using integrals, and compare the model with experimental measurements.",
        "power": "Total peak power",
        "energy": "Estimated energy",
        "average": "Average power",
        "period": "Analysis interval",
        "curve_title": "Estimated power curve",
        "curve_desc": "Reference quadratic model for a solar day. Adjust the parameters in the sidebar.",
        "scenario": "Scenario comparison",
        "scenario_desc": "See how accumulated energy changes when peak power varies.",
        "scenario_name": "Scenario",
        "scenario_power": "Maximum power (W)",
        "scenario_energy": "Energy (kWh)",
        "measurement_title": "Experimental measurements",
        "measurement_desc": "Upload a CSV file to compare the model with recorded data. Required columns: hora and potencia_w.",
        "template": "Download CSV template",
        "upload": "Choose CSV file",
        "quality": "Data quality overview",
        "valid": "Valid records",
        "incomplete": "Incomplete rows",
        "duplicates": "Duplicate times",
        "negative": "Negative power values",
        "outliers": "Potential outliers",
        "score": "Indicative score",
        "measured_energy": "Energy integrated from measurements",
        "curve_fit": "Quadratic fit of measurements",
        "r2": "Coefficient of determination R²",
        "measurement_curve": "Measured power and fitted curve",
        "no_measurements": "No measurements uploaded yet. Use the template or upload your own CSV.",
        "integral_title": "Integral calculus analysis",
        "integral_desc": "Accumulated energy is the area under the power curve over the selected time interval.",
        "function": "Power function",
        "antiderivative": "Antiderivative",
        "analytic": "Analytical integration",
        "numeric": "Trapezoidal rule",
        "difference": "Absolute difference",
        "steps": "Integration subintervals",
        "geometry": "Geometric application",
        "length_panel": "Panel length (m)",
        "width_panel": "Panel width (m)",
        "panel_area": "Total panel area",
        "radius": "Initial radius (m)",
        "slope": "Radius slope (m/m)",
        "length": "Length (m)",
        "volume": "Volume of revolution",
        "hyp_title": "Hypothesis laboratory",
        "hyp_desc": "Change maximum power to explore scenarios and compare their effect on accumulated energy.",
        "variation": "Maximum power variation",
        "base": "Baseline model",
        "hypothesis": "Hypothesis",
        "save": "Save scenario",
        "saved": "Scenario saved to this session's history.",
        "history_title": "Scenario history",
        "history_desc": "Saved scenarios are kept for the current app session.",
        "empty_history": "You have not saved any scenarios yet.",
        "clear": "Clear history",
        "report_title": "Laboratory report",
        "report_desc": "Generate a report with current parameters, integration results, and project information.",
        "pdf": "Download PDF report",
        "csv": "Download CSV data",
        "zip": "Download complete ZIP package",
        "team": "Project team",
        "institution": "Universidad Simón Bolívar · Multimedia Engineering · Integral Calculus",
        "note": "Methodological note",
        "caution": "The power model is an academic approximation. The quality indicator is indicative and does not replace instrument calibration. Do not extrapolate the quadratic fit beyond the measured interval.",
        "hour": "Hour",
        "watts": "Power (W)",
        "area_note": "The physical panel area is a geometric quantity and must not be confused with the area under the power-time curve, which represents energy.",
        "invalid_csv": "The CSV must contain hora and potencia_w columns.",
        "invalid_time": "One or more times could not be interpreted. Use decimal values (8.5) or HH:MM format.",
        "negative_warning": "Negative power values were found. Review the measurements; negative values were not integrated.",
        "need_rows": "At least two distinct times with numeric, non-negative power values are required.",
        "quality_note": "The score summarizes missing values, duplicates, and potential outliers; use it as a review signal, not as certification.",
        "date": "Date",
        "variation_col": "Variation (%)",
        "count_col": "Panels",
        "energy_col": "Energy (kWh)",
        "interval": "Interval",
    },
}

if "language" not in st.session_state:
    st.session_state.language = "Español (Colombia)"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "history" not in st.session_state:
    st.session_state.history = []
if "measurements" not in st.session_state:
    st.session_state.measurements = None
if "measurement_quality" not in st.session_state:
    st.session_state.measurement_quality = None
if "page_index" not in st.session_state:
    st.session_state.page_index = 0

def set_language(value):
    st.session_state.language = value

def set_theme(value):
    st.session_state.dark_mode = value

def set_page(index):
    st.session_state.page_index = index

lang = "en" if st.session_state.language == "English (USA)" else "es"
T = TEXT[lang]
dark = st.session_state.dark_mode
if dark:
    C = {
        "bg": "#0B1726", "surface": "#14253A", "surface2": "#1A3049",
        "text": "#EAF2FC", "muted": "#AFC1D5", "line": "#30465E",
        "blue": "#75B8FF", "green": "#55C99A", "accent": "#8ABEFF",
        "plot": "#14253A", "grid": "#3C526B",
    }
else:
    C = {
        "bg": "#F3F6FB", "surface": "#FFFFFF", "surface2": "#EAF1F8",
        "text": "#172D46", "muted": "#60748C", "line": "#D9E3EF",
        "blue": "#1769AA", "green": "#16845D", "accent": "#1C66A8",
        "plot": "#FFFFFF", "grid": "#DDE5EF",
    }

st.markdown(
    f"""
    <style>
    :root {{
      color-scheme: {"dark" if dark else "light"};
      --sl-bg: {C["bg"]}; --sl-surface: {C["surface"]};
      --sl-surface2: {C["surface2"]}; --sl-text: {C["text"]};
      --sl-muted: {C["muted"]}; --sl-line: {C["line"]};
      --sl-blue: {C["blue"]}; --sl-green: {C["green"]};
    }}
    html, body, [data-testid="stAppViewContainer"] {{
      background: var(--sl-bg) !important; color: var(--sl-text) !important;
    }}
    [data-testid="stMain"] > div {{ background: var(--sl-bg) !important; }}
    [data-testid="stMainBlockContainer"] {{
      max-width: 1450px; padding-top: 1.2rem; padding-bottom: 2rem;
    }}
    [data-testid="stSidebar"] > div:first-child {{
      background: var(--sl-surface2) !important;
      border-right: 1px solid var(--sl-line);
    }}
    .stApp, .stApp p, .stApp label, .stApp span, .stApp li,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp strong,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span, [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
      color: var(--sl-text) !important;
    }}
    .stCaption, [data-testid="stCaptionContainer"], .muted {{
      color: var(--sl-muted) !important;
    }}
    .brandbar {{
      display:flex; align-items:center; justify-content:space-between;
      gap:1.2rem; padding:1.25rem 1.5rem; margin:.25rem 0 1rem 0;
      background:var(--sl-surface); border:1px solid var(--sl-line);
      border-radius:20px; box-shadow:0 8px 28px rgba(20,45,75,.06);
    }}
    .brand-copy {{ flex:1; min-width:0; }}
    .eyebrow {{ color:var(--sl-blue) !important; font-size:.76rem;
      font-weight:800; letter-spacing:.12em; margin-bottom:.35rem; }}
    .brand-title {{ color:var(--sl-text) !important; font-size:clamp(1.55rem,2.5vw,2.25rem);
      line-height:1.12; font-weight:850; margin:0; }}
    .brand-subtitle {{ color:var(--sl-muted) !important; font-size:1rem; margin-top:.5rem; }}
    .brand-tag {{ display:inline-block; margin-top:.75rem; padding:.3rem .65rem;
      border-radius:999px; background:var(--sl-surface2); color:var(--sl-blue) !important;
      font-size:.72rem; font-weight:750; letter-spacing:.04em; }}
    [data-testid="stMetric"] {{
      background:var(--sl-surface) !important; border:1px solid var(--sl-line);
      border-radius:16px; padding:1rem 1.1rem; min-height:112px;
      box-shadow:0 4px 16px rgba(20,45,75,.035);
    }}
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {{ color:var(--sl-text) !important; }}
    [data-testid="stMetricLabel"] {{ font-size:.82rem; }}
    [data-testid="stMetricValue"] {{ font-weight:800; }}
    .section-kicker {{ color:var(--sl-blue) !important; font-weight:800;
      font-size:.75rem; letter-spacing:.12em; text-transform:uppercase; }}
    .section-title {{ color:var(--sl-text) !important; font-size:1.45rem;
      font-weight:800; margin:.15rem 0 .25rem 0; }}
    .section-desc {{ color:var(--sl-muted) !important; margin:0 0 1rem 0; }}
    .info-card {{ background:var(--sl-surface); border:1px solid var(--sl-line);
      border-radius:16px; padding:1rem 1.15rem; height:100%; }}
    .info-label {{ color:var(--sl-muted) !important; font-size:.78rem;
      font-weight:700; text-transform:uppercase; letter-spacing:.06em; }}
    .info-value {{ color:var(--sl-text) !important; font-size:1.35rem;
      font-weight:800; margin-top:.25rem; }}
    .note-card {{ background:var(--sl-surface2); border-left:4px solid var(--sl-blue);
      border-radius:10px; padding:.9rem 1rem; color:var(--sl-text) !important; }}
    [data-testid="stRadio"] > div {{ gap:.35rem; }}
    [data-testid="stRadio"] label {{ color:var(--sl-text) !important; }}
    div[data-testid="stRadio"] > label {{ display:none; }}
    div.stButton > button, div.stDownloadButton > button {{
      border-radius:10px; font-weight:700; min-height:2.65rem;
    }}
    div.stButton > button[kind="primary"],
    div.stDownloadButton > button[kind="primary"] {{
      background:var(--sl-blue) !important; border-color:var(--sl-blue) !important;
      color:#FFFFFF !important;
    }}
    [data-testid="stDataFrame"], [data-testid="stTable"] {{
      border:1px solid var(--sl-line); border-radius:12px; overflow:hidden;
    }}
    input, textarea, [data-baseweb="select"] > div,
    [data-baseweb="input"] > div, [data-baseweb="textarea"] > div {{
      background:var(--sl-surface) !important;
      color:var(--sl-text) !important;
      border-color:var(--sl-line) !important;
    }}
    [data-baseweb="select"] *, [data-baseweb="input"] *,
    [data-baseweb="textarea"] *, [data-testid="stNumberInput"] button {{
      color:var(--sl-text) !important;
    }}
    [data-testid="stRadio"] div[role="radiogroup"] {{
      display:flex; flex-wrap:wrap; gap:.3rem; padding:.45rem;
      background:var(--sl-surface); border:1px solid var(--sl-line);
      border-radius:14px;
    }}
    [data-testid="stRadio"] div[role="radio"] {{
      padding:.25rem .6rem; border-radius:10px;
    }}
    hr {{ border-color:var(--sl-line) !important; }}
    a {{ color:var(--sl-blue) !important; }}
    .footer {{ color:var(--sl-muted) !important; text-align:center;
      font-size:.78rem; padding:1rem 0 .4rem 0; }}
    @media (max-width: 760px) {{
      .brandbar {{ padding:1rem; }} .brand-title {{ font-size:1.55rem; }}
      [data-testid="stMainBlockContainer"] {{ padding-left:1rem; padding-right:1rem; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(f"""<style>
/* Solar Lab reference layout */
[data-testid="stSidebar"] > div:first-child {{ background:var(--sl-surface2) !important; }}
[data-testid="stSidebar"] {{ min-width:250px; }}
[data-testid="stSidebar"] button {{
  width:100%; min-height:2.8rem; text-align:left; border-radius:12px !important;
  border:1px solid transparent !important; font-weight:700 !important;
  transition:background .2s ease, transform .2s ease, box-shadow .2s ease !important;
}}
[data-testid="stSidebar"] button:hover {{
  transform:translateX(3px); background:var(--sl-surface) !important;
  border-color:var(--sl-line) !important;
}}
.sl-topbar {{ display:flex; align-items:center; gap:.6rem; min-height:3rem; padding:.2rem 0 .8rem 0; }}
.sl-topbar h2 {{ color:var(--sl-text) !important; font-size:1.3rem; margin:0; font-weight:850; }}
.sl-topbar small {{ color:var(--sl-muted) !important; letter-spacing:.08em; font-size:.7rem; }}
.sl-hero {{
  position:relative; overflow:hidden; min-height:190px; padding:2rem 2.2rem;
  border-radius:20px; margin:.3rem 0 1.25rem 0;
  background-image:linear-gradient(90deg,rgba(8,28,53,.92) 0%,rgba(8,35,62,.78) 42%,rgba(8,35,62,.1) 100%),
  url("https://images.unsplash.com/photo-1756913455114-182d7584ed49?auto=format&fit=crop&fm=jpg&q=82&w=1800");
  background-size:cover; background-position:center 52%;
  box-shadow:0 12px 32px rgba(12,35,65,.15);
  animation:sl-enter .7s ease both;
}}
.sl-hero:after {{
  content:""; position:absolute; width:170px; height:170px; right:8%; top:10%;
  border-radius:50%; background:rgba(255,220,110,.18); filter:blur(16px);
  animation:sl-sun 5s ease-in-out infinite alternate;
}}
.sl-hero-content {{ position:relative; z-index:1; max-width:650px; }}
.sl-hero h1 {{ color:white !important; font-size:clamp(1.8rem,3vw,2.55rem); line-height:1.08; font-weight:850; margin:0 0 .55rem 0; }}
.sl-hero p {{ color:rgba(255,255,255,.93) !important; max-width:610px; font-size:1rem; line-height:1.55; margin:0; }}
.sl-eyebrow {{ color:#B9E5FF !important; font-size:.73rem; font-weight:800; letter-spacing:.15em; margin-bottom:.65rem; }}
[data-testid="stMetric"] {{
  background:var(--sl-surface) !important; border:1px solid var(--sl-line) !important;
  border-radius:16px !important; padding:1rem 1.1rem !important;
  box-shadow:0 5px 16px rgba(18,48,78,.055) !important;
  animation:sl-rise .55s ease both; transition:transform .22s ease, box-shadow .22s ease !important;
}}
[data-testid="stMetric"]:hover {{ transform:translateY(-3px); box-shadow:0 10px 24px rgba(18,48,78,.10) !important; }}
[data-testid="stMetricLabel"], [data-testid="stMetricValue"], [data-testid="stMetricDelta"] {{ color:var(--sl-text) !important; }}
[data-testid="stMetricValue"] {{ font-weight:850 !important; }}
.sl-section-title {{ color:var(--sl-text) !important; font-size:1.3rem; font-weight:850; margin:.2rem 0 .25rem 0; }}
.sl-section-sub {{ color:var(--sl-muted) !important; font-size:.9rem; margin:0 0 .9rem 0; }}
.sl-panel {{ background:var(--sl-surface); border:1px solid var(--sl-line); border-radius:17px; padding:1rem 1.1rem; box-shadow:0 5px 18px rgba(18,48,78,.045); height:100%; animation:sl-rise .6s ease both; }}
.sl-panel h3 {{ color:var(--sl-text) !important; font-size:1.02rem; margin:0 0 .7rem 0; font-weight:800; }}
.sl-conclusion {{ background:var(--sl-surface); border:1px solid var(--sl-line); border-radius:15px; padding:1rem; min-height:118px; box-shadow:0 4px 14px rgba(18,48,78,.04); animation:sl-rise .7s ease both; }}
.sl-conclusion strong {{ color:var(--sl-text) !important; display:block; margin-bottom:.35rem; }}
.sl-conclusion p {{ color:var(--sl-muted) !important; font-size:.88rem; margin:0; line-height:1.45; }}
.sl-index {{ display:inline-flex; width:28px; height:28px; border-radius:50%; align-items:center; justify-content:center; margin-right:.35rem; color:white !important; font-weight:800; background:#2678DC; }}
.sl-feature {{ border:1px solid var(--sl-line); background:var(--sl-surface); padding:.75rem .5rem; border-radius:13px; text-align:center; color:var(--sl-text) !important; font-size:.8rem; font-weight:700; }}
.stButton button, .stDownloadButton button {{ min-height:2.7rem; border-radius:12px !important; font-weight:750 !important; transition:transform .2s ease, box-shadow .2s ease !important; }}
.stButton button:hover, .stDownloadButton button:hover {{ transform:translateY(-2px); box-shadow:0 7px 16px rgba(18,48,78,.12) !important; }}
.sl-footer {{ color:var(--sl-muted) !important; text-align:center; padding:1.2rem 0 .5rem 0; font-size:.78rem; }}
@keyframes sl-enter {{ from {{ opacity:0; transform:translateY(10px); }} to {{ opacity:1; transform:translateY(0); }} }}
@keyframes sl-rise {{ from {{ opacity:0; transform:translateY(12px); }} to {{ opacity:1; transform:translateY(0); }} }}
@keyframes sl-sun {{ from {{ transform:translateY(2px) scale(.92); opacity:.45; }} to {{ transform:translateY(-10px) scale(1.12); opacity:.9; }} }}
@media(max-width:850px) {{ .sl-hero {{ min-height:210px; padding:1.4rem; background-position:62% center; }} .sl-hero h1 {{ font-size:1.65rem; }} }}

/* High-contrast theme-aware buttons: never inherit low-contrast defaults. */
.stApp div[data-testid="stButton"] > button,
.stApp div[data-testid="stDownloadButton"] > button,
.stApp button[data-testid="stBaseButton-secondary"] {{
  background:var(--sl-surface2) !important;
  color:var(--sl-text) !important;
  -webkit-text-fill-color:var(--sl-text) !important;
  border:1px solid var(--sl-line) !important;
  font-weight:750 !important;
  opacity:1 !important;
}}
.stApp button[data-testid="stBaseButton-secondary"] *,
.stApp button[data-testid="stBaseButton-primary"] *,
.stApp div[data-testid="stButton"] > button *,
.stApp div[data-testid="stDownloadButton"] > button * {{
  color:inherit !important;
  -webkit-text-fill-color:inherit !important;
  opacity:1 !important;
}}
.stApp button[data-testid="stBaseButton-primary"],
.stApp div[data-testid="stButton"] > button[kind="primary"],
.stApp div[data-testid="stDownloadButton"] > button[kind="primary"] {{
  background:{"#3478D4" if dark else "#1769AA"} !important;
  color:#FFFFFF !important;
  -webkit-text-fill-color:#FFFFFF !important;
  border:1px solid {"#3478D4" if dark else "#1769AA"} !important;
  font-weight:800 !important;
}}
.stApp button[data-testid="stBaseButton-primary"]:hover,
.stApp button[data-testid="stBaseButton-secondary"]:hover {{
  filter:brightness(1.06);
}}
/* Keep the banner title white on both themes, above the photographic overlay. */
html body .stApp .sl-hero .sl-hero-content h1 {{
  color:#FFFFFF !important;
  -webkit-text-fill-color:#FFFFFF !important;
  text-shadow:0 2px 10px rgba(0,0,0,.35) !important;
}}
html body .stApp .sl-hero .sl-hero-content p {{
  color:#FFFFFF !important;
  -webkit-text-fill-color:#FFFFFF !important;
  text-shadow:0 1px 5px rgba(0,0,0,.3) !important;
}}
/* Institutional marks share one aligned header row. */
.sl-topbar h2 {{ font-size:1.55rem !important; line-height:1.15; }}
[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"] {{
  background:var(--sl-surface) !important;
}}
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {{
  background:{"#3478D4" if dark else "#1769AA"} !important;
  color:#FFFFFF !important;
  -webkit-text-fill-color:#FFFFFF !important;
}}
</style>""", unsafe_allow_html=True)

# Main institutional header: university identity is prominent in the content frame.
logo_uni = ASSETS / "logo_universidad_simon_bolivar.png"
logo_program = ASSETS / ("logo_ingenieria_multimedia_oscuro.png" if dark else "logo_ingenieria_multimedia_claro.png")

main_header, lang_es_col, lang_en_col, light_col, dark_col = st.columns([5.8, 1.0, 1.0, 1.0, 1.0], gap="small")
with main_header:
    uni_col, title_col, program_col = st.columns([2.0, 4.6, 0.7], vertical_alignment="center")
    with uni_col:
        if logo_uni.exists():
            st.image(str(logo_uni), width=190)
    with title_col:
        st.markdown(
            '<div class="sl-topbar"><div><h2>Solar Lab – Integral Insights</h2>'
            '<small>UNIVERSIDAD SIMÓN BOLÍVAR · INGENIERÍA MULTIMEDIA</small></div></div>',
            unsafe_allow_html=True,
        )
    with program_col:
        if logo_program.exists():
            st.image(str(logo_program), width=76)
with lang_es_col:
    st.button("🇨🇴 Español", key="lang_es_btn", type="primary" if lang == "es" else "secondary",
              use_container_width=True, on_click=set_language, args=("Español (Colombia)",))
with lang_en_col:
    st.button("🇺🇸 English", key="lang_en_btn", type="primary" if lang == "en" else "secondary",
              use_container_width=True, on_click=set_language, args=("English (USA)",))
with light_col:
    st.button("☀️ Claro", key="theme_light_btn", type="primary" if not dark else "secondary",
              use_container_width=True, on_click=set_theme, args=(False,))
with dark_col:
    st.button("🌙 Oscuro", key="theme_dark_btn", type="primary" if dark else "secondary",
              use_container_width=True, on_click=set_theme, args=(True,))

with st.sidebar:
    st.markdown("### " + ("Navegación" if lang == "es" else "Navigation"))
    nav_icons = ["⌂", "▤", "∫", "⚗", "◷", "▧"]
    for idx, label in enumerate(T["nav"]):
        active = st.session_state.page_index == idx
        st.button(
            f"{nav_icons[idx]}   {label}",
            key=f"nav_page_{idx}",
            type="primary" if active else "secondary",
            use_container_width=True,
            on_click=set_page,
            args=(idx,),
        )
    st.divider()
    st.markdown("### ☀️ " + T["model"])
    st.caption(T["institution"])
    panels = st.number_input(T["panels"], min_value=1, max_value=100, value=1, step=1)
    pmax = st.slider(T["peak"] + " (W)", min_value=50, max_value=600, value=300, step=10)
    start = st.slider(T["start"], min_value=6.0, max_value=12.0, value=6.0, step=0.5)
    end = st.slider(T["end"], min_value=12.0, max_value=18.0, value=18.0, step=0.5)
    st.divider()
    st.markdown("**" + T["team"] + "**")
    for member in TEAM:
        st.caption("· " + member)

page = T["nav"][st.session_state.page_index]

if end <= start:
    st.error("El intervalo final debe ser mayor que el inicial.")
    st.stop()

def power(t, peak):
    return peak * (1 - ((np.asarray(t, dtype=float) - 12) ** 2) / 36)

def primitive(t, peak):
    return peak * (t - ((t - 12) ** 3) / 108)

def analytic_energy(a, b, peak):
    return float(primitive(b, peak) - primitive(a, peak))

def integrate_trapezoid(a, b, peak, number_of_intervals=2400):
    grid = np.linspace(a, b, number_of_intervals + 1)
    values = power(grid, peak)
    return float(np.trapezoid(values, grid) if hasattr(np, "trapezoid") else np.trapz(values, grid))

def parse_hour(value):
    if isinstance(value, (int, float, np.integer, np.floating)):
        return float(value)
    text = str(value).strip()
    if ":" in text:
        parts = text.split(":")
        return float(parts[0]) + float(parts[1]) / 60
    return float(text.replace(",", "."))

def section_heading(kicker, title, description):
    st.markdown(
        f'<div class="section-kicker">{kicker}</div><div class="section-title">{title}</div><p class="section-desc">{description}</p>',
        unsafe_allow_html=True,
    )

def make_power_figure(x_values, y_values, title, fill=True, measured_x=None, measured_y=None):
    fig, ax = plt.subplots(figsize=(10, 3.8), dpi=150)
    fig.patch.set_facecolor(C["plot"])
    ax.set_facecolor(C["plot"])
    ax.plot(x_values, y_values, color=C["blue"], linewidth=3, label=T["watts"])
    if fill:
        ax.fill_between(x_values, y_values, color=C["blue"], alpha=.13)
    if measured_x is not None and measured_y is not None:
        ax.scatter(measured_x, measured_y, color=C["green"], s=34, zorder=4, label=T["measurement_title"])
        ax.legend(frameon=False)
    ax.set_title(title, color=C["text"], fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(T["hour"], color=C["muted"])
    ax.set_ylabel(T["watts"], color=C["muted"])
    ax.tick_params(colors=C["muted"])
    for spine in ax.spines.values():
        spine.set_color(C["line"])
    ax.grid(True, color=C["grid"], alpha=.8, linewidth=.7)
    fig.tight_layout()
    return fig

x = np.linspace(start, end, 2401)
y = power(x, pmax) * panels
peak_total = pmax * panels
energy_wh = analytic_energy(start, end, pmax) * panels
energy_kwh = energy_wh / 1000
numeric_wh = integrate_trapezoid(start, end, pmax) * panels
average_power = energy_wh / (end - start)

# ------------------------------ OVERVIEW ------------------------------
if page == T["nav"][0]:
    st.markdown(
        f'<div class="sl-hero"><div class="sl-hero-content"><div class="sl-eyebrow">{T["course"]}</div>'
        f'<h1>Solar Lab – Integral Insights</h1><p>{T["intro"]}</p></div></div>',
        unsafe_allow_html=True,
    )
    quality_now = st.session_state.measurement_quality
    quality_value = f'{quality_now["score"]:.0f}%' if quality_now else "—"
    metric_cols = st.columns(4, gap="medium")
    with metric_cols[0]:
        st.metric(T["power"], f"{peak_total:,.0f} W")
    with metric_cols[1]:
        st.metric(T["energy"], f"{energy_wh:,.1f} Wh")
    with metric_cols[2]:
        st.metric(T["average"], f"{average_power:,.1f} W")
    with metric_cols[3]:
        st.metric("Calidad de datos" if lang == "es" else "Data quality", quality_value,
                  help="Se calcula después de cargar mediciones reales" if lang == "es" else "Calculated after uploading real measurements")
    st.write("")
    left_chart, right_chart = st.columns([1.25, 1], gap="medium")
    with left_chart:
        st.markdown(f'<div class="sl-panel"><h3>📈 {T["curve_title"]}</h3><p class="sl-section-sub">{T["curve_desc"]}</p></div>', unsafe_allow_html=True)
        fig = make_power_figure(x, y, T["curve_title"])
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with right_chart:
        st.markdown(
            f'<div class="sl-panel"><h3>📊 {("Energía acumulada" if lang == "es" else "Accumulated energy")}</h3>'
            f'<p class="sl-section-sub">{("Integral de potencia desde la hora inicial" if lang == "es" else "Integrated power since the start time")}</p></div>',
            unsafe_allow_html=True,
        )
        energy_curve = np.array([analytic_energy(start, float(t), pmax) * panels for t in x])
        efig, eax = plt.subplots(figsize=(8, 3.8), dpi=150)
        efig.patch.set_facecolor(C["plot"])
        eax.set_facecolor(C["plot"])
        eax.plot(x, energy_curve, color=C["green"], linewidth=3)
        eax.fill_between(x, energy_curve, color=C["green"], alpha=.15)
        eax.set_xlabel(T["hour"], color=C["muted"])
        eax.set_ylabel("Wh", color=C["muted"])
        eax.tick_params(colors=C["muted"])
        for spine in eax.spines.values():
            spine.set_color(C["line"])
        eax.grid(True, color=C["grid"], alpha=.8)
        efig.tight_layout()
        st.pyplot(efig, use_container_width=True)
        plt.close(efig)

    st.markdown(
        f'<div class="sl-section-title">🏅 {("Conclusiones analíticas" if lang == "es" else "Analytical conclusions")}</div>',
        unsafe_allow_html=True,
    )
    if lang == "es":
        conclusions = [
            ("Comportamiento de la potencia",
             f"La potencia alcanza su máximo de {peak_total:,.1f} W al mediodía. El modelo describe una curva simétrica en el intervalo seleccionado."),
            ("Energía generada",
             f"La energía estimada es {energy_wh:,.2f} Wh ({energy_kwh:,.4f} kWh), obtenida mediante la integral definida."),
            ("Confiabilidad y limitaciones",
             f"Las mediciones cargadas tienen un indicador de calidad de {quality_value}." if quality_now else
             "El resultado corresponde a un modelo hipotético. Carga un CSV para evaluar la calidad de mediciones reales."),
        ]
    else:
        conclusions = [
            ("Power behaviour",
             f"Power reaches its {peak_total:,.1f} W peak at noon. The model describes a symmetric curve over the selected interval."),
            ("Energy generated",
             f"Estimated energy is {energy_wh:,.2f} Wh ({energy_kwh:,.4f} kWh), calculated using the definite integral."),
            ("Reliability and limitations",
             f"Uploaded measurements have an indicative quality score of {quality_value}." if quality_now else
             "This result comes from a hypothetical model. Upload a CSV to assess real measurement quality."),
        ]
    conclusion_cols = st.columns(3, gap="medium")
    for col, (title, description), number in zip(conclusion_cols, conclusions, ["1", "2", "3"]):
        with col:
            st.markdown(
                f'<div class="sl-conclusion"><strong><span class="sl-index">{number}</span> {title}</strong>'
                f'<p>{description}</p></div>',
                unsafe_allow_html=True,
            )

    st.write("")
    action_a, action_b, action_c = st.columns([1.35, 1, 1], gap="medium")
    model_csv = pd.DataFrame({"hora": x, "potencia_w": y, "energia_acumulada_wh": energy_curve})
    csv_data = model_csv.to_csv(index=False).encode("utf-8-sig")
    chart_png = io.BytesIO()
    export_fig = make_power_figure(x, y, T["curve_title"])
    export_fig.savefig(chart_png, format="png", dpi=180, bbox_inches="tight")
    plt.close(export_fig)
    with action_a:
        st.button(
            "📑  " + ("Generar informe PDF + CSV" if lang == "es" else "Open PDF + CSV reports"),
            key="dashboard_report_btn", type="primary", use_container_width=True,
            on_click=set_page, args=(5,),
        )
    with action_b:
        st.download_button(
            "📥  " + ("Descargar datos CSV" if lang == "es" else "Download CSV data"),
            csv_data, "solar_lab_datos.csv", "text/csv", use_container_width=True,
        )
    with action_c:
        st.download_button(
            "🖼️  " + ("Descargar gráfica" if lang == "es" else "Download chart"),
            chart_png.getvalue(), "solar_lab_curva.png", "image/png", use_container_width=True,
        )
    feature_cols = st.columns(5, gap="small")
    feature_labels = [
        "∫  Integración analítica", "⌁  Ajuste de curvas", "⚗  Hipótesis",
        "◉  Geometría", "◷  Historial",
    ]
    for col, label in zip(feature_cols, feature_labels):
        with col:
            st.markdown(f'<div class="sl-feature">{label}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="sl-footer">Solar Lab – Integral Insights · {T["institution"]}<br>'
        'Foto: Vlad Burac · Unsplash</div>',
        unsafe_allow_html=True,
    )

# ------------------------------ MEASUREMENTS ------------------------------
elif page == T["nav"][1]:
    section_heading("03  /  EXPERIMENTAL DATA", T["measurement_title"], T["measurement_desc"])
    template = pd.DataFrame({
        "hora": ["06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00"],
        "potencia_w": [0, 133.33, 233.33, 300, 233.33, 133.33, 0],
    })
    st.download_button(
        T["template"],
        template.to_csv(index=False).encode("utf-8-sig"),
        "plantilla_mediciones_solar.csv",
        "text/csv",
    )
    uploaded = st.file_uploader(T["upload"], type=["csv"])
    if uploaded is not None:
        try:
            source = pd.read_csv(uploaded)
            if not {"hora", "potencia_w"}.issubset(source.columns):
                st.error(T["invalid_csv"])
            else:
                data = source[["hora", "potencia_w"]].copy()
                data["hora"] = data["hora"].apply(
                    lambda value: np.nan if pd.isna(value) else parse_hour(value)
                )
                data["potencia_w"] = pd.to_numeric(data["potencia_w"], errors="coerce")
                incomplete_count = int(data.isna().any(axis=1).sum())
                data = data.dropna().sort_values("hora")
                negative_count = int((data["potencia_w"] < 0).sum())
                duplicate_count = int(data.duplicated(subset=["hora"]).sum())
                outlier_count = 0
                if len(data) >= 4:
                    q1, q3 = data["potencia_w"].quantile([.25, .75])
                    iqr = q3 - q1
                    outlier_count = int(((data["potencia_w"] < q1 - 1.5 * iqr) | (data["potencia_w"] > q3 + 1.5 * iqr)).sum())
                if negative_count:
                    st.warning(T["negative_warning"])
                data = data[data["potencia_w"] >= 0].groupby("hora", as_index=False)["potencia_w"].mean()
                if len(data) < 2 or data["hora"].nunique() < 2:
                    st.error(T["need_rows"])
                    st.session_state.measurements = None
                    st.session_state.measurement_quality = None
                else:
                    integrated = float(np.trapezoid(data["potencia_w"], data["hora"]) if hasattr(np, "trapezoid") else np.trapz(data["potencia_w"], data["hora"]))
                    score = max(0, 100 - min(30, incomplete_count * 5) - min(25, duplicate_count * 5) - min(25, negative_count * 10) - min(20, outlier_count * 3))
                    data["energia_acumulada_wh"] = np.r_[0, np.cumsum(np.diff(data["hora"]) * (data["potencia_w"].to_numpy()[1:] + data["potencia_w"].to_numpy()[:-1]) / 2)]
                    st.session_state.measurements = data
                    st.session_state.measurement_quality = {
                        "incomplete": incomplete_count, "duplicates": duplicate_count,
                        "negative": negative_count, "outliers": outlier_count,
                        "score": score, "energy": integrated,
                    }
        except (ValueError, TypeError, ZeroDivisionError):
            st.error(T["invalid_time"])
        except Exception as exc:
            st.error(f"{T['invalid_csv']} ({exc})")

    measured = st.session_state.measurements
    quality = st.session_state.measurement_quality
    if measured is not None and quality is not None:
        section_heading("04  /  DATA QUALITY", T["quality"], T["quality_note"])
        q1, q2, q3, q4, q5 = st.columns(5)
        q1.metric(T["valid"], len(measured))
        q2.metric(T["incomplete"], quality["incomplete"])
        q3.metric(T["duplicates"], quality["duplicates"])
        q4.metric(T["negative"], quality["negative"])
        q5.metric(T["score"], f'{quality["score"]:.0f}/100')
        st.metric(T["measured_energy"], f'{quality["energy"]:,.3f} Wh')
        st.dataframe(measured, use_container_width=True, hide_index=True)
        fig = make_power_figure(measured["hora"], measured["potencia_w"], T["measurement_curve"], fill=False)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        if len(measured) >= 3:
            mx = measured["hora"].to_numpy(dtype=float)
            my = measured["potencia_w"].to_numpy(dtype=float)
            coeff = np.polyfit(mx, my, 2)
            fit_x = np.linspace(mx.min(), mx.max(), 240)
            fit_y = np.polyval(coeff, fit_x)
            residual = my - np.polyval(coeff, mx)
            ss_res = float(np.sum(residual ** 2))
            ss_tot = float(np.sum((my - my.mean()) ** 2))
            r_squared = 1 - ss_res / ss_tot if ss_tot else 1.0
            fit_fig, fit_ax = plt.subplots(figsize=(10, 3.8), dpi=150)
            fit_fig.patch.set_facecolor(C["plot"])
            fit_ax.set_facecolor(C["plot"])
            fit_ax.scatter(mx, my, color=C["green"], s=42, label=T["measurement_title"])
            fit_ax.plot(fit_x, fit_y, color=C["blue"], linewidth=2.8, label=T["curve_fit"])
            fit_ax.set_title(T["measurement_curve"], color=C["text"], fontsize=13, fontweight="bold")
            fit_ax.set_xlabel(T["hour"], color=C["muted"])
            fit_ax.set_ylabel(T["watts"], color=C["muted"])
            fit_ax.tick_params(colors=C["muted"])
            fit_ax.grid(True, color=C["grid"], alpha=.8)
            fit_ax.legend(frameon=False)
            fit_fig.tight_layout()
            st.pyplot(fit_fig, use_container_width=True)
            plt.close(fit_fig)
            st.metric(T["r2"], f"{r_squared:.4f}")
        else:
            st.info("Se requieren al menos tres horas distintas para calcular un ajuste cuadrático." if lang == "es" else "At least three distinct times are required for a quadratic fit.")
    else:
        st.info(T["no_measurements"])

# ------------------------------ INTEGRAL CALCULUS ------------------------------
elif page == T["nav"][2]:
    section_heading("05  /  MATHEMATICAL MODEL", T["integral_title"], T["integral_desc"])
    st.latex(r"P(t)=P_{\max}\left(1-\frac{(t-12)^2}{36}\right)")
    st.latex(r"E=\int_a^b P(t)\,dt")
    result_cols = st.columns(3)
    result_cols[0].metric(T["analytic"], f"{energy_wh:,.4f} Wh")
    result_cols[1].metric(T["numeric"], f"{numeric_wh:,.4f} Wh")
    result_cols[2].metric(T["difference"], f"{abs(energy_wh-numeric_wh):.6f} Wh")
    with st.expander("Desarrollo matemático / Mathematical derivation", expanded=True):
        st.markdown("**" + T["function"] + "**")
        st.latex(r"P(t)=P_{\max}-\frac{P_{\max}}{36}(t-12)^2")
        st.markdown("**" + T["antiderivative"] + "**")
        st.latex(r"F(t)=P_{\max}\left(t-\frac{(t-12)^3}{108}\right)")
        st.markdown("**" + T["analytic"] + "**")
        st.latex(r"E=F(b)-F(a)")
        st.caption(f'{T["steps"]}: 2400')
    st.divider()
    section_heading("06  /  GEOMETRY", T["geometry"], T["area_note"])
    g1, g2 = st.columns(2)
    with g1:
        panel_length = st.number_input(T["length_panel"], min_value=.1, max_value=5.0, value=1.7, step=.05)
    with g2:
        panel_width = st.number_input(T["width_panel"], min_value=.1, max_value=5.0, value=1.0, step=.05)
    st.metric(T["panel_area"], f"{panel_length * panel_width * panels:.3f} m²")
    st.latex(r"A_{\mathrm{total}}=N\cdot L\cdot W")
    st.divider()
    st.markdown("**Volumen de revolución / Volume of revolution**")
    v1, v2, v3 = st.columns(3)
    with v1:
        r0 = st.number_input(T["radius"], min_value=.001, max_value=1.0, value=.1, step=.01)
    with v2:
        slope = st.number_input(T["slope"], min_value=0.0, max_value=1.0, value=.05, step=.01)
    with v3:
        length = st.number_input(T["length"], min_value=.1, max_value=10.0, value=2.0, step=.1)
    volume = math.pi * (r0**2 * length + r0 * slope * length**2 + slope**2 * length**3 / 3)
    st.metric(T["volume"], f"{volume:.6f} m³")
    st.latex(r"V=\pi\int_0^L(r_0+mx)^2\,dx")

# ------------------------------ HYPOTHESES ------------------------------
elif page == T["nav"][3]:
    section_heading("07  /  SCENARIO LAB", T["hyp_title"], T["hyp_desc"])
    variation = st.slider(T["variation"], min_value=-50, max_value=50, value=0, step=5)
    hyp_peak = pmax * (1 + variation / 100)
    hyp_energy = analytic_energy(start, end, hyp_peak) * panels
    baseline_energy = energy_wh
    hc1, hc2, hc3 = st.columns(3)
    hc1.metric(T["base"], f"{baseline_energy/1000:,.4f} kWh")
    hc2.metric(T["hypothesis"], f"{hyp_energy/1000:,.4f} kWh")
    hc3.metric("Cambio" if lang == "es" else "Change", f"{variation:+d}%")
    hx = np.linspace(start, end, 1000)
    hfig, hax = plt.subplots(figsize=(10, 3.8), dpi=150)
    hfig.patch.set_facecolor(C["plot"])
    hax.set_facecolor(C["plot"])
    hax.plot(hx, power(hx, pmax)*panels, color=C["muted"], linewidth=2.4, label=T["base"])
    hax.plot(hx, power(hx, hyp_peak)*panels, color=C["blue"], linewidth=3, label=T["hypothesis"])
    hax.fill_between(hx, power(hx, hyp_peak)*panels, color=C["blue"], alpha=.12)
    hax.set_xlabel(T["hour"], color=C["muted"]); hax.set_ylabel(T["watts"], color=C["muted"])
    hax.set_title(T["hyp_title"], color=C["text"], fontweight="bold")
    hax.tick_params(colors=C["muted"]); hax.grid(True, color=C["grid"], alpha=.8); hax.legend(frameon=False)
    hfig.tight_layout()
    st.pyplot(hfig, use_container_width=True)
    plt.close(hfig)
    if st.button(T["save"], type="primary"):
        st.session_state.history.append({
            T["date"]: datetime.now().strftime("%Y-%m-%d %H:%M"),
            T["variation_col"]: variation,
            T["count_col"]: int(panels),
            T["energy_col"]: hyp_energy / 1000,
            T["interval"]: f"{start:g}:00–{end:g}:00",
        })
        st.success(T["saved"])

# ------------------------------ HISTORY ------------------------------
elif page == T["nav"][4]:
    section_heading("08  /  SESSION RECORD", T["history_title"], T["history_desc"])
    if st.session_state.history:
        history_frame = pd.DataFrame(st.session_state.history)
        st.dataframe(history_frame, use_container_width=True, hide_index=True)
        st.download_button(T["csv"], history_frame.to_csv(index=False).encode("utf-8-sig"), "historial_solar_lab.csv", "text/csv")
        if st.button(T["clear"]):
            st.session_state.history = []
            st.rerun()
    else:
        st.info(T["empty_history"])

# ------------------------------ REPORTS ------------------------------
elif page == T["nav"][5]:
    section_heading("09  /  EXPORT CENTER", T["report_title"], T["report_desc"])
    report_rows = [
        ["Indicador" if lang == "es" else "Metric", "Resultado" if lang == "es" else "Result"],
        [T["panels"], str(panels)],
        [T["power"], f"{peak_total:.2f} W"],
        [T["period"], f"{start:g}:00 – {end:g}:00"],
        [T["analytic"], f"{energy_wh:.4f} Wh"],
        [T["numeric"], f"{numeric_wh:.4f} Wh"],
        [T["difference"], f"{abs(energy_wh-numeric_wh):.6f} Wh"],
    ]
    report_buffer = io.BytesIO()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="SolarTitle", parent=styles["Title"], textColor=colors.HexColor("#1769AA"), fontSize=20, leading=24))
    story = []
    if logo_uni.exists():
        story.append(RLImage(str(logo_uni), width=5.0*cm, height=1.35*cm, kind="proportional"))
    story += [
        Paragraph("Solar Lab – Integral Insights", styles["SolarTitle"]),
        Paragraph(T["subtitle"], styles["Heading2"]),
        Spacer(1, 8),
        Paragraph(T["institution"], styles["BodyText"]),
        Spacer(1, 8),
        Paragraph("<b>" + T["team"] + ":</b> " + " · ".join(TEAM), styles["BodyText"]),
        Spacer(1, 14),
    ]
    report_table = Table(report_rows, colWidths=[7.2*cm, 8.2*cm])
    report_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1769AA")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), .45, colors.HexColor("#D4DFEC")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F2F6FB")]),
        ("PADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story += [
        report_table, Spacer(1, 14),
        Paragraph("Conclusión" if lang == "es" else "Conclusion", styles["Heading2"]),
        Paragraph(T["integral_desc"], styles["BodyText"]),
        Spacer(1, 8),
        Paragraph(T["caution"], styles["BodyText"]),
    ]
    SimpleDocTemplate(report_buffer, pagesize=A4, rightMargin=1.7*cm, leftMargin=1.7*cm, topMargin=1.5*cm, bottomMargin=1.5*cm).build(story)
    pdf_bytes = report_buffer.getvalue()

    grid = np.linspace(start, end, 241)
    export = pd.DataFrame({
        "hora": grid,
        "potencia_w": power(grid, pmax) * panels,
        "energia_acumulada_wh": [analytic_energy(start, t, pmax) * panels for t in grid],
    })
    csv_bytes = export.to_csv(index=False).encode("utf-8-sig")
    package = io.BytesIO()
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("informe_solar_lab.pdf", pdf_bytes)
        archive.writestr("datos_solar_lab.csv", csv_bytes)
        archive.writestr("README.txt", T["institution"] + "\n" + "Solar Lab – Integral Insights")
    dl1, dl2, dl3 = st.columns(3)
    with dl1:
        st.download_button(T["pdf"], pdf_bytes, "informe_solar_lab_integral_insights.pdf", "application/pdf", type="primary", use_container_width=True)
    with dl2:
        st.download_button(T["csv"], csv_bytes, "datos_solar_lab.csv", "text/csv", use_container_width=True)
    with dl3:
        st.download_button(T["zip"], package.getvalue(), "solar_lab_paquete_completo.zip", "application/zip", use_container_width=True)
    st.markdown(f'<div class="note-card">{T["caution"]}</div>', unsafe_allow_html=True)

st.divider()
st.markdown(
    f'<div class="footer">Solar Lab – Integral Insights · {T["institution"]}<br>© Proyecto académico · Ingeniería Multimedia</div>',
    unsafe_allow_html=True,
)
