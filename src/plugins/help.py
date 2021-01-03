from nonebot import on_command
from nonebot.rule import regex
from nonebot.adapters.cqhttp import Bot, Event

help_cmd = on_command('help')
@help_cmd.handle()
async def get_help(bot: Bot, event: Event, stat: dict):
    ret_msg = '总司bot是一个用于查询codeforces信息的机器人\n\n'
    ret_msg += 'info: 查询个人信息\n'
    ret_msg += 'ct: 查询近期比赛\n'

    ret_msg += '\n新功能绝赞开发中...'
    await bot.send(message=ret_msg, event=event)