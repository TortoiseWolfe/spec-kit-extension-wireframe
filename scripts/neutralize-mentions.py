#!/usr/bin/env python3
"""
Turn every active @mention in machine-generated Markdown into inline code.

GitHub emails anyone whose @handle appears in an issue or comment body. The
scheduled /extension-status triage copies handles from upstream search results,
so outside people were notified on every run (issue #4). Run every generated
body through this filter before posting it:

  python3 scripts/neutralize-mentions.py < body.md > body.safe.md

Rules:
  - `@name` and `@org/team` become `` `@name` `` (inline code never notifies).
  - Text already inside inline code or a fenced block is left alone.
  - Email addresses and URLs containing @ are left alone (GitHub does not
    treat them as mentions).
  - Running it twice gives the same result.
"""
import re
import sys

# Fenced blocks (``` or ~~~) and inline code spans are kept verbatim.
_PROTECTED = re.compile(
    r"(^[ \t]*(?:```|~~~).*?^[ \t]*(?:```|~~~)[ \t]*$"  # fenced block
    r"|``[^`\n]*``"  # double-backtick span
    r"|`[^`\n]*`"  # single-backtick span
    r"|<!--.*?-->"  # HTML comment (state lines)
    r"|https?://[^\s<>)\]]+)",  # bare URL
    re.DOTALL | re.MULTILINE,
)

# A handle starts with a letter or digit; may contain hyphens; may be org/team.
# Not preceded by a word char, backtick, slash, dot or @ (emails, URLs, spans).
_MENTION = re.compile(
    r"(?<![\w`/.@])@([A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:/[A-Za-z0-9_.-]+)?)"
)


def neutralize(text: str) -> str:
    out = []
    pos = 0
    for m in _PROTECTED.finditer(text):
        out.append(_MENTION.sub(r"`@\1`", text[pos : m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(_MENTION.sub(r"`@\1`", text[pos:]))
    return "".join(out)


def main() -> int:
    sys.stdout.write(neutralize(sys.stdin.read()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
