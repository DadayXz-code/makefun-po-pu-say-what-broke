#!/usr/bin/env python3
"""Say What Actually Broke — make.fun entry.

Writes one single-line software error message to <output dir>/entry.txt.

The line tells the brutal truth about a real failure (a payment that went
through while the order itself failed) and stays funny on a single read,
while also telling the user what to do next instead of paying twice.

Usage:
    python3 main.py [output_dir]

The output directory defaults to the MAKEFUN_OUTPUT_DIR environment
variable, or /output when neither is given. Only the Python standard
library is used, and the output is fully deterministic: the same bytes
are written on every run.
"""

import os
import sys

# The entry text: one line, at most 200 characters, naming the real
# failure in plain words and telling the user what to do next.
ENTRY_TEXT = (
    "Payment succeeded, order failed: we took your money and lost the "
    "receipt. Don't pay twice \u2014 check your bank first, then come "
    "shout at us."
)

MAX_CHARS = 200


def resolve_output_dir(argv):
    """Return the output directory from argv, the environment, or /output."""
    if len(argv) > 1:
        return argv[1]
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def validate_text(text):
    """Check the entry text against the bounty gate before writing it.

    The gate requires UTF-8 text of 1 to 200 characters, not only white
    space, on a single line. Raises ValueError when the text breaks a rule.
    """
    stripped = text.strip()
    if not stripped:
        raise ValueError("entry text must not be empty or only whitespace")
    if len(text) != len(stripped):
        raise ValueError("entry text must not start or end with whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry text must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry text is {} characters, over the {} limit".format(
                len(text), MAX_CHARS
            )
        )
    return text


def write_entry(output_dir):
    """Write ENTRY_TEXT to entry.txt inside output_dir and return the path."""
    validate_text(ENTRY_TEXT)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY_TEXT + "\n")
    return path


def main(argv):
    output_dir = resolve_output_dir(argv)
    path = write_entry(output_dir)
    print("Wrote {} ({} characters)".format(path, len(ENTRY_TEXT)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
