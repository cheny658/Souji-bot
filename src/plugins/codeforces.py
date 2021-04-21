import requests
import json
import time
import sys
import pymysql
import datetime
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
sys.path.append('./plugins')
from image_processor import img_splice, img_save


def user_info_processor(event: Event):
    cur_time = time.time()

    # Parse url, then get json_object
    name = str(event.message)
    if name == '':
        ret_msg = '输入想要查的人吧，如!info tourist'
        return ret_msg

    url = 'http://codeforces.com/api/user.info?handles=' + name
    try:
        info_result = requests.get(url)
    except requests.exceptions.ConnectionError:
        ret_msg = '访问api失败，重试一下吧'
        return ret_msg

    info_box = []
    json_obj = json.loads(info_result.text)
    # Structure information
    if str(json_obj['status']) == 'OK':
        user_info = json_obj['result'][0]
        info_box.append(user_info['handle'] + '的codeforces信息:')

        # Process rating and rank
        if 'rating' in user_info:
            user_rating = str(user_info['rating'])
            user_rank = str(user_info['rank'])
            user_max_rating = str(user_info['maxRating'])
            user_max_rank = str(user_info['maxRank'])
            info_box.append('rating: ' + user_rating)
            info_box.append('rank: ' + user_rank)
            info_box.append('max rating: ' + user_max_rating)
            info_box.append('max rank: ' + user_max_rank)

            # Process the latest rating changing info
            url = 'http://codeforces.com/api/user.rating?handle=' + name
            try:
                rating_changing_result = requests.get(url)
            except requests.exceptions.ConnectionError:
                ret_msg = '访问api失败，重试一下吧'
                return ret_msg

            latest_rating_json_obj = json.loads(rating_changing_result.text)
            latest_rating_info = latest_rating_json_obj['result'][-1]
            info_box.append('最近一次在:')
            info_box.append(latest_rating_info['contestName'])
            info_box.append('位居第' + str(latest_rating_info['rank']) + '名')
            info_box.append('rating变动: ' +
                            str(latest_rating_info['oldRating']) + ' -> ' +
                            str(latest_rating_info['newRating']))

        else:
            info_box.clear()
            info_box.append('这家伙好懒，还没打过比赛呢！')

        # Process register time
        register_time = float(user_info['registrationTimeSeconds'])
        time_span = (cur_time - register_time) / (86400.0 * 365.0)
        time_span = round(time_span, 1)
        info_box.append(' ')
        info_box.append('Ta是一位练习时长' + str(time_span) + '年的算法竞赛生')

        ret_img = img_splice(info_box)
        file_name = user_info['handle'] + '_user_info.png'
        img_save(ret_img, file_name)
        ret_msg = '[CQ:image,file=' + file_name + ']'
        return ret_msg
    else:
        # Can't find
        ret_msg = '没这个人！'
        return ret_msg


user_info_cmd = on_command('info')
@user_info_cmd.handle()
async def get_user_info(bot: Bot, event: Event, state: dict):
    ret_msg = user_info_processor(event)
    await bot.send(message=ret_msg, event=event)


infome_cmd = on_command('infome')
@infome_cmd.handle()
async def get_myinfo(bot: Bot, event: Event, state: dict):
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
        ret_msg = ret_msg + '尚未绑定，请使用setid指令绑定Codeforces账号'
        await bot.send(message=ret_msg, event=event)
    else:
        event.message = result[0][1]
        ret_msg = user_info_processor(event)
        await bot.send(message=ret_msg, event=event)


contest_info_cmd = on_command('ct')
@contest_info_cmd.handle()
async def get_contest_info(bot: Bot, event: Event, state: dict):
    url = 'https://codeforces.com/api/contest.list?gym=false'
    try:
        contest_result = requests.get(url)
    except requests.exceptions.ConnectionError:
        await bot.send(message='访问api失败，重试一下吧', event=event)
        return
    contest_json = json.loads(contest_result.text)
    info_box = ['近期的比赛: \n']
    for item in contest_json['result']:
        if item['phase'] == 'FINISHED':
            info_box.pop()
            break
        info_box.append('比赛: ' + item['name'])
        info_box.append('日期: ' + str(datetime.datetime.fromtimestamp(item['startTimeSeconds'])))
        durationSeconds = item['durationSeconds']
        hours = durationSeconds // 3600
        minutes = (durationSeconds - hours * 3600) // 60
        info_box.append('时长: ' + str(hours) + 'h' + str(minutes) + 'min')
        info_box.append('Contest ID: ' + str(item['id']))
        info_box.append(' ')

    ret_img = img_splice(info_box)
    file_name = 'contest.png'
    img_save(ret_img, file_name)
    ret_msg = '[CQ:image,file=' + file_name + ']'

    await bot.send(message=ret_msg, event=event)