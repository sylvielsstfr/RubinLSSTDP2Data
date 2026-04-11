# RubinLSSTDP2Data — Notebook Catalogue

**Author:** Sylvie Dagoret-Campagne  
**Affiliation:** IJCLab / IN2P3 / CNRS  
**Project:** Rubin Observatory / LSST Data Preview 2 (DP2) — LSSTCam Survey Analysis  
**Environment:** USDF RSP (Rubin Science Platform) — `LSST` kernel (Python 3.12, `lsst_distrib`)  
**Last update:** 2026-04-08

---

## Overview

This directory contains a series of Jupyter notebooks developed to explore and analyse
LSSTCam observational data accessible through two complementary interfaces:

- **Butler** (`lsst.daf.butler`): the LSST data access middleware, used for processed data products
  (coadds, DiaObjects, DiaSources, Objects, Sources, ForcedSources, survey property maps, …).
- **ConsDB** (`lsst.summit.utils.ConsDbClient`): the Consolidated Database, used for visit-level
  metadata (pointing coordinates, filters, observing conditions, etc.).

The notebooks are named `YYYY-MM-DD_<topic>.ipynb` and are ordered chronologically.  
Many notebooks depend on data or concepts introduced by earlier ones; dependencies are noted
in each entry.

---

## Notebook Catalogue

### Group 1 — Survey Overview (ConsDB + HEALPix)

---

#### 2026-03-07 — `2026-03-07_AccessToDP2.ipynb`

**Topic:** First contact with DP2 data via the Butler.

Entry point to LSST Data Preview 2. Demonstrates how to:

- Instantiate a `Butler` pointing at the `dp2_prep` repository and the
  `LSSTCam/runs/DRP/v30_0_4/DM-54249` collection.
- Load the `lsst_cells_v2` sky tessellation (`skyMap`) and query tract/patch structure.
- Retrieve observation metadata (date, filter, pointing, MJD) and build a `pandas` DataFrame.
- Map each science exposure to its tract and patch via `skymap.findTract` / `tract_info.findPatch`.
- Produce bar charts of visit counts per band for each `(tract, target)` combination.
- Focus on the six LSST Deep Drilling Fields: XMM-LSS, COSMOS, ECDFS, ELAIS-S1, EDFS_a, EDFS_b.
- Inspect available dataset types in the collection.

**Key dependencies:** `lsst.daf.butler`, `lsst.skymap`, `lsst.geom`,
`pandas`, `matplotlib`, `seaborn`, `astropy`

**References:**
- USDF Plot Navigator: https://usdf-rsp.slac.stanford.edu/plot-navigator
- DRP Campaign wiki: https://rubinobs.atlassian.net/wiki/spaces/DM/pages/661192727/LSSTCam+Intermittent+DRP+Runs

---

#### 2026-03-09 — `2026-03-09_ConsDB_LSSTCam.ipynb`

**Topic:** LSSTCam visit metadata from ConsDB — sky coverage and observing conditions.

Primary data-retrieval notebook for the ConsDB-based analysis chain.

- Connect to the ConsDB REST API endpoint.
- Query `cdb_lsstcam.visit1` and `cdb_lsstcam.exposure`, inner-join on `visit_id`.
- Clean data (remove engineering/pinhole filters, drop visits with missing coordinates).
- Visualise sky coverage in Mollweide projection (colour-coded by elapsed time) with
  Galactic plane and DDF overlays.
- Plot time series of observing conditions: airmass, temperature, pressure, humidity,
  wind speed/direction, DIMM seeing, telescope focus.

**Key dependencies:** `lsst.summit.utils.ConsDbClient`, `numpy`, `matplotlib`, `astropy`

**References:**
- ConsDB docs: https://consdb.lsst.io/index.html
- SDM schema: https://sdm-schemas.lsst.io/

---

#### 2026-03-09 — `2026-03-09_ConsDB_LSSTCam_HEALPix.ipynb`

**Topic:** HEALPix sky maps of LSSTCam visit counts — all bands and per band.

Takes ConsDB data from the previous notebook and builds HEALPix visit-count maps
(NSIDE = 64, pixel ≈ 0.92 deg²).

- One all-band map + six per-band maps (u, g, r, i, z, y) in Mollweide projection.
- Galactic plane and DDF overlays via `hp.projplot` / `hp.projscatter`.
- Summary table: total visits, sky area, maximum depth, mean/median depth per band.

**Key dependencies:** `healpy`, `numpy`, `matplotlib`, `astropy`

---

#### 2026-03-10 — `2026-03-10_ConsDB_LSSTCam_HEALPix_Monthly_zoommaps.ipynb`

**Topic:** Month-by-month evolution of LSSTCam visit counts (individual zoomed maps per band).

Extends the HEALPix notebook by slicing visit data by calendar month.
For each month: per-band HEALPix maps in Mollweide projection, summary table, grouped and
stacked bar charts of visit counts, and normalised band fraction chart.
Each band is shown in a separate figure.

**Key dependencies:** `healpy`, `numpy`, `pandas`, `matplotlib`, `astropy`

---

#### 2026-03-10 — `2026-03-10_ConsDB_LSSTCam_HEALPix_Monthly_subplots.ipynb`

**Topic:** Month-by-month evolution — bands grouped as 2×3 subplots per monthly figure.

Same analysis as the previous notebook, but the six band maps are grouped into a
2×3 subplot grid per month for a more compact presentation.
Note: NSIDE = 32 due to smaller subplot size.

**Key dependencies:** `healpy`, `numpy`, `pandas`, `matplotlib`, `astropy`

---

### Group 2 — Survey Property Maps (HealSparse)

---

#### 2026-03-11 — `2026-03-11_ExploreDP2_SurveyPropertyMaps.ipynb`

**Topic:** Exploration of all survey property map types available in DP2.

Accesses the **survey property maps** (HealSparse format) from the `dp2_prep` butler.
Catalogues the 14 available map types per band (exposure time, epochs, PSF size,
PSF ellipticity e1/e2, magnitude limit, sky background, sky noise, DCR shifts/ellipticities),
lists their dataset types and dimensions, and demonstrates retrieval via
`butler.get(map_name, dataId={'band': ..., 'skymap': ...})`.
Also displays pipeline-generated PNG/PDF `SurveyWidePropertyMapPlot` images.

**Key dependencies:** `lsst.daf.butler`, `healsparse`, `numpy`, `matplotlib`

**Available map types (14 per band × 6 bands = 84 maps):**
`exposure_time_sum`, `epoch_min/max/mean`, `psf_size`, `psf_e1/e2`,
`psf_maglim`, `sky_background`, `sky_noise`, `dcr_dra/ddec`, `dcr_e1/e2`

---

#### 2026-03-11 — `2026-03-11_ExploreDP2_SurveyPropertyMapsasPlots.ipynb`

**Topic:** Display survey property maps as interactive matplotlib plots (alternative rendering).

Companion to the exploration notebook above. Focuses on rendering the HealSparse maps
as `pcolormesh` / `imshow` plots using `matplotlib` with adaptive colour normalisation
(linear, LogNorm, SymLogNorm) and field-centred zoom views for each DDF.

**Key dependencies:** `lsst.daf.butler`, `healsparse`, `numpy`, `matplotlib`

---

#### 2026-03-11 — `2026-03-11_DP2_SurveyPropertyMaps_AllBands_AllDDF.ipynb`

**Topic:** Survey property maps — all 6 bands × all 6 DDF fields — 2×3 subplot grids.

Retrieves a selected HealSparse survey property map from the DP2 butler and
produces **2×3 subplot grids** (one panel per band: u, g, r, i, z, y)
centred on each of the six main LSST Deep Drilling Fields:
COSMOS, ECDFS, EDFS-a, ELAIS-S1, XMM-LSS, ECDFS-ext.
Displays exposure time, PSF magnitude limit, and sky noise maps by default.

**Requires:** butler connection and `coll_hsp` from `2026-03-11_ExploreDP2_SurveyPropertyMaps.ipynb`.

**Key dependencies:** `lsst.daf.butler`, `healsparse`, `numpy`, `matplotlib`

---

#### 2026-03-12 — `2026-03-12_ExploreDP2_SurveyPropertyMaps_Healpix.ipynb`

**Topic:** Survey property maps — native HEALPix representation via `healpy`.

Alternative visualisation approach: each `HealSparseMap` is converted to a dense
HEALPix array (`healsparse → healpy`) and displayed with `hp.mollview` / `hp.gnomview`.
Provides fine control over projection, coordinate graticule, Galactic plane overlay,
and adaptive colour normalisation. Includes a 2×3 band grid, local `pcolormesh` views,
statistics over a DDF region, and a loop over all 14 available map types.

**Key dependencies:** `lsst.daf.butler`, `healsparse`, `healpy`, `numpy`, `matplotlib`

---

### Group 3 — Deep Drilling Fields: DiaObjects, Tracts, Light Curves

---

#### 2026-03-13 — `2026-03-13_DP2_DDF_Tracts_SkyMap_Mollweide.ipynb`

**Topic:** SkyMap tracts covering the Deep Drilling Fields — geometry and visualisation.

- Instantiates a Gen3 Butler and loads the `lsst_cells_v2` SkyMap.
- Identifies all tracts overlapping the DDF fields (WFD and uDDF).
- Displays the tracts and their patches in a Mollweide projection coloured by tract ID,
  with DDF centres overlaid.
- Produces ±5° Cartesian zoom plots for each individual DDF.

**Key dependencies:** `lsst.daf.butler`, `lsst.skymap`, `lsst.geom`,
`numpy`, `matplotlib`, `astropy`

---

#### 2026-03-13 — `2026-03-13_DP2_DDF_DiaObjects_Query.ipynb`

**Topic:** DiaObject catalog query over a DDF — TAP and Butler access methods.

Queries the **DiaObject** catalog for a user-selected DDF via two methods:
- **TAP / ADQL** for cone search on Qserv.
- **Butler Gen3** for per-tract parquet tables (`dia_object`, `dia_source`,
  `dia_object_forced_source`).

Filters on `nDiaSources >= MIN_NSOURCES`, plots spatial distributions and
variability diagnostics, and prepares the table for coordinate-based
cross-matching with Fink alerts (sky-coordinate cross-match, since
`diaObjectId` values differ between Alert Production and DRP pipelines).

**Key dependencies:** `lsst.daf.butler`, `pyvo`, `numpy`, `pandas`, `matplotlib`, `astropy`

---

#### 2026-03-13 — `2026-03-13_DP2_DDF_DiaObjects_Butler_LCandLuptitudes.ipynb`

**Topic:** DiaObject / DiaSource catalogs via Butler — light curves and Luptitudes.

Retrieves `dia_object`, `dia_source`, and `dia_object_forced_source` catalogs
for COSMOS DDF using Butler Gen3. Plots multi-band light curves (u, g, r, i, z, y)
with DiaSource detections (marker `o`) and forced photometry (marker `+`),
in both AB magnitude and Luptitude (asinh magnitude) representations.
Features dual x-axes (MJD + calendar date), interactive zoom via `ipympl`.

Actual Butler schema used:
- `dia_object` : dims `(skymap, tract)`
- `dia_source` : dims `(skymap, tract)`
- `dia_object_forced_source` : dims `(skymap, tract, patch)` — 21 refs per tract

**Key dependencies:** `lsst.daf.butler`, `numpy`, `pandas`, `matplotlib`, `ipympl`, `astropy`

---

#### 2026-03-14 — `2026-03-14_DP2_DDF_DiaObjects_LightCurves.ipynb`

**Topic:** Multi-band light curves from saved CSV files — DiaSource + ForcedPhotometry.

Reads three CSV files generated by `2026-03-13_DP2_DDF_DiaObjects_Butler_LCandLuptitudes.ipynb`:
`DiaObjects_COSMOS_nmin200.csv`, `DiaSources_COSMOS_nmin200.csv`, `ForcedSrc_COSMOS_nmin200.csv`.

Plots multi-band light curves for DiaObjects with `nDiaSources > CUT_NDIASOURCES`:
independent y-axes per band, fixed 16–28 mag range, top calendar-date axis,
bottom MJD axis, interactive zoom via `ipympl`.

**Input data folder:** `data_DP2_DDF_DIAOBJ_BUTLER_01/`

**Key dependencies:** `numpy`, `pandas`, `matplotlib`, `ipympl`

---

#### 2026-03-16 — `2026-03-16_DP2_DDF_staticObjects_Butler.ipynb`

**Topic:** Static Object / Source catalog query over a DDF via Butler.

Retrieves **Object**, **Source**, and **ForcedSource** (static sky) catalogs
for a user-selected DDF using Butler Gen3 only.
Applies star/galaxy separation (`extendedness < 0.5`), selects isolated primary stars,
and prepares the table for photometric calibration or cross-matching.

Butler schema: `object` (tract), `source` (tract), `object_forced_source` (tract × patch).

**Key dependencies:** `lsst.daf.butler`, `numpy`, `pandas`, `matplotlib`, `astropy`

---

#### 2026-03-17 — `2026-03-17_DP2_DDF_VisitTractPatch_Butler.ipynb`

**Topic:** Mapping visits to tracts and patches via Butler registry.

Retrieves the list of visits associated with a DDF from the Butler registry
and maps each visit to its corresponding tract/patch in the sky tessellation.
Produces a visit–tract–patch association table for downstream use
(e.g. BPS submit of DRP pipeline jobs).

**Key dependencies:** `lsst.daf.butler`, `lsst.skymap`, `lsst.geom`,
`numpy`, `pandas`, `matplotlib`

---

#### 2026-03-19 — `2026-03-19_DP2_DDF_CoaddsstaticObjects_Butler.ipynb`

**Topic:** Viewing DeepCoadd images aligned with static Object catalog selections.

Retrieves `deepCoadd` images for selected tract/patch combinations via Butler
and overlays Object catalog positions (isolated primary stars) on the coadd.
Combines static catalog queries from `2026-03-16` with image access to
validate the spatial cross-identification of static sources.

**Key dependencies:** `lsst.daf.butler`, `lsst.afw`, `numpy`, `matplotlib`

---

### Group 4 — Visit–Tract–Patch Cross-matching and Image Visualisation

---

#### 2026-03-25 — `2026-03-25_FindObservationsInButlerRegistryInTractPatch.ipynb`

**Topic:** Associate visits from the Butler registry with tracts and patches — Fink DRP preparation.

**Goal:** Build a complete visit × tract association table to be used for submitting
DRP pipeline jobs via BPS for the Fink alert broker.

- Queries the Butler main registry for all observations in a DDF.
- Maps each visit to tract/patch using `skymap.findTract` / `tract_info.findPatch`.
- Produces a tidy DataFrame suitable for BPS submit configuration.

**Key dependencies:** `lsst.daf.butler`, `lsst.skymap`, `lsst.geom`,
`numpy`, `pandas`, `matplotlib`

---

#### 2026-03-26 — `2026-03-26_DP2_ConstDB_Butler_LSSTCam_VisitsTractPatch.ipynb`

**Topic:** Cross-check ConsDB visit table vs Butler registry — tract/patch mapping.

Cross-checks ConsDB visit metadata with the Butler registry and associates
each visit with its corresponding sky tract and patch.
Combines the ConsDB query from `2026-03-09_ConsDB_LSSTCam.ipynb` with the
tract/patch mapping approach of `2026-03-25`.
Output is a merged visit table used for survey monitoring and DRP submission.

**Key dependencies:** `lsst.daf.butler`, `lsst.skymap`, `lsst.geom`,
`lsst.summit.utils.ConsDbClient`, `numpy`, `pandas`, `matplotlib`, `astropy`

---

#### 2026-03-26 — `2026-03-26_LSSTCamDeepCoaddsMosaicFirefly.ipynb`

**Topic:** View LSSTCam DeepCoadd mosaic in the Firefly interactive image viewer.

Loads `deepCoadd` images from the Butler and displays them interactively
using the Firefly web viewer via `lsst.afw.display` and `firefly_client`.
Allows zooming, panning, WCS-aware coordinate display, and overlay of
catalog sources on the coadd mosaic.

**Key dependencies:** `lsst.daf.butler`, `lsst.afw.display`, `firefly_client`,
`lsst.skymap`, `lsst.geom`, `numpy`, `matplotlib`

---

#### 2026-03-26 — `2026-03-26_LSSTCamDeepCoaddsMosaicMatplotlib.ipynb`

**Topic:** View LSSTCam DeepCoadd mosaic in matplotlib.

Same purpose as the Firefly notebook, but renders the DeepCoadd mosaic using
`matplotlib` only (no browser-based viewer required). Uses `lsst.afw.math.binImage`
for downsampling large coadd tiles before display.
Suitable for batch or offline environments.

LSST pipeline version: `w_2025_10`.

**Key dependencies:** `lsst.daf.butler`, `lsst.afw`, `lsst.skymap`, `lsst.geom`,
`numpy`, `matplotlib`

---

#### 2026-04-04 — `2026-04-04_LSSTCamSingleVisitFirefly.ipynb`

**Topic:** View a single LSSTCam visit (calexp) in the Firefly interactive image viewer.

Loads a single `calexp` (calibrated science exposure) from the Butler
using the DP2 DRP collection `LSSTCam/runs/DRP/DP2/v30_0_0/DM-53881`
and displays it interactively in Firefly via `lsst.afw.display`.

- Butler repository: `dp2_prep`; skymap: `lsst_cells_v2`.
- DRP collection covers three epochs of raw data:
  - epoch1: 2025-04-24 → 2025-07-02
  - epoch2: 2025-07-03 → 2025-09-21
  - epoch3: 2025-10-24 → 2026-01-06
- Demonstrates selection of a specific visit by `(instrument, detector, visit)` dataId.
- Overlays source catalog detections (from `src`) on the calexp in Firefly.
- Serves as an interactive quality-control tool for single-epoch images.

**Key dependencies:** `lsst.daf.butler`, `lsst.afw.display`, `firefly_client`,
`lsst.skymap`, `lsst.geom`, `numpy`, `matplotlib`

**References:**
- DRP run DM-53881: https://rubinobs.atlassian.net/browse/DM-53881
- DP1 Firefly tutorial: https://dp1.lsst.io/tutorials/notebook/103/notebook-103-5.html
- Quantum graphs: https://tigress-web.princeton.edu/~lkelvin/pipelines/current/drp_pipe/

---

### Group 5 — Focal Plane Geometry Extraction

---

#### 2026-04-03 — `2026-04-03_LSSTCamExtractFocalPlane.ipynb`

**Topic:** Extract LSSTCam CCD geometry from the camera model.

Extracts the CCD centre positions and corner coordinates for all detectors
of the LSSTCam focal plane using `lsst.afw.cameraGeom`.
The output CSV file (`ccd_geometry.csv`) is used by the notebooks in
`~/Desktop/RubinLSSTSkyAlerts/notebooks/04_calib/` for focal-plane
heatmap visualisations of photometric calibration diagnostics.

Must be run at SLAC (USDF RSP) and the output file copied locally.
LSST pipeline version: `w_2026_10`.

Inspired by: https://github.com/PFLeget/dp2_psf/blob/master/rayTracingFocalPlane/extract_ccd_geometry.py

**Key dependencies:** `lsst.daf.butler`, `lsst.afw.cameraGeom`, `lsst.geom`,
`numpy`, `matplotlib`

---

### Other — Legacy / Tutorial notebooks

---

#### `203_1_Survey_property_maps.ipynb`

**Topic:** Tutorial/reference notebook for survey property maps (DP1-era).

Legacy tutorial notebook (no date prefix). Covers survey property map access
patterns from DP1, used as a reference when adapting to DP2.

---

## Language Notes

All code comments in the notebooks have been translated from French to English to improve international accessibility and collaboration. The technical content, variable names, and functionality remain unchanged.

## Environment Setup

All notebooks run inside the Rubin Science Platform (RSP) JupyterHub at USDF,
using the `LSST` kernel which provides the full `lsst_distrib` stack.

```bash
# Select the LSST kernel in JupyterLab, then verify
import lsst.pipe.base; print(lsst.pipe.base.__version__)
```

ConsDB access requires configuring the proxy bypass:

```python
import os
os.environ['no_proxy'] += ',.consdb'
```

---

## Data Folders

| Folder | Contents |
|--------|----------|
| `data_DP2_DDF_DIAOBJ_BUTLER_01/` | CSV exports of DiaObject / DiaSource / ForcedSource catalogs for COSMOS DDF (generated by notebook 2026-03-13) |
| `data_fromFink/` | Alert data downloaded from the Fink broker for cross-matching |
| `tools/` | Shared utility scripts |

---

## Cross-references with Other Projects

| This project | Links to |
|---|---|
| `2026-04-03_LSSTCamExtractFocalPlane.ipynb` | Produces `ccd_geometry.csv` used in `~/Desktop/RubinLSSTSkyAlerts/notebooks/04_calib/` |
| `2026-03-25`, `2026-03-26` visit–tract notebooks | Feed visit lists to Fink alert broker DRP submission |
| `2026-03-13_DP2_DDF_DiaObjects_Query.ipynb` | Prepares DDF DiaObject tables for Fink coordinate cross-matching |

---

## Survey Status

Current DP2 survey progress and nightly validation:
https://survey-strategy.lsst.io/progress/sv_status/sv_20250930.html

DRP campaign wiki:
https://rubinobs.atlassian.net/wiki/spaces/DM/pages/661192727/LSSTCam+Intermittent+DRP+Runs
