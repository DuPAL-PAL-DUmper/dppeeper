# Changelog
Changelog for the dppeeper utility

## [0.0.7] - 2024-08-25
### Added
- Allow the TOML to specify pin naming override with the `names_override` optional entry
- Add pin number for CLK pins

## [0.0.6] - 2024-08-25
### Fixed
- When using multiple clock buttons, now each button toggles the correct clock

## [0.0.5] - 2024-08-18
### Added
- Support for 'NC' pins in mapping
- Support for optional pin "rotation shift" in mapping, as to orientate the labels properly (especially for qfp or PLCC)

### Changed
- Depdends on dupicolib >= 0.4.2

## [0.0.4] - 2024-08-15
### Added
- Attempt to check for oscillating pins and color the label purplish if found

## [0.0.3] - 2024-08-15
### Fixed
- Do a set of the latest changes to the pins before triggering the powercycle

## [0.0.2] - 2024-08-14
### Changed
- HI-Z checks on an IC now depend on a specific field defined in the TOML

## [0.0.1] - 2024-08-13
- Initial release
