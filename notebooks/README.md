# RubinLSSTDP2Data — Notebook Catalogue

**Author:** Sylvie Dagoret-Campagne  
**Project:** Rubin Observatory / LSST Data Preview 2 (DP2) — LSSTCam Survey Analysis  
**Environment:** USDF RSP (Rubin Science Platform) — `LSST` kernel (Python 3.12, `lsst_distrib`)

---

## Overview

This directory contains a series of Jupyter notebooks developed to explore and analyse  
LSSTCam observational data accessible through two complementary interfaces:

- **Butler** (`lsst.daf.butler`): the LSST data access middleware, used for processed data products.
- **ConsDB** (`lsst.summit.utils.ConsDbClient`): the Consolidated Database, used for visit-level metadata (pointing coordinates, filters, observing conditions, etc.).

The notebooks are named `YYYY-MM-DD_<topic>.ipynb` and should be run in order,  
as each builds on concepts or data structures introduced by its predecessors.

---

## Notebooks

### 2026-03-07 — `2026-03-07_AccessToDP2.ipynb`

**Topic:** First contact with DP2 data via the Butler.

This notebook serves as the entry point to LSST Data Preview 2.  
It demonstrates how to:

- Instantiate a `Butler` pointing at the `dp2_prep` repository and the  
  `LSSTCam/runs/DRP/v30_0_4/DM-54249` processing collection.
- Load the `lsst_cells_v2` sky tessellation (`skyMap`) and query its tract/patch structure.
- Iterate over `exposure` dimension records to retrieve observation metadata  
  (date, filter, pointing, exposure time, MJD) and assemble them into a `pandas` DataFrame.
- Map each science exposure to its corresponding Butler tract and patch using  
  `skymap.findTract` / `tract_info.findPatch`.
- Produce stacked bar charts (vertical and horizontal) showing the visit count  
  per band for each `(tract, target)` combination.
- Focus on the six LSST Deep Drilling Fields (DDFs): XMM-LSS, COSMOS, ECDFS,  
  ELAIS-S1, EDFS_a, and EDFS_b.
- Inspect available dataset types in the collection (raw, calexp, dia_source, dia_object, …).

**Key dependencies:** `lsst.daf.butler`, `lsst.skymap`, `lsst.geom`,  
`pandas`, `matplotlib`, `seaborn`, `astropy`

**References:**
- USDF Plot Navigator: https://usdf-rsp.slac.stanford.edu/plot-navigator  
- DRP Campaign wiki: https://rubinobs.atlassian.net/wiki/spaces/DM/pages/661192727/LSSTCam+Intermittent+DRP+Runs

---

### 2026-03-09 — `2026-03-09_ConsDB_LSSTCam.ipynb`

**Topic:** LSSTCam visit metadata from ConsDB — sky coverage and observing conditions.

This notebook is the primary data-retrieval notebook for the ConsDB-based analysis chain.  
It connects directly to the Consolidated Database and explores visit-level metadata  
for LSSTCam observations taken since 2025-04-15.

Key steps:

- Connect to the ConsDB REST API endpoint (`http://consdb-pq.consdb:8080/consdb`)  
  using `ConsDbClient`.
- Query both `cdb_lsstcam.visit1` and `cdb_lsstcam.exposure`, then inner-join them  
  on `visit_id` using `astropy.table.join`.
- Clean the data: remove engineering/pinhole filters (`other`, `none`, `other:pinhole`)  
  and drop visits with missing pointing coordinates (`s_ra`, `s_dec`).
- Explore unique observation dates, physical filters, science programs,  
  and observation reasons.
- Plot the distribution of exposure times.
- Visualise the sky coverage in a Mollweide projection, colour-coded by elapsed time  
  since the first visit (using the `Spectral` colormap).
- Overlay the Galactic plane (computed from `astropy.coordinates.SkyCoord`) and  
  the six Deep Drilling Fields.
- A helper function `ra_to_mollweide()` handles the RA → [-π, +π] conversion  
  and axis inversion required by matplotlib's Mollweide projection.
- Plot time series of key observing-condition quantities stored in ConsDB:  
  airmass, air temperature, pressure, humidity, wind speed, wind direction,  
  DIMM seeing, and telescope focus position.

**Key dependencies:** `lsst.summit.utils.ConsDbClient`, `lsst.geom`,  
`numpy`, `matplotlib`, `seaborn`, `astropy`, `tqdm`

**References:**
- ConsDB REST API: https://usdf-rsp-dev.slac.stanford.edu/consdb/  
- SDM schema browser: https://sdm-schemas.lsst.io/  
- ConsDB documentation: https://consdb.lsst.io/index.html

---

### 2026-03-09 — `2026-03-09_ConsDB_LSSTCam_HEALPix.ipynb`

**Topic:** HEALPix sky maps of LSSTCam visit counts — all bands and per band.

This notebook takes the ConsDB data retrieved in `2026-03-09_ConsDB_LSSTCam.ipynb`  
and converts the visit pointing coordinates into HEALPix visit-count maps  
(`healpy`, NSIDE = 64, pixel size ≈ 0.92 deg).

Key features:

- A helper `visits_to_healpix_map(ra_deg, dec_deg)` accumulates visit counts  
  into HEALPix pixels; unobserved pixels are set to `hp.UNSEEN`.
- The Galactic plane trace is computed in ICRS using `astropy.coordinates.SkyCoord`  
  and sorted by RA to avoid spurious connecting lines at the 0°/360° wrap.
- All sky overlays (Galactic plane, Deep Drilling Field markers and labels)  
  use `hp.projplot`, `hp.projscatter`, and `hp.projtext` with `lonlat=True`  
  — these are projection-aware healpy functions that accept plain ICRS (RA, Dec) degrees,  
  avoiding any manual RA-wrapping.
- One combined sky map (all bands) and six individual maps (one per band: u, g, r, i, z, y)  
  are displayed in Mollweide projection with `flip='astro'` (RA increases to the left).
- A summary table reports, per band: total visit count, number of observed HEALPix pixels,  
  covered sky area (deg²), maximum visit depth per pixel, mean and median visit depth.
- Two bar charts compare total visits and sky coverage across bands.

**Key dependencies:** `healpy`, `numpy`, `matplotlib`, `astropy`

---

### 2026-03-10 — `2026-03-10_ConsDB_LSSTCam_HEALPix_Monthly_zoommaps.ipynb`

**Topic:** Month-by-month evolution of LSSTCam visit counts across the 6 LSST bands.

This notebook extends `2026-03-09_ConsDB_LSSTCam_HEALPix.ipynb` by adding a  
**temporal dimension**: the visit data are sliced by calendar month so that the  
growth and spatial distribution of the survey can be tracked over time.

Workflow:

1. **Date extraction** — The integer `day_obs` field (format `YYYYMMDD`) is parsed  
   with `pd.to_datetime` and converted to a `pandas.Period` (`year_month`).  
   The sorted list of unique months drives all subsequent loops.

2. **Monthly HEALPix sky maps** (Section 6) — For each month and each of the  
   6 bands (*u, g, r, i, z, y*), a HEALPix visit-count map is built and displayed  
   in Mollweide projection with the Galactic plane and DDF overlays.  
   Months or bands with zero visits are skipped gracefully.  
   Per-band statistics (visit count, pixel count, sky area, max depth) are printed.

3. **Summary table** (Section 7) — A tidy `pandas.DataFrame` (`df_monthly`) collects  
   visit counts for every `(month, band)` combination, plus a `Total` column.

4. **Grouped bar chart** (Section 8) — One group of 6 colour-coded bars per month,  
   one bar per band, with the total visit count annotated above each group.

5. **Stacked bar chart** (Section 9) — Same data in a stacked layout to show the  
   cumulative visit count per month.

6. **Normalised band fraction** (Section 10) — A 100%-stacked bar chart showing  
   the relative contribution of each band per month, useful for detecting changes  
   in the survey scheduling strategy.

**Key dependencies:** `healpy`, `numpy`, `pandas`, `matplotlib`, `astropy`

---
---

### 2026-03-10 — `2026-03-10_ConsDB_LSSTCam_HEALPix_Monthly_subplots.ipynb`

**Topic:** Month-by-month evolution of LSSTCam visit counts across the 6 LSST bands.

This notebook do the same task as in  `2026-03-10_ConsDB_LSSTCam_HEALPix_Monthly_zoommaps.ipynb` by adding a   **temporal dimension**: the visit data are sliced by calendar month so that the  
growth and spatial distribution of the survey can be tracked over time.
However bands-skymaps are grouped as subplots in the monthly figures.
Note NSIDE = 32 due to tiny subplots.

Workflow:

1. **Date extraction** — The integer `day_obs` field (format `YYYYMMDD`) is parsed  
   with `pd.to_datetime` and converted to a `pandas.Period` (`year_month`).  
   The sorted list of unique months drives all subsequent loops.

2. **Monthly HEALPix sky maps** (Section 6) — For each month and each of the  
   6 bands (*u, g, r, i, z, y*), a HEALPix visit-count map is built and displayed  
   in Mollweide projection with the Galactic plane and DDF overlays.  
   Months or bands with zero visits are skipped gracefully.  
   Per-band statistics (visit count, pixel count, sky area, max depth) are printed.

3. **Summary table** (Section 7) — A tidy `pandas.DataFrame` (`df_monthly`) collects  
   visit counts for every `(month, band)` combination, plus a `Total` column.

4. **Grouped bar chart** (Section 8) — One group of 6 colour-coded bars per month,  
   one bar per band, with the total visit count annotated above each group.

5. **Stacked bar chart** (Section 9) — Same data in a stacked layout to show the  
   cumulative visit count per month.

6. **Normalised band fraction** (Section 10) — A 100%-stacked bar chart showing  
   the relative contribution of each band per month, useful for detecting changes  
   in the survey scheduling strategy.

**Key dependencies:** `healpy`, `numpy`, `pandas`, `matplotlib`, `astropy`

---




## Environment Setup

All notebooks run inside the Rubin Science Platform (RSP) JupyterHub at USDF,  
using the `LSST` kernel which provides the full `lsst_distrib` stack.

```bash
# Select the LSST kernel in JupyterLab, then verify
import lsst.pipe.base; print(lsst.pipe.base.__version__)
```

ConsDB access requires that the proxy bypass is configured:

```python
import os
os.environ['no_proxy'] += ',.consdb'
```

---

## Survey Status

Current DP2 survey progress and nightly validation:  
https://survey-strategy.lsst.io/progress/sv_status/sv_20250930.html
