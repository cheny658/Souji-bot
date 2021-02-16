from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
import numpy as np

ping_cmd = on_command('ping')
roll_cmd = on_command('roll')

@ping_cmd.handle()
async def get_ping_info(bot: Bot, event: Event, stat: dict):
    ret_msg = 'pong'
    await bot.send(message=ret_msg, event=event)

@roll_cmd.handle()
async def get_roll_pts(bot: Bot, event: Event, stat: dict):
    event_msg = str(event.message)
    if event_msg == '':
        await bot.send(message='请参照!roll x y的形式(x≤y|y≤x, x∈N, y∈N)如: !roll 0 100', event=event)
        return
    box = event_msg.split()
    flag = False
    if len(box) != 2:
        flag = True
    elif box[0].isdigit() == False or box[1].isdigit() == False:
        flag = True
    if flag:
        await bot.send(message='无效参数，请给定随机数区间如: !roll 0 100', event=event)
        return
    left = min(int(box[0]), int(box[1]))
    right = max(int(box[0]), int(box[1]))
    ret_msg = str(np.random.randint(left, right + 1))
    await bot.send(message=ret_msg, event=event)