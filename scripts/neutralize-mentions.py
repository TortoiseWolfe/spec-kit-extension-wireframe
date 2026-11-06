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

It also escapes every "&" as "&amp;", because a browser decodes HTML character
references (for example &#64;name, &commat;name or even &#64name) into a live
"@name". After escaping, they show as literal text and the page looks the same.

Left alone: email addresses (an ASCII letter, digit or underscore right before
the "@"). Handles inside links are changed too: a link may stop working, which
is cheaper than guessing where a link ends.

Running it twice gives the same result.
"""
import re
import sys

ZWJ = "\u200d"

# "@" that starts a handle. GitHub's rule is ASCII, so ours is too: anything
# that is not an ASCII letter, digit or underscore before the "@" counts as a
# boundary, and a handle can follow it.
_MENTION = re.compile(r"(?<![A-Za-z0-9_])@(?=[A-Za-z0-9])")

# Every "&" that is not already "&amp;". Browsers decode HTML character
# references (&#64;, &#x40;, &commat;) and even some without the closing ";"
# (&#64victim), so we do not try to recognise them: all "&" are escaped, and
# the page shows the same text. "&amp;" is skipped so a second run changes
# nothing.
_AMP = re.compile(r"&(?!amp;)")


def neutralize(text: str) -> str:
    text = _AMP.sub("&amp;", text)
    return _MENTION.sub("@" + ZWJ, text)


def main() -> int:
    sys.stdout.write(neutralize(sys.stdin.read()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
