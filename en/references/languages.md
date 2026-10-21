# Per-language notes

Open only the section you need. The general rule is the same everywhere: the existing project's style wins.

## Contents
- Python
- Go
- Rust
- C / C++
- C#
- JavaScript / TypeScript
- Dart / Flutter
- Kotlin / Java
- Bash / shell

## Python

- Types in signatures — yes; on local variables — no. `from typing import List, Dict` isn't needed in 3.9+: `list[str]`, `dict[str, int]`, `X | None`.
- `pathlib` instead of `os.path` in new code; `with open(...)` without an extra `try`.
- f-strings, comprehensions, `enumerate`, `zip`, unpacking. `any()`/`all()` instead of flags in a loop.
- `if not items:` instead of `if len(items) == 0:`; `return cond` instead of `return True if cond else False`.
- `dataclass` — when an object really has fields and gets passed around; not for three script settings.
- `if __name__ == "__main__":` — yes in modules that get imported; a throwaway script can skip it.
- `logging` — in services and libraries; in a script `print` is fine. `sys.exit("bad args")` is a normal way to fail with a message.
- Catch specific exceptions: `except FileNotFoundError`, `except KeyError`. A bare `except Exception: pass` only with a reason.

## Go

- Short names are the language norm: `r`, `w`, `ctx`, `err`, `n`, `buf`, `c` for a client, a one- or two-letter method receiver (`func (s *Server)`).
- `if err != nil { return fmt.Errorf("read cfg: %w", err) }` — wrap with short lowercase context, without "failed to" at every layer.
- Don't create an interface until there's a second implementation or a test that needs it. Interfaces are declared by the consumer.
- No `GetName()` getters — just `Name()`.
- Comments on exported identifiers are customary (`// Run starts ...`), but short, one line. On unexported ones — only when needed.
- `gofmt`. No alignment or blank lines to create "sections".
- `log.Fatal` in `main` is fine; `panic` is not for ordinary errors.

## Rust

- `?` wherever possible; `anyhow`/`thiserror` per project. `unwrap()` is acceptable in tests, prototypes and where the invariant is obvious (then prefer `expect("...")` with a short reason).
- Don't clone for convenience when you can borrow; but don't fight the borrow checker at the cost of readability.
- `impl Trait` in arguments, iterators with `map/filter/collect` instead of manual loops where it reads simpler.
- `match` with early return; `if let`/`let else` instead of nesting.
- `///` doc comments on a crate's public API; inside a binary — only as needed.
- `rustfmt`, `clippy` without unnecessary `#[allow]`.

## C / C++

- Naming and brace style strictly as in the project (snake_case, camelCase, Allman/K&R).
- C++: `auto`, range-for, `std::unique_ptr`, `std::string_view`, `std::optional`. No manual `new`/`delete` in new code.
- Don't write an `XManager` wrapper class around three functions — free functions in a namespace are fine.
- Doxygen `@brief @param @return` — only if the project uses it.
- In C: short names (`fd`, `len`, `p`, `buf`), `goto out;` for resource cleanup is a normal human idiom.
- Don't add `#pragma region`, license banners or "File: foo.cpp / Author / Description" headers unless neighbouring files have them.

## C#

- `var` for locals where the type is obvious on the right. Expression-bodied members for one-liners.
- `?.`, `??`, `is not null`, pattern matching, `using var`.
- `/// <summary>` XML docs on a library's public API; private methods in an app don't need them.
- Don't spawn `IFooService` + `FooService` for every entity if there's no DI container and no second implementation.
- `async`/`await` without `.ConfigureAwait(false)` in applications (in libraries — per project).

## JavaScript / TypeScript

- `const` by default, `let` when reassigned. Arrow functions, destructuring, `?.`, `??`, template strings.
- TS: don't annotate what's inferred (`const n: number = 5`). Types go at the boundaries (parameters, exports, API responses).
- Don't wrap every `fetch` in `try/catch` with `console.error` and `return null` — let the error bubble up to where it's shown to the user.
- Don't leave `console.log` behind, except intentional CLI output.
- Vanilla JS — no unnecessary classes; a module of functions is fine.
- JSDoc — only if the project has no TS and uses it.

## Dart / Flutter

- `final` by default, `const` widget constructors where possible.
- Don't split `build` into a dozen five-line `_buildXxx()` methods — either keep it in the tree or extract a separate widget if it's reused or genuinely large.
- `?.`, `??`, `!` — as appropriate; `late` only if it's really initialized later.
- `dart format`. No comments above every widget in the tree (`// Title text`).

## Kotlin / Java

- Kotlin: `val`, data classes, extension functions, `?.let`, `when`, scope functions without three levels of nesting.
- Java: `var` (10+), records, streams — where they read simpler than a loop. No getters/setters on everything unless it's a bean.
- Javadoc on every private method — no.

## Bash / shell

- `set -euo pipefail` at the top — yes, that's common practice.
- Short lowercase variable names: `dir`, `f`, `out`. Uppercase for exported env vars.
- Don't print `echo "Starting script..."` or colored banners without reason.
- `[[ ]]`, `$(...)`, quotes around variables. Functions when something actually repeats.
- Error message to stderr and exit: `echo "no such dir: $dir" >&2; exit 1`.
