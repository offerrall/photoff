#pragma once
#include <cuda_runtime.h>

extern "C" {

// Buffer Management ----------------------------------------------------------

__declspec(dllexport) uchar4* create_buffer(uint32_t width,
                                            uint32_t height);

__declspec(dllexport) uchar4* copy_buffer(const uchar4* src_buffer,
                                          uint32_t width,
                                          uint32_t height);

__declspec(dllexport) void free_buffer(uchar4* buffer);

__declspec(dllexport) void fill_color(uchar4* buffer,
                                      uint32_t width,
                                      uint32_t height,
                                      unsigned char r,
                                      unsigned char g, 
                                      unsigned char b,
                                      unsigned char a);

// ---------------------------------------------------------------------------

// Host - Device Memory Transfer ----------------------------------------------

__declspec(dllexport) void copy_to_host(uchar4* h_dst,
                                        const uchar4* d_src,
                                        uint32_t width,
                                        uint32_t height);

__declspec(dllexport) void copy_to_device(uchar4* d_dst,
                                          const uchar4* h_src,
                                          uint32_t width,
                                          uint32_t height);

// ---------------------------------------------------------------------------

// Blend -----------------------------------------------------------

__declspec(dllexport) void blend_buffers(uchar4* dst,
                                         const uchar4* src,
                                         uint32_t dst_width,
                                         uint32_t dst_height,
                                         uint32_t src_width,
                                         uint32_t src_height,
                                         int32_t x,
                                         int32_t y);

// ---------------------------------------------------------------------------

// Fill effects ---------------------------------------------------------------

__declspec(dllexport) void fill_color(uchar4* buffer,
                                      uint32_t width,
                                      uint32_t height,
                                      unsigned char r,
                                      unsigned char g, 
                                      unsigned char b,
                                      unsigned char a);

// ---------------------------------------------------------------------------

// Filters -------------------------------------------------------------------

__declspec(dllexport) void apply_corner_radius(uchar4* buffer,
                                               uint32_t width,
                                               uint32_t height,
                                               uint32_t size);

__declspec(dllexport) void apply_stroke(const uchar4* src_buffer,
                                        uchar4* dst_buffer,
                                        uint32_t width,
                                        uint32_t height,
                                        int stroke_width,
                                        unsigned char stroke_r,
                                        unsigned char stroke_g,
                                        unsigned char stroke_b,
                                        unsigned char stroke_a,
                                        int mode);

__declspec(dllexport) void apply_shadow(const uchar4* src_buffer,
                                        uchar4* dst_buffer,
                                        uint32_t width,
                                        uint32_t height,
                                        float radius,
                                        float intensity,
                                        unsigned char shadow_r,
                                        unsigned char shadow_g,
                                        unsigned char shadow_b,
                                        unsigned char shadow_a,
                                        int mode);

__declspec(dllexport) void apply_opacity(uchar4* buffer,
                                         uint32_t width,
                                         uint32_t height,
                                         float opacity);

// ---------------------------------------------------------------------------

// Resize --------------------------------------------------------------------

__declspec(dllexport) void resize_bilinear(uchar4* dst,
                                           const uchar4* src,
                                           uint32_t dst_width,
                                           uint32_t dst_height,
                                           uint32_t src_width,
                                           uint32_t src_height);

__declspec(dllexport) void resize_nearest(uchar4* dst,
                                          const uchar4* src,
                                          uint32_t dst_width,
                                          uint32_t dst_height,
                                          uint32_t src_width,
                                          uint32_t src_height);

__declspec(dllexport) void resize_bicubic(uchar4* dst,
                                          const uchar4* src,
                                          uint32_t dst_width,
                                          uint32_t dst_height,
                                          uint32_t src_width,
                                          uint32_t src_height);

// ---------------------------------------------------------------------------

}