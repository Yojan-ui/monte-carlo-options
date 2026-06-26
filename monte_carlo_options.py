import numpy as np
from scipy.stats import norm
from tabulate import tabulate
import time

S0 = 100.0
K  = 105.0
T  = 1.0
r  = 0.05
sigma = 0.20
N_PATHS = 100_000
N_STEPS = 252

def black_scholes(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def monte_carlo_option(S, K, T, r, sigma, n_paths, n_steps, option_type="call"):
    dt = T / n_steps
    Z = np.random.standard_normal((n_paths, n_steps))
    log_returns = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
    S_T = S * np.exp(np.cumsum(log_returns, axis=1))[:, -1]
    payoffs = np.maximum(S_T - K, 0) if option_type == "call" else np.maximum(K - S_T, 0)
    discounted = np.exp(-r * T) * payoffs
    return np.mean(discounted), np.std(discounted) / np.sqrt(n_paths), S_T

np.random.seed(42)
print("\n" + "="*55)
print("   MONTE CARLO OPTIONS PRICER")
print("="*55)
start = time.time()
mc_call, se_call, ST = monte_carlo_option(S0,K,T,r,sigma,N_PATHS,N_STEPS,"call")
mc_put,  se_put,  _  = monte_carlo_option(S0,K,T,r,sigma,N_PATHS,N_STEPS,"put")
elapsed = time.time()-start
bs_call = black_scholes(S0,K,T,r,sigma,"call")
bs_put  = black_scholes(S0,K,T,r,sigma,"put")
print(f"\nDone in {elapsed:.2f}s — {N_PATHS:,} paths\n")
rows = [
    ["Call — Black-Scholes", f"${bs_call:.4f}", "—"],
    ["Call — Monte Carlo",   f"${mc_call:.4f}", f"±${se_call:.4f}  err={abs(mc_call-bs_call)/bs_call*100:.2f}%"],
    ["Put  — Black-Scholes", f"${bs_put:.4f}",  "—"],
    ["Put  — Monte Carlo",   f"${mc_put:.4f}",  f"±${se_put:.4f}  err={abs(mc_put-bs_put)/bs_put*100:.2f}%"],
]
print(tabulate(rows, headers=["Method","Price","Std Error"], tablefmt="rounded_outline"))
print(f"\nS_T  mean=${np.mean(ST):.2f}  std=${np.std(ST):.2f}  5th=${np.percentile(ST,5):.2f}  95th=${np.percentile(ST,95):.2f}")
print(f"ITM paths (call): {(ST>K).mean()*100:.1f}%\n")
