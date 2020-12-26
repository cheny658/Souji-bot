import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

def bot_init():
    nonebot.init()
    driver = nonebot.get_driver()
    driver.register_adapter("cqhttp", CQHTTPBot)

    # loading plugins
    nonebot.load_builtin_plugins()
    nonebot.get_asgi()

if __name__ == "__main__":
    # init
    bot_init()


    # start
    nonebot.run()
