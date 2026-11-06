#!/usr/bin/env python3
"""
Stop machine-generated Markdown from tagging anyone on GitHub.

GitHub emails anyone whose @handle appears in an issue or comment body. The
scheduled /extension-status triage copies handles from upstream search results,
so outside people were notified on every run (issue #4). Run every generated
body through this filter before posting it:

  python3 scripts/neutralize-mentions.py < body.md > body.safe.md

How it works: it puts a zero-width joiner (U+200D, an invisible character)
right after the "@" of every handle. GitHub only sees a mention when a letter
or digit follows the "@", so the handle still reads the same on screen but
never notifies. It does not try to understand Markdown (code spans, fences,
comments), because a filter that guesses the context can be fooled by odd
backticks; this one fails closed.

Left alone: email addresses (a letter or digit before the "@"), and "@"
characters inside a plain https:// link, which GitHub turns into a link and
never into a mention.

Running it twice gives the same result.
"""
import re
import sys

ZWJ = "‍"

# A bare URL: GitHub links it, and handles inside a link are not mentions.
_URL = re.compile(r"https?://[^\s<>|`\"')\]]+")

# "@" that starts a handle: not part of an email (word char before) and
# followed by a letter or digit.
_MENTION = re.compile(r"(?<!\w)@(?=[A-Za-z0-9])")


def neutralize(text: str) -> str:
    out = []
    pos = 0
    for m in _URL.finditer(text):
        out.append(_MENTION.sub("@" + ZWJ, text[pos : m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(_MENTION.sub("@" + ZWJ, text[pos:]))
    return "".join(out)


def main() -> int:
    sys.stdout.write(neutralize(sys.stdin.read()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
