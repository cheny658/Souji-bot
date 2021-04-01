from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event

help_cmd = on_command('help')
@help_cmd.handle()
async def get_help(bot: Bot, event: Event, stat: dict):
    ret_msg = '[CQ:image,file=bot-help.png]'
    await bot.send(message=ret_msg, event=event)

