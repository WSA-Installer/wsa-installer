/*
 * aaptpp.h — C ABI for AAPT++ (Android package inspection).
 *
 * Drop aaptpp.dll next to your application and link aaptpp.lib.
 * All string/binary results use a two-pass contract:
 *   1. Call with out_buf == NULL, out_len pointing to a size_t.
 *      The function writes the required buffer size (bytes, excluding the
 *      NUL terminator for strings) into *out_len and returns that size.
 *   2. Allocate a buffer of that size (+1 for NUL on strings), then call again
 *      with out_buf pointing to it. The function fills it and returns bytes
 *      written. For binary data the size is exact (no NUL added).
 *   3. Free the buffer with aaptpp_free().
 *
 * Example (resolve icon path):
 *   size_t n = 0;
 *   aaptpp_resolve_icon_path(L"app.apk", NULL, &n);
 *   char* buf = (char*)malloc(n);
 *   aaptpp_resolve_icon_path(L"app.apk", buf, &n);
 *   // use buf ...
 *   aaptpp_free((uint8_t*)buf);
 */

#ifndef AAPTPP_H
#define AAPTPP_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Free a buffer previously returned/filled by an aaptpp_* function.
 * Pass the same pointer you allocated (or that was written into out_buf).
 */
void aaptpp_free(unsigned char* ptr);

/*
 * Return aggregated package info as a JSON string (NUL-terminated).
 * Caller frees the returned buffer with aaptpp_free.
 */
size_t aaptpp_package_info_json(
    const char* path,
    char* out_buf,
    size_t* out_len);

/*
 * Extract the best application icon as PNG bytes.
 * prefer_round != 0 prefers the round icon when present.
 * Returns bytes written (or required). Caller frees with aaptpp_free.
 */
size_t aaptpp_extract_best_icon(
    const char* path,
    int prefer_round,
    unsigned char* out_buf,
    size_t* out_len);

/*
 * Resolve the concrete icon resource path (e.g. "res/mipmap-xxxhdpi/ic_launcher.png")
 * declared by the manifest. Returns a NUL-terminated C string; free with aaptpp_free.
 * Returns 0 (and writes nothing) if no icon path could be resolved.
 */
size_t aaptpp_resolve_icon_path(
    const char* path,
    char* out_buf,
    size_t* out_len);

/*
 * Convert a PNG buffer to an ICO buffer (PNG embedded, natively supported by
 * Windows). png points to png_len bytes. out_buf receives ICO bytes;
 * returns bytes written (or required). Caller frees with aaptpp_free.
 */
size_t aaptpp_png_to_ico(
    const unsigned char* png,
    size_t png_len,
    unsigned char* out_buf,
    size_t* out_len);

#ifdef __cplusplus
}
#endif

#endif /* AAPTPP_H */
