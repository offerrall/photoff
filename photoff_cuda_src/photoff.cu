#include "photoff.h"
#include <stdio.h>

__global__ void cropKernel(const uchar4* src,
                           uchar4* dst,
                           uint32_t src_width,
                           uint32_t src_height,
                           uint32_t dst_width,
                           uint32_t dst_height,
                           int crop_x,
                           int crop_y) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x >= dst_width || y >= dst_height) return;

    int src_x = crop_x + x;
    int src_y = crop_y + y;

    if (src_x < src_width && src_y < src_height) {
        dst[y * dst_width + x] = src[src_y * src_width + src_x];
    } else {
        dst[y * dst_width + x] = make_uchar4(0, 0, 0, 0);
    }
}

__global__ void chromaKeyKernel(uchar4* buffer,
                                const uchar4* key_buffer,
                                uint32_t buffer_width,
                                uint32_t buffer_height,
                                uint32_t key_width,
                                uint32_t key_height,
                                int channel,
                                unsigned char threshold,
                                bool invert,
                                bool zero_all_channels) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    
    if (x >= buffer_width || y >= buffer_height) return;
    
    int buffer_idx = y * buffer_width + x;
    
    if (x < key_width && y < key_height) {
        int key_idx = y * key_width + x;
        uchar4 keyPixel = key_buffer[key_idx];
        
        unsigned char channelValue;
        switch(channel) {
            case 0: channelValue = keyPixel.x; break; // R
            case 1: channelValue = keyPixel.y; break; // G
            case 2: channelValue = keyPixel.z; break; // B
            case 3: channelValue = keyPixel.w; break; // A
            default: channelValue = keyPixel.y; break; // Default to G
        }
        
        bool makeTransparent = invert ? 
                              (channelValue <= threshold) : 
                              (channelValue > threshold);
        
        if (makeTransparent) {
            if (zero_all_channels) {
                buffer[buffer_idx] = make_uchar4(0, 0, 0, 0); // Poner todo el píxel a 0
            } else {
                buffer[buffer_idx].w = 0; // Solo modificar alfa, manteniendo RGB intacto
            }
        }
    }
}


__global__ void grayscaleKernel(uchar4* buffer,
                               uint32_t width,
                               uint32_t height) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    
    if (x >= width || y >= height) return;
    
    int idx = y * width + x;
    uchar4 pixel = buffer[idx];
    
    if (pixel.w == 0) return;
    
    unsigned char gray = (unsigned char)(
        0.299f * pixel.x + 
        0.587f * pixel.y + 
        0.114f * pixel.z
    );
    
    buffer[idx].x = gray;
    buffer[idx].y = gray;
    buffer[idx].z = gray;
}

__device__ float gaussianWeight(float distance, float sigma) {
    return expf(-(distance * distance) / (2.0f * sigma * sigma));
}

__global__ void gaussianBlurKernel(const uchar4* src,
                                   uchar4* dst,
                                   uint32_t width,
                                   uint32_t height,
                                   float radius) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    
    if (x >= width || y >= height) return;
    
    float sigma = radius / 2.0f;
    
    int kernelSize = ceilf(radius * 3.0f);
    kernelSize = max(1, min(kernelSize, 25));
    
    float sumR = 0.0f, sumG = 0.0f, sumB = 0.0f, sumA = 0.0f;
    float totalWeight = 0.0f;
    
    for (int ky = -kernelSize; ky <= kernelSize; ky++) {
        for (int kx = -kernelSize; kx <= kernelSize; kx++) {
            int sampleX = min(width - 1, max(0, x + kx));
            int sampleY = min(height - 1, max(0, y + ky));
            
            float distance = sqrtf((float)(kx * kx + ky * ky));
            
            if (distance > kernelSize) continue;
            
            float weight = gaussianWeight(distance, sigma);
            
            uchar4 sample = src[sampleY * width + sampleX];
            
            float alpha = sample.w / 255.0f;
            
            sumR += sample.x * weight * alpha;
            sumG += sample.y * weight * alpha;
            sumB += sample.z * weight * alpha;
            sumA += sample.w * weight;
            
            totalWeight += weight;
        }
    }
    
    if (totalWeight > 0.0f) {
        float alpha = sumA / (totalWeight * 255.0f);
        
        if (alpha > 0.0f) {
            dst[y * width + x].x = (unsigned char)(sumR / (totalWeight * alpha));
            dst[y * width + x].y = (unsigned char)(sumG / (totalWeight * alpha));
            dst[y * width + x].z = (unsigned char)(sumB / (totalWeight * alpha));
            dst[y * width + x].w = (unsigned char)(sumA / totalWeight);
        } else {
            dst[y * width + x] = make_uchar4(0, 0, 0, 0);
        }
    } else {
        dst[y * width + x] = make_uchar4(0, 0, 0, 0);
    }
}

__global__ void copyBufferKernel(uchar4* dst,
                                 const uchar4* src,
                                 uint32_t width,
                                 uint32_t height) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    
    if (x >= width || y >= height) return;
    
    int idx = y * width + x;
    dst[idx] = src[idx];
}

__device__ float calculateShadowWeight(int x,
                                       int y,
                                       const uchar4* buffer,
                                       uint32_t width,
                                       uint32_t height,
                                       float radius,
                                       bool isInner) {
    float minDistance = radius;
    int r2 = radius * radius;
    
    for (int dy = -radius; dy <= radius; dy++) {
        for (int dx = -radius; dx <= radius; dx++) {
            if (dx*dx + dy*dy > r2) continue;
            
            int nx = x + dx;
            int ny = y + dy;
            
            if (nx >= 0 && nx < width && ny >= 0 && ny < height) {
                bool hasAlpha = buffer[ny * width + nx].w > 0;
                if (hasAlpha != isInner) {
                    float distance = sqrtf(dx*dx + dy*dy);
                    minDistance = min(minDistance, distance);
                }
            }
        }
    }
    
    float weight = 1.0f - (minDistance / radius);
    return max(0.0f, min(1.0f, weight));
}

__global__ void shadowKernel(const uchar4* src,
                             uchar4* dst,
                             uint32_t width,
                             uint32_t height,
                             float radius,
                             float intensity,
                             uchar4 shadow_color,
                             bool isInner) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    
    if (x >= width || y >= height) return;
    
    int idx = y * width + x;
    uchar4 srcPixel = src[idx];
    
    if ((isInner && srcPixel.w == 0) || (!isInner && srcPixel.w > 0)) {
        dst[idx] = srcPixel;
        return;
    }
    
    float shadowWeight = calculateShadowWeight(x, y, src, width, height, radius, isInner);
    shadowWeight *= intensity;
    
    if (isInner) {
        float invWeight = 1.0f - shadowWeight;
        dst[idx].x = (unsigned char)(srcPixel.x * invWeight + shadow_color.x * shadowWeight);
        dst[idx].y = (unsigned char)(srcPixel.y * invWeight + shadow_color.y * shadowWeight);
        dst[idx].z = (unsigned char)(srcPixel.z * invWeight + shadow_color.z * shadowWeight);
        dst[idx].w = srcPixel.w;
    } else {
        if (shadowWeight > 0.0f) {
            float finalAlpha = shadow_color.w / 255.0f * shadowWeight;
            dst[idx].x = shadow_color.x;
            dst[idx].y = shadow_color.y;
            dst[idx].z = shadow_color.z;
            dst[idx].w = (unsigned char)(finalAlpha * 255.0f);
        } else {
            dst[idx] = make_uchar4(0, 0, 0, 0);
        }
    }
}

__device__ float bicubicWeight(float x, float a = -0.5f) {
    x = fabsf(x);
    if (x <= 1.0f) {
        return ((a + 2.0f) * x * x * x) - ((a + 3.0f) * x * x) + 1.0f;
    } else if (x < 2.0f) {
        return (a * x * x * x) - (5.0f * a * x * x) + (8.0f * a * x) - (4.0f * a);
    }
    return 0.0f;
}

__global__ void resizeBicubicKernel(uchar4* dst,
                                    const uchar4* src,
                                    uint32_t dst_width,
                                    uint32_t dst_height,
                                    uint32_t src_width,
                                    uint32_t src_height) {
    int dst_x = blockIdx.x * blockDim.x + threadIdx.x;
    int dst_y = blockIdx.y * blockDim.y + threadIdx.y;

    if (dst_x >= dst_width || dst_y >= dst_height) return;

    float scale_x = (float)(src_width) / dst_width;
    float scale_y = (float)(src_height) / dst_height;
    
    float src_x = dst_x * scale_x;
    float src_y = dst_y * scale_y;

    int x0 = floorf(src_x - 1.0f);
    int y0 = floorf(src_y - 1.0f);
    
    float4 result = make_float4(0.0f, 0.0f, 0.0f, 0.0f);
    float totalWeight = 0.0f;

    #pragma unroll
    for (int dy = 0; dy < 4; dy++) {
        int sy = y0 + dy;
        float wy = bicubicWeight(src_y - sy);
        
        #pragma unroll
        for (int dx = 0; dx < 4; dx++) {
            int sx = x0 + dx;
            
            if (sx >= 0 && sx < src_width && sy >= 0 && sy < src_height) {
                float wx = bicubicWeight(src_x - sx);
                float weight = wx * wy;
                
                uchar4 pixel = src[sy * src_width + sx];
                result.x += weight * pixel.x;
                result.y += weight * pixel.y;
                result.z += weight * pixel.z;
                result.w += weight * pixel.w;
                totalWeight += weight;
            }
        }
    }

    if (totalWeight > 0.0f) {
        result.x = fmaxf(0.0f, fminf(255.0f, result.x / totalWeight));
        result.y = fmaxf(0.0f, fminf(255.0f, result.y / totalWeight));
        result.z = fmaxf(0.0f, fminf(255.0f, result.z / totalWeight));
        result.w = fmaxf(0.0f, fminf(255.0f, result.w / totalWeight));
    }

    dst[dst_y * dst_width + dst_x] = make_uchar4(
        __float2int_rn(result.x),
        __float2int_rn(result.y),
        __float2int_rn(result.z),
        __float2int_rn(result.w)
    );
}

__global__ void resizeBilinearKernel(uchar4* dst,
                                     const uchar4* src,
                                     uint32_t dst_width,
                                     uint32_t dst_height,
                                     uint32_t src_width,
                                     uint32_t src_height) {

    int dst_x = blockIdx.x * blockDim.x + threadIdx.x;
    int dst_y = blockIdx.y * blockDim.y + threadIdx.y;

    if (dst_x >= dst_width || dst_y >= dst_height) return;

    float scale_x = (float)(src_width - 1) / dst_width;
    float scale_y = (float)(src_height - 1) / dst_height;
    
    float src_x = dst_x * scale_x;
    float src_y = dst_y * scale_y;
    
    int x1 = (int)src_x;
    int y1 = (int)src_y;
    int x2 = min(x1 + 1, (int)src_width - 1);
    int y2 = min(y1 + 1, (int)src_height - 1);
    
    float wx2 = src_x - x1;
    float wy2 = src_y - y1;
    float wx1 = 1.0f - wx2;
    float wy1 = 1.0f - wy2;
    
    uchar4 p11 = src[y1 * src_width + x1];
    uchar4 p21 = src[y1 * src_width + x2];
    uchar4 p12 = src[y2 * src_width + x1];
    uchar4 p22 = src[y2 * src_width + x2];
    
    int dst_idx = dst_y * dst_width + dst_x;
    dst[dst_idx].x = (unsigned char)(
        p11.x * wx1 * wy1 +
        p21.x * wx2 * wy1 +
        p12.x * wx1 * wy2 +
        p22.x * wx2 * wy2);
    
    dst[dst_idx].y = (unsigned char)(
        p11.y * wx1 * wy1 +
        p21.y * wx2 * wy1 +
        p12.y * wx1 * wy2 +
        p22.y * wx2 * wy2);
    
    dst[dst_idx].z = (unsigned char)(
        p11.z * wx1 * wy1 +
        p21.z * wx2 * wy1 +
        p12.z * wx1 * wy2 +
        p22.z * wx2 * wy2);
    
    dst[dst_idx].w = (unsigned char)(
        p11.w * wx1 * wy1 +
        p21.w * wx2 * wy1 +
        p12.w * wx1 * wy2 +
        p22.w * wx2 * wy2);
}

__global__ void resizeNearestKernel(uchar4* dst,
                                    const uchar4* src,
                                    uint32_t dst_width,
                                    uint32_t dst_height,
                                    uint32_t src_width,
                                    uint32_t src_height) {

    int dst_x = blockIdx.x * blockDim.x + threadIdx.x;
    int dst_y = blockIdx.y * blockDim.y + threadIdx.y;

    if (dst_x >= dst_width || dst_y >= dst_height) return;

    float scale_x = (float)src_width / dst_width;
    float scale_y = (float)src_height / dst_height;

    int src_x = (int)(dst_x * scale_x);
    int src_y = (int)(dst_y * scale_y);
    
    dst[dst_y * dst_width + dst_x] = src[src_y * src_width + src_x];
}


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

__global__ void strokeKernel(const uchar4* src,
                             uchar4* dst,
                             uint32_t width,
                             uint32_t height,
                             int stroke_width,
                             uchar4 stroke_color) {

    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    
    if (x >= width || y >= height) return;
    
    int idx = y * width + x;
    uchar4 pixel = src[idx];

    if (pixel.w != 0) {
        dst[idx] = pixel;
        return;
    }
    
    int r2 = stroke_width * stroke_width;
    for (int dy = -stroke_width; dy <= stroke_width; dy++) {
        for (int dx = -stroke_width; dx <= stroke_width; dx++) {
            if (dx*dx + dy*dy > r2) continue;
            
            int nx = x + dx;
            int ny = y + dy;
            if (nx < 0 || nx >= width || ny < 0 || ny >= height) continue;
            
            if (src[ny * width + nx].w != 0) {
                dst[idx] = stroke_color;
                return;
            }
        }
    }
    dst[idx] = pixel;
}

__global__ void innerStrokeKernel(const uchar4* src,
                                  uchar4* dst,
                                  uint32_t width,
                                  uint32_t height,
                                  int stroke_width,
                                  uchar4 stroke_color) {

    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    
    if (x >= width || y >= height) return;
    
    int idx = y * width + x;
    uchar4 pixel = src[idx];

    if (pixel.w == 0) {
        dst[idx] = pixel;
        return;
    }
    
    int r2 = stroke_width * stroke_width;
    bool isBorder = false;
    
    if (x < stroke_width || x >= width - stroke_width || 
        y < stroke_width || y >= height - stroke_width) {
        isBorder = true;
    }
    
    if (!isBorder) {
        for (int dy = -stroke_width; dy <= stroke_width && !isBorder; dy++) {
            for (int dx = -stroke_width; dx <= stroke_width && !isBorder; dx++) {
                if (dx*dx + dy*dy > r2) continue;
                
                int nx = x + dx;
                int ny = y + dy;
                if (nx < 0 || nx >= width || ny < 0 || ny >= height) {
                    isBorder = true;
                } else if (src[ny * width + nx].w == 0) {
                    isBorder = true;
                }
            }
        }
    }
    
    dst[idx] = isBorder ? stroke_color : pixel;
}

__global__ void applyOpacityKernel(uchar4* buffer, 
                                   uint32_t width, 
                                   uint32_t height,
                                   float opacity) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x >= width || y >= height) return;

    int idx = y * width + x;
    uchar4 pixel = buffer[idx];
    
    float currentAlpha = pixel.w / 255.0f;
    float newAlpha = currentAlpha * opacity;
    buffer[idx].w = static_cast<unsigned char>(newAlpha * 255.0f);
}

__global__ void flipKernel(uchar4* buffer,
                           uint32_t width,
                           uint32_t height,
                           bool flipHorizontal,
                           bool flipVertical) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    
    if (x >= width || y >= height) return;
    
    if ((flipHorizontal && x >= width/2) || 
        (flipVertical && y >= height/2)) return;
    
    int src_x = flipHorizontal ? (width - 1 - x) : x;
    int src_y = flipVertical ? (height - 1 - y) : y;
    
    if (src_x == x && src_y == y) return;
    
    int idx1 = y * width + x;
    int idx2 = src_y * width + src_x;
    
    uchar4 temp = buffer[idx1];
    buffer[idx1] = buffer[idx2];
    buffer[idx2] = temp;
}


__global__ void fillGradientKernel(uchar4* buffer, 
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
                                   bool seamless) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x >= (int)width || y >= (int)height) return;

    float factor = 0.0f;

    float nx = (float)x / (float)(width - 1) - 0.5f;
    float ny = (float)y / (float)(height - 1) - 0.5f;

    switch(direction) {
        case 0: // horizontal
            factor = (float)x / (float)(width - 1);
            break;
        case 1: // vertical
            factor = (float)y / (float)(height - 1);
            break;
        case 2: // diagonal
            float u = (float)x / (float)(width - 1);
            float v = (float)y / (float)(height - 1);
            factor = (u + v) * 0.5f;
            break;
        case 3: // radial
            factor = sqrtf(nx*nx + ny*ny) * 1.414f;
            factor = min(1.0f, factor);
            break;
    }

    if (seamless) {
        factor = factor < 0.5f ? 
                factor * 2.0f : 
                2.0f * (1.0f - factor);
    }

    unsigned char R = (unsigned char)(r1 + (r2 - r1) * factor);
    unsigned char G = (unsigned char)(g1 + (g2 - g1) * factor);
    unsigned char B = (unsigned char)(b1 + (b2 - b1) * factor);
    unsigned char A = (unsigned char)(a1 + (a2 - a1) * factor);

    int idx = y * width + x;
    buffer[idx] = make_uchar4(R, G, B, A);
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

void copy_buffers_same_size(uchar4* dst,
                            const uchar4* src,
                            uint32_t width,
                            uint32_t height) {
    if (!dst || !src) {
        printf("Error: Null pointer provided to copy_buffers_same_size\n");
        return;
    }
    
    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x, (height + block.y - 1) / block.y);
    
    copyBufferKernel<<<grid, block>>>(dst, src, width, height);
    
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        printf("CUDA Error in copy_buffers_same_size: %s\n", cudaGetErrorString(err));
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

void resize_bilinear(uchar4* dst,
                     const uchar4* src,
                     uint32_t dst_width,
                     uint32_t dst_height,
                     uint32_t src_width,
                     uint32_t src_height) {
    if (!dst || !src) return;

    dim3 block(16, 16);
    dim3 grid((dst_width + block.x - 1) / block.x,
              (dst_height + block.y - 1) / block.y);
              
    resizeBilinearKernel<<<grid, block>>>(dst, src,
                                         dst_width, dst_height,
                                         src_width, src_height);
    
    cudaDeviceSynchronize();
}

void resize_nearest(uchar4* dst,
                    const uchar4* src,
                    uint32_t dst_width,
                    uint32_t dst_height,
                    uint32_t src_width,
                    uint32_t src_height) {
    if (!dst || !src) return;

    dim3 block(16, 16);
    dim3 grid((dst_width + block.x - 1) / block.x,
                (dst_height + block.y - 1) / block.y);
                
    resizeNearestKernel<<<grid, block>>>(dst, src,
                                        dst_width, dst_height,
                                        src_width, src_height);
    
    cudaDeviceSynchronize();
}

void resize_bicubic(uchar4* dst,
                    const uchar4* src,
                    uint32_t dst_width,
                    uint32_t dst_height,
                    uint32_t src_width,
                    uint32_t src_height) {
    if (!dst || !src) return;

    dim3 block(16, 16);
    dim3 grid((dst_width + block.x - 1) / block.x,
                (dst_height + block.y - 1) / block.y);
            
    resizeBicubicKernel<<<grid, block>>>(dst, src,
                                        dst_width, dst_height,
                                        src_width, src_height);

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

void apply_stroke(uchar4* buffer,
                  const uchar4* copy_buffer,
                  uint32_t width,
                  uint32_t height,
                  int stroke_width,
                  unsigned char stroke_r,
                  unsigned char stroke_g,
                  unsigned char stroke_b,
                  unsigned char stroke_a,
                  int mode) {

    uchar4 stroke_color = make_uchar4(stroke_r, stroke_g, stroke_b, stroke_a);
    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x,
              (height + block.y - 1) / block.y);
    
    if (mode == 0) {
        strokeKernel<<<grid, block>>>(copy_buffer, buffer, width, height,
                                        stroke_width, stroke_color);
    } else if (mode == 1) {
        innerStrokeKernel<<<grid, block>>>(copy_buffer, buffer, width, height,
                                             stroke_width, stroke_color);
    }
    
    cudaDeviceSynchronize();
}


void apply_opacity(uchar4* buffer,
                   uint32_t width,
                   uint32_t height,
                   float opacity) {
    if (!buffer) return;
    
    opacity = min(max(opacity, 0.0f), 1.0f);

    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x,
            (height + block.y - 1) / block.y);
            
    applyOpacityKernel<<<grid, block>>>(buffer, width, height, opacity);
    cudaDeviceSynchronize();
}

void apply_shadow(uchar4* buffer,
                  const uchar4* copy_buffer,
                  uint32_t width,
                  uint32_t height,
                  float radius,
                  float intensity,
                  unsigned char shadow_r,
                  unsigned char shadow_g,
                  unsigned char shadow_b,
                  unsigned char shadow_a,
                  int mode) {
    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x,
              (height + block.y - 1) / block.y);
    
    uchar4 shadow_color = make_uchar4(shadow_r, shadow_g, shadow_b, shadow_a);
    bool isInner = mode == 1;
    
    shadowKernel<<<grid, block>>>(copy_buffer, buffer,
                                  width, height,
                                  radius, intensity,
                                  shadow_color, isInner);
    
    cudaDeviceSynchronize();
}


void apply_flip(uchar4* buffer,
                uint32_t width,
                uint32_t height,
                bool flip_horizontal,
                bool flip_vertical) {
    if (!buffer) return;
    
    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x,
              (height + block.y - 1) / block.y);
              
    flipKernel<<<grid, block>>>(buffer, width, height,
                               flip_horizontal, flip_vertical);
    
    cudaDeviceSynchronize();
}

void apply_grayscale(uchar4* buffer,
                    uint32_t width,
                    uint32_t height) {
    if (!buffer) return;
    
    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x,
              (height + block.y - 1) / block.y);
              
    grayscaleKernel<<<grid, block>>>(buffer, width, height);
    
    cudaDeviceSynchronize();
}

void crop_image(uchar4* dst,
                const uchar4* src,
                uint32_t src_width,
                uint32_t src_height,
                uint32_t dst_width,
                uint32_t dst_height,
                int crop_x,
                int crop_y) {
    if (!src || !dst) return;

    dim3 block(16, 16);
    dim3 grid((dst_width + block.x - 1) / block.x,
              (dst_height + block.y - 1) / block.y);

    cropKernel<<<grid, block>>>(src, dst,
                                src_width, src_height,
                                dst_width, dst_height,
                                crop_x, crop_y);
    cudaDeviceSynchronize();
}

void fill_gradient(uchar4* buffer,
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
                   bool seamless) {
    if (!buffer) return;

    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x,
              (height + block.y - 1) / block.y);

    fillGradientKernel<<<grid, block>>>(buffer, width, height,
                                            r1, g1, b1, a1,
                                            r2, g2, b2, a2,
                                            direction, seamless);
    cudaDeviceSynchronize();
}

void apply_gaussian_blur(uchar4* buffer,
                         const uchar4* copy_buffer,
                         uint32_t width,
                         uint32_t height,
                         float radius) {
    
    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x,
              (height + block.y - 1) / block.y);
    
    gaussianBlurKernel<<<grid, block>>>(copy_buffer, buffer, width, height, radius);
    
    cudaDeviceSynchronize();
}

void apply_chroma_key(uchar4* buffer,
                    const uchar4* key_buffer,
                    uint32_t buffer_width,
                    uint32_t buffer_height,
                    uint32_t key_width,
                    uint32_t key_height,
                    int channel,
                    unsigned char threshold,
                    bool invert,
                    bool zero_all_channels) {
    if (!buffer || !key_buffer) return;
    
    dim3 block(16, 16);
    dim3 grid((buffer_width + block.x - 1) / block.x,
              (buffer_height + block.y - 1) / block.y);
              
    chromaKeyKernel<<<grid, block>>>(buffer, key_buffer, 
                                     buffer_width, buffer_height, 
                                     key_width, key_height, 
                                     channel, threshold, invert,
                                     zero_all_channels);
    
    cudaDeviceSynchronize();
}

}