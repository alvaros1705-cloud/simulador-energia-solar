import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from pathlib import Path

# ------------------------------------------------------------
# Configuración general
# ------------------------------------------------------------
st.set_page_config(
    page_title="Simulador de energía solar | Ingeniería Multimedia",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

# ------------------------------------------------------------
# Funciones matemáticas
# ------------------------------------------------------------
def power(t, pmax):
    """Potencia del modelo cuadrático, válida entre 6:00 y 18:00."""
    return pmax * (1 - ((t - 12) ** 2) / 36)


def antiderivative(t, pmax):
    """Antiderivada de P(t) = Pmax * (1 - (t-12)^2/36)."""
    return pmax * (t - ((t - 12) ** 3) / 108)


def analytical_energy(a, b, pmax):
    return antiderivative(b, pmax) - antiderivative(a, pmax)


def numerical_energy(a, b, pmax, steps=2001):
    x = np.linspace(a, b, steps)
    y = power(x, pmax)
    # Compatibilidad con distintas versiones de NumPy.
    if hasattr(np, "trapezoid"):
        return float(np.trapezoid(y, x))
    return float(np.trapz(y, x))


def volume_of_revolution(r0, slope, length):
    # V = pi * integral_0^L (r0 + slope*x)^2 dx
    integral = (
        r0**2 * length
        + r0 * slope * length**2
        + (slope**2 * length**3) / 3
    )
    return math.pi * integral


# ------------------------------------------------------------
# Tema claro / oscuro
# ------------------------------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark_mode = st.toggle(
    "🌗 Cambiar tema visual",
    value=st.session_state.dark_mode,
    key="theme_switch",
    help="Cambia la apariencia de la aplicación sin modificar los cálculos."
)
st.session_state.dark_mode = dark_mode

if dark_mode:
    bg = "#071426"
    panel = "#10243A"
    text = "#F3F7FF"
    muted = "#B4C5DA"
    accent = "#38BDF8"
    grid = "#29445F"
    logo_multimedia = ASSETS_DIR / "logo_ingenieria_multimedia_oscuro.png"
    theme_name = "oscuro"
    glow_blue = "rgba(37,99,235,.22)"
    glow_green = "rgba(16,185,129,.15)"
    glow_violet = "rgba(139,92,246,.20)"
else:
    bg = "#F5F7FF"
    panel = "#FFFFFF"
    text = "#17243B"
    muted = "#52627A"
    accent = "#315FEA"
    grid = "#DCE4F2"
    logo_multimedia = ASSETS_DIR / "logo_ingenieria_multimedia_claro.png"
    theme_name = "claro"
    glow_blue = "rgba(37,99,235,.11)"
    glow_green = "rgba(16,185,129,.10)"
    glow_violet = "rgba(139,92,246,.11)"

st.markdown(
    f"""
    <style>
    :root {{
      --azul: #315FEA; --verde: #0F9F79; --violeta: #8052D6;
    }}
    .stApp {{
      background:
        radial-gradient(ellipse at 8% 2%, rgba(49,95,234,.13), transparent 35%),
        radial-gradient(ellipse at 92% 8%, rgba(128,82,214,.12), transparent 34%),
        radial-gradient(ellipse at 55% 92%, rgba(15,159,121,.10), transparent 38%),
        linear-gradient(135deg, {bg} 0%, #F0F6FF 48%, #F7F2FF 100%);
      color: {text};
    }}
    [data-testid="stHeader"] {{ background: transparent; }}
    [data-testid="stSidebar"] {{
      background: linear-gradient(155deg, {panel}, #EEF4FF 58%, #F5F0FF);
      border-right: 1px solid {grid};
    }}
    [data-testid="stMarkdownContainer"], [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"], p, label, h1, h2, h3, h4 {{ color: {text}; }}
    [data-testid="stCaptionContainer"], .stCaption {{ color: {muted} !important; }}
    [data-testid="stAlert"] {{ border-radius: 15px; border: 1px solid {grid}; }}
    div[data-testid="stMetric"] {{
      background: linear-gradient(145deg, {panel}, rgba(235,243,255,.92), rgba(246,240,255,.88));
      border: 1px solid {grid}; border-top: 3px solid transparent;
      border-image: linear-gradient(90deg, #315FEA, #0F9F79, #8052D6) 1;
      padding: 14px 15px; border-radius: 15px;
      box-shadow: 0 8px 24px rgba(35,55,95,.07);
    }}
    div[data-testid="stDataFrame"], div[data-testid="stTable"] {{
      border: 1px solid {grid}; border-radius: 13px; overflow: hidden;
    }}
    .brand-divider {{
      border: 0; height: 3px; border-radius: 8px;
      background: linear-gradient(90deg, #315FEA, #0F9F79, #8052D6);
      margin: .65rem 0 1.35rem 0;
    }}
    .university-subtitle {{
      color: {text}; font-size: clamp(1.05rem, 2vw, 1.45rem);
      font-weight: 800; letter-spacing: .025em; margin: 0;
      background: linear-gradient(90deg, #315FEA, #0F9F79, #8052D6);
      -webkit-background-clip: text; background-clip: text; color: transparent;
    }}
    .hero-panel {{
      padding: clamp(1.1rem, 3vw, 2rem); border-radius: 22px;
      border: 1px solid {grid};
      background: linear-gradient(115deg, rgba(49,95,234,.12), rgba(15,159,121,.09), rgba(128,82,214,.12));
      box-shadow: 0 14px 38px rgba(35,55,95,.08); margin: .4rem 0 1rem 0;
    }}
    .hero-kicker {{
      text-transform: uppercase; letter-spacing: .16em; font-size: .72rem;
      font-weight: 800; color: {accent}; margin-bottom: .45rem;
    }}
    .project-title {{
      font-size: clamp(1.45rem, 3.3vw, 2.35rem); line-height: 1.15;
      font-weight: 900; margin-bottom: .45rem; color: {text};
    }}
    .hero-subtitle {{ color: {muted}; font-size: clamp(.88rem, 1.5vw, 1.02rem); }}
    .footer-card {{
      background: linear-gradient(125deg, {panel}, rgba(49,95,234,.07), rgba(15,159,121,.055), rgba(128,82,214,.08));
      border: 1px solid {grid}; border-radius: 18px;
      border-top: 3px solid transparent;
      border-image: linear-gradient(90deg, #315FEA, #0F9F79, #8052D6) 1;
      padding: 1.1rem 1.3rem; margin-top: 1rem;
      box-shadow: 0 10px 28px rgba(35,55,95,.07);
    }}
    .footer-heading {{ color: {accent}; font-weight: 850; margin-bottom: .45rem; }}
    .student-list {{ line-height: 1.8; margin: 0; }}
    .stButton > button, .stDownloadButton > button,
    [data-testid="stBaseButton-primary"], [data-testid="stBaseButton-secondary"] {{
      color: #FFFFFF !important;
      background: linear-gradient(100deg, #315FEA, #0F9F79, #8052D6) !important;
      border: 1px solid rgba(49,95,234,.18) !important; border-radius: 11px !important;
      font-weight: 750 !important; box-shadow: 0 5px 16px rgba(49,95,234,.20);
      transition: transform .15s ease, filter .15s ease;
    }}
    .stButton > button p, .stDownloadButton > button p,
    [data-testid="stBaseButton-primary"] p, [data-testid="stBaseButton-secondary"] p {{
      color: #FFFFFF !important;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover,
    [data-testid="stBaseButton-primary"]:hover, [data-testid="stBaseButton-secondary"]:hover {{
      color: #FFFFFF !important; filter: brightness(1.08); transform: translateY(-1px);
    }}
    [data-testid="stSlider"] [role="slider"] {{ border-color: #315FEA; }}
    [data-testid="stToggle"] label, [data-testid="stCheckbox"] label,
    [data-testid="stRadio"] label {{ color: {text} !important; }}
    @media (max-width: 700px) {{
      .university-subtitle {{ font-size: 1rem; }}
      .footer-card {{ padding: .85rem; }} .hero-panel {{ border-radius: 15px; }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# Encabezado institucional
left, right = st.columns([2.0, 3.0], vertical_alignment="center")
with left:
    if (ASSETS_DIR / "logo_universidad_simon_bolivar.png").exists():
        st.image(str(ASSETS_DIR / "logo_universidad_simon_bolivar.png"), use_container_width=True)
with right:
    st.markdown(
        '<p class="university-subtitle">Proyecto académico de aula</p>',
        unsafe_allow_html=True
    )

st.markdown('<hr class="brand-divider">', unsafe_allow_html=True)

# ------------------------------------------------------------
# Título y presentación
# ------------------------------------------------------------
st.markdown(
    """
    <section class="hero-panel">
      <div class="hero-kicker">☀️ Laboratorio interactivo · Matemáticas aplicadas</div>
      <div class="project-title">Simulador de aprovechamiento de la energía solar</div>
      <div class="hero-subtitle">⚡ Cálculo Integral &nbsp;·&nbsp; 🎨 Ingeniería Multimedia &nbsp;·&nbsp; 🧮 Modelo matemático hipotético</div>
    </section>
    """,
    unsafe_allow_html=True
)
st.info(
    "Este simulador trabaja con un modelo idealizado. Sus resultados son estimaciones "
    "matemáticas y no mediciones de un panel fotovoltaico real."
)

# ------------------------------------------------------------
# Parámetros del modelo
# ------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Parámetros del modelo")
    n_panels = st.number_input("🔋 Cantidad de paneles iguales", min_value=1, max_value=100, value=1, step=1)
    pmax = st.slider("⚡ Potencia máxima por panel (W)", min_value=50, max_value=600, value=300, step=10)
    start = st.slider("🌅 Hora inicial del intervalo", min_value=6.0, max_value=12.0, value=6.0, step=0.5)
    end = st.slider("🌇 Hora final del intervalo", min_value=12.0, max_value=18.0, value=18.0, step=0.5)
    st.caption("La función base tiene potencia cero a las 6:00 y a las 18:00, y alcanza su máximo a las 12:00.")
    st.divider()
    st.caption(f"🎨 Tema visual activo: {theme_name}")

if start >= end:
    st.error("La hora final debe ser mayor que la hora inicial.")
    st.stop()

# Colores de gráficas según el tema
plot_bg = bg
plot_fg = text
plot_grid = grid
plot_accent = accent

# ------------------------------------------------------------
# 1. Potencia y energía
# ------------------------------------------------------------
st.header("1. 📈 Modelo de potencia y energía acumulada")
st.latex(r"P(t)=P_{\max}\left(1-\frac{(t-12)^2}{36}\right),\quad 6\leq t\leq18")
st.write(
    "La función representa una jornada idealizada: la potencia aumenta durante la mañana, "
    "alcanza su máximo al mediodía y disminuye durante la tarde."
)

energy_one = analytical_energy(start, end, pmax)
energy_total = energy_one * n_panels
numeric_one = numerical_energy(start, end, pmax)
numeric_total = numeric_one * n_panels
difference = abs(energy_one - numeric_one)

c1, c2, c3, c4 = st.columns(4)
c1.metric("⚡ Potencia máxima por panel", f"{pmax:,.0f} W")
c2.metric("🔆 Energía por panel", f"{energy_one:,.2f} Wh", f"{energy_one/1000:,.3f} kWh")
c3.metric("🔋 Energía total", f"{energy_total:,.2f} Wh", f"{energy_total/1000:,.3f} kWh")
c4.metric("🧮 Diferencia analítica-numérica", f"{difference:,.6f} Wh")

x = np.linspace(6, 18, 500)
y = power(x, pmax)
fig, ax = plt.subplots(figsize=(10, 4.5))
fig.patch.set_facecolor(plot_bg)
ax.set_facecolor(plot_bg)
ax.plot(x, y, color="#2563EB", linewidth=2.8, label="Potencia del modelo")
xf = np.linspace(start, end, 300)
ax.fill_between(xf, power(xf, pmax), color="#10B981", alpha=0.28, label="Área integrada")
ax.axvline(start, color="#E07A5F", linestyle="--", linewidth=1.2, label=f"Inicio: {start:g}:00")
ax.axvline(end, color="#6C8EBF", linestyle="--", linewidth=1.2, label=f"Final: {end:g}:00")
ax.set_xlabel("Hora del día", color=plot_fg)
ax.set_ylabel("Potencia (W)", color=plot_fg)
ax.set_title("Variación de la potencia durante la jornada", color=plot_fg)
ax.set_xlim(6, 18)
ax.grid(True, alpha=0.25, color=plot_grid)
ax.tick_params(colors=plot_fg)
for spine in ax.spines.values():
    spine.set_color(plot_grid)
legend = ax.legend()
for label in legend.get_texts():
    label.set_color(plot_fg)
st.pyplot(fig, use_container_width=True)
plt.close(fig)

with st.expander("📚 Verificación matemática: Teorema Fundamental del Cálculo"):
    st.latex(r"F(t)=P_{\max}\left(t-\frac{(t-12)^3}{108}\right)")
    st.latex(
        rf"E_{{1\ panel}}=F({end:g})-F({start:g})"
        rf"={energy_one:,.4f}\;Wh"
    )
    st.write(
        f"Para {n_panels} panel(es), bajo el supuesto de paneles iguales y condiciones equivalentes, "
        f"la energía estimada es {energy_total:,.4f} Wh ({energy_total/1000:,.4f} kWh)."
    )
    st.write(
        f"Verificación numérica por regla compuesta del trapecio: {numeric_total:,.4f} Wh. "
        f"Diferencia absoluta frente al cálculo analítico para un panel: {difference:,.8f} Wh."
    )
    st.caption("La diferencia numérica puede variar ligeramente según el número de intervalos utilizado.")

# ------------------------------------------------------------
# 2. Escenarios
# ------------------------------------------------------------
st.header("2. 🧪 Comparación de escenarios hipotéticos")
st.write("Los factores 0,80; 1,00 y 1,20 representan variaciones hipotéticas de la potencia máxima, no eficiencias medidas.")
scenario_rows = []
for factor in [0.8, 1.0, 1.2]:
    e = analytical_energy(start, end, pmax * factor) * n_panels
    scenario_rows.append({
        "Escenario": {0.8: "−20 %", 1.0: "Base", 1.2: "+20 %"}[factor],
        "Factor": factor,
        "Potencia máxima por panel (W)": pmax * factor,
        "Energía total (Wh)": e,
        "Energía total (kWh)": e / 1000
    })
scenario_df = pd.DataFrame(scenario_rows)
st.dataframe(scenario_df, use_container_width=True, hide_index=True)
st.bar_chart(scenario_df.set_index("Escenario")[["Energía total (kWh)"]])

# ------------------------------------------------------------
# 3. Área de paneles
# ------------------------------------------------------------
st.header("3. 📐 Cálculo geométrico: superficie de los paneles")
g1, g2, g3 = st.columns(3)
with g1:
    panel_length = st.number_input("Largo de un panel (m)", min_value=0.1, max_value=5.0, value=1.70, step=0.05)
with g2:
    panel_width = st.number_input("Ancho de un panel (m)", min_value=0.1, max_value=5.0, value=1.00, step=0.05)
with g3:
    area_count = st.number_input("Cantidad de paneles para superficie", min_value=1, max_value=100, value=int(n_panels), step=1)
area_one = panel_length * panel_width
area_all = area_one * area_count
a1, a2 = st.columns(2)
a1.metric("📏 Superficie por panel", f"{area_one:.4f} m²")
a2.metric("🧩 Superficie total", f"{area_all:.4f} m²")
st.caption("Este ejercicio calcula el área rectangular mediante largo × ancho. No es el área bajo la curva de potencia.")

# ------------------------------------------------------------
# 4. Volumen por discos
# ------------------------------------------------------------
st.header("4. 🌀 Cálculo geométrico: volumen por el método de discos")
st.write("Se utiliza el perfil ilustrativo del documento: r(x) = r₀ + m·x, para 0 ≤ x ≤ L.")
v1, v2, v3 = st.columns(3)
with v1:
    r0 = st.number_input("Radio inicial r₀ (m)", min_value=0.001, max_value=1.0, value=0.10, step=0.01, format="%.3f")
with v2:
    slope = st.number_input("Pendiente m", min_value=0.0, max_value=1.0, value=0.05, step=0.01, format="%.3f")
with v3:
    length = st.number_input("Longitud L (m)", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
volume = volume_of_revolution(r0, slope, length)
st.metric("📦 Volumen del sólido de revolución", f"{volume:.6f} m³")
st.latex(r"V=\pi\int_0^L(r_0+mx)^2\,dx")
xx = np.linspace(0, length, 200)
rr = r0 + slope * xx
fig2, ax2 = plt.subplots(figsize=(9, 3.8))
fig2.patch.set_facecolor(plot_bg)
ax2.set_facecolor(plot_bg)
ax2.plot(xx, rr, color="#8B5CF6", linewidth=2.7, label="Perfil del radio r(x)")
ax2.fill_between(xx, 0, rr, color="#8B5CF6", alpha=0.20)
ax2.set_xlabel("Longitud x (m)", color=plot_fg)
ax2.set_ylabel("Radio r(x) (m)", color=plot_fg)
ax2.set_title("Perfil utilizado para el sólido de revolución", color=plot_fg)
ax2.grid(True, alpha=0.25, color=plot_grid)
ax2.tick_params(colors=plot_fg)
for spine in ax2.spines.values():
    spine.set_color(plot_grid)
legend2 = ax2.legend()
for label in legend2.get_texts():
    label.set_color(plot_fg)
st.pyplot(fig2, use_container_width=True)
plt.close(fig2)
st.caption("Este volumen es un ejercicio geométrico ilustrativo. No constituye un diseño estructural ni representa el volumen real de un soporte comercial.")

# ------------------------------------------------------------
# 5. Mediciones reales
# ------------------------------------------------------------
st.header("5. 🧾 Registro opcional de mediciones reales")
st.warning(
    "Esta sección es independiente del modelo hipotético. Solo debe utilizarse si el equipo obtiene "
    "mediciones reales con instrumentos adecuados y bajo condiciones seguras. No inventen ni completen datos faltantes."
)
uploaded = st.file_uploader("📂 Cargar CSV con columnas hora y potencia_w (opcional)", type=["csv"])
if uploaded is not None:
    try:
        measured = pd.read_csv(uploaded)
        required = {"hora", "potencia_w"}
        if not required.issubset(set(measured.columns)):
            st.error("El CSV debe incluir las columnas requeridas: hora y potencia_w.")
        else:
            measured = measured[["hora", "potencia_w"]].dropna().sort_values("hora")
            if len(measured) < 2:
                st.error("Se necesitan al menos dos mediciones válidas.")
            else:
                st.dataframe(measured, use_container_width=True, hide_index=True)
                fig3, ax3 = plt.subplots(figsize=(9, 3.8))
                fig3.patch.set_facecolor(plot_bg)
                ax3.set_facecolor(plot_bg)
                ax3.plot(measured["hora"], measured["potencia_w"], marker="o", color="#10B981")
                ax3.set_xlabel("Hora", color=plot_fg)
                ax3.set_ylabel("Potencia medida (W)", color=plot_fg)
                ax3.set_title("Mediciones reales cargadas por el equipo", color=plot_fg)
                ax3.grid(True, alpha=0.25, color=plot_grid)
                ax3.tick_params(colors=plot_fg)
                for spine in ax3.spines.values():
                    spine.set_color(plot_grid)
                st.pyplot(fig3, use_container_width=True)
                plt.close(fig3)
                st.caption("La integración de mediciones discretas depende del intervalo y de la calidad de los datos. No se mezclan con el resultado hipotético.")
    except Exception as exc:
        st.error(f"No fue posible leer el archivo: {exc}")

# ------------------------------------------------------------
# Resumen descargable
# ------------------------------------------------------------
st.divider()
st.subheader("6. 📋 Resumen del escenario actual")
summary = pd.DataFrame([{
    "Paneles": n_panels,
    "Pmax por panel (W)": pmax,
    "Intervalo": f"{start:g}:00–{end:g}:00",
    "Energía por panel (kWh)": energy_one / 1000,
    "Energía total (kWh)": energy_total / 1000,
    "Área total (m²)": area_all,
    "Volumen (m³)": volume
}])
st.dataframe(summary, use_container_width=True, hide_index=True)
csv = summary.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "⬇️ Descargar resumen del escenario (CSV)",
    data=csv,
    file_name="resumen_simulacion_energia_solar.csv",
    mime="text/csv",
    use_container_width=True
)

# ------------------------------------------------------------
# Pie institucional y créditos
# ------------------------------------------------------------
st.markdown('<hr class="brand-divider">', unsafe_allow_html=True)
st.markdown('<div class="footer-card">', unsafe_allow_html=True)
footer_left, footer_right = st.columns([3.5, 1], vertical_alignment="center")
with footer_left:
    st.markdown('<div class="footer-heading">👩‍🎓 Equipo de trabajo</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="student-list">
        • Sara Gáfaro Salamanca<br>
        • Leidy Stephania Delgado Galvis<br>
        • Angel David Carrascal Claro<br>
        • Samuel David Jaimes Estrada
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style="margin-top:.8rem; margin-bottom:0;">
        <strong>🎓 Programa:</strong> Ingeniería Multimedia<br>
        <strong>📘 Asignatura:</strong> Cálculo Integral
        </p>
        """,
        unsafe_allow_html=True
    )
with footer_right:
    if logo_multimedia.exists():
        st.image(str(logo_multimedia), width=140)
st.markdown('</div>', unsafe_allow_html=True)
st.caption("Universidad Simón Bolívar · Proyecto académico de aula · Los resultados dependen de los supuestos y parámetros seleccionados.")
