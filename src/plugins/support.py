from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event

sup_cmd = on_command('sup')
@sup_cmd.handle()
async def get_sup(bot: Bot, event: Event, stat: dict):
    ret_msg = '[CQ:image,file=sup.png]'
    await bot.send(message=ret_msg, event=event)
    ret_msg = '[CQ:record,file=thx.png]'
    await bot.send(message=ret_msg, event=event