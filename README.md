# Monte Carlo Options Pricer

Simulates European call & put option prices using Monte Carlo methods (Geometric Brownian Motion) and validates the results against the analytical Black-Scholes formula.

## What it does

- Simulates 100,000+ stock price paths using Geometric Brownian Motion (GBM)
- Prices European Call and Put options via Monte Carlo simulation
- Computes the closed-form Black-Scholes price for the same options
- Compares both methods, reporting price, standard error, and convergence
- Outputs distribution stats on terminal stock price (mean, std dev, percentiles) and probability of finishing in-the-money

## Why this matters

Black-Scholes gives an exact price for vanilla European options, but most real-world derivatives (exotic options, path-dependent payoffs, American options) don't have closed-form solutions. Monte Carlo simulation is the general-purpose tool used when no analytical formula exists — this project validates the simulation approach against the known closed-form answer as a sanity check.

## Sample output
