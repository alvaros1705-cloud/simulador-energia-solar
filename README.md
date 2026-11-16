# Solar Lab – Integral Insights

Laboratorio web académico para modelar y analizar la energía solar mediante cálculo integral. Desarrollado en Python y Streamlit para la asignatura **Cálculo Integral** del programa de **Ingeniería Multimedia** de la **Universidad Simón Bolívar**.

## Identidad institucional
- Universidad Simón Bolívar.
- Programa: Ingeniería Multimedia.
- Asignatura: Cálculo Integral.
- Integrantes:
  1. Sara Gáfaro Salamanca
  2. Leidy Stephania Delgado Galvis
  3. Angel David Carrascal Claro
  4. Samuel David Jaimes Estrada
- Se conservan los tres recursos gráficos institucionales originales dentro de `assets/`.

## Experiencia de usuario
- Diseño académico con navegación superior y panel lateral de parámetros.
- Tema claro institucional como presentación principal y modo oscuro alternativo.
- Contraste de texto, controles, métricas y tablas definido mediante `.streamlit/config.toml` y estilos de interfaz.
- Español (Colombia) e inglés (USA).
- Interfaz adaptable al ancho de pantalla.

## Herramientas académicas
1. Modelo cuadrático de potencia entre 6:00 y 18:00: `P(t)=Pmax(1-(t-12)^2/36)`.
2. Cálculo analítico de la integral definida y verificación numérica mediante regla del trapecio.
3. Indicadores de potencia máxima, potencia promedio y energía estimada.
4. Comparación de escenarios de -20 %, base y +20 %.
5. Carga de mediciones CSV con columnas `hora` y `potencia_w`.
6. Revisión orientativa de datos incompletos, horas duplicadas, potencias negativas y posibles valores atípicos.
7. Integración de mediciones, energía acumulada y ajuste cuadrático con R².
8. Laboratorio de hipótesis para variar la potencia máxima e historial de escenarios de la sesión.
9. Aplicaciones geométricas: área de paneles y volumen de revolución.
10. Exportación de informe PDF, datos CSV y paquete ZIP.

## Ejecución local
Requiere Python 3.10 o superior.

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
Repositorio: `alvaros1705-cloud/simulador-energia-solar`  
Rama: `main`  
Archivo principal: `app.py`  
Configuración visual: `.streamlit/config.toml`

La aplicación se encuentra conectada a Streamlit Community Cloud.

## Validación
El flujo de GitHub Actions ubicado en `.github/workflows/validate.yml` ejecuta:
- Compilación de sintaxis de `app.py`.
- Pruebas de regresión matemática para la energía analítica y la integración numérica.

## Consideraciones académicas
Los valores iniciales representan una aproximación didáctica, no mediciones certificadas. El indicador de calidad de datos es orientativo. El ajuste cuadrático no debe extrapolarse fuera del intervalo observado. El historial se conserva durante la sesión de la aplicación.
