#!/usr/bin/env python3
"""Finds typical signs of generated code in source files."""
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

RISKY = [
    ("shell", re.compile(
        r"shell\s*=\s*True|\bos\.system\(|\bpopen\(|\bsystem\(|sh\W+-c\b")),
    ("tls check off", re.compile(
        r"verify\s*=\s*False|InsecureSkipVerify:\s*true"
        r"|rejectUnauthorized:\s*false|badCertificateCallback\s*=.*true")),
    ("unsafe deserialize", re.compile(
        r"pickle\.loads?\(|yaml\.load\((?!.*Loader)"
        r"|Binary[F]ormatter|Object[I]nputStream")),
    ("eval", re.compile(r"\beval\(|\bexec\(|new Function\(")),
    ("unsafe c call", re.compile(
        r"\b(gets|strcpy|strcat|sprintf|tmpnam|mktemp)\(")),
    ("weak rng", rx(
        r"(token|secret|passw\w*|key|otp|nonce|salt)\w*\s*:?=.*",
        r"(Math\.random|random\.(rand\w*|choice)|math/rand|\brand\(\)",
        r"|new Random\()")),
    ("weak hash", rx(r"(md[5]|sha[1])\W.*pass")),
    ("hardcoded secret", rx(
        r"(passw(or)?d|secret|api_?key|token)\w*\s*:?=\s*",
        r"[\"'][^\"'\s]{8,}[\"']")),
    ("world-writable", re.compile(r"\b0o?777\b|chmod\s+(-R\s+)?777")),
    ("innerHTML", re.compile(r"\.innerHTML\s*\+?=")),
    ("sql concat", rx(
        r"f[\"']\s*(select|insert|update|delete)\b.*\{",
        r"|[\"'`]\s*(select|insert|update|delete)\b[^\"'`]*[\"'`]\s*\+",
        r"|(select|insert|update|delete)\b.*[\"']\s*%\s*\(?\w")),
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
        for name, r in RISKY:
            if r.search(ln):
                hits.append((n, f"risky: {name}", s))

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
