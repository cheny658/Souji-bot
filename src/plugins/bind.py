import pymysql
import requests
import json
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event

setid_cmd = on_command('setid')
@setid_cmd.handle()
async def set_id(bot: Bot, event: Event, state: dict):
    qq_id = str(event.user_id)
    db = pymysql.connect(host='localhost', user="botdb_root", password="Mynameischeny658", database='botdb')
    cursor = db.cursor()
    sql_check = "SELECT * FROM bot_users_tbl WHERE qq_id = '%s'" % qq_id
    cursor.execute(sql_check)
    result = cursor.fetchall()
    if len(result) == 0:
        url = 'http://codeforces.com/api/user.info?handles=' + str(event.message)
        try:
            info_result = requests.get(url)
        except requests.exceptions.ConnectionError:
            await bot.send(message='访问api失败，重试一下吧', event=event)
            return

        json_obj = json.loads(info_result.text)
        if str(json_obj['status']) != 'OK':
            ret_msg = ''
            if event.detail_type == 'group':
                ret_msg = '[CQ:at,qq=%s]' % qq_id
            ret_msg = ret_msg + '绑定失败，无效的Codeforces账号'
            await bot.send(message=ret_msg, event=event)
            return
        name = json_obj['result'][0]['handle']
        sql_insert = "INSERT INTO bot_users_tbl(qq_id, cf_id) values ('%s'" % qq_id + ", '%s')" % name
        cursor.execute(sql_insert)
        db.commit()
        ret_msg = ''
        if event.detail_type == 'group':
            ret_msg = '[CQ:at,qq=%s]' % qq_id
        ret_msg = ret_msg + '绑定成功！'
        await bot.send(message=ret_msg, event=event)
    else:
        ret_msg = ''
        if event.detail_type == 'group':
            ret_msg = '[CQ:at,qq=%s]' % qq_id
        ret_msg = ret_msg + '已经绑定账号%s，如需更新请先使用unset指令解绑' % result[0][1]
        await bot.send(message=ret_msg, event=event)


unset_cmd = on_command('unset')
@unset_cmd.handle()
async def unset(bot: Bot, event: Event, state: dict):
    qq_id = str(event.user_id)
    db = pymysql.connect(host='localhost', user="botdb_root", password="Mynameischeny658", database='botdb')
    cursor = db.cursor()
    sql_check = "SELECT * FROM bot_users_tbl WHERE qq_id = '%s'" % qq_id
    cursor.execute(sql_check)
    result = cursor.fetchall()
    if len(result) == 0:
        ret_msg = ''
        if event.detail_type == 'group':
            ret_msg = '[CQ:at,qq=%s]' % qq_id
        ret_msg = ret_msg + '暂未绑定，无需解绑'
        await bot.send(message=ret_msg, event=event)
    else:
        sql_delete = "DELETE FROM bot_users_tbl WHERE qq_id = '%s'" % qq_id
        cursor.execute(sql_delete)
        db.commit()
        ret_msg = ''
        if event.detail_type == 'group':
            ret_msg = '[CQ:at,qq=%s]' % qq_id
        ret_msg = ret_msg + '解绑成功！'
        await bot.send(message=ret_msg, event=event)
