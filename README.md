# Solar Lab – Integral Insights

Aplicación académica interactiva para el análisis de energía solar mediante cálculo integral, desarrollada con Python y Streamlit para la asignatura Cálculo Integral del programa de Ingeniería Multimedia de la Universidad Simón Bolívar.

## Identidad académica
- Universidad Simón Bolívar.
- Programa: Ingeniería Multimedia.
- Asignatura: Cálculo Integral.
- Equipo:
  - Sara Gáfaro Salamanca
  - Leidy Stephania Delgado Galvis
  - Angel David Carrascal Claro
  - Samuel David Jaimes Estrada
- Se conservan los logotipos institucionales existentes en `assets/`.

## Funcionalidades
1. Interfaz en español (Colombia) e inglés (USA).
2. Modo claro principal y modo oscuro alternativo.
3. Panel con potencia máxima, energía estimada, potencia promedio y diferencia de integración.
4. Modelo cuadrático de potencia entre 6:00 y 18:00: `P(t)=Pmax(1-(t-12)^2/36)`.
5. Integración analítica y verificación numérica mediante regla del trapecio.
6. Comparación de escenarios de -20 %, base y +20 %.
7. Carga de mediciones CSV con columnas `hora` y `potencia_w`.
8. Revisión orientativa de datos incompletos, duplicados, potencias negativas y posibles valores atípicos.
9. Integración de mediciones, energía acumulada y ajuste cuadrático con R².
10. Laboratorio de hipótesis para variar la potencia máxima.
11. Historial de escenarios durante la sesión.
12. Ejercicios geométricos de área rectangular y volumen de revolución.
13. Exportación de informe PDF, datos CSV y paquete ZIP.

## Instalación local
Python 3.10 o superior:

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue
La aplicación está preparada para Streamlit Community Cloud, conectada al repositorio existente `alvaros1705-cloud/simulador-energia-solar`, rama `main`, archivo principal `app.py`.

## Consideraciones
Los parámetros iniciales son hipotéticos y no representan mediciones certificadas. El indicador de calidad es orientativo. El ajuste cuadrático no debe extrapolarse fuera del intervalo observado. El historial se conserva solo durante la sesión actual y no es almacenamiento permanente.
