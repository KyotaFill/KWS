"""Edition boundaries and real Tk/API screenshots on a disposable test database."""
import hashlib
import json
import os
import socket
import threading
import time
import tkinter as tk
from pathlib import Path
from typing import get_args

import pyotp
import pytest
import uvicorn
from fastapi.testclient import TestClient
from PIL import Image, ImageGrab

from apps.desktop.api.client import DesktopSettings
from apps.desktop.views.admin_workspace import SECTIONS
from apps.desktop.views.shell import DesktopShell
from apps.server.api.app import create_app
from apps.server.infrastructure.config import Settings
from packages.contracts.printing import PrintCreate, ScanInput
from packages.contracts.reports import ReportCode


def test_edition_removed_routes_are_not_registered():
    app = create_app(Settings(database_url="postgresql+psycopg://localhost/unused"))
    try:
        with TestClient(app) as client:
            for path in ("consignment-receipts", "serials/lookup", "custom-fields", "fulfillment", "quality/sources", "moves", "transfers", "returns", "counts", "reversals", "imports", "master/stock-owners", "master/consignment-agreements"):
                assert client.get("/api/v1/" + path).status_code == 404, path
        assert get_args(ReportCode) == ("R01", "R02", "R03", "R04", "R06", "R08")
        assert get_args(PrintCreate.model_fields["template"].annotation) == ("RECEIPT", "ISSUE", "PRODUCT_LABEL", "LOCATION_LABEL")
        assert get_args(ScanInput.model_fields["flow"].annotation) == ("RECEIPT", "ISSUE")
    finally:
        app.state.database.dispose()


def test_brand_and_state_are_independent(monkeypatch, tmp_path):
    from apps.desktop.local_store.device import default_data_directory
    from packages.contracts.compatibility import compatible, server_headers
    monkeypatch.setenv("WMS_API_URL", "http://127.0.0.1:9999/api/v1")
    assert DesktopSettings().api_url != "http://127.0.0.1:9999/api/v1"
    assert default_data_directory().name == "kws-lan"
    assert compatible(server_headers())
    assert not compatible({"X-WMS-API-Protocol": "1", "X-WMS-Recovery-Protocol": "lookup-v1,send-v1"})
    with Image.open("apps/desktop/assets/kws-logo-transparent.png") as logo:
        assert logo.mode == "RGBA"
        assert logo.getextrema()[3] == (0, 255)


@pytest.mark.integration
@pytest.mark.gui
def test_actual_kws_screens(orders, tmp_path):
    f = orders
    account, secret = f.iam.user("kws-review", mfa=True)
    for role in ("SYSADMIN", "MASTER_DATA"):
        f.iam.grant(account, role)
    for role in ("BUYER", "SELLER", "WAREHOUSE_MANAGER", "RECEIVER", "CONTROLLER", "DIRECTOR"):
        f.iam.grant(account, role, f.warehouse)
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    server = uvicorn.Server(uvicorn.Config(f.client.app, log_level="error", lifespan="off"))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
    thread.start()
    root = tk.Tk()
    root.geometry("1440x900+0+0")
    shell = None
    records = []
    target = Path(os.environ.get("KWS_CAPTURE_DIR", tmp_path / "screenshots"))
    target.mkdir(parents=True, exist_ok=True)
    try:
        shell = DesktopShell(root, DesktopSettings(api_url=f"http://127.0.0.1:{sock.getsockname()[1]}/api/v1", local_data_dir=tmp_path / "desktop"))
        def settle(condition=lambda: True):
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                root.update()
                busy = any(getattr(o, "pending", None) for o in shell.worker_owners())
                if condition() and not busy:
                    for _ in range(12):
                        root.update()
                        time.sleep(.025)
                    return
                time.sleep(.01)
            pytest.fail("KWS screen did not settle: " + shell.session_view.status.get())
        def shot(key):
            root.update()
            path = target / (key + ".png")
            x,y = root.winfo_rootx(),root.winfo_rooty()
            ImageGrab.grab(bbox=(x,y,x+root.winfo_width(),y+root.winfo_height())).save(path)
            records.append(dict(feature=key, file="assets/readme/"+path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(), source="Actual KWS Tk UI with real API and disposable PostgreSQL test data"))
        settle()
        shot("login")
        session = shell.session_view
        session.username.set("kws-review")
        session.password.set("Test-only-password-2026!")
        session.login()
        settle()
        session.code.set(pyotp.TOTP(secret).at(f.iam.now))
        session.mfa()
        settle(lambda: shell.authenticated)
        for _, key, _, _ in SECTIONS:
            assert shell.open_key(key)
            settle()
            assert shell.notebook.select() == str(getattr(shell, key))
            shot(key)
        assert not hasattr(shell,"import_view")
        assert not hasattr(shell,"transfer_view")
        (target / "screenshots.json").write_text(json.dumps(records,ensure_ascii=False,indent=2)+"\n")
    finally:
        if shell:
            shell.close()
            shell.finish()
        else:
            root.destroy()
        server.should_exit = True
        thread.join(10)
        sock.close()
