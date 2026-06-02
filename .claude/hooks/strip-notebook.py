"""PostToolUse hook: strip outputs from .ipynb files after Edit/Write/MultiEdit.

Reads Claude Code's hook JSON from stdin, pulls out the edited file path, and
if it's a .ipynb runs nbstripout on it in-place. Silent no-op on non-notebooks.
"""
import json
import subprocess
import sys

NBSTRIPOUT = r"C:\Users\usuario\AppData\Roaming\Python\Python312\Scripts\nbstripout.exe"


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    path = (payload.get("tool_response") or {}).get("filePath") or payload.get(
        "tool_input", {}
    ).get("file_path", "")
    if not path or not path.lower().endswith(".ipynb"):
        return
    subprocess.run([NBSTRIPOUT, path], check=False)


if __name__ == "__main__":
    main()
