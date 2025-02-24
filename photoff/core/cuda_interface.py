from cffi import FFI

ffi = FFI()

ffi.cdef("""
    typedef struct { unsigned char x, y, z, w; } uchar4;
    
    uchar4* create_buffer(uint32_t width,
                          uint32_t height);

    void free_buffer(uchar4* buffer);
         
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

    void apply_stroke(uchar4* buffer,
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
    
""")

_lib = ffi.dlopen("photoff.dll")