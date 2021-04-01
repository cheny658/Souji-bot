from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event

cnm_cmd = on_command('cnm')
@cnm_cmd.handle()
async def cnm_voice(bot: Bot, event: Event, stat: dict):
    ret_msg = '[CQ:record,file=cnm.mp3]'
    await bot.send(message=ret_msg, event=event)