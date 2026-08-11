# Post-hoc diagnostics (NOT protocol results)

Minimum uniform inflation k of the declared z=3, phi=1 confidence boxes at
which the declared class (60-cell grid, TV <= 50) becomes feasible, with the
implied effective number of independent sites S/k^2:

| dataset | k | eff. independent sites | segregating sites |
|---|---|---|---|
| HU-YRI | 32.9 | 5,377 | 5,803,697 |
| HU-ESN | 31.4 | 5,701 | 5,632,055 |
| HU-LWK | 35.0 | 5,006 | 6,130,501 |
| HU-MSL | 29.8 | 6,510 | 5,782,224 |
| HU-GWD | 35.4 | 4,835 | 6,065,952 |
| HU-CEU | 49.8 | 1,413 | 3,507,865 |
| HU-CHB | 83.4 | 480 | 3,343,513 |
| DENG-YRI | 13.4 | 31,591 | 5,708,347 |
| COUSINS-YRI | 50.3 | 5,458 | 13,810,698 |

Reading: for these spectra to be consistent with ANY single-population
Kingman history on the declared grid, the error model must concede that the
millions of segregating sites carry only about 5x10^2 to 3x10^4 effective
independent observations. The companion theorem package (v0.2.0) shows
severe-versus-continuous discrimination in the disputed window needs about
5x10^13 independent sites under ideal conditions: roughly ten orders of
magnitude more than the data support.

## Independent corroboration of the rejections (LP-free)

Constrained least squares (LSMR; no linear-programming code shared with the
harness) finds best-achievable max residuals of 21-91 declared half-widths
per dataset, tracking the LP inflation factors dataset-by-dataset from above,
as an approximate method must. Worst-fit classes: the highest-frequency bins
for every Hu spectrum and Cousins (all show non-monotone tail upticks in the
raw data — the ancestral-misidentification signature, which no Kingman
history can reproduce), and classes 1-3 for CEU, CHB and Deng-YRI (the
singleton-excess/growth signature). Deng-YRI is the only spectrum without a
tail uptick and has the smallest rejection magnitude, consistent with its
producers' processing critique. Successor-protocol note: the frozen
sensitivity axes did not include singleton/doubleton exclusion or a
mispolarisation term; both belong in any A2 error model.
