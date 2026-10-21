# README и описание репозитория

Сгенерированный README узнаётся сразу: эмодзи в каждом заголовке, «✨ Features» на двенадцать пунктов, стена бейджей, «🤝 Contributing», «⭐ Star this repo if you find it useful!». Автор проекта так не пишет — ему лень, и он знает, что важно: что это, как поставить, как запустить.

## README

Начинай с одного-двух предложений: что это и зачем. Можно от первого лица и с причиной: «надоело вручную X, поэтому написал Y». Потом только те разделы, которые реально нужны этому проекту, обычно установка и использование. Для маленького проекта README на полэкрана — нормально.

Чего не делать:

- Эмодзи в заголовках и списках.
- Бейджи, которых нет на самом деле: CI, coverage, версия, загрузки. Бейдж можно, если за ним есть настоящий CI или пакет.
- Маркетинговые слова: powerful, blazing-fast, seamless, robust, comprehensive, elegant, effortless, cutting-edge, «мощный», «удобный и быстрый», «полноценное решение». Конструкции «Whether you're a beginner or a pro...», «This project aims to...».
- Шаблонные разделы ради галочки: Contributing, Code of Conduct, Acknowledgments, Roadmap, Support, Table of Contents для трёх разделов.
- Выдуманное: фичи, флаги, команды, платформы, которых нет в коде. Лицензию не придумывай — если в репо нет LICENSE, раздел не пиши или спроси.
- Длинные тире через каждую фразу. Люди чаще пишут обычный дефис или просто ставят точку.
- Список фич из прилагательных. Если перечисляешь — конкретно: «показывает трек из любого плеера с MPRIS», а не «🎵 Seamless media integration».

Что делать:

- Команды — реальные и копируемые, в блоках кода.
- Честно про ограничения: «проверял только на Arch», «Windows пока нет», «конфиг читается только при старте».
- Язык — тот, на котором автор общается и пишет комментарии в проекте. Один язык, а не всё дублями.
- Скриншот или гифка — только если пользователь их дал; не вставляй заглушки `![screenshot](screenshot.png)`.

## Описание репозитория

Одна строка в поле About на GitHub: до ~80 символов, без эмодзи, без точки в конце, без «A powerful...». Просто что это: `rust applet for cosmic panel that shows the current track`, `скилл для claude: код без признаков нейронки`. Темы (topics) — три-пять настоящих, без спама.

## Пример

До:

```markdown
# 🎵 CosmicMedia Applet 🚀

![Build](https://img.shields.io/badge/build-passing-green) ![License](https://img.shields.io/badge/license-MIT-blue) ![Stars](https://img.shields.io/github/stars/user/repo)

> A powerful, elegant and blazing-fast media applet for the COSMIC Desktop Environment! ✨

## ✨ Features

- 🎶 **Seamless MPRIS2 Integration** — Works with all your favorite players!
- ⚡ **Blazing Fast** — Written in Rust for maximum performance!
- 🎨 **Beautiful Design** — Fits perfectly into your desktop!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

⭐ Star this repo if you find it useful!
```

После:

```markdown
# cosmic-media-applet

Апплет для панели COSMIC, показывает текущий трек через MPRIS2.
Работает с любым плеером, который его поддерживает (проверял на
spotify, mpv и firefox).

## Сборка

    cargo build --release
    sudo install -Dm755 target/release/cosmic-media-applet /usr/bin/

Потом добавить апплет в панель через настройки COSMIC.

## Что не работает

- обложки пока не показываются
- если плееров несколько, берётся первый попавшийся
```
