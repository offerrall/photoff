#include "photoff.h"
#include <stdio.h>


__global__ void fillColorKernel(uchar4* buffer,
                                uchar4 color, 
                                uint32_t width,
                                uint32_t height) {

    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x < width && y < height) {
        int idx = y * width + x;
        buffer[idx] = color;
    }
}


__global__ void blendKernel(uchar4* dst,
                            const uchar4* src,
                            uint32_t dst_width,
                            uint32_t dst_height,
                            uint32_t src_width,
                            uint32_t src_height,
                            int32_t pos_x,
                            int32_t pos_y) {

    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x >= dst_width || y >= dst_height) return;

    int src_x = x - pos_x;
    int src_y = y - pos_y;

    if (src_x >= 0 && src_x < src_width && 
        src_y >= 0 && src_y < src_height) {
        
        int dst_idx = y * dst_width + x;
        int src_idx = src_y * src_width + src_x;
        
        uchar4 src_pixel = src[src_idx];
        uchar4 dst_pixel = dst[dst_idx];
        
        float srcA = src_pixel.w / 255.0f;
        float dstA = dst_pixel.w / 255.0f;

        // Case 1: pixel totally opaque
        if (src_pixel.w == 255) {
            dst[dst_idx] = src_pixel;
        } 
        // Case 2: pixel totally transparent
        else if (src_pixel.w == 0) {
            // Do nothing
        } 
        // Case 3: pixel semi-transparent
        else {
            float outA = srcA + dstA * (1.0f - srcA);

            // Avoid division by zero
            if (outA > 0.0f) {
                float outR = (src_pixel.x * srcA + dst_pixel.x * dstA * (1.0f - srcA)) / outA;
                float outG = (src_pixel.y * srcA + dst_pixel.y * dstA * (1.0f - srcA)) / outA;
                float outB = (src_pixel.z * srcA + dst_pixel.z * dstA * (1.0f - srcA)) / outA;

                dst[dst_idx].x = static_cast<unsigned char>(outR);
                dst[dst_idx].y = static_cast<unsigned char>(outG);
                dst[dst_idx].z = static_cast<unsigned char>(outB);
                dst[dst_idx].w = static_cast<unsigned char>(outA * 255.0f);
            } else {
                // Do nothing
            }
        }
    }
}

__global__ void cornerRadiusKernel(uchar4* buffer,
                                   uint32_t width,
                                   uint32_t height,
                                   uint32_t radius) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    
    if (x >= width || y >= height) return;
    
    int idx = y * width + x;
    
    if (x < radius && y < radius) {
        int dx = radius - 1 - x;
        int dy = radius - 1 - y;
        if (dx * dx + dy * dy > radius * radius) {
            buffer[idx] = make_uchar4(0, 0, 0, 0);
        }
    }

    else if (x >= width - radius && y < radius) {
        int dx = x - (width - radius);
        int dy = radius - 1 - y;
        if (dx * dx + dy * dy > radius * radius) {
            buffer[idx] = make_uchar4(0, 0, 0, 0);
        }
    }

    else if (x < radius && y >= height - radius) {
        int dx = radius - 1 - x;
        int dy = y - (height - radius);
        if (dx * dx + dy * dy > radius * radius) {
            buffer[idx] = make_uchar4(0, 0, 0, 0);
        }
    }

    else if (x >= width - radius && y >= height - radius) {
        int dx = x - (width - radius);
        int dy = y - (height - radius);
        if (dx * dx + dy * dy > radius * radius) {
            buffer[idx] = make_uchar4(0, 0, 0, 0);
        }
    }
}


extern "C" {

uchar4* create_buffer(uint32_t width,
                      uint32_t height) {

    uchar4* buffer;
    cudaError_t err = cudaMalloc(&buffer, width * height * sizeof(uchar4));
    if (err != cudaSuccess) {
        printf("Error in cudaMalloc: %s\n", cudaGetErrorString(err));
        return nullptr;
    }
    cudaDeviceSynchronize();
    return buffer;
}

void free_buffer(uchar4* buffer) {
    if (buffer) {
        cudaFree(buffer);
    }
    cudaDeviceSynchronize();
}

void copy_to_device(uchar4* d_dst,
                    const uchar4* h_src,
                    uint32_t width,
                    uint32_t height) {

    if (!d_dst || !h_src) return;

    cudaMemcpy(d_dst, h_src, width * height * sizeof(uchar4), 
               cudaMemcpyHostToDevice);
    
    cudaDeviceSynchronize();
}

void copy_to_host(uchar4* h_dst,
                  const uchar4* d_src,
                  uint32_t width,
                  uint32_t height) {

    if (!h_dst || !d_src) return;

    cudaMemcpy(h_dst, d_src, width * height * sizeof(uchar4), 
               cudaMemcpyDeviceToHost);

    cudaDeviceSynchronize();
}

void blend_buffers(uchar4* dst,
                   const uchar4* src,
                   uint32_t dst_width,
                   uint32_t dst_height,
                   uint32_t src_width,
                   uint32_t src_height,
                   int32_t x,
                   int32_t y) {
                    
    if (!dst || !src) return;

    dim3 block(16, 16);
    dim3 grid((dst_width + block.x - 1) / block.x,
              (dst_height + block.y - 1) / block.y);
              
    blendKernel<<<grid, block>>>(dst, src, dst_width, dst_height,
                                src_width, src_height, x, y);

    cudaDeviceSynchronize();
}

void fill_color(uchar4* buffer,
                uint32_t width,
                uint32_t height,
                unsigned char r,
                unsigned char g,
                unsigned char b,
                unsigned char a) {

    if (!buffer) return;

    uchar4 color = make_uchar4(r, g, b, a);
    
    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x,
              (height + block.y - 1) / block.y);
              
    fillColorKernel<<<grid, block>>>(buffer, color, width, height);

    cudaDeviceSynchronize();
}

void apply_corner_radius(uchar4* buffer,
                         uint32_t width,
                         uint32_t height,
                         uint32_t size) {
    if (!buffer) return;

    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x,
                (height + block.y - 1) / block.y);
                
    cornerRadiusKernel<<<grid, block>>>(buffer, width, height, size);

    cudaDeviceSynchronize();
}

}