# human-code (English)

A Claude skill for code without the tells of generation: no narrating comments, dividers, emoji in logs, bloated names or needless abstractions.

```
en/
├── SKILL.md                 core rules and checklist
├── references/languages.md  per-language notes
├── references/examples.md   before / after
└── scripts/smell.py         finds typical tells in files
```

Claude Code:

```
git clone https://github.com/Qwarwin4/human-code /tmp/hc && cp -r /tmp/hc/en ~/.claude/skills/human-code-en
```

Install either this or the Russian version at the repo root, not both — they trigger on the same requests.
