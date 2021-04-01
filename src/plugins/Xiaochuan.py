from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event

cnm_cmd = on_command('cnm')
@cnm_cmd.handle()
async def cnm_voice(bot: Bot, event: Event, stat: dict):
    ret_msg = '[CQ:record,file=cnm.mp3]'
    await bot.send(message=ret_msg, event=event)

sleep_cmd = on_command('sleep')
@sleep_cmd.handle()
async def sleep_voice(bot: Bot, event: Event, stat: dict):
    ret_msg = '[CQ:record,file=sleep.mp3]'
    await bot.send(message=ret_msg, event=event)

study_cmd = on_command('study')
@study_cmd.handle()
async def study_voice(bot: Bot, event: Event, stat: dict):
    ret_msg = '[CQ:record,file=study.mp3]'
    await bot.send(message=ret_msg, event=event)