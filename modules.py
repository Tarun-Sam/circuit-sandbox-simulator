# modules.py
# Contains all the engineering calculation modules for the tutor.

import matplotlib.pyplot as plt
import numpy as np
from helpers import get_float, get_binary_input, parse_engineering_notation

# ==============================================================================
# SECTION 1: CORE CIRCUIT ANALYSIS MODULES
# ==============================================================================

def ohms_law():
    """Calculates V, I, or R based on user input."""
    print("\n--- Ohm's Law (V=IR) ---")
    print("Enter exactly TWO known values. Leave the unknown blank.")
    V_str = input("Enter voltage V (e.g., 12, 5k): ")
    I_str = input("Enter current I (e.g., 2.5m, 10u): ")
    R_str = input("Enter resistance R (e.g., 1.2k, 4M): ")
    V = parse_engineering_notation(V_str) if V_str else None
    I = parse_engineering_notation(I_str) if I_str else None
    R = parse_engineering_notation(R_str) if R_str else None
    known_values = sum(val is not None for val in [V, I, R])
    if known_values != 2:
        print("Error: Please provide exactly TWO known values.")
        return
    if V is None: V = I * R; print(f"Calculated Voltage V = {I} A * {R} Ω = {V:.4f} V")
    elif I is None:
        if R == 0: print("Error: Resistance cannot be zero."); return
        I = V / R; print(f"Calculated Current I = {V} V / {R} Ω = {I:.4f} A")
    elif R is None:
        if I == 0: print("Error: Current cannot be zero."); return
        R = V / I; print(f"Calculated Resistance R = {V} V / {I} A = {R:.4f} Ω")
    print()

def rc_circuit():
    """Analyzes charging/discharging of an RC circuit."""
    print("\n--- RC Circuit ---")
    choice = input("Select mode: (1) Charging or (2) Discharging? ")
    
    R = get_float("Enter resistance R (Ω): ")
    C = get_float("Enter capacitance C (F): ")
    tau = R * C
    print(f"Time constant τ = R*C = {tau:.4f} s")
    t_sim = get_float(f"Enter time to simulate (s) (e.g., 5*τ = {5*tau:.2f}s): ")
    t = np.linspace(0, t_sim, 500)

    if choice == '1':
        V_supply = get_float("Enter supply voltage Vs (V): ")
        Vc = V_supply * (1 - np.exp(-t / tau))
        title = "Capacitor Charging in RC Circuit"
        print(f"Voltage across capacitor at t={t_sim}s: {Vc[-1]:.4f} V")
    elif choice == '2':
        V_initial = get_float("Enter initial capacitor voltage V0 (V): ")
        Vc = V_initial * np.exp(-t / tau)
        title = "Capacitor Discharging in RC Circuit"
        print(f"Voltage across capacitor at t={t_sim}s: {Vc[-1]:.4f} V")
    else:
        print("Invalid choice.")
        return

    if input("Plot voltage vs time? (yes/no): ").lower() == "yes":
        plt.plot(t, Vc)
        plt.title(title); plt.xlabel("Time (s)"); plt.ylabel("Voltage (V)")
        plt.grid(True); plt.show()
    print()

def rl_circuit():
    """Analyzes the energizing of an RL circuit."""
    print("\n--- RL Circuit: Current through Inductor ---")
    R = get_float("Enter resistance R (Ω): ")
    L = get_float("Enter inductance L (H): ")
    V = get_float("Enter supply voltage V (V): ")
    tau = L / R
    print(f"Time constant τ = L/R = {tau:.4f} s")
    t_sim = get_float(f"Enter time to simulate (s) (e.g., 5*τ = {5*tau:.2f}s): ")
    t = np.linspace(0, t_sim, 500)
    IL = (V/R) * (1 - np.exp(-t / tau))
    
    print(f"Inductor current at t={t_sim}s: {IL[-1]:.4f} A")

    if input("Plot current vs time? (yes/no): ").lower() == "yes":
        plt.plot(t, IL)
        plt.title("Inductor Current in RL Circuit"); plt.xlabel("Time (s)"); plt.ylabel("Current (A)")
        plt.grid(True); plt.show()
    print()

def ac_series():
    """Performs comprehensive analysis of a series RLC circuit."""
    print("\n--- AC Series RLC Circuit ---")
    R = get_float("Enter resistance R (Ω): ")
    L = get_float("Enter inductance L (H): ")
    C = get_float("Enter capacitance C (F): ")
    V_peak = get_float("Enter peak voltage V_peak (V): ")
    f = get_float("Enter frequency f (Hz): ")

    omega = 2 * np.pi * f
    Xl = omega * L
    Xc = 1 / (omega * C) if C > 0 else float('inf')
    X_total = Xl - Xc
    Z = np.sqrt(R**2 + X_total**2)
    V_rms = V_peak / np.sqrt(2)
    I_peak = V_peak / Z
    I_rms = V_rms / Z
    phase_angle_rad = np.arctan2(X_total, R)
    phase_angle_deg = np.degrees(phase_angle_rad)

    print("\n--- Impedance & Phase Analysis ---")
    print(f"Angular Frequency ω = {omega:.2f} rad/s")
    print(f"Inductive Reactance Xl = {Xl:.2f} Ω")
    print(f"Capacitive Reactance Xc = {Xc:.2f} Ω")
    print(f"Total Impedance Z = {Z:.2f} Ω at {phase_angle_deg:.2f}°")
    print(f"RMS Current I_rms = {I_rms:.4f} A")
    
    if L > 0 and C > 0:
        f0 = 1 / (2 * np.pi * np.sqrt(L*C))
        Q_factor = (1/R) * np.sqrt(L/C)
        BW = f0 / Q_factor
        print("\n--- Resonance Analysis ---")
        print(f"Resonant Frequency f0 = {f0:.2f} Hz")
        print(f"Quality Factor Q = {Q_factor:.2f}")
        print(f"Bandwidth BW = {BW:.2f} Hz")

    P_real = I_rms**2 * R
    Q_reactive = I_rms**2 * X_total
    S_apparent = V_rms * I_rms
    PF = P_real / S_apparent
    print("\n--- Power Analysis ---")
    print(f"Real Power (P) = {P_real:.4f} W")
    print(f"Reactive Power (Q) = {Q_reactive:.4f} VAR")
    print(f"Apparent Power (S) = {S_apparent:.4f} VA")
    print(f"Power Factor (PF) = {PF:.4f} ({'lagging' if Xl > Xc else 'leading'})")

    if input("\nPlot AC waveforms? (yes/no): ").lower() == "yes":
        t = np.linspace(0, 3/f, 500)
        v = V_peak * np.sin(omega*t)
        i = I_peak * np.sin(omega*t - phase_angle_rad)
        plt.figure(figsize=(10, 6))
        plt.plot(t, v, label="Voltage (V)")
        plt.plot(t, i, label="Current (A)", linestyle='--')
        plt.title("AC Voltage and Current Waveforms"); plt.xlabel("Time (s)"); plt.ylabel("Amplitude")
        plt.legend(); plt.grid(True); plt.show()
    print()

# ==============================================================================
# SECTION 2: FILTERS & SIGNAL PROCESSING MODULES
# ==============================================================================

def rc_low_pass_filter():
    """Analyzes an RC low-pass filter and plots its Bode response."""
    print("\n--- RC Low-Pass Filter ---")
    R = get_float("Enter resistance R (Ω): ")
    C = get_float("Enter capacitance C (F): ")
    fc = 1 / (2 * np.pi * R * C)
    print(f"The cutoff frequency (-3dB point) is: {fc:.2f} Hz")
    
    if input("Plot Bode (magnitude) plot? (yes/no): ").lower() == "yes":
        freq = np.logspace(1, int(np.log10(fc) + 3), 500)
        H_mag = 1 / np.sqrt(1 + (freq / fc)**2)
        H_db = 20 * np.log10(H_mag)
        plt.figure(figsize=(10, 6)); plt.semilogx(freq, H_db)
        plt.title('Bode Plot - Magnitude Response'); plt.xlabel('Frequency (Hz)'); plt.ylabel('Magnitude (dB)')
        plt.grid(which='both', linestyle='--')
        plt.axvline(fc, color='r', linestyle='--', label=f'Cutoff Freq = {fc:.2f} Hz')
        plt.axhline(-3, color='g', linestyle=':', label='-3 dB')
        plt.legend(); plt.show()
    print()

def laplace_transfer_function():
    """Generates the Laplace transfer function for a series RLC circuit."""
    print("\n--- RLC Circuit Laplace Transfer Function H(s) ---")
    R = get_float("Enter resistance R (Ω): ")
    L = get_float("Enter inductance L (H): ")
    C = get_float("Enter capacitance C (F): ")
    
    print("\nWhere is the output voltage Vout taken?")
    print("1. Across the Resistor (Band-pass response)")
    print("2. Across the Inductor (High-pass response)")
    print("3. Across the Capacitor (Low-pass response)")
    choice = input("Enter your choice (1-3): ")

    d2 = 1.0
    d1 = R/L
    d0 = 1/(L*C)
    denominator_str = f"s^2 + {d1:.2f}s + {d0:.2e}"

    if choice == '1':
        n1 = R/L
        print(f"\nH(s) = ({n1:.2f}s) / ({denominator_str})")
    elif choice == '2':
        print(f"\nH(s) = (s^2) / ({denominator_str})")
    elif choice == '3':
        n0 = 1/(L*C)
        print(f"\nH(s) = ({n0:.2e}) / ({denominator_str})")
    else:
        print("Invalid choice.")
    print()

# ==============================================================================
# SECTION 3: SEMICONDUCTOR & DEVICE MODULES
# ==============================================================================

def diode_forward():
    """Provides the approximate forward voltage for a silicon diode."""
    print("\n--- Silicon Diode (Approximation) ---")
    I = get_float("Enter forward current I (A): ")
    print(f"For a simple model, the forward voltage drop Vf is ≈ 0.7 V for I = {I} A.")
    print("(Note: This is an approximation. Real Vf varies slightly with current.)")
    print()

def zener_regulator():
    """Designs a simple Zener diode voltage regulator circuit."""
    print("\n--- Zener Diode Voltage Regulator Design ---")
    Vin = get_float("Enter input voltage Vin (V): ")
    Vz = get_float("Enter desired Zener voltage Vz (V): ")
    RL = get_float("Enter load resistance RL (Ω): ")

    if Vin <= Vz:
        print("Error: Input voltage must be greater than Zener voltage.")
        return

    IL_max = Vz / RL
    IZ_test = 0.1 * IL_max
    Is = IL_max + IZ_test
    Rs = (Vin - Vz) / Is
    
    IZ_noload = (Vin - Vz) / Rs
    PZ_max = Vz * IZ_noload

    print("\n--- Design Results ---")
    print(f"Max load current IL(max) = {IL_max*1000:.2f} mA")
    print(f"Required Series Resistor Rs = {Rs:.2f} Ω")
    print(f"Power dissipated by Rs = {(Is**2 * Rs):.4f} W")
    print("\n--- Zener Diode Specification ---")
    print(f"The Zener diode must have a power rating of at least {PZ_max:.4f} W.")
    print()
    
def bjt_ic():
    """Calculates BJT collector current based on base current and beta."""
    print("\n--- BJT Collector Current (Active Region) ---")
    Ib = get_float("Enter base current Ib (A): ")
    beta = get_float("Enter current gain β (default 100): ", allow_blank=True, default=100)
    Ic = Ib * beta
    print(f"Collector current Ic = Ib * β = {Ib} A * {beta} = {Ic:.4f} A")
    print()

def bjt_ce_amplifier():
    """Performs DC and AC analysis of a common-emitter amplifier."""
    print("\n--- BJT Common-Emitter Amplifier Analysis ---")
    print("Uses a standard voltage divider biasing configuration.")
    
    Vcc = get_float("Enter supply voltage Vcc (V): ")
    R1 = get_float("Enter resistor R1 (Ω): ")
    R2 = get_float("Enter resistor R2 (Ω): ")
    Rc = get_float("Enter collector resistor Rc (Ω): ")
    Re = get_float("Enter emitter resistor Re (Ω): ")
    beta = get_float("Enter transistor current gain β (default 150): ", allow_blank=True, default=150)
    
    Vb = Vcc * (R2 / (R1 + R2))
    Ve = Vb - 0.7
    Ie = Ve / Re
    Ic = Ie
    Vc = Vcc - (Ic * Rc)
    Vce = Vc - Ve
    
    print("\n--- DC Analysis (Q-Point) ---")
    print(f"Base Voltage Vb = {Vb:.2f} V")
    print(f"Collector Current Icq = {Ic*1000:.2f} mA")
    print(f"Collector-Emitter Voltage Vceq = {Vce:.2f} V")
    
    if Vce < 0.2:
        print("WARNING: Transistor is likely in saturation. AC analysis may be invalid.")
    
    re_prime = 26e-3 / Ie
    Zin_base = beta * (re_prime + Re)
    R_parallel = (R1 * R2) / (R1 + R2)
    Zin_total = (Zin_base * R_parallel) / (Zin_base + R_parallel)
    Av = -Rc / re_prime
    
    print("\n--- AC Small-Signal Analysis (Approximation) ---")
    print(f"Internal Emitter Resistance r_e' = {re_prime:.2f} Ω")
    print(f"Total Input Impedance Zin = {Zin_total/1000:.2f} kΩ")
    print(f"Voltage Gain Av (assuming bypassed Re) = {Av:.2f}")
    print()

# ==============================================================================
# SECTION 4: DIGITAL LOGIC MODULE
# ==============================================================================

def logic_gate_simulator():
    """Simulates the output of basic digital logic gates."""
    print("\n--- Digital Logic Gate Simulator ---")
    print("Select a gate:")
    print("1. AND  | 5. NAND")
    print("2. OR   | 6. NOR")
    print("3. NOT  | 7. XOR")
    print("4. BUF")
    choice = input("Enter choice: ")

    if choice in ['1', '2', '5', '6', '7']:
        a = get_binary_input("Enter input A (0 or 1): ")
        b = get_binary_input("Enter input B (0 or 1): ")
        if choice == '1': print(f"Result: {a} AND {b} = {int(a and b)}")
        if choice == '2': print(f"Result: {a} OR {b} = {int(a or b)}")
        if choice == '5': print(f"Result: {a} NAND {b} = {int(not (a and b))}")
        if choice == '6': print(f"Result: {a} NOR {b} = {int(not (a or b))}")
        if choice == '7': print(f"Result: {a} XOR {b} = {int(a ^ b)}")
    elif choice in ['3', '4']:
        a = get_binary_input("Enter input A (0 or 1): ")
        if choice == '3': print(f"Result: NOT {a} = {int(not a)}")
        if choice == '4': print(f"Result: BUF {a} = {a}")
    else:
        print("Invalid choice.")
    print()