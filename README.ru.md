# human-code

<p align="center">
  <a href="https://t.me/qwarwin4git"><img src="https://img.shields.io/badge/Telegram-Follow-26A5E4?style=for-the-badge&logo=telegram&logoColor=white&labelColor=1b1f24" height="40" alt="Telegram: follow the channel"></a>
  <a href="mailto:qwarwin@gmail.com"><img src="https://img.shields.io/badge/Gmail-Contact-EA4335?style=for-the-badge&logo=gmail&logoColor=white&labelColor=1b1f24" height="40" alt="Gmail: contact"></a>
</p>

[English](README.md)

Скилл для Claude, чтобы код выглядел так, будто его писал человек, а не нейронка.
Надоело каждый раз вычищать комменты вида `# increment counter`, эмодзи в принтах
и докстринги на трёхстрочных функциях, так что собрал всё в один скилл.

Что он делает: убирает комментарии-пересказы, разделители, лишние абстракции и
try/except на всё подряд. Следит, чтобы имена были по обычаям языка, а строки не
длиннее 80 символов. Ещё пишет нормальные коммиты и ридми, без Claude в соавторах.

Про безопасность тоже не забывает: ищет в коде границы доверия и проверяет там
враждебный ввод, включая логические дыры вроде двойного списания, гонок и
доверия пакетам клиента в модах, а не только типовые SQL-инъекции.

Есть две версии, ставить надо одну, они срабатывают на одно и то же:

- `human-code` - на русском
- `human-code-en` - на английском

## Установка

Claude Code:

    git clone https://github.com/Qwarwin4/human-code /tmp/hc
    cp -r /tmp/hc/human-code ~/.claude/skills/

В claude.ai: запаковать папку скилла в zip и загрузить в Settings > Capabilities > Skills.

## smell.py

Скрипт, который ищет типичные признаки в файлах, и заодно явно опасные вызовы
вроде `shell=True`, `verify=False` или `pickle.loads`:

    python human-code/scripts/smell.py src/

Это подсказка, а не линтер. Комментарий "почему" от пересказа он отличить не умеет,
так что смотрите глазами.

Английская версия скилла лежит в `human-code-en/`, то же самое.
