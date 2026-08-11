# Deviations from the frozen protocol (Release B)

Recorded 2026-08-11, BEFORE any real-data result was computed or inspected.

1. **Execution harness added.** Release A froze the machinery and every
   analytic literal but shipped no real-data driver. `run_audit.py` is added
   as the execution harness described by PROTOCOL.md section 9. It imports
   the frozen modules from the tagged protocol checkout unmodified, takes
   every ladder, window, threshold and box value from the frozen
   `bottleneck_audit.windows` module, and introduces no analytic choice of
   its own. Feasibility of each (file, overdispersion, budget) cell is
   established once via the first window-average programme; `LPInfeasible`
   marks the whole cell `class_rejected`, matching the protocol's outcome
   semantics.


2. **Post-hoc diagnostic added AFTER results inspection** (recorded
   2026-08-11, clearly labelled): `POST_HOC_DIAGNOSTICS.md` reports the
   minimum uniform inflation of the declared confidence boxes at which each
   spectrum becomes class-feasible. It is exploratory, not a protocol result,
   and alters no protocol output. It exists to quantify the rejection
   magnitude and to inform a possible successor protocol with a
   linkage-aware error model.
