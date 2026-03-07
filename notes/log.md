# Log

## 2026-03-06

### General

- [ ] Refactor AP world to be pythonic.
- [ ] Read through the docs, compare to where we're currently at.
  - [docs-guide.md](/notes/docs%20guide.md)
- [ ] Investigate the current state of our testing.
- [ ] Figure out how to run this.
- [ ] Produce a robust readme explaining how to get this world working on windows and linux.
- [ ] Move to using uv with a pyproject.toml.
- [ ] Rename `worlds/L4D2` to `worlds/l4d2`.

### AP Companion

- [x] Use pydantic basesettings for config.
- [ ] Convert what we can into pydantic basemodels.
- [x] Write a readme.

### From Yufii

- [ ] Death Link implementation.
  - Ensure death link functionality works correctly.
- [ ] Campaign finale check logic.
  - Fix issue with campaigns sending checks strangely when beating finales with other players.
- [ ] Achievement to zombie kill conversion.
  - Switch achievement-based checks to zombie kill count checks.
- [ ] Melee system fixes.
  - Resolve ongoing melee functionality issues.
- [ ] Special infected spawn tuning.
  - Adjust spawn patterns (partially fixed, needs verification).
- [ ] Visual bug fixes.
  - Address interaction issues (e.g., Sacrifice Tank door).
  - [x] Dead Center Tank door - Fixed
  - [x] Sacrifice Tank door - Fixed
  - [ ] Check for additional similar issues
- [ ] Zombie drop items toggle.
  - Consider option to disable zombies dropping items
