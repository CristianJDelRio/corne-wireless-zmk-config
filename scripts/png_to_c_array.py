#!/usr/bin/env python3
"""
Convierte una imagen PNG a un array C en formato LVGL CF_INDEXED_1BIT
para usar como logo en el nice!view (Sharp Memory Display 160x68 px, 1-bit).

Uso:
    python3 png_to_c_array.py <imagen.png> <nombre_variable>

Ejemplo:
    python3 png_to_c_array.py spiderman.png spiderman
    python3 png_to_c_array.py greenlantern.png greenlantern

Salida: codigo C listo para pegar en logo.c

Requiere: pip install Pillow
"""

import sys
import math
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Instala Pillow primero: pip install Pillow", file=sys.stderr)
    sys.exit(1)

DISPLAY_W = 160
DISPLAY_H = 68


def image_to_lvgl_1bit(img_path: str, var_name: str) -> str:
    img = Image.open(img_path).convert("L")  # escala de grises

    # Reescalar manteniendo aspect ratio, encajar en DISPLAY_W x DISPLAY_H
    img.thumbnail((DISPLAY_W, DISPLAY_H), Image.LANCZOS)

    w, h = img.size

    # Umbral: pixel >= 128 → blanco (1), < 128 → negro (0)
    pixels = img.point(lambda p: 1 if p >= 128 else 0, "1")
    pix = pixels.load()

    stride = math.ceil(w / 8)  # bytes por fila
    row_bytes = []
    for y in range(h):
        row = []
        for byte_i in range(stride):
            byte_val = 0
            for bit in range(8):
                x = byte_i * 8 + bit
                if x < w and pix[x, y]:
                    byte_val |= 1 << (7 - bit)
            row.append(byte_val)
        row_bytes.append(row)

    # Paleta LVGL CF_INDEXED_1BIT: 2 colores x 4 bytes ARGB
    palette = [0x00, 0x00, 0x00, 0xFF,   # color 0: negro
               0xFF, 0xFF, 0xFF, 0xFF]   # color 1: blanco

    all_bytes = palette + [b for row in row_bytes for b in row]
    data_size = len(all_bytes)

    # Formatear como array C
    hex_lines = []
    for i in range(0, len(all_bytes), 12):
        chunk = all_bytes[i:i+12]
        hex_lines.append("    " + ", ".join(f"0x{b:02X}" for b in chunk) + ",")

    lines = [
        f"/* Generado por png_to_c_array.py desde {Path(img_path).name} */",
        f"/* Imagen: {w}x{h} px, 1bpp, LVGL CF_INDEXED_1BIT */",
        "",
        "#include <lvgl.h>",
        "",
        f"#define LOGO_W {w}",
        f"#define LOGO_H {h}",
        "",
        "LV_ATTRIBUTE_MEM_ALIGN",
        f"static const uint8_t logo_map[] = {{",
    ]
    lines += hex_lines
    lines += [
        "};",
        "",
        f"const lv_img_dsc_t zmk_logo = {{",
        "    .header = {",
        "        .cf          = LV_IMG_CF_INDEXED_1BIT,",
        "        .always_zero = 0,",
        "        .reserved    = 0,",
        f"        .w           = LOGO_W,",
        f"        .h           = LOGO_H,",
        "    },",
        "    .data_size = sizeof(logo_map),",
        "    .data      = logo_map,",
        "};",
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <imagen.png> <nombre_variable>", file=sys.stderr)
        sys.exit(1)

    img_path, var_name = sys.argv[1], sys.argv[2]
    output = image_to_lvgl_1bit(img_path, var_name)
    print(output)
