from cffi import FFI

ffi = FFI()

ffi.cdef("""
    // Definiciones básicas
    typedef unsigned int uint32_t;
    typedef int int32_t;
    typedef _Bool bool;  // para 'bool' en C

    typedef struct { 
        unsigned char x, y, z, w; 
    } uchar4;

    // Buffer Management
    uchar4* create_buffer(uint32_t width, uint32_t height);
    void free_buffer(uchar4* buffer);

    // Host - Device Memory Transfer
    void copy_to_host(uchar4* h_dst, const uchar4* d_src, uint32_t width, uint32_t height);
    void copy_to_device(uchar4* d_dst, const uchar4* h_src, uint32_t width, uint32_t height);

    // Blend
    void blend_buffers(uchar4* dst, const uchar4* src,
                       uint32_t dst_width, uint32_t dst_height,
                       uint32_t src_width, uint32_t src_height,
                       int32_t x, int32_t y);

    // Fill effects
    void fill_color(uchar4* buffer,
                    uint32_t width, uint32_t height,
                    unsigned char r, unsigned char g,
                    unsigned char b, unsigned char a);

    void fill_gradient(uchar4* buffer,
                       uint32_t width, uint32_t height,
                       unsigned char r1, unsigned char g1,
                       unsigned char b1, unsigned char a1,
                       unsigned char r2, unsigned char g2,
                       unsigned char b2, unsigned char a2,
                       int direction, bool seamless);

    // Filters
    void apply_corner_radius(uchar4* buffer,
                             uint32_t width, uint32_t height,
                             uint32_t size);

    void apply_opacity(uchar4* buffer,
                       uint32_t width, uint32_t height,
                       float opacity);

    void apply_flip(uchar4* buffer,
                    uint32_t width, uint32_t height,
                    bool flip_horizontal, bool flip_vertical);

    // Filtros que requieren copia del buffer original
    void apply_stroke(uchar4* buffer, const uchar4* copy_buffer,
                      uint32_t width, uint32_t height,
                      int stroke_width,
                      unsigned char stroke_r, unsigned char stroke_g,
                      unsigned char stroke_b, unsigned char stroke_a,
                      int mode);

    void apply_shadow(uchar4* buffer, const uchar4* copy_buffer,
                      uint32_t width, uint32_t height,
                      float radius, float intensity,
                      unsigned char shadow_r, unsigned char shadow_g,
                      unsigned char shadow_b, unsigned char shadow_a,
                      int mode);

    // Resize / Crop
    void resize_bilinear(uchar4* dst, const uchar4* src,
                         uint32_t dst_width, uint32_t dst_height,
                         uint32_t src_width, uint32_t src_height);

    void resize_nearest(uchar4* dst, const uchar4* src,
                        uint32_t dst_width, uint32_t dst_height,
                        uint32_t src_width, uint32_t src_height);

    void resize_bicubic(uchar4* dst, const uchar4* src,
                        uint32_t dst_width, uint32_t dst_height,
                        uint32_t src_width, uint32_t src_height);

    void crop_image(uchar4* dst, const uchar4* src,
                    uint32_t src_width, uint32_t src_height,
                    uint32_t dst_width, uint32_t dst_height,
                    int crop_x, int crop_y);
""")

_lib = ffi.dlopen("photoff.dll")