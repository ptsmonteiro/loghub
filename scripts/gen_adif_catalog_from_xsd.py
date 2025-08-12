#!/usr/bin/env python3
"""
Generate assets/adif_3_1_5.json from the local ADX XSD (adx315.xsd).

This extracts element names and maps their types to a lightweight
catalog format used by LogHub for normalization and UI suggestions.

Usage:
  python scripts/gen_adif_catalog_from_xsd.py [path_to_xsd] [output_json]

Defaults:
  XSD:    ./adx315.xsd
  OUTPUT: ./assets/adif_3_1_5.json
"""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


XS = "{http://www.w3.org/2001/XMLSchema}"


def labelize(name: str) -> str:
    return name.replace("_", " ").title()


def type_from_xsd(tname: str) -> tuple[str, list[str] | None]:
    """Map XSD named types to catalog types.

    Returns (type, enum) where enum may be a list of allowed values.
    """
    t = tname.lower()
    if t in ("date",):
        return "date", None
    if t in ("time",):
        return "time", None
    if t in ("integer", "positiveinteger", "xs:unsignedint", "xs:int"):
        return "int", None
    if t in ("number", "numberge0"):
        return "float", None
    if t in ("boolean",):
        return "enum", ["Y", "N"]
    # Known enums we still treat as strings by default
    return "str", None


def main(xsd_path: Path, out_path: Path) -> int:
    tree = ET.parse(xsd_path)
    root = tree.getroot()

    # Build map of simpleType restrictions for inline types to help map base types
    simple_types: dict[str, str] = {}
    for st in root.findall(f".//{XS}simpleType"):
        name = st.attrib.get("name")
        if not name:
            continue
        restr = st.find(f"{XS}restriction")
        if restr is None:
            continue
        base = restr.attrib.get("base", "")
        # only store local name part
        simple_types[name] = base.split(":")[-1]

    catalog: dict[str, dict] = {}

    # Collect elements under RECORD and HEADER choices
    for el in root.findall(f".//{XS}element[@name='RECORD']"):
        # Under RECORD, get nested xs:element choices
        for field in el.findall(f".//{XS}choice//{XS}element"):
            tag = field.attrib.get("name")
            if not tag:
                continue
            typeref = field.attrib.get("type")
            ctype = "str"
            enum: list[str] | None = None
            if typeref:
                base = typeref.split(":")[-1]
                ctype, enum = type_from_xsd(base)
                # If type is a named simpleType alias, resolve once
                if ctype == "str" and base in simple_types:
                    ctype, enum = type_from_xsd(simple_types[base].lower())
            else:
                # Inline simpleType
                st = field.find(f"{XS}simpleType/{XS}restriction")
                if st is not None:
                    base = st.attrib.get("base", "")
                    base = base.split(":")[-1].lower()
                    ctype, enum = type_from_xsd(base)
                    # Special-case: certain inlined patterns that imply small int ranges
                    if ctype == "str" and base in ("positiveinteger", "integer"):
                        ctype = "int"
            catalog[tag] = {
                "type": ctype,
                "label": labelize(tag)
            }
            if enum:
                catalog[tag]["enum"] = enum

    # HEADER-level fields also useful for suggestions
    for el in root.findall(f".//{XS}element[@name='HEADER']"):
        for field in el.findall(f".//{XS}choice//{XS}element"):
            tag = field.attrib.get("name")
            if not tag:
                continue
            if tag in catalog:
                continue
            typeref = field.attrib.get("type")
            ctype = "str"
            enum: list[str] | None = None
            if typeref:
                base = typeref.split(":")[-1]
                ctype, enum = type_from_xsd(base)
            catalog[tag] = {
                "type": ctype,
                "label": labelize(tag)
            }
            if enum:
                catalog[tag]["enum"] = enum

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2, sort_keys=True)

    print(f"Wrote {len(catalog)} tags to {out_path}")
    return 0


if __name__ == "__main__":
    xsd = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("adx315.xsd")
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("assets/adif_3_1_5.json")
    raise SystemExit(main(xsd, out))

