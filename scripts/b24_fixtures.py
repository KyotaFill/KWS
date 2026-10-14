"""Reuse real domain setup fixtures, without collecting their tests a second time."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tests/foundation"))
from test_issues import issuing  # noqa: E402,F401
from test_openings import opening  # noqa: E402,F401
from test_orders import orders  # noqa: E402,F401
from test_receipts import receiving  # noqa: E402,F401
from test_reports_exports import reports  # noqa: E402,F401
