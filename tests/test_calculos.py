import numpy as np

def potencia(t, pmax):
    return pmax * (1 - ((np.asarray(t) - 12) ** 2) / 36)

def antiderivada(t, pmax):
    return pmax * (t - ((t - 12) ** 3) / 108)

def energia_analitica(a, b, pmax):
    return antiderivada(b, pmax) - antiderivada(a, pmax)

def test_energia_analitica_jornada_completa():
    assert abs(energia_analitica(6, 18, 300) - 2400) < 1e-9

def test_integracion_trapecio_aproxima_energia_analitica():
    x = np.linspace(6, 18, 2001)
    y = potencia(x, 300)
    numerica = np.trapezoid(y, x) if hasattr(np, "trapezoid") else np.trapz(y, x)
    assert abs(numerica - energia_analitica(6, 18, 300)) < 0.01

def test_energia_se_escala_con_numero_de_paneles():
    assert abs(energia_analitica(6, 18, 300) * 4 - 9600) < 1e-9
