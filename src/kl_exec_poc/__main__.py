"""
Module entry point for `python -m kl_exec_poc`.

Delegates to the CLI main function.
"""

from .cli import main


if __name__ == "__main__":
    import sys

    raise SystemExit(main(sys.argv[1:]))
