import platform
from PIL import Image, ImageFont, ImageDraw

R = 255
G = 255
B = 255

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
        font = './msyh.ttc'
    elif platform.system().lower() == 'linux':
        font = '/usr/share/fonts/truetype/windows_font/msyh.ttc'
    draw.text((10, 10), text, font=ImageFont.truetype(font, 50, encoding='utf-8'), fill='#000000', direction=None)
    return img

def img_splice(info_box):
    sz = len(info_box)
    ret = getOriginImage(sz)
    for i in range(0, sz):
        ret.paste(draw(info_box[i]), (0, 70 * i, 2160, 70 * (i + 1)))
    return ret
