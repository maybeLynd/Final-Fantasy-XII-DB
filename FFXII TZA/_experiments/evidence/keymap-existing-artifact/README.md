# ASTRA — existing keymap directory identity, 2026-09-21

**The existing account-specific keymap folder matches the observed Steam host
profile. This does not establish who created the folder, which startup wrote the
file, or whether the FF12 formatter safely consumed a returned stack pointer.**

## Question and sufficient method

`FABLE-REQ-ASTRA-KEYMAP-STEAMID-FOLDER` asks for a directory/account comparison as
evidence for keymap page UQ-146. H1: the existing account folder matches the host
profile; H2: it differs. A third possibility remains compatible with H1: an older
or copied artifact exists while a current startup would behave differently.

Method A: read existing files and bracketed host profile metadata. No live FF12
test is needed to compare existing artifacts. No game process, game API call,
directory creation, formatter execution or returned-pointer access was observed.
Treat this as an artifact result, not a live-original-game result.

## Identity, controls and observation

At `2026-09-21T09:24:31Z`, the before/after samples agree on Steam PID54064 and
its start time, executable path/hash/version, registry ActiveUser low32, account
name hash and profile-file hash. The selected `loginusers.vdf` record agrees with
both the registry account-name hash and ActiveUser low32; selection is unique.
The observed Steam client hash is
`48ea0576865d2dfda26001b7b210c3f7559d46e647424cd11704eb1ea842fe5a`, version
`10.96.30.42`. PowerShell `7.6.5`; exact capture/control sources are retained and
hashed. This is host metadata, **not** `ISteamUser::GetSteamID` called by FF12.

The selected profile identifier is `76561198045890736`. A directory with that
exact name exists below the game settings root and contains `keymap.ini`.
The root also contains `keymap.ini`. Both files are699bytes and have SHA-256
`8d98f85e0b571d819dc155c8774aad553f6e6119d6ede1cdd62245cfb9f6cf6d`.
Both match their entries in the retained `old-save-start-p/save-before.json`.
The observed keymap headers and Circle assignment are positive read controls.
Before/after hashes and file metadata agree. File timestamps predate the
observation and do not identify a writer or build. Other account folders are
not diagnosed from their spelling.

`raw.json` contains the bracketed observations; `observation.json` is the checked
reduction. `check.py` rejects a wrong account directory, a changed account during
the observation and an empty file population. The reader's profile controls
reject empty/ambiguous populations and wrong identity/name matches. No accounts,
credentials or settings were changed; unrelated profile records were not copied.

## Failed initial control and repair

The initial reader required a `MostRecent` field. The installed Steam client uses
an account record with `AutoLogin` and no `MostRecent`; the reader stopped with
`Missing/ambiguous account controls: no verdict` before writing an observation.
`capture-initial.ps1` and `initial-failure.json` preserve that failed method.

The corrected selector uses the uniquely matching active low32 **and** account
name hash. It does not infer an active user merely from a saved account record.
`profile-controls.ps1` executes the actual pure selection functions from the
capture source, including a current-format record with no `MostRecent`. Five
controls must pass; zero cases cannot pass. No semantic conclusion depended on
the failed attempt, so there is no earlier game conclusion to retract.

## Semantic limits and consumer

FABLE should record the requested folder comparison with these limits. UQ-146
remains open: matching artifacts do not demonstrate current formatter execution,
preservation of the returned string across that call, or safe behavior under
other CRT/build/stack states. Conversely, an empty account component alone cannot
identify stack clobbering; the same page describes an uninitialized-Steam path
that produces an empty string. A mismatched folder could also be an unrelated or
copied artifact. Do not substitute any such spelling for a causal observation.

If the lifetime question remains required, first check whether bounded execution
of the verified original caller/formatter path with the relevant CRT and explicit
stack/input state can distinguish it. Actual Steam initialization or normal
startup reachability may instead require C. Such an observation needs current
module identity, positive/detection controls and the string before/at consumption;
it is not prepared by this filesystem comparison. No laboratory rebuild or
unchanged invalid trace is requested.

## Reproduce and cleanup

```text
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/keymap-existing-artifact/check.py"
```

This checks retained evidence without touching Steam or FF12. Do not rerun
`capture.ps1` to validate a past observation; it deliberately refuses to overwrite
`raw.json`. No game or PC controls were opened; FF12 process count was0 at the
capture's final check. No save/configuration writes or native instrumentation
occurred, so no restore/detach action was needed. Bracketed reads are not atomic
and do not exclude a transient change between them.
