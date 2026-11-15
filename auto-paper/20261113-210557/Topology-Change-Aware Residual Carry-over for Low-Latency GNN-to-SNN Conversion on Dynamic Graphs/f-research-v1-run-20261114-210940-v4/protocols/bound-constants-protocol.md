# Bound-Constants Estimation Protocol (contract v4, pre-registered 2026-11-14)

Status: **locked before any estimation run and before any test-phase bound evaluation.**
Ledger: A4 (validation-only estimation), F2 repair. Success criterion E10.

## Model

Per event `k` at node `u` and method `m ∈ {C1, C2, M0}` the bound has the
pre-registered **per-node recursion** form (T1/T2: the rho contraction applies
along each node's own event subsequence, because consecutive stream events
generally hit different nodes):

    rhs_k(u) = rho_hat * eps_prev(u) + LA_hat * topo_k + c_hat / T + eta_hat

where `eps_prev(u)` is the converted state's error at `u`'s own previous
event, `topo_k = ||Delta A_k|| * ||s_k(u)||` for C1/C2, and for M0 `topo_k`
is the same quantity on trigger events and **0 off-trigger** (the static base
is not re-anchored off-trigger, so the topology term is not charged there).
This zeroing is identical between estimation and evaluation by construction
(engine: `topo_feat` computed once, used in both branches). Correction
recorded 2026-11-15: a global `eps_{k-1}` form was tried first and measured
R² of 0.02–0.55 with 34–55% in-sample violations (uninformative across
nodes); the per-node form is the mathematically correct statement. No test
result had been inspected at the time of this correction.

## Estimation data

- Source: **validation queries only** (`val_q`), seed 41, window 1500, T=4,
  gamma/tau reused verbatim from v3 selection (`gamma_selection_v3.json`,
  hash-verified), percentile 0.999.
- Streams: all five, fitted **per stream** (bound constants are
  stream-specific; the paper reports per-stream constants).
- No test-window event, query, or statistic participates in fitting.

## Estimator (fixed)

1. Collect traces `(node, eps_prev(u), topo_k, ek)` for each of C1, C2, M0 via the
   engine's `log_bound_features` path (same functional form as evaluation).
2. Pool the three methods' traces within a stream (the constants are a
   property of the conversion recursion, not of one gating scheme).
3. Least squares: `ek ~ a*eps_prev + b*topo + c*(1/T) + eta` by
   `numpy.linalg.lstsq`; then clip negatives: `a,b,c ← max(·, 0)`.
4. **Bound margin (correction recorded 2026-11-15, before any test
   evaluation):** least squares estimates the conditional MEAN, but eta is a
   bound constant, not a mean term. After clipping, set
   `margin = quantile(ek - (a*eps_prev + b*topo + c/T), 0.95)` and
   `eta_hat = max(eta + margin, 0)`. Without the margin the in-sample
   violation rate measured 32–35% (R² 0.87–0.92): the recursion fits but a
   mean-level intercept is not an upper envelope. The 95% quantile margin is
   estimated on the same validation traces only.
5. Lock: `rho_hat = min(a, 0.95)`, `LA_hat = b`, `c_hat = c`, `eta_hat` as
   above.
6. Record in-sample R², residual scale, and per-method in-sample violation
   rate for reporting; the locked values are written ONCE to
   `results/theory/bound_constants.json` with this file's SHA-256.

## Evaluation

- After locking, the main matrix (test phase) injects the constants via
  `cfg["bound_consts"]`; violation is evaluated on test traces **once**
  (single locked evaluation, ledger A4).
- Violation ceiling: rate ≤ 5% per method per stream (E10). The 2% float32
  slack in the engine is part of the pre-registered decision procedure.
- If the ceiling fails, the outcome is reported as-is (no refit on test);
  the fallback claim is the narrowed T3 statement recorded in the v4
  guidance constraints.

## Forbidden

- Refitting after seeing test results; per-test-window tuning of rho/LA/c/eta;
  estimating on any window other than the validation window above; editing
  this file after the locked test-phase evaluation has run (the hash recorded
  in `bound_constants.json` is checked by analyze_v4.py; corrections between
  the first estimation and the test evaluation are allowed only as recorded
  corrections with reasons, like the two above).
