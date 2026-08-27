import re
import os
from typing import List, Dict, Optional
from pathlib import Path

# Regex to extract stock code, country, and status from filename
FILENAME_PATTERN = re.compile(r"^(\d{2})(\d{2})\.([A-Z]+)\.(AU|US)\.(\d+)\.(\w+)\.md$")


def parse_filename(filename: str) -> Optional[Dict]:
    """Parse markdown filename into components."""
    match = FILENAME_PATTERN.match(filename)
    if not match:
        return None
    return {
        "year": match.group(1),
        "week": match.group(2),
        "code": match.group(3),
        "country": match.group(4),
        "n": int(match.group(5)),
        "status": match.group(6)
    }


def extract_conditions(filepath: str) -> List[str]:
    """Extract alert conditions from markdown file."""
    with open(filepath, "r") as f:
        lines = f.readlines()
    conditions = []
    for line in lines:
        line = line.strip()
        if line.startswith("> alert"):
            condition = line[2:].strip()  # Remove "> "
            conditions.append(condition)
    return conditions


def get_trade_files(base_folder: str) -> List[Dict]:
    """Get all trade files to monitor (status=watch or open)."""
    trade_files = []
    for filename in os.listdir(base_folder):
        if not filename.endswith(".md"):
            continue
        parsed = parse_filename(filename)
        if not parsed or parsed["status"] not in ["watch", "open"]:
            continue
        filepath = os.path.join(base_folder, filename)
        conditions = extract_conditions(filepath)
        trade_files.append({
            **parsed,
            "filepath": filepath,
            "conditions": conditions
        })

    # Group by (code, country) and pick highest n
    grouped = {}
    for file in trade_files:
        key = (file["code"], file["country"])
        if key not in grouped or file["n"] > grouped[key]["n"]:
            grouped[key] = file

    return list(grouped.values())