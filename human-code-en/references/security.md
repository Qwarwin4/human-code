# Security

Open the sections you need, not all of them. The lists below aren't a
checklist to tick off, they're hints about where to look. Section 1 matters
most: it's how you catch holes that aren't in any list.

## Contents
1. Finding holes that aren't in any list
2. Input and parsing
3. Files and paths
4. Processes and shell
5. Network and outgoing requests
6. Web and APIs
7. Auth, sessions, tokens
8. Money, stock and races
9. Secrets and logs
10. Cryptography
11. Memory and numbers
12. Resources and denial of service
13. Desktop and Linux
14. Android
15. Client-server in games and mods
16. Dependencies and builds
17. Per-language traps

## 1. Finding holes that aren't in any list

An AI already knows the common vulnerabilities. The dangerous ones come from
the logic of one particular program: who can do what, in what order, with
which rights. You don't recall those from a template, you derive them.

**Map the trust boundaries.** Who uses the program, who could be an attacker
(anonymous, a regular user, another user, an admin, another process on the
machine, the server you're talking to). What each of them controls. Data that
crosses a boundary is hostile until checked, even if "it's sent by our own
client".

**Write down the invariants.** What must always be true: "a user sees only
their own orders", "a balance never goes negative", "an item is never sold
twice", "files are only written inside data_dir", "a bot command only runs for
the owner". Then for each invariant look for a way to break it: another
endpoint, a repeated request, a concurrent request, a different input format,
a direct call bypassing the UI, an old client version.

**Ask each input hostile questions:**
- too big, empty, zero, negative, fractional, NaN, infinity;
- wrong type (string instead of number, array instead of object, duplicate key);
- null byte, newline, control characters, unicode look-alikes, a different
  normalization, different case, surrounding whitespace;
- refers to someone else's object (another id, path, chat_id);
- arrives twice, concurrently with another, out of order, after the
  permission was revoked;
- comes from the wrong place (a forged webhook, a local process, another
  origin).

**Ask each piece of state:** what if it changes between the check and the use;
what if the process dies halfway; what's left after an error — a half-written
file, money charged without an order, an item delivered without payment.

**Look at failure.** If signature verification, auth or parsing throws, is the
request rejected or does it go through? Only the first is safe. A `catch` with
`continue` around a permission check is a hole.

**Look at the seams.** Two components that are each correct often break
together: one normalizes the path and the other doesn't; one counts in cents
and the other in dollars; the frontend checks a limit and the backend doesn't;
the URL parser in the check and the one in the HTTP client read the string
differently.

**Look at what "nobody will call".** Debug endpoints, test bot commands, flags
like `--insecure`, old API versions, an admin panel without auth "because it's
on localhost".

## 2. Input and parsing

- Validate against an allowlist, not a denylist: allowed characters, range,
  length, enum. Stripping "dangerous" bits almost never gets all of them.
- Validate after decoding and normalization, not before; otherwise `%2e%2e`,
  double encoding and unicode slip through.
- Limit length before parsing, not after.
- Range-check numbers from outside before doing arithmetic or allocating
  memory based on them.
- Regexes on user input: no nested quantifiers (`(a+)+`), or ReDoS. Or cap the
  input length.
- Deserialize foreign data into data, not objects: no `pickle`, `yaml.load`
  without a safe loader, `BinaryFormatter`, Java `ObjectInputStream`, `eval`
  on JSON.
- XML from others: external entities and DTDs disabled.
- Template engines: a user string is data in a template, not the template.

## 3. Files and paths

- A path from outside: build it relative to a base dir, resolve it
  (`realpath`, `canonicalize`, `filepath.Clean` plus a prefix check) and check
  the result is inside the base. Account for absolute paths, `..`, symlinks,
  `\` on Windows, names like `CON`, `NUL`, colons and ADS.
- Archives: every name inside is a hostile path (zip slip). Plus a limit on
  total unpacked size and file count (zip bomb). Symlinks and hardlinks inside
  tar: reject or resolve them explicitly.
- TOCTOU: "checked the file doesn't exist, then created it" is a race. Create
  atomically (`O_CREAT|O_EXCL`, `O_NOFOLLOW`), work through the open file
  descriptor instead of the path again.
- Important files: write to a temp file in the same dir, `fsync`, then
  `rename`. Otherwise a crash leaves half a file.
- Temp files via `mkstemp`/`tempfile`/`os.CreateTemp`, not a predictable name
  in `/tmp`.
- Permissions: configs with secrets `0600`, dirs `0700`. No `0777`. Account for
  umask and for the file already existing with other permissions.
- User uploads: don't trust the extension or `Content-Type`, store outside the
  web root, generate the name yourself.

## 4. Processes and shell

- Run commands as an argument list without a shell: `subprocess.run([...])`,
  `exec.Command(name, args...)`, `Command::new`. No `shell=True`, `system()`,
  `popen()` with a concatenated string.
- Even without a shell, a user argument can start with `-` and become a flag
  (`--output=/etc/...`, `-oProxyCommand=`). Put `--` before positional
  arguments or check the first character.
- Full binary paths or a controlled `PATH` if the program runs with elevated
  rights or in someone else's environment.
- Don't pass secrets as command-line arguments; they show in `ps` and `/proc`.
  Use stdin, a 0600 file, or env (carefully).
- In bash: quote every variable, `set -euo pipefail`, no `eval` with outside
  data.

## 5. Network and outgoing requests

- TLS verification is always on. `verify=False`, `InsecureSkipVerify`,
  `rejectUnauthorized: false`, a custom `TrustManager` that accepts everything
  — only if the user explicitly asked and knows why.
- SSRF: if the server fetches a user-supplied URL, check the host after DNS
  resolution, not the string. Block private, loopback, link-local
  (`169.254.169.254`), their IPv6 counterparts and `::ffff:127.0.0.1` mapping,
  plus decimal and octal IP forms. Disable redirects or check each one. Connect
  to the IP you checked (DNS rebinding).
- Timeouts on everything: connect, read, total. A limit on response size.
- A third-party API response is input too. Don't put it into HTML, SQL or a
  path unchecked.
- Listen on `127.0.0.1`, not `0.0.0.0`, if the service shouldn't be reachable
  from outside. A local service without auth is open to every program on the
  machine and sometimes to the browser via DNS rebinding.
- Proxies and censorship workarounds: don't turn your proxy into an open one
  — access only from expected addresses or with a key; don't log where clients
  go.

## 6. Web and APIs

- SQL: parameterized queries only. Table and column names from input only via
  an allowlist.
- XSS: escape on output for the context (HTML, attribute, JS, URL). In JS use
  `textContent`, not `innerHTML`. Check the scheme of an `href` from input
  (`javascript:`).
- IDOR: every request for an object checks that the object belongs to the
  current user. An id in the URL or body is not proof of rights.
- Mass assignment: don't map the request body onto a model wholesale. Pick the
  allowed fields explicitly, or someone sends `"is_admin": true` or
  `"price": 1`.
- Price, discount, total, role, order status are always computed on the
  server. The client sends only the product id and quantity.
- CSRF: for cookie sessions, a token or `SameSite`. State changes only via
  non-GET requests.
- CORS: don't reflect any `Origin` with `credentials: true`.
- Open redirects: `?next=` only accepts a relative path or an allowlist.
- Webhooks (VK Callback, Telegram, payment providers): verify the signature or
  secret before any processing, compare in constant time, drop repeats by event
  id and stale ones by timestamp.
- VK and Telegram mini apps: verify launch params by signature on the server.
  A `user_id` from the frontend without a signature is forged in a minute.
- Rate limits on login, sending codes, creating orders, expensive endpoints.
- Headers and logs: a newline in input means header injection or a forged log
  line.
- Errors sent outside: no stack traces, paths or SQL.

## 7. Auth, sessions, tokens

- Permission checks live on the server, on every action, in one place, not in
  hiding a button.
- Tokens and codes come from a cryptographic RNG (`secrets`, `crypto/rand`,
  `OsRng`, `crypto.getRandomValues`, `RandomNumberGenerator`), long enough.
  Not `random`, not `Math.random`, not the time, not an id.
- Passwords: only `argon2id`, `scrypt` or `bcrypt`. Not `md5`/`sha*`, even
  salted.
- Compare secrets, signatures and tokens in constant time
  (`hmac.compare_digest`, `subtle.ConstantTimeCompare`).
- JWT: a fixed algorithm on the server, `none` rejected, check `exp`, `aud`,
  `iss`. The secret isn't in the code.
- The session changes after login and after a permission change; logout
  actually kills it on the server.
- One-time codes and links: expiry, single use, a limit on attempts.
- Password reset and email confirmation don't reveal whether an account
  exists.

## 8. Money, stock and races

The most common class of logic holes in shops, auto-delivery bots and games,
and it's barely present in the usual lists.

- "Read balance → check → write" as two queries is a double spend under
  concurrent requests. Do it as one atomic operation
  (`UPDATE ... SET bal = bal - ? WHERE id = ? AND bal >= ?` and check the row
  count), a transaction with a lock, or a mutex per resource if there's one
  process.
- Same for stock, promo codes, "one request per day" limits, referral bonuses.
- Idempotency: repeating the same request (double click, network retry,
  repeated webhook) must not create a second order or a second delivery. Use
  an idempotency key or a unique index on the event id.
- Deliver goods only after the payment provider confirms payment, not on the
  buyer's "I paid" message or a redirect to the success page.
- Money in integer minor units or decimal, not float. Negative quantities and
  amounts rejected explicitly.
- Rounding and overflow: what happens with a quantity of `2^31` or a price
  multiplied by a huge number.
- Order of steps: charge first, then deliver; if delivery fails, refund or
  flag for manual review, but never lose the event.

## 9. Secrets and logs

- Secrets come from env, a 0600 file or the OS keystore. Not in code, not in
  the repo, not in example configs with real values. `.env` goes in
  `.gitignore`.
- Don't log tokens, passwords, cookies, the `Authorization` header, or full
  request bodies with personal data. Mask them.
- A secret must not end up in a URL; it'll stay in proxy logs and history.
- Errors and panics can print a struct holding a secret: make sure the
  config's `Debug`/`__repr__`/`toString` doesn't show it.
- A secret leaked in a commit has to be revoked, not just removed from
  history. Tell the user.

## 10. Cryptography

- Don't invent. Use existing high-level tools: libsodium/NaCl, `age`, AEAD
  (`AES-GCM`, `ChaCha20-Poly1305`) from the standard library.
- No ECB, no encryption without authentication, no reused nonces with the
  same key.
- Sign data with HMAC, not `hash(secret + data)`.
- Derive keys from passwords with a KDF (`argon2`, `scrypt`, `pbkdf2` with
  many iterations), not a hash.

## 11. Memory and numbers

- C/C++: no `gets`, `strcpy`, `strcat`, `sprintf` without a size. Use
  `snprintf`, check the return value, explicit buffer sizes.
- A size from outside multiplied by an element size: check overflow before
  `malloc`. Watch signed vs unsigned in length comparisons.
- Use-after-free and double free: RAII and smart pointers in C++, one owner
  per resource.
- The format string is always a constant: `printf("%s", s)`, not `printf(s)`.
- Rust: `unsafe` only with a clear invariant next to it; indexing and
  arithmetic with outside numbers via `checked_*`, `get()`; in release builds
  overflow wraps instead of panicking.
- Go: races on maps and shared structs across goroutines — mutex or channel;
  test with `-race`. Slices of an outside buffer keep the whole buffer alive.
- Java/Kotlin/C#: integer overflow is silent, check sizes.

## 12. Resources and denial of service

- Limits on everything that grows with outside input: body size, element
  count, JSON nesting depth, connection count, queue size, file count.
- Decompression (gzip, zip, images): limit the output, not the input.
- Caches and maps keyed by input: bounded size with eviction.
- Timeouts on reading from clients (slowloris), on outside calls, on locks.
- One slow client or crashed handler must not hang the whole service.

## 13. Desktop and Linux

- A program running as root or via `sudo`/polkit/setuid: as little code with
  privileges as possible, a clean environment, full paths, no writes into
  user-writable dirs without `O_NOFOLLOW`.
- Load configs and plugins only from dirs owned by the user or root and not
  writable by others.
- Don't implicitly execute files from the current dir (Python looks for
  modules next to the script).
- D-Bus and sockets: check who's calling (sender uid, `SO_PEERCRED`) if the
  method does something privileged.
- Devices (`/dev/i2c-*` for DDC and so on): grant access to a group via udev
  instead of running the whole app as root.
- Auto-update only over HTTPS and with a signature or hash check.
- Installers and dotfiles scripts: no `curl | sh` from someone else's URL
  without checking, don't overwrite other files without a backup, no
  `chmod -R 777`.

## 14. Android

- Components (`Activity`, `Service`, `Receiver`, `Provider`) are
  `exported="false"` unless needed from outside. Exported ones check the
  caller and treat incoming `Intent` extras as hostile input.
- `PendingIntent` with `FLAG_IMMUTABLE` and an explicit component.
- `WebView`: no `addJavascriptInterface` for untrusted content, no
  `setAllowFileAccess`, no loading arbitrary URLs from an intent.
- Cleartext traffic disabled (`networkSecurityConfig`) except for explicitly
  needed local addresses.
- Secrets in the Android Keystore, not in `SharedPreferences` or the APK's
  code: APKs get decompiled.
- `Log.d` with user data stripped from release builds.
- A local server or proxy on the device listens on loopback only, preferably
  with a token: other apps on the phone can connect to it too.
- Native code via JNI: everything in section 11.

## 15. Client-server in games and mods

A mod's server side (Forge, Fabric, plugins) is the same trust boundary as a
web server. A modified client sends whatever packets it likes.

- Every packet from a client is checked on the server: does the entity exist,
  does it belong to the player, is the player close enough (distance), do they
  have the item, is the action on cooldown, are the values sane (speed, angle,
  damage, coordinates inside the world).
- Damage, explosions, giving items, teleporting, spawning entities are
  decided by the server. The client sends intent ("pressed fire"), not the
  result ("dealt 1000 damage to entity 42").
- Rate-limit packets per player.
- Run packet handlers on the main server thread (`enqueueWork`), or you race
  with the world.
- Strings and NBT from packets: limit length and depth.
- Don't load classes, resources or scripts by a name taken from a packet.

## 16. Dependencies and builds

- Add only the dependencies you need, with a checked name (typosquatting:
  `reqeusts`, `colourama`) and a pinned version (lock file).
- Don't include scripts and libraries from a CDN without `integrity`.
- CI: secrets not in logs, pull requests from forks don't get secrets.
- Docker: not as root, no secrets in layers, a minimal base image.

## 17. Per-language traps

- **Python:** `eval`/`exec`, `pickle`, `yaml.load`, `shell=True`,
  `tarfile.extractall` without a filter, `tempfile.mktemp`, `assert` for
  checks (stripped by `-O`), `random` for tokens, f-strings in SQL.
- **Go:** `InsecureSkipVerify`, `http.Get` without a timeout (the default
  client has none), `filepath.Join` doesn't protect against `..`, map races,
  `text/template` instead of `html/template` for HTML, `math/rand` for tokens.
- **Rust:** `unsafe` without an invariant, `as` silently truncates numbers,
  overflow in release, `std::process::Command` with `sh -c`, `Path::join` with
  an absolute path replaces the base.
- **C/C++:** section 11, plus `system()`, `tmpnam`, `rand()` for secrets,
  uninitialized memory sent over the network.
- **JS/TS:** `innerHTML`, `eval`, `new Function`, prototype pollution via
  merging objects from JSON (`__proto__`, `constructor`),
  `child_process.exec`, `==` in checks, unanchored regexes when checking an
  origin or URL.
- **C#:** `BinaryFormatter`, `Process.Start` with `UseShellExecute` and a
  string, `SqlCommand` with concatenation, `Random` for tokens.
- **Java/Kotlin:** deserialization, XXE in standard parsers, `Runtime.exec`
  with a string, logging input with old log4j-style libraries.
- **Dart/Flutter:** secrets in the app's code, `http` accepting any
  certificate via `badCertificateCallback: (_, __, ___) => true`, data in
  `SharedPreferences` instead of `flutter_secure_storage`.
- **Bash:** unquoted variables, `eval`, `rm -rf "$dir/"` with an empty
  variable (`${dir:?}`), parsing `ls`, temp files named with `$$`.
