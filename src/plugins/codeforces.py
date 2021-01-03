import requests
import json
import time
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event


user_info_cmd = on_command('info')
@user_info_cmd.handle()
async def get_user_info(bot: Bot, event: Event, state: dict):
    cur_time = time.time()

    # Parse url, then get json_object
    name = str(event.message)
    if name == '':
        await bot.send(message='输入想要查的人吧，如/info tourist', event=event)
        return

    url = 'http://codeforces.com/api/user.info?handles=' + name
    try:
        info_result = requests.get(url)
    except requests.exceptions.ConnectionError:
        await bot.send(message='访问api失败，重试一下吧', event=event)
        return

    json_obj = json.loads(info_result.text)

    # Structure information
    if str(json_obj['status']) == 'OK':
        user_info = json_obj['result'][0]
        ret_msg = user_info['handle'] + '的codeforces信息:\n\n'

        # Process rating and rank
        if 'rating' in user_info:
            user_rating = str(user_info['rating'])
            user_rank = str(user_info['rank'])
            user_max_rating = str(user_info['maxRating'])
            user_max_rank = str(user_info['maxRank'])
            ret_msg += 'rating: ' + user_rating + '\n'
            ret_msg += 'rank: ' + user_rank + '\n'
            ret_msg += 'max rating: ' + user_max_rating + '\n'
            ret_msg += 'max rank: ' + user_max_rank + '\n'

            # Process the latest rating changing info
            url = 'http://codeforces.com/api/user.rating?handle=' + name
            try:
                rating_changing_result = requests.get(url)
            except requests.exceptions.ConnectionError:
                await bot.send(message='访问api失败，重试一下吧', event=event)
                return

            latest_rating_json_obj = json.loads(rating_changing_result.text)
            latest_rating_info = latest_rating_json_obj['result'][-1]
            ret_msg += '最近一次在 ' + latest_rating_info['contestName'] + ' 位居第'
            ret_msg += str(latest_rating_info['rank']) + '名\n'
            ret_msg += 'rating变动: ' + \
                       str(latest_rating_info['oldRating']) + ' -> ' + \
                       str(latest_rating_info['newRating']) + '\n'
            ret_msg += '比赛传送门: http://codeforces.com/contest/' + str(latest_rating_info['contestId']) + '\n'

        else:
            ret_msg += '这家伙好懒，还没打过比赛呢！\n'

        # Process register time
        register_time = float(user_info['registrationTimeSeconds'])
        time_span = (cur_time - register_time) / (86400.0 * 365.0)
        time_span = round(time_span, 1)
        ret_msg += 'Ta是一位练习时长' + str(time_span) + '年的算法竞赛生\n'

    else:
        # Can't find
        ret_msg = '没这个人！'

    # Send message
    if ret_msg[-1] == '\n':
        ret_msg = ret_msg[0: -1]
    await bot.send(message=ret_msg, event=event)


contest_info_cmd = on_command('ct')
@contest_info_cmd.handle()
async def get_contest_info(bot: Bot, event:Event, state: dict):
    url = 'https://codeforces.com/api/contest.list?gym=false'
    try:
        contest_result = requests.get(url)
    except requests.exceptions.ConnectionError:
        await bot.send(message='访问api失败，重试一下吧', event=event)
        return
    contest_json = json.loads(contest_result.text)
    ret_msg = '近期的比赛: \n'
    contests_url = 'https://codeforces.com/contests/'
    for item in contest_json['result']:
        if item['phase'] == 'FINISHED':
            break
        ret_msg += '比赛: ' + item['name'] + '\n'
        ret_msg += '时长: ' + str(round(item['durationSeconds'] / 3600, 1)) + 'h\n'
        ret_msg += '地址: ' + contests_url + str(item['id']) + '\n\n'

    if ret_msg[-1] == '\n':
        ret_msg = ret_msg[0: -1]
    await bot.send(message=ret_msg, event=event)