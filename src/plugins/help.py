from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from image_processor import img_splice

help_cmd = on_command('help')
@help_cmd.handle()
async def get_help(bot: Bot, event: Event, stat: dict):
    info_box = []
    info_box.append('总司bot是一个用于查询codeforces信息的机器人')
    info_box.append('!info: 查询个人信息')
    info_box.append('!ct: 查询近期比赛')
    info_box.append('!sup: 打钱')
    info_box.append('!roll: 随机数功能')
    info_box.append('新功能绝赞开发中...')

    ret_img = img_splice(info_box)
    file_name = 'help.png'
    save_path = '../local_server/go-cqhttp/data/images/' + file_name
    ret_img.save(save_path)
    ret_msg = '[CQ:image,file=' + file_name + ']'
    await bot.send(message=ret_msg, event=event)