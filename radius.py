from PIL import Image, ImageDraw
from time import perf_counter

def add_rounded_corners(image: Image, radius: int) -> Image:
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
    result = Image.new('RGBA', image.size, (0, 0, 0, 0))
    
    if image.mode == 'RGBA':
        result.paste(image, (0, 0))
    else:
        result.paste(image.convert('RGBA'), (0, 0))
    
    alpha = Image.new('L', image.size, 255)
    w, h = image.size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))

    result.putalpha(alpha)
    return result

time_start = perf_counter()
image = Image.open('aa.jpg')
load_end = perf_counter() - time_start
print(f'Image loaded in {load_end} seconds')


rounded_image = add_rounded_corners(image, 100)
rounded_image.save('rounded_image.png')

end = perf_counter() - time_start

print(f'Image processed in {end} seconds')