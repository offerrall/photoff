#pragma once
#include <cuda_runtime.h>

extern "C" {

// Buffer Management ----------------------------------------------------------

__declspec(dllexport) uchar4* create_buffer(uint32_t width,
                                            uint32_t height);

__declspec(dllexport) void copy_buffers_same_size(uchar4* dst,
                                                  const uchar4* src,
                                                  uint32_t width,
                                                  uint32_t height);

__declspec(dllexport) void free_buffer(uchar4* buffer);

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

__declspec(dllexport) void fill_gradient(uchar4* buffer,
                                         uint32_t width,
                                         uint32_t height,
                                         unsigned char r1,
                                         unsigned char g1,
                                         unsigned char b1,
                                         unsigned char a1,
                                         unsigned char r2,
                                         unsigned char g2,
                                         unsigned char b2,
                                         unsigned char a2,
                                         int direction,
                                         bool seamless);

// ---------------------------------------------------------------------------

// Filters -------------------------------------------------------------------


// No copy needed
__declspec(dllexport) void apply_corner_radius(uchar4* buffer,
                                               uint32_t width,
                                               uint32_t height,
                                               uint32_t size);

__declspec(dllexport) void apply_opacity(uchar4* buffer,
                                         uint32_t width,
                                         uint32_t height,
                                         float opacity);

__declspec(dllexport) void apply_flip(uchar4* buffer,
                                      uint32_t width,
                                      uint32_t height,
                                      bool flip_horizontal,
                                      bool flip_vertical);

__declspec(dllexport) void apply_grayscale(uchar4* buffer,
                                           uint32_t width,
                                           uint32_t height);

__declspec(dllexport) void apply_chroma_key(uchar4* buffer,
                                            const uchar4* key_buffer,
                                            uint32_t buffer_width,
                                            uint32_t buffer_height,
                                            uint32_t key_width,
                                            uint32_t key_height,
                                            int channel,
                                            unsigned char threshold,
                                            bool invert,
                                            bool zero_all_channels);

// Copy needed
__declspec(dllexport) void apply_stroke(uchar4* buffer,
                                        const uchar4* copy_buffer,
                                        uint32_t width,
                                        uint32_t height,
                                        int stroke_width,
                                        unsigned char stroke_r,
                                        unsigned char stroke_g,
                                        unsigned char stroke_b,
                                        unsigned char stroke_a,
                                        int mode);

__declspec(dllexport) void apply_shadow(uchar4* buffer,
                                        const uchar4* copy_buffer,
                                        uint32_t width,
                                        uint32_t height,
                                        float radius,
                                        float intensity,
                                        unsigned char shadow_r,
                                        unsigned char shadow_g,
                                        unsigned char shadow_b,
                                        unsigned char shadow_a,
                                        int mode);
                                           
__declspec(dllexport) void apply_gaussian_blur(uchar4* buffer,
                                               const uchar4* copy_buffer,
                                               uint32_t width,
                                               uint32_t height,
                                               float radius);


// ---------------------------------------------------------------------------

// Resize and Crop --------------------------------------------------------------------

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

__declspec(dllexport) void crop_image(uchar4* dst,
                                      const uchar4* src,
                                      uint32_t src_width,
                                      uint32_t src_height,
                                      uint32_t dst_width,
                                      uint32_t dst_height,
                                      int crop_x,
                                      int crop_y);

// ---------------------------------------------------------------------------

}