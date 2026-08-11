#!/usr/bin/env python3
"""Release B execution harness: runs the frozen protocol on the declared data.

Imports only the frozen machinery from the tagged protocol checkout; every
analytic literal comes from the frozen bottleneck_audit.windows module. See
DEVIATIONS.md entry 1.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PROTOCOL_SRC = HERE / "protocol" / "src"
sys.path.insert(0, str(PROTOCOL_SRC))

from bottleneck_audit import (  # noqa: E402
    EmpiricalConstraintSet,
    LPInfeasible,
    claim_window_family,
    load_column_with_monomorphic,
    load_fitcoal_row,
)
from bottleneck_audit import windows as W  # noqa: E402

DATA = HERE / "data"
OUT = HERE / "results"
OUT.mkdir(exist_ok=True)

REFERENCE_WINDOWS = [tuple(W.REFERENCE_WINDOW), (0.0, 0.05)]
LOADERS = {"fitcoal": load_fitcoal_row, "column": load_column_with_monomorphic}


def main() -> None:
    start_edges = np.linspace(*W.GRID_EDGES[:2], W.GRID_EDGES[2])
    family = claim_window_family()
    manifest = json.loads((HERE / "data_manifest.json").read_text())
    rows: list[dict] = []
    aborted = 0
    total_cells = 0
    t0 = time.time()

    for entry in manifest:
        counts, n = LOADERS[entry["loader"]](DATA / entry["file"])
        assert n == entry["n"], f"sample size mismatch for {entry['id']}"
        file_rows: list[dict] = []
        for phi in W.OVERDISPERSION_LADDER:
            for budget in W.TV_BUDGETS:
                total_cells += 1
                cs = EmpiricalConstraintSet.build(
                    counts, n, start_edges,
                    z_score=W.Z_SCORE, overdispersion=phi, tv_budget=budget,
                    box_lower=W.BOX[0], box_upper=W.BOX[1],
                )
                base = {
                    "dataset": entry["id"], "n": n,
                    "segregating_sites": cs.segregating_sites,
                    "overdispersion": phi, "tv_budget": budget,
                }
                try:
                    cs.window_average_interval(tuple(family[0]["window"]))
                except LPInfeasible:
                    file_rows.append({**base, "outcome": "class_rejected"})
                    continue
                except RuntimeError as exc:
                    aborted += 1
                    file_rows.append({**base, "outcome": "aborted", "error": str(exc)[:200]})
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
                            "f2_gap": max(f2_lo.dual_gap, f2_hi.dual_gap),
                        }
                        for ref in REFERENCE_WINDOWS:
                            f1_lo, f1_hi = cs.depression_ratio_interval(window, ref)
                            tag = "primary" if ref == tuple(W.REFERENCE_WINDOW) else "sensitivity"
                            row[f"f1_lower_{tag}"] = f1_lo.certified_bound
                            row[f"f1_upper_{tag}"] = f1_hi.certified_bound
                            row[f"f1_gap_{tag}"] = max(f1_lo.dual_gap, f1_hi.dual_gap)
                            row[f"severity_excluded_{tag}"] = bool(
                                f1_lo.certified_bound > W.SEVERITY_THRESHOLD
                            )
                        file_rows.append(row)
                    except LPInfeasible:
                        file_rows.append({**wbase, "outcome": "class_rejected"})
                    except RuntimeError as exc:
                        aborted += 1
                        file_rows.append({**wbase, "outcome": "aborted", "error": str(exc)[:200]})
        (OUT / f"{entry['id']}.json").write_text(
            json.dumps(file_rows, indent=1, sort_keys=True) + "\n"
        )
        rows.extend(file_rows)
        print(f"{entry['id']}: {len(file_rows)} rows  ({time.time()-t0:.0f}s elapsed)", flush=True)

    receipt = {
        "package": "sfs-bottleneck-audit",
        "protocol": "sfs-bottleneck-audit-protocol v0.1.1 "
                    "(tag v0.1.1-candidate; doi 10.5281/zenodo.21893436)",
        "date": "2026-08-11",
        "datasets": len(manifest),
        "rows": len(rows),
        "constraint_cells": total_cells,
        "aborted_rows": aborted,
        "kill_criterion_5pct": bool(aborted / max(1, len(rows)) > 0.05),
    }
    (OUT / "RELEASE_B_RECEIPT.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
