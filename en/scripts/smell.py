#!/usr/bin/env python3
"""Finds typical signs of generated code in source files."""
import re
import sys
from pathlib import Path

CMT = {
    ".py": "#", ".sh": "#", ".rb": "#", ".toml": "#", ".yaml": "#", ".yml": "#",
    ".go": "//", ".rs": "//", ".c": "//", ".h": "//", ".cpp": "//", ".hpp": "//",
    ".cc": "//", ".cs": "//", ".js": "//", ".ts": "//", ".tsx": "//", ".jsx": "//",
    ".dart": "//", ".kt": "//", ".java": "//", ".swift": "//", ".zig": "//",
}

EMOJI = re.compile("[\\U0001F300-\\U0001FAFF\\u2600-\\u27BF\\u2B50]")

RULES = [
    ("divider", re.compile(r"^\s*(#|//|/\*|--)\s*([=\-*#~]{4,}|.*[=\-*#~]{4,}\s*$)")),
    ("example usage", re.compile(r"(#|//)\s*(example usage|usage example|пример использования)", re.I)),
    ("in a real app", re.compile(r"in a (real|production)[- ](app|application|world|scenario|system)|в реальном (приложении|проекте)", re.I)),
    ("stub todo", re.compile(r"(TODO|FIXME):?\s*(implement|add (proper|real)|your code)", re.I)),
    ("edit trace", re.compile(r"(#|//)\s*(fixed|changed|updated|modified|new|added|исправлено|изменено|добавлено)\b\s*[:\-]", re.I)),
    ("args block", re.compile(r"^\s*(Args|Arguments|Returns|Parameters|Raises)\s*:\s*$|@param\s|@returns?\s|# Arguments$")),
    ("module header", re.compile(r"(this (module|file|script) (provides|contains|implements)|этот (модуль|файл|скрипт) (содержит|реализует))", re.I)),
    ("chatty print", re.compile(r"(print|console\.log|println!?|fmt\.Print\w*|Console\.WriteLine)\s*\(.*(Starting|Successfully|completed successfully|Done!)", re.I)),
]

NARRATE = re.compile(r"^\s*(#|//)\s*(check (if|whether)|loop (through|over)|iterate|increment|initiali[sz]e|create|return (the|a)|get the|set the|call the|define|import|extract|fetch|convert|parse the|calculate|compute|encode|decode|send the|read the|write the|open the|close the|update the|add the|handle the|validate|проверяем|получаем|создаём|создаем|возвращаем)\b", re.I)


def scan(path):
    ext = path.suffix.lower()
    mark = CMT.get(ext)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError) as e:
        print(f"{path}: skip ({e})", file=sys.stderr)
        return []

    hits = []
    code = cmts = 0
    for n, ln in enumerate(lines, 1):
        s = ln.strip()
        if not s:
            continue
        if mark and s.startswith(mark):
            cmts += 1
            if NARRATE.match(ln):
                hits.append((n, "narrating comment", s))
        else:
            code += 1
        if EMOJI.search(ln):
            hits.append((n, "emoji", s))
        for name, rx in RULES:
            if rx.search(ln):
                hits.append((n, name, s))

    if code >= 10 and cmts / code > 0.25:
        hits.append((0, "comment density", f"{cmts} comment lines on {code} code lines"))
    return hits


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: smell.py <file|dir>...")

    files = []
    for a in sys.argv[1:]:
        p = Path(a)
        if p.is_dir():
            files += [f for f in p.rglob("*") if f.suffix.lower() in CMT and f.is_file()]
        else:
            files.append(p)

    total = 0
    for f in files:
        for n, name, s in scan(f):
            total += 1
            print(f"{f}:{n}: {name}: {s[:100]}")

    if total:
        print(f"\n{total} hits", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
