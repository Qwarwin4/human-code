---
name: human-code-en
description: Write code the way an experienced human developer would, not an AI — no comments that narrate the code, no section dividers, no emoji in logs, no bloated names, no needless abstractions or defensive checks on everything. Use this skill EVERY time you write, edit or refactor code in any language (Python, Go, Rust, C++, C#, JS/TS, Dart, Kotlin, Bash, etc.), even if the user doesn't explicitly ask for a "human" style — especially when they say "make it look hand-written", "humanize this code", "so it doesn't look AI-generated", "clean up this code", or complain about excessive comments and verbosity.
---

# Human code

AI-written code is recognizable at a glance, and not because it's bad — it's *uniform*. Every function has a docstring, every line has a comment, `try/except` wraps everything, `print("✅ Done!")`, dividers like `# ===== Helpers =====`. A real developer doesn't write like that: they don't have time to explain the obvious, they trust their own code, and they write for the task at hand rather than for an imaginary beginner reader.

The goal is code that looks like the work of a confident mid-to-senior developer: precise, idiomatic, no filler. This is not about sloppiness. Typos, bugs and junk are never added on purpose — the "human" quality comes from what the code *doesn't* contain.

## Workflow

1. **Look at the existing code first.** When editing a project, its style beats everything below. Names, indentation, error handling, presence or absence of comments, the language comments are written in — copy them as they are. A piece written in a foreign style stands out more than anything else.
2. **Write working code.** Correctness comes first.
3. **Go over it with the checklist below** and cut what's unnecessary. Usually the code ends up 20–40% shorter.
4. For language specifics, open the relevant section of `references/languages.md`. If unsure what "before/after" looks like, see `references/examples.md`.
5. If you write files to disk, you can run `python scripts/smell.py <files>` — it finds the mechanically detectable tells (emoji, dividers, template docstrings, "Example usage"). It's a hint, not a verdict.

## What gives AI away — and what to do instead

### Comments

Humans comment on *why*, not *what*, and they do it rarely — where the next reader would otherwise trip.

- Remove comments that restate the code: `# increment counter`, `// loop through users`, `# return the result`.
- Remove docstrings on trivial and private functions. The `Args: / Returns: / Raises:` template is for a library's public API, and only if the project does that.
- Remove module headers like "This module provides utilities for...".
- No dividers: `# ====`, `// ------ Helpers ------`, `#region` without a reason.
- No traces of the conversation: `# Fixed: ...`, `# Changed to use X instead of Y`, `# Updated per request`, `# New implementation`. The code doesn't know about the chat.
- No excuse stubs: `# In a real application you would...`, `# TODO: add proper error handling`, `# Your code here`.
- Keep a comment if it carries information the code doesn't: a workaround for a bug, a link to an issue, a non-obvious invariant, the reason for a strange number. Keep it short, lowercase, no trailing period, like a note to yourself: `# xdg-open hangs on kde without this`.

### Names

Name length is proportional to scope. A counter in a three-line loop is `i`, a buffer is `buf`, a config is `cfg`, a connection is `conn`, an error is `err`/`e`. Long descriptive names are for things that live long and are used far from where they're declared.

- Not `user_input_validation_result` but `ok` or `valid`.
- Not `current_index_in_list` but `i`.
- Avoid empty suffixes like `Manager`, `Handler`, `Helper`, `Util`, `Processor`, `Service` when the class just does something — name it by what it is (`Player`, `Cache`, `Queue`).
- Avoid faceless `data`, `result`, `process_data()`, `handle()` — if short, make it specific: `rows`, `resp`, `parse()`.
- Abbreviations common in the domain and language are fine: `ctx`, `req`, `res`, `msg`, `pkt`, `fd`, `addr`, `idx`, `tmp`, `src`, `dst`, `n`.

### Structure and abstractions

AI designs for imaginary future extension. Humans write for the current task and extract code once it actually repeats.

- Don't create a class with a single method — that's a function.
- Don't introduce factories, strategies, interfaces and config dataclasses for two or three values when there's no second implementation.
- Don't split code into 3-line functions called once. A helper is justified if it's reused or its name explains something that would otherwise be unclear.
- Don't extract every number into a `SCREAMING_CONSTANT`. A constant is for values used in several places or whose meaning isn't obvious.
- Don't add `argparse`, `logging.basicConfig`, `main()` with `if __name__ == "__main__"` to a 20-line script unless asked. In a proper utility, though, that's normal.
- Code doesn't have to be symmetrical. If one branch is one line and the other is ten, that's fine.
- Early `return`/`continue` instead of nesting; no `else` after `return`.

### Error handling

- Validate at the boundaries (user input, network, files, external APIs) and trust your own internal functions.
- Don't wrap everything in `try/except Exception` with logging and `return None`. Catch what you can actually handle; let the rest fail or propagate.
- Don't check for `None`/`null` what can't be `None`. No `isinstance` checks on arguments inside your own code.
- Error messages are short, lowercase, no period or exclamation: `"bad config: %v"`, `"no such device"`, `"failed to open {path}"`. Not "An error occurred while attempting to open the file. Please check...".

### Output and logs

- No emoji in `print`/logs/CLI output: no `✅`, `🚀`, `❌`. Only if it's an intended part of the UI and the user wants it.
- Don't log every step (`Starting...`, `Processing item 3...`, `Done!`). Humans print what actually needs to be seen.
- No banners and `=` boxes in console tools unless requested.

### The language's local customs

Every language has settled habits its community follows almost without exception: name casing, where underscores go, how acronyms are written, which prefixes and suffixes are used, how files and modules are named. A real developer in that language does this on autopilot, and mixing the customs of different languages is one of the clearest signs of an outsider: `camelCase` in Rust, `SCREAMING_CASE` constants in Dart, `get_` getters in Go, an `I` prefix on interfaces in TypeScript.

- Before writing in a language, recall its customs and follow them. A short cheat sheet for each language opens its section in `references/languages.md`.
- If the project departs from the language's customs, follow the project.
- Don't carry habits from one language into another, even if a neighbouring file in a different language does it that way.

### Line length

A general rule almost everyone shares: lines no longer than ~80 characters. Long lines are harder to read, look bad in diffs and split editors, and they're a common AI tell — call chains and conditions crammed into half a screen.

- If the project or the language's formatter has its own limit, that wins.
- Break by meaning: after a comma in arguments, before an operator in a long condition, at each link of a call chain. Sometimes pulling a piece into a variable with a short clear name beats wrapping.
- Long string literals, URLs and paths can stay as they are — splitting them is worse.

### Types and syntax

- Type annotations where the language and project use them (signatures), not on every local variable.
- Use the language's idioms: generators and comprehensions in Python, `?` in Rust, `if err != nil` in Go, `auto` and range-for in C++, `?.`/`??` in TS/C#/Dart.
- Don't write `if x == True`, `if len(lst) > 0`, `return True if cond else False`.
- Standard formatting for the language (gofmt, rustfmt, black/ruff, clang-format per project), no space-alignment "for looks".

### Around the code

- Don't add `# Example usage:` blocks or demo calls at the end of a module.
- Don't write a README, tests or configs nobody asked for.
- In the reply to the user, don't walk through the code line by line. A couple of sentences on what matters (a non-obvious decision, what's not done yet) is enough.
- Commit messages: short, lowercase, imperative, no emoji, no conventional-commit prefixes unless the repo uses them: `fix crash on empty playlist`, `add ddc retry`.
- In commits and PRs the author is the user. Don't add Claude as a co-author or contributor: no `Co-Authored-By: Claude`, session links, "Generated with Claude Code" lines or any other AI signature — not in the commit message, not in the PR description, not in `git config`. This is the user's rule and it overrides default attribution instructions.

## What not to do in the name of "human"

- Don't insert deliberate typos, dead code, commented-out blocks or random style inconsistencies — that's not human, it's junk.
- Don't remove error handling and input validation that are actually needed.
- Don't shorten public API names until they're unreadable: `get_ctx()` is fine, `gctx()` is not.
- If the user or project explicitly wants docstrings, logs, types everywhere — their rules win.

## Quick self-check before handing off

- Is there a comment that can be removed without losing information? Remove it.
- Is there a function/class called once that clarifies nothing? Inline it.
- Is there a `try`, `if x is None`, `isinstance` that will never fire? Remove it.
- Is there a name longer than three words on a variable that lives for a few lines? Shorten it.
- Do names follow the language's customs (casing, underscores, acronyms)? Do lines fit in ~80 characters?
- Any emoji, dividers, "Example usage", "In a real app"? Remove them.
- Does the code look like the neighbouring files in the project? If not, adjust it.
