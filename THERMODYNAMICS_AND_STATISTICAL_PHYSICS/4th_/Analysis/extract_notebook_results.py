import pandas as pd
import pint
from scipy.stats import linregress
from pathlib import Path


def main() -> None:
    unit = pint.UnitRegistry()

    # Part 1: Calorimeter heat capacity (as in calculate.ipynb)
    m = 267 * unit.gram
    m1 = 272 * unit.gram
    m2 = 279 * unit.gram

    T1 = unit.Quantity(22, unit.degree_Celsius).to(unit.kelvin)
    T2 = unit.Quantity(65, unit.degree_Celsius).to(unit.kelvin)
    T = unit.Quantity(33, unit.degree_Celsius).to(unit.kelvin)

    c_w = 4.18 * unit.joule / (unit.gram * unit.kelvin)
    c_w_n = 1 * unit.joule / (unit.gram * unit.kelvin)
    c_w = {0: c_w, 1: c_w_n}[1]

    C_k = c_w * (m2 * (T2 - T) + m1 * (T1 - T)) / (T - T1)

    C_manufacturer_calorimeter = float(78) * unit.joule / unit.kelvin
    C_manufacturer_calorimeter_uncertainty = 2 * unit.joule / unit.kelvin

    # Load data
    analysis_dir = Path(__file__).resolve().parent
    data_dir = analysis_dir.parent / "DATA"
    data1 = pd.read_csv(data_dir / "DataPart2.csv")
    data2 = pd.read_csv(data_dir / "DataPart3.csv")

    magnitude = lambda x: x.magnitude if isinstance(x, pint.Quantity) else x
    tounit = lambda x: lambda y: y.to(x)

    # Part 2: Environment effect
    T_0 = float(281) * unit.kelvin
    delta_symbol = "Δ"
    mw = float(218) * unit.gram

    data1["t(min)"] = [t * unit.minute for t in data1["t(min)"]]
    data1["T(K)"] = [temp * unit.kelvin for temp in data1["T(K)"]]
    data1[f"{delta_symbol}T"] = [round(temp - T_0, 3) for temp in data1["T(K)"]]
    data1[f"{delta_symbol}Q"] = [
        round((mw * c_w + C_manufacturer_calorimeter) * dT, 3)
        for dT in data1[f"{delta_symbol}T"]
    ]
    data1["t(seconds)"] = data1["t(min)"].map(tounit(unit.second))

    slope_DT, intercept_DT, r_value_DT, p_value_DT, std_err_DT = linregress(
        data1["t(seconds)"].map(magnitude),
        data1[f"{delta_symbol}T"].map(magnitude),
    )
    slope_Q, intercept_Q, r_value_Q, p_value_Q, std_err_Q = linregress(
        data1["t(seconds)"].map(magnitude),
        data1[f"{delta_symbol}Q"].map(magnitude),
    )
    dQ_env_dt = slope_Q * unit.joule / unit.second

    # Part 3: Thermal conductivity of Cu
    data2["t(min)"] = [t * unit.minute for t in data2["t(min)"]]
    data2["T(K)"] = [temp * unit.kelvin for temp in data2["T(K)"]]
    data2["DeltaT(rod)(K)"] = [dtemp * unit.kelvin for dtemp in data2["DeltaT(rod)(K)"]]
    data2[f"{delta_symbol}T"] = [round(temp - T_0, 3) for temp in data2["T(K)"]]
    data2["t(seconds)"] = data2["t(min)"].map(tounit(unit.second))

    mw3 = (634 - 267) * unit.gram
    data2[f"{delta_symbol}Qtotal"] = [
        round((mw3 * c_w + C_manufacturer_calorimeter) * dT, 3)
        for dT in data2[f"{delta_symbol}T"]
    ]

    slope_Q_total_t, intercept_Q_total_t, r_value_Q_total_t, p_value_Q_total_t, std_err_Q_total_t = linregress(
        data2["t(seconds)"].map(magnitude),
        data2[f"{delta_symbol}Qtotal"].map(magnitude),
    )
    dQtot_dt = slope_Q_total_t * unit.joule / unit.second

    dT_mean = (data2["DeltaT(rod)(K)"].map(magnitude)).mean()
    dx = (24.5 * unit.centimeter).to(unit.meter)
    dT_dx = (dT_mean * unit.kelvin) / dx

    A = 4.91e-4 * unit.meter**2
    dQ_dt = dQtot_dt - dQ_env_dt
    lambda_Cu = (dQ_dt / (A * dT_dx)).to(unit.watt / (unit.meter * unit.kelvin))

    # Part 4: Electrical conductivity of Al
    A4 = 4.91e-4 * unit.meter**2
    l4 = 0.42 * unit.meter
    V = 0.88 * unit.volt
    I = 0.393 * unit.ampere
    R = (V / I).to(unit.ohm)
    sigma_Al = (l4 / (R * A4)).to(1 / (unit.ohm * unit.meter))

    print("=== Part 1 ===")
    print(f"c_w_used = {c_w}")
    print(f"C_k = {C_k:.6g}")
    print(
        f"C_k (manufacturer) = {C_manufacturer_calorimeter:.6g} ± {C_manufacturer_calorimeter_uncertainty:.6g}"
    )

    print("\n=== Part 2 ===")
    print(f"T0 = {T_0}")
    print(f"mw = {mw}")
    print(f"slope(ΔT vs t) = {slope_DT:.8g} K/s, R2 = {r_value_DT**2:.6g}")
    print(f"slope(ΔQ_env vs t) = {slope_Q:.8g} J/s, R2 = {r_value_Q**2:.6g}")
    print(f"dQ_env/dt = {dQ_env_dt:.6g}")

    print("\n=== Part 3 ===")
    print(f"mw_part3 = {mw3}")
    print(f"slope(ΔQ_total vs t) = {slope_Q_total_t:.8g} J/s, R2 = {r_value_Q_total_t**2:.6g}")
    print(f"dQ_total/dt = {dQtot_dt:.6g}")
    print(f"dT_mean(rod) = {dT_mean:.6g} K")
    print(f"dx_used = {dx:.6g}")
    print(f"A = {A:.6g}")
    print(f"dQ_net/dt = {dQ_dt:.6g}")
    print(f"lambda_Cu = {lambda_Cu:.6g}")

    print("\n=== Part 4 ===")
    print(f"V = {V}, I = {I}, R = {R:.6g}")
    print(f"l_used = {l4:.6g}")
    print(f"A = {A4:.6g}")
    print(f"sigma_Al = {sigma_Al:.6g}")


if __name__ == "__main__":
    main()
