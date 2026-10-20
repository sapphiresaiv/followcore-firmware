# Release policy

This repository contains public documentation and release metadata only.
Private MCU source, development history, ELF/debug files, keys, and raw
engineering logs must never be pushed here.

- Use ASCII paths under `firmware/<variant>/releases/<version>/`.
- Use variant-qualified release tags, for example
  `followcore-can-v3.0.0-rc.3`.
- Attach actual BIN and browser/tool ZIP files to GitHub Releases, not Git history.
- Publish exact SHA256 values, source identifiers, compatibility, release notes,
  third-party notices, and truthful validation limitations.
- Mark `-rc.N` builds as prereleases; do not promote them as stable automatically.
- Never overwrite an existing version or replace an asset silently. Use a new
  candidate/revision for changed firmware.
- Keep S3 and F303 artifacts distinct. Do not publish a planned protocol variant
  as though it were available.

`release-manifest.json` is a public distribution record. The controller does not
currently consume it as an automatic update instruction. Public Git commit IDs
describe documentation; MCU source identifiers refer to separate private
repositories. No private development repository is linked as a public remote.
