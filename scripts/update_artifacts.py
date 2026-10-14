"""Generate source checksums; ignore untracked runtime state through git rules."""
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def main():
    names = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT).split(b"\0")
    paths = sorted({n.decode() for n in names if n and n.decode() != "SHA256SUMS.txt"})
    entries = [f"{hashlib.sha256((ROOT / p).read_bytes()).hexdigest()}  {p}\n" for p in paths if (ROOT / p).is_file()]
    (ROOT / "SHA256SUMS.txt").write_text("".join(entries))
    print(f"Updated {len(entries)} source checksums")
if __name__ == "__main__":
    main()
