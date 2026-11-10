# Simulador de aprovechamiento de energía solar

Aplicación web académica desarrollada en Python con Streamlit para el proyecto de Cálculo Integral del programa de Ingeniería Multimedia de la Universidad Simón Bolívar.

## Identidad institucional
- Encabezado con el logo de la Universidad Simón Bolívar.
- Pie de página con los cuatro integrantes del equipo, programa académico y asignatura.
- Logo de Ingeniería Multimedia con variantes para tema claro y oscuro.
- Selector de tema claro/oscuro.
- Identidad visual con paleta azul, verde y violeta, gradientes suaves, tarjetas y botones personalizados.
- Diseño adaptable de Streamlit para pantallas de computador, tableta y celular.

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

## Archivos del repositorio
- `app.py`: aplicación principal.
- `requirements.txt`: dependencias.
- `plantilla_mediciones_reales.csv`: plantilla para mediciones reales.
- `assets/`: logos institucionales y del programa.

## Publicación en Streamlit Community Cloud
1. Subir todos los archivos y la carpeta `assets` al repositorio de GitHub, conservando la estructura.
2. En Streamlit Community Cloud, seleccionar el repositorio.
3. Elegir la rama `main`.
4. Indicar `app.py` como archivo principal.
5. Desplegar la aplicación.

## Modelo matemático
`P(t) = Pmax * (1 - (t - 12)^2 / 36)`, para `6 <= t <= 18`.

Con `Pmax = 300 W`, la función alcanza 300 W a las 12:00 y es cero a las 6:00 y a las 18:00. La energía para un intervalo `[a,b]` se calcula integrando la función. Para un panel entre las 6:00 y las 18:00, el resultado analítico es 2400 Wh = 2.4 kWh.

## Advertencias académicas
- Los parámetros iniciales son hipotéticos y no representan mediciones de una instalación real.
- Los factores 0.8, 1.0 y 1.2 son escenarios de variación de potencia máxima, no eficiencias medidas.
- El cálculo de superficie es un ejercicio geométrico rectangular y no equivale al área bajo la curva de potencia.
- El sólido de revolución es ilustrativo; no es un diseño estructural validado.
- La interfaz aprovecha el diseño adaptable de Streamlit; debe comprobarse en navegadores y tamaños de pantalla reales antes de su entrega definitiva.
