# human-code

Скилл для Claude: код без признаков генерации — без комментариев-пересказов, разделителей, эмодзи в логах, раздутых имён и лишних абстракций; с обычаями каждого языка и строками до 80 символов.

A Claude skill for code without the tells of generation — no narrating comments, dividers, emoji in logs, bloated names or needless abstractions; follows each language's customs and keeps lines under 80.

```
human-code/       русская версия
human-code-en/    English version
  SKILL.md                 правила и чек-лист / rules and checklist
  references/languages.md  обычаи и заметки по языкам / per-language customs
  references/examples.md   до / после — before / after
  scripts/smell.py         находит типичные признаки / finds typical tells
```

Ставь одну из двух — они срабатывают на одни и те же запросы.
Install only one of the two — they trigger on the same requests.

## Установка / Install

Claude.ai: загрузить `human-code.skill` или `human-code-en.skill` в Settings → Capabilities → Skills.

Claude Code:

```
git clone https://github.com/Qwarwin4/human-code /tmp/hc
cp -r /tmp/hc/human-code ~/.claude/skills/      # или / or human-code-en
```

## smell.py

```
python human-code/scripts/smell.py src/
```

Выход с кодом 1, если что-то нашлось. Это подсказка, а не линтер.
Exits with 1 if anything is found. It's a hint, not a linter.
