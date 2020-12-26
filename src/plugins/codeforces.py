from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event


nnhr = on_command("考研运势")

@nnhr.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    print(event.message)
    ret_msg = "你说的这个东西，爷不知道"
    if (str(event.message) == "622"):
        ret_msg = "一\'研\'为定！"
    elif (str(event.message) == "616"):
        ret_msg = "啊这，这么悲伤的事情，不忍心说啊。"
    elif (str(event.message) == "纯爱战士"):
        ret_msg = "纯爱战士一次上岸"
    elif (str(event.message) == "牛头人"):
        ret_msg = "牛头人biss"
    await bot.send(message=ret_msg, event=event)