"""Tests for scripts/neutralize-mentions.py (issue #4).

Run: python3 -m unittest discover -s tests -v
"""
import html
import importlib.util
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "neutralize-mentions.py"
Z = "\u200d"

# What GitHub treats as a mention: "@" not preceded by an ASCII word char, then
# a letter or digit (a simplified copy of its own mention rule).
GITHUB_MENTION = re.compile(r"(?<![A-Za-z0-9_])@[A-Za-z0-9]")


def load():
    spec = importlib.util.spec_from_file_location("neutralize_mentions", SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class NeutralizeMentions(unittest.TestCase):
    def setUp(self):
        self.fn = load().neutralize

    def assertNoMention(self, text):
        out = self.fn(text)
        self.assertIsNone(GITHUB_MENTION.search(out), out)

    def test_table_cell_author(self):
        row = "| #4 | 13d | @hindermath | Some title | https://example.com/4 |"
        self.assertEqual(
            self.fn(row),
            f"| #4 | 13d | @{Z}hindermath | Some title | https://example.com/4 |",
        )

    def test_list_item_author(self):
        self.assertEqual(
            self.fn("- #4455 (open) — Add thing — @someone — https://x.test/1"),
            f"- #4455 (open) — Add thing — @{Z}someone — https://x.test/1",
        )

    def test_handle_with_hyphen_and_digits(self):
        self.assertNoMention("by @jiezeng2004-design.")

    def test_team_mention(self):
        self.assertNoMention("cc @github/spec-kit-maintainers")

    def test_title_with_at_mentions_phrase(self):
        self.assertNoMention("copied @mentions here")

    def test_delimiters_do_not_hide_a_mention(self):
        self.assertNoMention('(@a) [@b] "@c" <@d> *@e* _@f_ -@g /@h .@i ,@j')

    def test_odd_backticks_do_not_hide_a_mention(self):
        for s in ["`@victim", "``@victim`", "`a` `@victim", "``` @victim", "x ` y @victim ` z `"]:
            self.assertNoMention(s)

    def test_unclosed_fence_does_not_hide_a_mention(self):
        self.assertNoMention("```\n@victim\n")
        self.assertNoMention("```\n@one\n``\n@two\n```\n@three")
        self.assertNoMention("~~~\n@victim\n```\n")

    def test_html_comment_does_not_hide_a_mention(self):
        self.assertNoMention("<!-- x --> @victim <!-- y -->")
        self.assertNoMention("<!-- @victim -->")

    def test_url_does_not_hide_a_mention(self):
        for s in [
            "https://x.test/a|@victim",
            "https://x.test/a)@victim",
            "https://x.test/a]@victim",
            'https://x.test/a"@victim',
            "https://x.test/a`@victim",
            "https://x.test/a<@victim",
            "https://x.test/a @victim",
            "https://medium.com/@victim/post",
            "https://u:p@host.test/@victim",
        ]:
            self.assertNoMention(s)

    def test_non_ascii_before_at_does_not_hide_a_mention(self):
        for s in ["é@victim", "日本@victim", "ß@victim"]:
            self.assertNoMention(s)

    def test_html_character_references_do_not_make_a_mention(self):
        for s in [
            "&#64;victim",
            "&#x40;victim",
            "&#X40;victim",
            "&commat;victim",
            "@&#118;ictim",
            "@&#x76;ictim",
            "&#64;&#118;ictim",
            "&#38;#64;victim",
            "&#0064;victim",
            "&#64victim",
            "&#x40victim",
            "<div>&#64victim</div>",
            "&commatvictim",
        ]:
            out = self.fn(s)
            # every "&" is now "&amp;", so nothing decodes
            self.assertIsNone(re.search(r"&(?!amp;)", out), out)
            self.assertNoMention(html.unescape(out))

    def test_ampersand_text_renders_the_same(self):
        out = self.fn("R&D and AT&T &amp; co & more")
        self.assertEqual(html.unescape(out), "R&D and AT&T & co & more")

    def test_email_address_is_untouched(self):
        s = "write to someone@example.com"
        self.assertEqual(self.fn(s), s)

    def test_double_at_does_not_hide_a_mention(self):
        self.assertNoMention("@@victim")

    def test_non_handle_at_is_untouched(self):
        s = "the @-mentions rule, a lone @ and @) too"
        self.assertEqual(self.fn(s), s)

    def test_state_line_is_untouched(self):
        s = "<!-- extension-status-state: catalog_hash=abc123 run_at=2026-11-05T13:00:00Z -->"
        self.assertEqual(self.fn(s), s)

    def test_idempotent(self):
        once = self.fn("| @a | @b-c |\nsee @d")
        self.assertEqual(self.fn(once), once)

    def test_text_is_otherwise_unchanged(self):
        s = "| @a | @b |\nplain line\n"
        self.assertEqual(self.fn(s).replace(Z, ""), s)

    def test_cli_reads_stdin_writes_stdout(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input="hi @hindermath\n",
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        self.assertEqual(r.stdout, f"hi @{Z}hindermath\n")


if __name__ == "__main__":
    unittest.main()
