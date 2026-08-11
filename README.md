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

## Archive

- Zenodo (version): https://doi.org/10.5281/zenodo.21893572
- Zenodo (concept): https://doi.org/10.5281/zenodo.21893571
- Protocol: https://doi.org/10.5281/zenodo.21893436 (tag v0.1.1-candidate)
- Archived bytes verified identical to the v0.1.0-candidate release asset.

## Release B2 (v0.2.0): executed audit under the A2 error model

Protocol A2: tag v0.2.0-candidate, doi 10.5281/zenodo.21893667. Receipt:
4,963 rows, 4,884 bounded, 79 class-rejected, 0 aborted.

Pre-registered findings (family-union intervals per declared setting, tight
budget V=0.5, primary reference window):

- **The claimants' own YRI spectrum**, under the most information-preserving
  declared setting (e=0.005, all classes, n_eff=10,000), certifies the
  depression ratio within **[0.162, 0.934]** across the entire 12-mapping
  claim-window family: the ancient window average is certifiably depressed
  below the recent baseline AND certifiably far above FitCoal-level severity
  (0.05-0.1). The independent Cousins-Durvasula YRI processing agrees:
  **[0.132, 0.961]**. "Depressed, not severe" is the certified reading of
  both YRI processings under those settings.
- **CEU and CHB** (out-of-Africa contrasts) certifiably exclude severity in
  9 of their feasible settings each and never certify depression, matching
  the dispute's shared premise that the signal is African-specific.
- **Across the full concession ladder the sets widen to uninformative**, and
  Deng et al.'s more conservative YRI processing is uninformative at the
  family-union level: the severity question remains class-identified, and
  every certified statement above is conditional on its declared setting.
- B2 Zenodo (version): https://doi.org/10.5281/zenodo.21893989
