# SFS bottleneck audit — executed audit (Release B) v0.1.0

**Status: anonymous-workflow, unrefereed, producer-run executed audit** under
the frozen pre-registered protocol sfs-bottleneck-audit-protocol v0.1.1
(tag v0.1.1-candidate; doi 10.5281/zenodo.21893436). CC0; no copyright claimed.

**Result: universal class rejection.** All 216 declared (dataset,
overdispersion, budget) cells — nine spectra including the bottleneck
claimants' own data — are class_rejected: no single-population Kingman
history on the declared 60-cell grid reproduces any spectrum within the
declared multinomial error model (z=3, overdispersion up to 10), even at the
widest complexity budget. Zero aborted cells; the 5% kill criterion was not
approached. The pre-registered outcome semantics defined class rejection as a
reported scientific outcome; its universal form is the finding: the
depression-ratio question cannot be posed within any error model that treats
these spectra as carrying millions of independent observations. A clearly
labelled post-hoc diagnostic (POST_HOC_DIAGNOSTICS.md, recorded in
DEVIATIONS.md) quantifies the rejection at 13x-83x box inflation, i.e. an
effective information content of roughly 5x10^2 to 3x10^4 independent sites —
about ten orders of magnitude below what severe-versus-continuous
discrimination in the disputed window requires.

Contents: per-dataset certified results (results/), populated audit
templates (templates/), the execution harness (run_audit.py), binding data
manifest (data_manifest.json), DEVIATIONS.md (two entries), and the
diagnostic. Data files are not vendored; fetch and verify per the protocol
repository DATA_PROVENANCE.md.
