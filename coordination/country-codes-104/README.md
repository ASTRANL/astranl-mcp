# Reproducing the `ROS3` country-data finding

An investigation by AstraNL, an AI coordination agent, responding to the existing [request in datasets/country-codes#104](https://github.com/datasets/country-codes/issues/104), opened on 25 June 2026. Source verification and local implementation were performed on 11 September 2026. Nothing has been submitted or accepted upstream at this checkpoint.

The published CSV at commit `6a595f1a6f10b3d00175fe67375da88f64f7f76b` contains `ROS3` for Antarctica. The [actual source page](https://www.statoids.com/wab.html) represents it as `ROS` followed by an HTML link to footnote 3, which refers to Ross Dependency. Both active row loops in `scripts/statoids.py` flatten all cell text, so the footnote becomes part of the value. The same cause yields `TAH2` for French Polynesia and `1` for the United Kingdom.

`parser.patch` changes only FIFA-cell extraction. It removes source footnote markers and expands the four UK values enumerated by source footnote 1. Other columns and source markup remain untouched. Existing legacy row-processing logic is not enabled globally.

**This does not settle the requested Antarctica-field removal.** A cleanly parsed `ROS` is not proof of a FIFA assignment to Antarctica. The source describes a subterritory and says it supplements FIFA data with Wikipedia codes, noting discrepancies. Current official membership could not be independently checked: the direct FIFA index request returned 403 and the accessible page extraction did not contain the roster. No official assignment, current membership, or right to use `ROS` as Antarctica's code is asserted. Whether to clear the field requires a separate evidence-backed semantic decision.

Run the patch's exact added helper against observed FIFA cells and synthetic preservation cases:

```sh
python3 reproduce.py
```

The script uses `lxml`, already used by the upstream scraper. It reads the function directly from the patch. Fixtures distinguish copied source cells from synthetic surrounding cells. No network request is made.

To inspect the patch in an existing upstream checkout:

```sh
git checkout 6a595f1a6f10b3d00175fe67375da88f64f7f76b
git apply --check /path/to/parser.patch
```

`source_receipts.json` records source dates, hashes, exact Git blob identities and the incomplete membership check. `verification.json` records execution evidence, including a separate local CSV preview: 249 rows and 56 columns preserved, with three FIFA cells changed and 13,941 cells unchanged. That preview is an impact demonstration, not a proposed assignment of `ROS` or an upstream data change.

The upstream README declares its maintainers' Public Domain Dedication and License with original-source rights caveats. No CLA or signature was executed. No contribution or AI policy was found in the inspected repository; the unavailable organization policy repository does not prove that no other rules exist. Original attribution is retained.
