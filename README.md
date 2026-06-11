# BhuMe Boundary Take-Home Submission

## Overview

This repository contains my solution for the BhuMe Boundary Take-Home Assessment. The goal is to improve the alignment of official land parcel boundaries with their actual locations visible in satellite imagery.

## Approach

The provided starter kit includes a baseline that estimates a village-wide translation using the example truth polygons.

My solution:

* Calculates centroid shifts between official plots and example truth plots.
* Computes the median X and Y offsets for the village.
* Applies the median shift to all plots.
* Assigns confidence scores to predictions.
* Flags uncertain plots instead of forcing corrections.
* Exports predictions in the required GeoJSON format.

## Project Structure

bhume/

* baseline.py
* geo.py
* io.py
* score.py
* **init**.py

data/

* 34855_vadnerbhairav_chandavad_nashik/

  * input.geojson
  * imagery.tif
  * boundaries.tif
  * example_truths.geojson
  * predictions.geojson

Other files:

* quickstart.py
* CONTRACT.md
* pyproject.toml

## Running the Project

Install dependencies:

```bash
python -m uv sync
```

Run:

```bash
.\.venv\Scripts\python.exe quickstart.py
```

## Public Example Results

Results obtained on the provided example truths:

* Corrected plots: 4
* Flagged plots: 2
* Median IoU (Prediction): 0.875
* Median IoU (Official): 0.612
* Accurate Rate (IoU ≥ 0.5): 1.000
* Improved Fraction: 1.000

## Output

Predictions are generated as:

```text
data/34855_vadnerbhairav_chandavad_nashik/predictions.geojson
```

## Notes

This solution is based on the provided starter kit and demonstrates a complete load → predict → score workflow for parcel boundary correction.
