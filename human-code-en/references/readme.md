# README and repository description

A generated README is obvious at once: emoji in every heading, a twelve-item "✨ Features", a wall of badges, "🤝 Contributing", "⭐ Star this repo if you find it useful!". A project's author doesn't write like that — they're lazy and they know what matters: what it is, how to install it, how to run it.

## README

Open with one or two sentences: what it is and why. First person and a reason are fine: "got tired of doing X by hand, so I wrote Y". Then only the sections this project actually needs, usually install and usage. Half a screen is fine for a small project.

Don't:

- Emoji in headings and lists.
- Badges that aren't real: CI, coverage, version, downloads. A badge is fine if there's an actual CI or package behind it.
- Marketing words: powerful, blazing-fast, seamless, robust, comprehensive, elegant, effortless, cutting-edge. Phrases like "Whether you're a beginner or a pro...", "This project aims to...".
- Boilerplate sections for the sake of it: Contributing, Code of Conduct, Acknowledgments, Roadmap, Support, a Table of Contents for three sections.
- Invented things: features, flags, commands, platforms that aren't in the code. Don't make up a license — if there's no LICENSE file, skip the section or ask.
- Em dashes in every sentence. People usually type a plain hyphen or just end the sentence.
- A feature list made of adjectives. If you list things, be concrete: "shows the track from any MPRIS player", not "🎵 Seamless media integration".

Do:

- Real, copyable commands in code blocks.
- Be honest about limitations: "only tested on Arch", "no Windows yet", "config is only read at startup".
- Use the language the author speaks and writes comments in. One language, not everything twice.
- Screenshots or gifs only if the user provided them; no `![screenshot](screenshot.png)` placeholders.

## Repository description

One line in the GitHub About field: under ~80 characters, no emoji, no trailing period, no "A powerful...". Just what it is: `rust applet for cosmic panel that shows the current track`. Topics: three to five real ones, no spam.

## Example

Before:

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

After:

```markdown
# cosmic-media-applet

Panel applet for COSMIC that shows the current track over MPRIS2.
Works with any player that supports it (tried spotify, mpv and
firefox).

## Build

    cargo build --release
    sudo install -Dm755 target/release/cosmic-media-applet /usr/bin/

Then add the applet to the panel in COSMIC settings.

## Known issues

- no cover art yet
- with several players running it just picks the first one
```
