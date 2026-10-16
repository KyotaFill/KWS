# KWS development

- Read `/home/kien/.codex/RTK.md` when available; prefix shell commands with `rtk` in that environment.
- This is an independent derivative of WMS, with the scope in `01_Tai_lieu/NGHIEP_VU.md`.
- Keep PostgreSQL migrations 001–026 and SQLite migrations immutable. Internal SQL schema remains `wms`.
- Preserve server-side authorization, separation of duties, version checks, idempotency, atomic stock/audit/ACK updates.
- The local deployment uses MySQL `kws_mysql` since 2026-10-16; preserve PostgreSQL for recovery. See `07_Kiem_tra/mysql/STATUS.md`.
- Use disposable MySQL through `scripts/check_mysql.py` or disposable PostgreSQL through `scripts/check_application.py`; never use the operating database for tests.
- Tk updates and teardown belong to the main thread. Wait for workers during exit/reload.
- Do not commit credentials, user databases or operational screenshots.
- Regenerate `SHA256SUMS.txt` with `scripts/update_artifacts.py`; verify with `scripts/check_artifacts.py`.
- Diagrams and README describe actual KWS code. Never label inherited WMS release evidence as KWS test results.
