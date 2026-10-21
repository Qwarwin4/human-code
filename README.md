# human-code

Скилл для Claude: код без признаков генерации — без комментариев-пересказов, разделителей, эмодзи в логах, раздутых имён и лишних абстракций.

```
human-code/
├── SKILL.md                 основные правила и чек-лист
├── references/languages.md  заметки по языкам
├── references/examples.md   до / после
└── scripts/smell.py         находит типичные признаки в файлах
```

## Установка

Claude.ai: Settings → Capabilities → Skills → загрузить `human-code.skill` (или zip папки).

Claude Code:

```
git clone https://github.com/Qwarwin4/human-code ~/.claude/skills/human-code
```

## smell.py

```
python scripts/smell.py src/
```

Выход с кодом 1, если что-то нашлось. Это подсказка, а не линтер — комментарий «почему» он не тронет, но и смысл не поймёт.
