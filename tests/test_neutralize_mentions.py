"""Tests for scripts/neutralize-mentions.py (issue #4).

Run: python3 -m unittest discover -s tests -v
"""
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "neutralize-mentions.py"


def load():
    spec = importlib.util.spec_from_file_location("neutralize_mentions", SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class NeutralizeMentions(unittest.TestCase):
    def setUp(self):
        self.fn = load().neutralize

    def test_table_cell_author_is_wrapped(self):
        row = "| #4 | 13d | @hindermath | Some title | https://example.com/4 |"
        self.assertEqual(
            self.fn(row),
            "| #4 | 13d | `@hindermath` | Some title | https://example.com/4 |",
        )

    def test_list_item_author_is_wrapped(self):
        self.assertEqual(
            self.fn("- #4455 (open) — Add thing — @someone — https://x.test/1"),
            "- #4455 (open) — Add thing — `@someone` — https://x.test/1",
        )

    def test_handle_with_hyphen_and_digits(self):
        self.assertEqual(self.fn("by @jiezeng2004-design."), "by `@jiezeng2004-design`.")

    def test_team_mention_is_wrapped_whole(self):
        self.assertEqual(self.fn("cc @github/spec-kit-maintainers"), "cc `@github/spec-kit-maintainers`")

    def test_title_with_at_mentions_phrase(self):
        self.assertEqual(self.fn("copied @mentions here"), "copied `@mentions` here")

    def test_already_in_code_span_is_untouched(self):
        s = "author `@hindermath` filed it"
        self.assertEqual(self.fn(s), s)

    def test_fenced_block_is_untouched(self):
        s = "before\n```\n@hindermath\n```\nafter @other"
        self.assertEqual(self.fn(s), "before\n```\n@hindermath\n```\nafter `@other`")

    def test_email_address_is_untouched(self):
        s = "write to someone@example.com"
        self.assertEqual(self.fn(s), s)

    def test_url_with_at_is_untouched(self):
        s = "https://medium.com/@someone/post and https://x.test/a@b"
        self.assertEqual(self.fn(s), s)

    def test_html_comment_state_line_is_untouched(self):
        s = "<!-- extension-status-state: catalog_hash=abc run_at=2026-11-05 -->"
        self.assertEqual(self.fn(s), s)

    def test_idempotent(self):
        once = self.fn("| @a | @b-c |\nsee @d")
        self.assertEqual(self.fn(once), once)

    def test_no_active_mention_survives(self):
        import re

        out = self.fn("@a @b\n| @c |\n(@d) [@e] \"@f\" @g/h")
        stripped = re.sub(r"`[^`]*`", "", out)
        self.assertNotIn("@", stripped)

    def test_cli_reads_stdin_writes_stdout(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input="hi @hindermath\n",
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(r.stdout, "hi `@hindermath`\n")


if __name__ == "__main__":
    unittest.main()
