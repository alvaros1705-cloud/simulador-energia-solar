import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

st.set_page_config(
    page_title="Simulador de energía solar | Cálculo Integral",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ Simulador de aprovechamiento de la energía solar")
st.caption("Proyecto de aula · Cálculo Integral · Modelo matemático hipotético")

st.info(
    "Este simulador trabaja con un modelo idealizado. Sus resultados son estimaciones "
    "matemáticas y no mediciones de un panel fotovoltaico real."
)

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
    # Regla compuesta del trapecio, para contrastar con el cálculo analítico.
    return float(np.trapezoid(y, x))

def volume_of_revolution(r0, slope, length):
    # V = pi * integral_0^L (r0 + slope*x)^2 dx
    integral = (
        r0**2 * length
        + r0 * slope * length**2
        + (slope**2 * length**3) / 3
    )
    return math.pi * integral

with st.sidebar:
    st.header("Parámetros del modelo")
    n_panels = st.number_input("Cantidad de paneles iguales", min_value=1, max_value=100, value=1, step=1)
    pmax = st.slider("Potencia máxima por panel (W)", min_value=50, max_value=600, value=300, step=10)
    start = st.slider("Hora inicial del intervalo", min_value=6.0, max_value=12.0, value=6.0, step=0.5)
    end = st.slider("Hora final del intervalo", min_value=12.0, max_value=18.0, value=18.0, step=0.5)
    st.caption("La función base tiene potencia cero a las 6:00 y a las 18:00, y alcanza su máximo a las 12:00.")

if start >= end:
    st.error("La hora final debe ser mayor que la hora inicial.")
    st.stop()

st.header("1. Modelo de potencia y energía acumulada")
st.latex(r"P(t)=P_{\\max}\\left(1-\\frac{(t-12)^2}{36}\\right),\\quad 6\\leq t\\leq18")
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
c1.metric("Potencia máxima por panel", f"{pmax:,.0f} W")
c2.metric("Energía por panel", f"{energy_one:,.2f} Wh", f"{energy_one/1000:,.3f} kWh")
c3.metric("Energía total", f"{energy_total:,.2f} Wh", f"{energy_total/1000:,.3f} kWh")
c4.metric("Diferencia analítica-numérica", f"{difference:,.6f} Wh")

x = np.linspace(6, 18, 500)
y = power(x, pmax)
fig, ax = plt.subplots()
ax.plot(x, y, label="Potencia del modelo")
xf = np.linspace(start, end, 300)
ax.fill_between(xf, power(xf, pmax), alpha=0.25, label="Área integrada")
ax.axvline(start, linestyle="--", linewidth=1, label=f"Inicio: {start:g}:00")
ax.axvline(end, linestyle="--", linewidth=1, label=f"Final: {end:g}:00")
ax.set_xlabel("Hora del día")
ax.set_ylabel("Potencia (W)")
ax.set_title("Variación de la potencia durante la jornada")
ax.set_xlim(6, 18)
ax.grid(True, alpha=0.25)
ax.legend()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

with st.expander("Verificación matemática: Teorema Fundamental del Cálculo"):
    st.latex(r"F(t)=P_{\\max}\\left(t-\\frac{(t-12)^3}{108}\\right)")
    st.latex(
        rf"E_{{1\\ panel}}=F({end:g})-F({start:g})"
        rf"={energy_one:,.4f}\\;Wh"
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

st.header("2. Comparación de escenarios hipotéticos")
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

st.header("3. Cálculo geométrico: superficie de los paneles")
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
a1.metric("Superficie por panel", f"{area_one:.4f} m²")
a2.metric("Superficie total", f"{area_all:.4f} m²")
st.caption("Este ejercicio calcula el área rectangular mediante largo × ancho. No es el área bajo la curva de potencia.")

st.header("4. Cálculo geométrico: volumen por el método de discos")
st.write("Se utiliza el perfil ilustrativo del documento: r(x) = r₀ + m·x, para 0 ≤ x ≤ L.")
v1, v2, v3 = st.columns(3)
with v1:
    r0 = st.number_input("Radio inicial r₀ (m)", min_value=0.001, max_value=1.0, value=0.10, step=0.01, format="%.3f")
with v2:
    slope = st.number_input("Pendiente m", min_value=0.0, max_value=1.0, value=0.05, step=0.01, format="%.3f")
with v3:
    length = st.number_input("Longitud L (m)", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
volume = volume_of_revolution(r0, slope, length)
st.metric("Volumen del sólido de revolución", f"{volume:.6f} m³")
st.latex(r"V=\\pi\\int_0^L(r_0+mx)^2\\,dx")
xx = np.linspace(0, length, 200)
rr = r0 + slope * xx
fig2, ax2 = plt.subplots()
ax2.plot(xx, rr, label="Perfil del radio r(x)")
ax2.fill_between(xx, 0, rr, alpha=0.2)
ax2.set_xlabel("Longitud x (m)")
ax2.set_ylabel("Radio r(x) (m)")
ax2.set_title("Perfil utilizado para el sólido de revolución")
ax2.grid(True, alpha=0.25)
ax2.legend()
st.pyplot(fig2, use_container_width=True)
plt.close(fig2)
st.caption("Este volumen es un ejercicio geométrico ilustrativo. No constituye un diseño estructural ni representa el volumen real de un soporte comercial.")

st.header("5. Registro opcional de mediciones reales")
st.warning(
    "Esta sección es independiente del modelo hipotético. Solo debe utilizarse si el equipo obtiene "
    "mediciones reales con instrumentos adecuados y bajo condiciones seguras. No inventen ni completen datos faltantes."
)
uploaded = st.file_uploader("Cargar CSV con columnas hora y potencia_w (opcional)", type=["csv"])
if uploaded is not None:
    try:
        measured = pd.read_csv(uploaded)
        required = {"hora", "potencia_w"}
        if not required.issubset(set(measured.columns)):
            st.error("El CSV debe incluir exactamente las columnas requeridas: hora y potencia_w (puede contener otras columnas).")
        else:
            measured = measured[["hora", "potencia_w"]].dropna().sort_values("hora")
            if len(measured) < 2:
                st.error("Se necesitan al menos dos mediciones válidas.")
            else:
                st.dataframe(measured, use_container_width=True, hide_index=True)
                fig3, ax3 = plt.subplots()
                ax3.plot(measured["hora"], measured["potencia_w"], marker="o")
                ax3.set_xlabel("Hora")
                ax3.set_ylabel("Potencia medida (W)")
                ax3.set_title("Mediciones reales cargadas por el equipo")
                ax3.grid(True, alpha=0.25)
                st.pyplot(fig3, use_container_width=True)
                plt.close(fig3)
                st.caption("La integración de mediciones discretas depende del intervalo y de la calidad de los datos. No se mezclan con el resultado hipotético.")
    except Exception as exc:
        st.error(f"No fue posible leer el archivo: {exc}")

st.divider()
st.subheader("Resumen del escenario actual")
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
csv = summary.to_csv(index=False).encode("utf-8")
st.download_button("Descargar resumen del escenario (CSV)", data=csv, file_name="resumen_simulacion_energia_solar.csv", mime="text/csv")

st.caption("Proyecto académico. Los resultados dependen de los supuestos y parámetros seleccionados por el usuario.")
