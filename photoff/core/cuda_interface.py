from cffi import FFI

ffi = FFI()

ffi.cdef("""
    typedef struct { unsigned char x, y, z, w; } uchar4;
    
    uchar4* create_buffer(uint32_t width,
                          uint32_t height);

    void free_buffer(uchar4* buffer);

    uchar4* copy_buffer(const uchar4* src_buffer,
                        uint32_t width,
                        uint32_t height);

    void copy_to_device(uchar4* d_dst,
                        const uchar4* h_src,
                        uint32_t width,
                        uint32_t height);
    
    void copy_to_host(uchar4* h_dst,
                      const uchar4* d_src,
                      uint32_t width,
                      uint32_t height);

    void blend_buffers(uchar4* dst,
                       const uchar4* src,
                       uint32_t dst_width,
                       uint32_t dst_height,
                       uint32_t src_width,
                       uint32_t src_height,
                       int32_t x,
                       int32_t y);

    void fill_color(uchar4* buffer,
                    uint32_t width,
                    uint32_t height,
                    unsigned char r,
                    unsigned char g, 
                    unsigned char b,
                    unsigned char a);

    void apply_corner_radius(uchar4* buffer,
                             uint32_t width,
                             uint32_t height,
                             uint32_t size);

    void apply_stroke(const uchar4* src_buffer,
                      uchar4* dst_buffer,
                      uint32_t width,
                      uint32_t height,
                      int stroke_width,
                      unsigned char stroke_r,
                      unsigned char stroke_g,
                      unsigned char stroke_b,
                      unsigned char stroke_a,
                      int mode);

    void resize_bilinear(uchar4* dst,
                        const uchar4* src,
                        uint32_t dst_width,
                        uint32_t dst_height,
                        uint32_t src_width,
                        uint32_t src_height);

    void resize_nearest(uchar4* dst,
                        const uchar4* src,
                        uint32_t dst_width,
                        uint32_t dst_height,
                        uint32_t src_width,
                        uint32_t src_height);

    void resize_bicubic(uchar4* dst,
                        const uchar4* src,
                        uint32_t dst_width,
                        uint32_t dst_height,
                        uint32_t src_width,
                        uint32_t src_height);

    void apply_opacity(uchar4* buffer,
                       uint32_t width,
                       uint32_t height,
                       float opacity);

    void apply_shadow(const uchar4* src_buffer,
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

    void apply_flip(uchar4* buffer,
                    uint32_t width,
                    uint32_t height,
                    bool flip_horizontal,
                    bool flip_vertical);

    void crop_image(const uchar4* src_buffer,
                    uchar4* dst_buffer,
                    uint32_t src_width,
                    uint32_t src_height,
                    uint32_t dst_width,
                    uint32_t dst_height,
                    int crop_x,
                    int crop_y);

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
                    bool seamless);

""")

_lib = ffi.dlopen("photoff.dll")