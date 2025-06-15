#pragma once
#include <cuda_runtime.h>
#include <stdint.h>

#ifdef _WIN32
  #define EXPORT __declspec(dllexport)
#else
  #define EXPORT
#endif

extern "C" {

// Buffer Management ----------------------------------------------------------

EXPORT uchar4* create_buffer(uint32_t width, uint32_t height);
EXPORT void copy_buffers_same_size(uchar4* dst, const uchar4* src, uint32_t width, uint32_t height);
EXPORT void free_buffer(uchar4* buffer);

// Host - Device Memory Transfer ----------------------------------------------

EXPORT void copy_to_host(uchar4* h_dst, const uchar4* d_src, uint32_t width, uint32_t height);
EXPORT void copy_to_device(uchar4* d_dst, const uchar4* h_src, uint32_t width, uint32_t height);

// Blend ----------------------------------------------------------------------

EXPORT void blend_buffers(uchar4* dst, const uchar4* src, uint32_t dst_width, uint32_t dst_height,
                          uint32_t src_width, uint32_t src_height, int32_t x, int32_t y);

// Fill Effects ---------------------------------------------------------------

EXPORT void fill_color(uchar4* buffer, uint32_t width, uint32_t height,
                       unsigned char r, unsigned char g, unsigned char b, unsigned char a);

EXPORT void fill_gradient(uchar4* buffer, uint32_t width, uint32_t height,
                          unsigned char r1, unsigned char g1, unsigned char b1, unsigned char a1,
                          unsigned char r2, unsigned char g2, unsigned char b2, unsigned char a2,
                          int direction, bool seamless);

// Filters --------------------------------------------------------------------

EXPORT void apply_corner_radius(uchar4* buffer, uint32_t width, uint32_t height, uint32_t size);
EXPORT void apply_opacity(uchar4* buffer, uint32_t width, uint32_t height, float opacity);
EXPORT void apply_flip(uchar4* buffer, uint32_t width, uint32_t height, bool flip_horizontal, bool flip_vertical);
EXPORT void apply_grayscale(uchar4* buffer, uint32_t width, uint32_t height);

EXPORT void apply_chroma_key(uchar4* buffer, const uchar4* key_buffer,
                             uint32_t buffer_width, uint32_t buffer_height,
                             uint32_t key_width, uint32_t key_height,
                             int channel, unsigned char threshold,
                             bool invert, bool zero_all_channels);

EXPORT void apply_stroke(uchar4* buffer, const uchar4* copy_buffer, uint32_t width, uint32_t height,
                         int stroke_width, unsigned char stroke_r, unsigned char stroke_g,
                         unsigned char stroke_b, unsigned char stroke_a, int mode);

EXPORT void apply_shadow(uchar4* buffer, const uchar4* copy_buffer, uint32_t width, uint32_t height,
                         float radius, float intensity,
                         unsigned char shadow_r, unsigned char shadow_g,
                         unsigned char shadow_b, unsigned char shadow_a, int mode);

EXPORT void apply_gaussian_blur(uchar4* buffer, const uchar4* copy_buffer,
                                uint32_t width, uint32_t height, float radius);

// Resize and Crop ------------------------------------------------------------

EXPORT void resize_bilinear(uchar4* dst, const uchar4* src,
                            uint32_t dst_width, uint32_t dst_height,
                            uint32_t src_width, uint32_t src_height);

EXPORT void resize_nearest(uchar4* dst, const uchar4* src,
                           uint32_t dst_width, uint32_t dst_height,
                           uint32_t src_width, uint32_t src_height);

EXPORT void resize_bicubic(uchar4* dst, const uchar4* src,
                           uint32_t dst_width, uint32_t dst_height,
                           uint32_t src_width, uint32_t src_height);

EXPORT void crop_image(uchar4* dst, const uchar4* src,
                       uint32_t src_width, uint32_t src_height,
                       uint32_t dst_width, uint32_t dst_height,
                       int crop_x, int crop_y);

}
