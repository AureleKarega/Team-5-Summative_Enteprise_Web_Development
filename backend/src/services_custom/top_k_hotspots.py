from collections import defaultdict
from math import floor

def coord_to_cell(lat, lon, cell_size_deg=0.01):
    """
    Map lat/lon to grid cell indices (simple rectangular grid).
    cell_size_deg ~ 0.01 deg ~ ~1.1 km (varies)
    """
    if lat is None or lon is None:
        return None
    return (floor(lat / cell_size_deg), floor(lon / cell_size_deg))

def count_pickup_cells(rows, lat_col='pickup_latitude', lon_col='pickup_longitude', cell_size_deg=0.01):
    """
    rows: iterable of dict-like rows
    Returns dict: cell -> count
    """
    counts = defaultdict(int)
    for r in rows:
        lat = r.get(lat_col)
        lon = r.get(lon_col)
        if lat is None or lon is None:
            continue
        cell = coord_to_cell(lat, lon, cell_size_deg)
        counts[cell] += 1
    return counts

def manual_top_k(counts_dict, k):
    """
    Manual selection of top-k from dictionary counts without using built-in sorted/heap.
    Uses repeated linear scan to pick max k times (O(k*n)). Not optimal for huge n, but valid.
    Returns list of tuples (cell, count) sorted descending.
    """
    items = list(counts_dict.items())
    result = []
    used = set()
    n = len(items)
    for _ in range(min(k, n)):
        best_idx = -1
        best_val = None
        for i, (cell, cnt) in enumerate(items):
            if i in used:
                continue
            if best_val is None or cnt > best_val:
                best_val = cnt
                best_idx = i
        if best_idx == -1:
            break
        used.add(best_idx)
        result.append(items[best_idx])
    return result

def top_k_hotspots(rows, k=10, cell_size_deg=0.01):
    counts = count_pickup_cells(rows, cell_size_deg=cell_size_deg)
    topk = manual_top_k(counts, k)
    # convert cell back to approximate coordinates (center of cell)
    hotspots = []
    for (cell, cnt) in topk:
        ci, cj = cell
        center_lat = (ci + 0.5) * cell_size_deg
        center_lon = (cj + 0.5) * cell_size_deg
        hotspots.append({
            "cell": cell,
            "center_lat": center_lat,
            "center_lon": center_lon,
            "count": cnt
        })
    return hotspots
