<h1 align="center">human-code</h1>

<p align="center"><b>English</b> | <a href="README.ru.md">Русский</a></p>

<p align="center">
  <a href="https://t.me/qwarwin4git"><img src="https://img.shields.io/badge/Telegram-Follow-26A5E4?style=for-the-badge&labelColor=1b1f24&logo=telegram&logoColor=white" height="40" alt="Telegram: follow the channel"></a>
  <a href="mailto:qwarwin@gmail.com"><img src="https://img.shields.io/badge/Gmail-Contact-EA4335?style=for-the-badge&labelColor=1b1f24&logo=gmail&logoColor=white" height="40" alt="Gmail: contact"></a>
</p>

A skill for Claude that makes the code it writes look like a person wrote it.
I got tired of cleaning up `# increment counter` comments, emoji in prints and
docstrings on three-line functions every time, so I put it all in one skill.

What it does: drops comments that just restate the code, section dividers,
needless abstractions and try/except around everything. Keeps names in line
with each language's conventions and lines under 80 chars. Also writes normal
commit messages and READMEs, and doesn't add Claude as a co-author.

It also doesn't skip security: it finds the trust boundaries in the code and
checks hostile input there, including logic stuff like double spends, races
and trusting client packets in mods, not only the usual SQL injection list.

There are two versions, install only one since they trigger on the same stuff:

- `human-code-en` - English
- `human-code` - Russian

## Install

Claude Code:

    git clone https://github.com/Qwarwin4/human-code /tmp/hc
    cp -r /tmp/hc/human-code-en ~/.claude/skills/

On claude.ai: zip the skill folder and upload it in Settings > Capabilities > Skills.

## smell.py

A small script that looks for the usual tells in your files, plus obviously
risky calls like `shell=True`, `verify=False` or `pickle.loads`:

    python human-code-en/scripts/smell.py src/

It's a hint, not a linter. It can't tell a "why" comment from one that just
narrates the code, so check by eye.
