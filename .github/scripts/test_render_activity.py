"""Offline tests for render_activity.py (python -m unittest discover -s .github/scripts -v)."""
import contextlib
import datetime as dt
import io
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render_activity as ra  # noqa: E402

FIXTURE = HERE / "fixtures" / "sample_activity.json"
SVGS = ["neural-activity-dark.svg", "neural-activity-light.svg", "telemetry-dark.svg", "telemetry-light.svg"]
LIMITS = {"neural-activity": 120_000, "telemetry": 30_000}


def render(out):
    with contextlib.redirect_stdout(io.StringIO()):
        return ra.main(["--input", str(FIXTURE), "--out", str(out)])


class RenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "a"
        assert render(cls.out) == 0

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_outputs_are_wellformed_and_sandbox_safe(self):
        for name in SVGS:
            raw = (self.out / name).read_text(encoding="ascii")
            root = ET.fromstring(raw)
            self.assertTrue(root.tag.endswith("svg"), name)
            for bad in ("<script", "foreignObject", "href", "@import", "<image"):
                self.assertNotIn(bad, raw, f"{bad} in {name}")
            style = "".join(re.findall(r"<style>(.*?)</style>", raw, re.S))
            self.assertNotIn("http", style, name)
            self.assertIn("prefers-reduced-motion", raw, name)
            self.assertIn("<title", raw, name)
            self.assertIn("<desc", raw, name)

    def test_size_limits(self):
        for name in SVGS:
            limit = LIMITS[name.rsplit("-", 1)[0]]
            self.assertLessEqual((self.out / name).stat().st_size, limit, name)

    def test_deterministic(self):
        out2 = Path(self.tmp.name) / "b"
        self.assertEqual(render(out2), 0)
        for name in SVGS + ["activity.json"]:
            self.assertEqual((self.out / name).read_bytes(), (out2 / name).read_bytes(), name)

    def test_caption_shows_public_and_private(self):
        raw = (self.out / "neural-activity-dark.svg").read_text(encoding="ascii")
        self.assertRegex(raw, r"public \d")
        self.assertRegex(raw, r"private \d")


class MetricTests(unittest.TestCase):
    def test_streaks(self):
        today = dt.date(2025, 1, 10)
        start = today - dt.timedelta(days=364)
        counts = {start + dt.timedelta(days=i): 0 for i in range(365)}
        for d in (1, 2, 3, 4, 5):  # longest run: 5 days
            counts[dt.date(2024, 6, d)] = 1
        for d in (7, 8, 9):  # current run ends yesterday (today is empty)
            counts[dt.date(2025, 1, d)] = 2
        series = {k.isoformat(): {"public": v, "private": 0} for k, v in counts.items()}
        m = ra.compute(series, today, False, {}, {"public": 1, "private": None})["metrics"]
        self.assertEqual(m["longest_streak"], 5)
        self.assertEqual(m["current_streak"], 3)
        self.assertEqual(m["active_days"], 8)
        self.assertEqual(m["total"], 11)
        self.assertIsNone(m["private"])

    def test_private_split(self):
        today = dt.date(2025, 1, 10)
        series = {"2025-01-09": {"public": 2, "private": 3}}
        m = ra.compute(series, today, True, {}, {"public": 1, "private": 2})["metrics"]
        self.assertEqual((m["public"], m["private"], m["total"]), (2, 3, 5))


class CarryForwardTests(unittest.TestCase):
    PREV = {"private_known": True, "updated": "2025-01-09", "repos": {"public": 2, "private": 5},
            "languages": [{"name": "Python", "color": "#3572A5", "pct": 100.0}],
            "days": [{"date": "2025-01-08", "public": 1, "private": 4}, {"date": "2025-01-09", "public": 0, "private": 2}]}

    def raw(self, series):
        return {"series": series, "private_known": False, "languages": {}, "repos": {"public": 2, "private": None}}

    def test_private_counts_carried_forward(self):
        out = ra.carry_forward(self.raw({"2025-01-08": {"public": 1, "private": 0}, "2025-01-10": {"public": 3, "private": 0}}), self.PREV)
        self.assertTrue(out["private_known"])
        self.assertEqual(out["series"]["2025-01-08"], {"public": 1, "private": 4})
        self.assertEqual(out["series"]["2025-01-10"], {"public": 3, "private": 0})
        self.assertEqual((out["repos"]["private"], out["private_as_of"]), (5, "2025-01-09"))

    def test_calendar_with_private_is_split_not_doubled(self):
        out = ra.carry_forward(self.raw({"2025-01-08": {"public": 5, "private": 0}}), self.PREV)
        self.assertEqual(out["series"]["2025-01-08"], {"public": 1, "private": 4})

    def test_no_snapshot_keeps_public_only(self):
        out = ra.carry_forward(self.raw({"2025-01-08": {"public": 1, "private": 0}}), None)
        self.assertFalse(out["private_known"])

    def test_no_placeholder_text_without_private(self):
        series = {"2025-01-09": {"public": 2, "private": 0}}
        data = ra.compute(series, dt.date(2025, 1, 10), False, {}, {"public": 1, "private": None})
        for svg in (ra.render_telemetry(data, "dark"), ra.render_neural(data, "light")):
            self.assertNotIn("syncing", svg)
            ET.fromstring(svg)


class ParserTests(unittest.TestCase):
    SNIPPET = (
        '<td tabindex="0" data-ix="0" style="width: 11px" data-date="2025-09-28" id="contribution-day-component-0-0" '
        'data-level="0" role="gridcell" class="ContributionCalendar-day"></td>'
        '<td data-date="2025-09-29" id="contribution-day-component-1-0" data-level="2" class="ContributionCalendar-day"></td>'
        '<td data-date="2025-09-30" id="contribution-day-component-2-0" data-level="4"></td>'
        '<tool-tip id="tooltip-a" for="contribution-day-component-0-0" popover="manual">No contributions on September 28th.</tool-tip>'
        '<tool-tip id="tooltip-b" for="contribution-day-component-1-0" popover="manual">3 contributions on September 29th.</tool-tip>'
        '<tool-tip id="tooltip-c" for="contribution-day-component-2-0" popover="manual">1,204 contributions on September 30th.</tool-tip>'
    )

    def test_parse(self):
        self.assertEqual(ra.parse_contributions_html(self.SNIPPET),
                         {"2025-09-28": 0, "2025-09-29": 3, "2025-09-30": 1204})

    def test_parse_rejects_unknown_markup(self):
        with self.assertRaises(ra.RenderError):
            ra.parse_contributions_html("<html></html>")


if __name__ == "__main__":
    unittest.main()
