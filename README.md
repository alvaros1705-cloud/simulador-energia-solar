# Simulador de aprovechamiento de energía solar

Aplicación web académica desarrollada en Python con Streamlit.

## Funcionalidades
- Modelo cuadrático de potencia entre las 6:00 y las 18:00.
- Cálculo analítico de energía mediante el Teorema Fundamental del Cálculo.
- Verificación numérica mediante la regla compuesta del trapecio.
- Modificación de potencia máxima, intervalo horario y cantidad de paneles.
- Comparación de escenarios hipotéticos de -20 %, base y +20 %.
- Cálculo de superficie rectangular de paneles.
- Cálculo de volumen de un sólido de revolución por el método de discos.
- Carga opcional de mediciones reales en CSV, separadas del modelo hipotético.
- Descarga de resumen de resultados en CSV.

## Ejecución local

1. Instalar Python 3.10 o superior.
2. Abrir una terminal en esta carpeta.
3. Instalar dependencias:

   `pip install -r requirements.txt`

4. Ejecutar:

   `streamlit run app.py`

5. Abrir en el navegador la dirección local que indique Streamlit (normalmente http://localhost:8501).

## Formato para mediciones reales (opcional)

El CSV debe contener al menos estas dos columnas:

- `hora`: hora decimal (por ejemplo, 8.5 para las 8:30).
- `potencia_w`: potencia medida en vatios.

No introducir valores inventados. Esta sección es independiente de la simulación teórica.

## Modelo matemático utilizado

`P(t) = Pmax * (1 - (t - 12)^2 / 36)`, para `6 <= t <= 18`.

Con `Pmax = 300 W`, la función alcanza 300 W a las 12:00 y es cero a las 6:00 y a las 18:00. La energía para un intervalo `[a,b]` se calcula integrando la función. Para un panel entre las 6:00 y las 18:00, el resultado analítico es 2400 Wh = 2.4 kWh.

## Advertencias académicas

- Los parámetros iniciales son hipotéticos y no representan mediciones de una instalación real.
- Los factores 0.8, 1.0 y 1.2 son escenarios de variación de potencia máxima, no eficiencias medidas.
- El cálculo de superficie es un ejercicio geométrico rectangular y no equivale al área bajo la curva de potencia.
- El sólido de revolución es ilustrativo; no es un diseño estructural validado.
