from PIL import Image, ImageFont, ImageDraw

def getOriginImage(rows):
    ret = Image.new(mode='RGBA', size=(1080, 70 * rows), color=(255, 255, 255))
    return ret

def draw(text):
    img = Image.new(mode='RGBA', size=(1080, 70), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text, font=ImageFont.truetype('./simsun.ttc', 50), fill='#000000', direction=None)
    return img

def img_splice(info_box):
    sz = len(info_box)
    ret = getOriginImage(sz)
    for i in range(0, sz):
        ret.paste(draw(info_box[i]), (0, 70 * i, 1080, 70 * (i + 1)))
    return ret