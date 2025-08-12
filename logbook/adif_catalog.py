"""
ADIF 3.1.5 catalog: tag metadata and lightweight validators.

This provides infrastructure to integrate the full ADIF tag set without
changing storage. Unknown tags are still accepted as JSON extras; when a
catalog entry exists, we can validate/coerce and drive UI suggestions.

To load the full spec, drop a JSON file at `assets/adif_3_1_5.json` with
entries like:

{
  "CALL": {"type": "str", "max": 32, "label": "Callsign"},
  "QSO_DATE": {"type": "date", "label": "QSO Date"},
  "POTA_REF": {"type": "str", "label": "POTA Ref"},
  ...
}

Types supported: str, int, float, date (YYYYMMDD), time (HHMM or HHMMSS), enum.
"""

from __future__ import annotations

import json
import os
import datetime as dt
from dataclasses import dataclass
from typing import Optional, Dict


@dataclass(frozen=True)
class TagMeta:
    name: str
    type: str = "str"
    max: Optional[int] = None
    enum: Optional[list[str]] = None
    label: Optional[str] = None


def _load_catalog_from_json(path: str) -> Dict[str, TagMeta]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    out: Dict[str, TagMeta] = {}
    for k, v in raw.items():
        nm = str(k).upper()
        out[nm] = TagMeta(
            name=nm,
            type=str(v.get("type", "str")),
            max=v.get("max"),
            enum=v.get("enum"),
            label=v.get("label"),
        )
    return out


def _default_seed() -> Dict[str, TagMeta]:
    # Minimal seed so the UI is immediately useful; the full spec can be loaded.
    base = {
        "IOTA": TagMeta(name="IOTA", type="str", max=10, label="IOTA"),
        "SOTA_REF": TagMeta(name="SOTA_REF", type="str", max=16, label="SOTA Ref"),
        "MY_SOTA_REF": TagMeta(name="MY_SOTA_REF", type="str", max=16, label="My SOTA Ref"),
        "POTA_REF": TagMeta(name="POTA_REF", type="str", max=16, label="POTA Ref"),
        "MY_POTA_REF": TagMeta(name="MY_POTA_REF", type="str", max=16, label="My POTA Ref"),
        "MY_SIG": TagMeta(name="MY_SIG", type="str", max=16, label="My SIG"),
        "MY_SIG_INFO": TagMeta(name="MY_SIG_INFO", type="str", max=32, label="My SIG Info"),
        "SIG": TagMeta(name="SIG", type="str", max=16, label="SIG"),
        "SIG_INFO": TagMeta(name="SIG_INFO", type="str", max=32, label="SIG Info"),
        "V2_PREFIX": TagMeta(name="V2_PREFIX", type="str", max=32, label="V2 Prefix"),
        "VUCC_GRIDS": TagMeta(name="VUCC_GRIDS", type="str", max=64, label="VUCC Grids"),
        "MY_VUCC_GRIDS": TagMeta(name="MY_VUCC_GRIDS", type="str", max=64, label="My VUCC Grids"),
        "STATE": TagMeta(name="STATE", type="str", max=16, label="State"),
        "CNTY": TagMeta(name="CNTY", type="str", max=32, label="County"),
        "TEN_TEN": TagMeta(name="TEN_TEN", type="int", label="10-10"),
        "AGE": TagMeta(name="AGE", type="int", label="Age"),
        "PROP_MODE": TagMeta(name="PROP_MODE", type="str", max=16, label="Prop Mode"),
        "SAT_MODE": TagMeta(name="SAT_MODE", type="str", max=16, label="Sat Mode"),
        "SAT_NAME": TagMeta(name="SAT_NAME", type="str", max=32, label="Satellite"),
        "WWFF": TagMeta(name="WWFF", type="str", max=16, label="WWFF"),
        "MY_WWFF": TagMeta(name="MY_WWFF", type="str", max=16, label="My WWFF"),
    }
    return base


# Load catalog: JSON file overrides the seed
ADIF_CATALOG: Dict[str, TagMeta] = {}
try:
    ADIF_CATALOG = _default_seed()
    ADIF_CATALOG.update(_load_catalog_from_json(os.path.join("assets", "adif_3_1_5.json")))
except Exception:
    # Be resilient; seed set is sufficient for UI hints
    pass


def normalize_extra_value(tag: str, val: str) -> str:
    """Coerce basic types to canonical ADIF string forms where possible.

    - date: YYYYMMDD
    - time: HHMMSS (accepts HHMM)
    - int/float: trimmed string preserving value
    - enum/str: stripped string
    """
    meta = ADIF_CATALOG.get(tag.upper())
    if not meta:
        return str(val).strip()
    t = meta.type
    s = str(val).strip()
    if s == "":
        return s
    try:
        if t == "date":
            # Accept YYYYMMDD or YYYY-MM-DD, output YYYYMMDD
            if len(s) == 10 and s[4] == "-":
                s = s.replace("-", "")
            dt.datetime.strptime(s, "%Y%m%d")
            return s
        if t == "time":
            # Accept HHMM or HHMMSS, output HHMMSS
            if len(s) == 4:
                dt.datetime.strptime(s, "%H%M")
                return s + "00"
            dt.datetime.strptime(s, "%H%M%S")
            return s
        if t == "int":
            return str(int(s))
        if t == "float":
            return str(float(s))
        if t == "enum" and meta.enum:
            up = s.upper()
            if up in meta.enum:
                return up
            # if not valid, keep original for user to see/change later
            return s
        return s
    except Exception:
        # On failure, keep original so the user can correct it later
        return str(val)


def tag_suggestions(limit: int = 200) -> list[str]:
    # Return up to `limit` tag names sorted for datalist suggestions
    names = sorted(ADIF_CATALOG.keys())
    return names[:limit]

