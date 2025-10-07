"""Objetivo: script y futura app para el cálculo de la Dapp de cloruros y el cálculo de vida útil
de un hormigón"""

import numpy as np
from scipy.special import erfc
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Datos experimentales (ejemplo)
x_mm = np.array([0, 5, 10, 15, 25, 35])  # mm
C_exp = np.array([1.20, 0.85, 0.60, 0.35, 0.15, 0.08])  # %

# Parámetros conocidos
t_years = 1
t_seconds = t_years * 365.25 * 24 * 3600

# Modelo teórico de Fick
def C_teo(x_mm, Dapp, Csup, Cini):
    x_m = x_mm / 1000.0
    return Cini + (Csup - Cini) * erfc(x_m / (2 * np.sqrt(Dapp * t_seconds)))

# Estimaciones iniciales (importante para convergencia)
D0 = 1e-12  # m²/s
Csup0 = 1.2
Cini0 = 0.05

# Ajuste no lineal
popt, pcov = curve_fit(C_teo, x_mm, C_exp, p0=[D0, Csup0, Cini0])
Dapp, Csup_fit, Cini_fit = popt

print(f"Dapp ajustado = {Dapp:.3e} m²/s")
print(f"Csup ajustado = {Csup_fit:.3f} %")
print(f"Cini ajustado = {Cini_fit:.3f} %")

# Graficar ajuste
x_fit = np.linspace(0, 40, 200)
plt.scatter(x_mm, C_exp, label="Experimental", color='red')
plt.plot(x_fit, C_teo(x_fit, *popt), label="Ajuste Fick", color='blue')
plt.xlabel("Profundidad (mm)")
plt.ylabel("Concentración de Cl⁻ (%)")
plt.legend()
plt.title("Ajuste del perfil de cloruros y cálculo de Dapp")
plt.grid(True)
plt.show()
