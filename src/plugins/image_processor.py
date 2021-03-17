import platform
from PIL import Image, ImageFont, ImageDraw

R = 255
G = 255
B = 255

# 指定要使用的字体和大小；/Library/Fonts/是macOS字体目录；Linux的字体目录是/usr/share/fonts/
def getOriginImage(rows):
    ret = Image.new(mode='RGBA', size=(2160, 70 * rows), color=(R, G, B))
    return ret

def img_save(img: Image, file_name):
    save_path = '../../go-cqhttp/data/images/' + file_name
    img.save(save_path)

def draw(text):
    img = Image.new(mode='RGBA', size=(2160, 70), color=(R, G, B))
    draw = ImageDraw.Draw(img)
    if platform.system().lower() == 'windows':
        font = './simsun.ttc'
    elif platform.system().lower() == 'linux':
        font = './DejaVuSansMono-Bold.ttf'
    draw.text((10, 10), text, font=ImageFont.truetype(font, 50), fill='#000000', direction=None)
    return img

def img_splice(info_box):
    sz = len(info_box)
    ret = getOriginImage(sz)
    for i in range(0, sz):
        ret.paste(draw(info_box[i]), (0, 70 * i, 2160, 70 * (i + 1)))
    return ret