# Corne Wireless ZMK Config

ZMK firmware configuration for a wireless Corne (crkbd) split keyboard running on nice!nano v2 controllers.

## Hardware

- **Controllers**: nice!nano v2 (left and right halves)
- **Keyboard**: Corne (crkbd) — 42-key split ergonomic layout
- **Displays**: nice!view Sharp Memory Display (160×68px, 1-bit mono) — one per half
- **Connectivity**: Bluetooth 5.0 wireless + USB fallback

## Key Files

| File | Purpose |
|---|---|
| `build.yaml` | GitHub Actions build matrix — defines which board/shield combos to build |
| `config/west.yml` | ZMK dependency manifest — pins ZMK to `v0.3` |
| `config/corne.conf` | Kconfig options (BT power, debounce, WPM, ZMK Studio) |
| `config/corne.keymap` | Keymap with 4 layers: Base, Lower, Raise, Adjust |
| `config/boards/shields/` | Custom shield files (nice!view logo overrides) |

## Layers

| Layer | Activation | Content |
|---|---|---|
| 0 Base | Default | QWERTY |
| 1 Lower | Hold thumb left | Numbers 1-0, arrows |
| 2 Raise | Hold thumb right | Symbols, brackets |
| 3 Adjust | Lower + Raise (tri-layer) | F-keys, BT profiles, media |

## nice!view Display

Each half shows:
- Active layer name
- Battery level (bar + %)
- Bluetooth connection status
- WPM (words per minute)
- Custom logo (Spider-Man left, Green Lantern right)

The logo images are defined in `config/boards/shields/nice_view_custom_left/logo.c` and `nice_view_custom_right/logo.c` as 1-bit monochrome C arrays (160×68 px).

To generate a new logo from a PNG image, run:
```bash
python3 scripts/png_to_c_array.py my_image.png logo_left
```

## Building

Builds run automatically via GitHub Actions on every push. The workflow uses ZMK's official `build-user-config.yml`.

Build targets defined in `build.yaml`:
- `nice_nano_v2` + `corne_left nice_view_adapter nice_view nice_view_custom_left` (with ZMK Studio snippet)
- `nice_nano_v2` + `corne_right nice_view_adapter nice_view nice_view_custom_right`
- `nice_nano_v2` + `settings_reset`

Download the `.uf2` artifacts from the GitHub Actions run.

## Flashing Firmware

1. Double-tap the reset button on the nice!nano to enter bootloader mode — a USB drive called `NICENANO` appears
2. Drag the `.uf2` file onto the drive
3. The controller reboots automatically
4. Flash left half first, then right half

For settings reset (pair a new device or clear BT profiles), flash `settings_reset.uf2` to both halves.

## ZMK Studio

ZMK Studio is enabled on the left half. Connect via USB and open [studio.zmk.fm](https://studio.zmk.fm) to remap keys in real time without reflashing.

## ZMK Version

Pinned to `v0.3` in `config/west.yml`. To upgrade, change the `revision` field and test the build.
