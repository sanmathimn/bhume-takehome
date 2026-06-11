"""Improved baseline for BhuMe."""

from __future__ import annotations

import statistics

import geopandas as gpd
from shapely.affinity import translate


def _utm_for(geom) -> str:
    lon = geom.centroid.x
    return f"EPSG:{32600 + int((lon + 180) // 6) + 1}"


def global_median_shift(village):

    if village.example_truths is None:
        raise ValueError(
            f"{village.slug} has no example_truths.geojson to estimate a shift from"
        )

    utm = _utm_for(village.example_truths.geometry.iloc[0])

    official_u = village.plots.to_crs(utm)
    truth_u = village.example_truths.to_crs(utm)

    dxs = []
    dys = []

    for pn in village.example_truths.index:
        if pn in official_u.index:
            o = official_u.loc[pn, "geometry"].centroid
            t = truth_u.loc[pn, "geometry"].centroid

            dxs.append(t.x - o.x)
            dys.append(t.y - o.y)

    if not dxs:
        raise ValueError(
            "No overlapping plots between example truths and cadastre"
        )

    mdx = statistics.median(dxs)
    mdy = statistics.median(dys)

    shifted = official_u.copy()

    shifted["geometry"] = shifted.geometry.apply(
        lambda g: translate(g, mdx, mdy)
    )

    # Calculate areas in UTM (meters)
    median_area = shifted.geometry.area.median()

    statuses = []
    confidences = []
    notes = []

    for geom in shifted.geometry:

        area_ratio = geom.area / median_area

        if 0.5 <= area_ratio <= 2.0:
            statuses.append("corrected")
            confidences.append(0.85)
            notes.append(
                f"Median village shift applied dx={mdx:.1f}m dy={mdy:.1f}m"
            )
        else:
            statuses.append("flagged")
            confidences.append(0.40)
            notes.append(
                "Uncertain plot size relative to village median"
            )

    preds = shifted.to_crs("EPSG:4326")

    preds["status"] = statuses
    preds["confidence"] = confidences
    preds["method_note"] = notes

    return preds[
        [
            "plot_number",
            "status",
            "confidence",
            "method_note",
            "geometry",
        ]
    ]