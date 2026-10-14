"""Verify KWS feature/document/image links against the actual application."""
import hashlib
import json
import re
from pathlib import Path

from apps.desktop.views.admin_workspace import SECTIONS

ROOT = Path(__file__).resolve().parents[1]
def main():
    features=json.loads((ROOT/"01_Tai_lieu/current_features.json").read_text())
    assert [f["key"] for f in features] == [s[1] for s in SECTIONS]
    shots=json.loads((ROOT/"assets/readme/screenshots.json").read_text())
    assert {x["feature"] for x in shots} == {s[1] for s in SECTIONS}|{"login"}
    for shot in shots:
        assert hashlib.sha256((ROOT/shot["file"]).read_bytes()).hexdigest() == shot["sha256"]
    for feature in features:
        assert (ROOT/feature["source"]).is_file()
        assert (ROOT/feature["image"]).is_file()
    for path in [ROOT/"README.md", *list((ROOT/"01_Tai_lieu").glob("*.md")), *list((ROOT/"03_So_do").rglob("*.md"))]:
        raw=path.read_text()
        for link in re.findall(r'\]\(([^)]+)\)|src="([^"]+)"',raw):
            target=next(x for x in link if x).split("#")[0]
            if not target or "://" in target:
                continue
            assert (path.parent/target).exists(), (path,target)
    print(f"PASS {len(features)} features, {len(shots)} screenshot hashes and documentation links")
if __name__ == "__main__":
    main()
