#!/usr/bin/env python3
"""Находит в исходниках типичные признаки сгенерированного кода."""
import re
import sys
from pathlib import Path

WIDTH = 80

HASH = {".py", ".sh", ".rb", ".toml", ".yaml", ".yml"}
SLASH = {
    ".go", ".rs", ".c", ".h", ".cpp", ".hpp", ".cc", ".cs", ".js", ".ts",
    ".tsx", ".jsx", ".dart", ".kt", ".java", ".swift", ".zig",
}
CMT = {e: "#" for e in HASH} | {e: "//" for e in SLASH}

EMOJI = re.compile("[\\U0001F300-\\U0001FAFF\\u2600-\\u27BF\\u2B50]")
URL = re.compile(r"https?://\S+")


def rx(*parts):
    return re.compile("".join(parts), re.I)


RULES = [
    ("divider", rx(
        r"^\s*(#|//|/\*|--)\s*",
        r"([=\-*#~]{4,}|.*[=\-*#~]{4,}\s*$)")),
    ("example usage", rx(
        r"(#|//)\s*(example usage|usage example|пример использования)")),
    ("real-app excuse", rx(
        r"in a (real|production)[- ]",
        r"(app|application|world|scenario|system)",
        r"|в реальном (приложении|проекте)")),
    ("stub todo", rx(
        r"(TODO|FIXME):?\s*(implement|add (proper|real)|your code)")),
    ("edit trace", rx(
        r"(#|//)\s*(fixed|changed|updated|modified|new|added",
        r"|исправлено|изменено|добавлено)\b\s*[:\-]")),
    ("args block", re.compile(
        r"^\s*(Args|Arguments|Returns|Parameters|Raises)\s*:\s*$"
        r"|@param\s|@returns?\s|# Arguments$")),
    ("module header", rx(
        r"this (module|file|script) (provides|contains|implements)",
        r"|этот (модуль|файл|скрипт) (содержит|реализует)")),
    ("chatty print", rx(
        r"(print|console\.log|println!?|fmt\.Print\w*|Console\.WriteLine)",
        r"\s*\(.*(Starting|Successfully|completed successfully|Done!)")),
]

NARRATE = rx(
    r"^\s*(#|//)\s*(check (if|whether)|loop (through|over)|iterate",
    r"|increment|initiali[sz]e|create|return (the|a)|get the|set the",
    r"|call the|define|import|extract|fetch|convert|parse the|calculate",
    r"|compute|encode|decode|send the|read the|write the|open the",
    r"|close the|update the|add the|handle the|validate",
    r"|проверяем|получаем|создаём|создаем|возвращаем)\b",
)


def scan(path):
    mark = CMT.get(path.suffix.lower())
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
        w = len(ln.expandtabs(4))
        if w > WIDTH and not URL.search(ln):
            hits.append((n, f"long line ({w})", s))
        if EMOJI.search(ln):
            hits.append((n, "emoji", s))
        for name, r in RULES:
            if r.search(ln):
                hits.append((n, name, s))

    if code >= 10 and cmts / code > 0.25:
        hits.append((0, "comment density", f"{cmts} comments / {code} code"))
    return hits


def files(args):
    for a in args:
        p = Path(a)
        if p.is_dir():
            yield from (f for f in p.rglob("*")
                        if f.suffix.lower() in CMT and f.is_file())
        else:
            yield p


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: smell.py <file|dir>...")

    total = 0
    for f in files(sys.argv[1:]):
        for n, name, s in scan(f):
            total += 1
            print(f"{f}:{n}: {name}: {s[:60]}")

    if total:
        print(f"\n{total} hits", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
