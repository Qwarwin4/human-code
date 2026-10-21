# human-code

[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:qwarwin@gmail.com)
[![Telegram](https://img.shields.io/badge/Telegram-channel-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/qwarwin4git)


[Русский](README.ru.md)

A skill for Claude that makes the code it writes look like a person wrote it.
I got tired of cleaning up `# increment counter` comments, emoji in prints and
docstrings on three-line functions every time, so I put it all in one skill.

What it does: drops comments that just restate the code, section dividers,
needless abstractions and try/except around everything. Keeps names in line
with each language's conventions and lines under 80 chars. Also writes normal
commit messages and READMEs, and doesn't add Claude as a co-author.

There are two versions, install only one since they trigger on the same stuff:

- `human-code-en` - English
- `human-code` - Russian

## Install

Claude Code:

    git clone https://github.com/Qwarwin4/human-code /tmp/hc
    cp -r /tmp/hc/human-code-en ~/.claude/skills/

On claude.ai: zip the skill folder and upload it in Settings > Capabilities > Skills.

## smell.py

A small script that looks for the usual tells in your files:

    python human-code-en/scripts/smell.py src/

It's a hint, not a linter. It can't tell a "why" comment from one that just
narrates the code, so check by eye.
