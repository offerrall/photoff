#pragma once
#include <cuda_runtime.h>

extern "C" {

// Buffer Management ----------------------------------------------------------

__declspec(dllexport) uchar4* create_buffer(uint32_t width,
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


}