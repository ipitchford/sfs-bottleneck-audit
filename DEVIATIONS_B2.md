# Deviations (Release B2)

1. Execution harness `run_audit_a2.py` written before execution, mirroring
   the B1 harness deviation: it calls only frozen v0.2.0-candidate machinery
   with frozen literals and introduces no analytic choice.
2. `results_a2/B2_SUMMARY.json` and the README findings text were produced
   AFTER results inspection (labelled post hoc): they aggregate the frozen
   per-row outputs (family-union intervals per declared setting at the tight
   budget) and add no new computation on the data.
