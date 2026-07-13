from __future__ import annotations
import re
from typing import Tuple


DANGEROUS_PATTERNS = [
    r"\bformat\b",                       # format a drive
    r"\bdel\b.*[\\/]\*",                 # mass delete
    r"\bdel\b\s+/[sqf]",                 # del /s /q /f recursive force
    r"\brmdir\b\s+/s",                   # recursive directory removal
    r"\brd\b\s+/s",
    r"\bRemove-Item\b.*-Recurse",        # PowerShell recursive remove
    r"\bdiskpart\b",
    r"\bcipher\b\s+/w",                  # wipe free space
    r"\bshutdown\b",
    r"\bRestart-Computer\b",
    r"\breg\b\s+delete",                 # registry deletion
    r"\bRemove-Item\b.*[A-Za-z]:\\\*",   # remove drive root
    r":\\\s*$",
    r"\bvssadmin\b\s+delete",
    r"\bbcdedit\b",
    r"\bcd\b.*&&.*\bdel\b",
]

def screen_command(command : str)->Tuple[bool, str]:
    lowered = command.lower()
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, lowered, flags=re.IGNORECASE):
            return False, f"Command is not safe to use, pattern : {pattern}"

    return True, "Command is safe to use"