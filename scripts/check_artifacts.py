"""Verify generated source checksums."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def main():
    entries = (ROOT / "SHA256SUMS.txt").read_text().splitlines()
    for line in entries:
        digest, name = line.split("  ", 1)
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    print(f"PASS {len(entries)} source checksums")
if __name__ == "__main__":
    main()
