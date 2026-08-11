#!/usr/bin/env python3
"""Release B2 harness: the frozen A2 error model on the declared data.

Mirrors run_audit.py; every literal comes from the frozen protocol_a2 and
windows modules at tag v0.2.0-candidate.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "protocol" / "src"))

from bottleneck_audit import (  # noqa: E402
    LPInfeasible,
    claim_window_family,
    load_column_with_monomorphic,
    load_fitcoal_row,
)
from bottleneck_audit import windows as W  # noqa: E402
from bottleneck_audit import protocol_a2 as A2  # noqa: E402

DATA = HERE / "data"
OUT = HERE / "results_a2"
OUT.mkdir(exist_ok=True)
REFERENCE_WINDOWS = [tuple(W.REFERENCE_WINDOW), (0.0, 0.05)]
LOADERS = {"fitcoal": load_fitcoal_row, "column": load_column_with_monomorphic}


def main() -> None:
    edges = np.linspace(*W.GRID_EDGES[:2], W.GRID_EDGES[2])
    family = claim_window_family()
    manifest = json.loads((HERE / "data_manifest.json").read_text())
    all_rows: list[dict] = []
    aborted = 0
    cells = 0
    t0 = time.time()

    for entry in manifest:
        counts, n = LOADERS[entry["loader"]](DATA / entry["file"])
        assert n == entry["n"]
        file_rows: list[dict] = []
        for e in A2.E_LADDER:
            for variant in A2.CLASS_VARIANTS:
                for n_eff in A2.BLOCK_NEFF_LADDER:
                    for budget in A2.TV_BUDGETS_A2:
                        cells += 1
                        cs = A2.build_a2_constraint_set(
                            counts, n, edges, e=e, variant=variant,
                            n_eff=n_eff, tv_budget=budget,
                            z_score=W.Z_SCORE,
                            box_lower=W.BOX[0], box_upper=W.BOX[1],
                        )
                        base = {
                            "dataset": entry["id"], "n": n,
                            "e": e, "variant": variant, "n_eff": n_eff,
                            "overdispersion": cs.overdispersion,
                            "tv_budget": budget,
                        }
                        try:
                            cs.window_average_interval(tuple(family[0]["window"]))
                        except LPInfeasible:
                            file_rows.append({**base, "outcome": "class_rejected"})
                            continue
                        except RuntimeError as exc:
                            aborted += 1
                            file_rows.append({**base, "outcome": "aborted", "error": str(exc)[:150]})
                            continue
                        for member in family:
                            window = tuple(member["window"])
                            wbase = {
                                **base,
                                "generation_time_years": member["generation_time_years"],
                                "reference_diploid_size": member["reference_diploid_size"],
                                "window_left": window[0], "window_right": window[1],
                            }
                            try:
                                f2_lo, f2_hi = cs.window_average_interval(window)
                                row = {
                                    **wbase, "outcome": "bounded",
                                    "f2_lower": f2_lo.certified_bound,
                                    "f2_upper": f2_hi.certified_bound,
                                }
                                for ref in REFERENCE_WINDOWS:
                                    f1_lo, f1_hi = cs.depression_ratio_interval(window, ref)
                                    tag = "primary" if ref == tuple(W.REFERENCE_WINDOW) else "sensitivity"
                                    row[f"f1_lower_{tag}"] = f1_lo.certified_bound
                                    row[f"f1_upper_{tag}"] = f1_hi.certified_bound
                                    row[f"severity_excluded_{tag}"] = bool(
                                        f1_lo.certified_bound > W.SEVERITY_THRESHOLD
                                    )
                                file_rows.append(row)
                            except LPInfeasible:
                                file_rows.append({**wbase, "outcome": "class_rejected"})
                            except RuntimeError as exc:
                                aborted += 1
                                file_rows.append({**wbase, "outcome": "aborted", "error": str(exc)[:150]})
        (OUT / f"{entry['id']}.json").write_text(
            json.dumps(file_rows, indent=1, sort_keys=True) + "\n"
        )
        all_rows.extend(file_rows)
        bounded = sum(1 for r in file_rows if r["outcome"] == "bounded")
        print(f"{entry['id']}: {len(file_rows)} rows, {bounded} bounded ({time.time()-t0:.0f}s)", flush=True)

    receipt = {
        "package": "sfs-bottleneck-audit",
        "protocol": "sfs-bottleneck-audit-protocol v0.2.0 (A2; tag v0.2.0-candidate; "
                    "doi 10.5281/zenodo.21893667)",
        "date": "2026-08-11",
        "datasets": len(manifest),
        "rows": len(all_rows),
        "constraint_cells": cells,
        "bounded_rows": sum(1 for r in all_rows if r["outcome"] == "bounded"),
        "class_rejected_rows": sum(1 for r in all_rows if r["outcome"] == "class_rejected"),
        "aborted_rows": aborted,
        "kill_criterion_5pct": bool(aborted / max(1, len(all_rows)) > 0.05),
    }
    (OUT / "RELEASE_B2_RECEIPT.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
