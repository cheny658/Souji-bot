from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from image_processor import img_splice, img_save

help_cmd = on_command('help')
@help_cmd.handle()
async def get_help(bot: Bot, event: Event, stat: dict):
    info_box = []
    info_box.append('总司bot是一个用于查询codeforces信息的机器人')
    info_box.append('!info: 查询选手信息')
    info_box.append('!setid: 绑定指令')
    info_box.append('!unset: 解除绑定')
    info_box.append('!infome: 查询绑定账号的信息')
    info_box.append('!ct: 查询未来的比赛信息')
    info_box.append('!sup: 打钱')
    info_box.append('!roll: 随机数指令')
    info_box.append('!ping: 网络测试指令')

    info_box.append('新功能绝赞开发中...')

    ret_img = img_splice(info_box)
    file_name = 'help.png'
    img_save(ret_img, file_name)
    ret_msg = '[CQ:image,file=' + file_name + ']'
    await bot.send(message=ret_msg, event=event)