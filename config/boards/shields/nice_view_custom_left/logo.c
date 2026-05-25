/*
 * Spider-Man logo - left half
 *
 * PLACEHOLDER: Este archivo contiene un borde simple como prueba.
 * Para usar el logo real de Spider-Man:
 *
 *   1. Consigue un PNG monocromatico de 160x68 px (o menor, con padding)
 *   2. Ejecuta: python3 scripts/png_to_c_array.py spiderman.png spiderman
 *   3. Reemplaza logo_map[] con el array generado y ajusta W y H
 *
 * El display Sharp Memory del nice!view es 160x68 px, 1-bit (blanco/negro).
 */

#include <lvgl.h>

/* Dimensions del logo (ajustar si tu imagen es diferente) */
#define LOGO_W 68
#define LOGO_H 68
#define LOGO_STRIDE ((LOGO_W + 7) / 8)  /* = 9 bytes por fila */

/* 8 bytes de paleta (color0 = negro, color1 = blanco) + 68*9 bytes de pixeles */
LV_ATTRIBUTE_MEM_ALIGN
static const uint8_t logo_map[] = {
    /* Paleta LVGL CF_INDEXED_1BIT (2 colores x 4 bytes ARGB) */
    0x00, 0x00, 0x00, 0xFF,  /* color 0: negro/fondo */
    0xFF, 0xFF, 0xFF, 0xFF,  /* color 1: blanco/trazo */

    /* Datos de pixeles: 68 filas x 9 bytes (68 px + 4 bits padding por fila) */
    /* PLACEHOLDER: rectangulo borde - reemplazar con logo Spider-Man */
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0,  /* fila 0  (borde superior) */
#define _R 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10,
    _R _R _R _R _R _R _R _R _R _R  /* filas 1-10  */
    _R _R _R _R _R _R _R _R _R _R  /* filas 11-20 */
    _R _R _R _R _R _R _R _R _R _R  /* filas 21-30 */
    _R _R _R _R _R _R _R _R _R _R  /* filas 31-40 */
    _R _R _R _R _R _R _R _R _R _R  /* filas 41-50 */
    _R _R _R _R _R _R _R _R _R _R  /* filas 51-60 */
    _R _R _R _R _R _R              /* filas 61-66 */
#undef _R
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0,  /* fila 67 (borde inferior) */
};

/*
 * Simbolo exportado que el widget de nice!view referencia via LV_IMG_DECLARE(zmk_logo).
 * Si el build falla con "multiple definition of zmk_logo", verifica en el source de
 * ZMK v0.3 el nombre exacto del simbolo y si usa __attribute__((weak)).
 */
const lv_img_dsc_t zmk_logo = {
    .header = {
        .cf        = LV_IMG_CF_INDEXED_1BIT,
        .always_zero = 0,
        .reserved  = 0,
        .w         = LOGO_W,
        .h         = LOGO_H,
    },
    .data_size = sizeof(logo_map),
    .data      = logo_map,
};
