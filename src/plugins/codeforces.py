import requests
import json
import time
import sys
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
sys.path.append('./plugins')
from image_processor import img_splice


user_info_cmd = on_command('info')
@user_info_cmd.handle()
async def get_user_info(bot: Bot, event: Event, state: dict):
    cur_time = time.time()

    # Parse url, then get json_object
    name = str(event.message)
    if name == '':
        await bot.send(message='输入想要查的人吧，如!info tourist', event=event)
        return

    url = 'http://codeforces.com/api/user.info?handles=' + name
    try:
        info_result = requests.get(url)
    except requests.exceptions.ConnectionError:
        await bot.send(message='访问api失败，重试一下吧', event=event)
        return

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
                await bot.send(message='访问api失败，重试一下吧', event=event)
                return

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
        save_path = '../local_server/go-cqhttp/data/images/' + file_name
        ret_img.save(save_path)
        ret_msg = '[CQ:image,file=' + file_name + ']'
        await bot.send(message=ret_msg, event=event)

    else:
        # Can't find
        await bot.send(message='没这个人！', event=event)


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
            break
        info_box.append('比赛: ' + item['name'])
        info_box.append('时长: ' + str(round(item['durationSeconds'] / 3600, 1)) + 'h')
        info_box.append('Contest ID: ' + str(item['id']))

    ret_img = img_splice(info_box)
    file_name = 'contest.png'
    save_path = '../local_server/go-cqhttp/data/images/' + file_name
    ret_img.save(save_path)
    ret_msg = '[CQ:image,file=' + file_name + ']'

    await bot.send(message=ret_msg, event=event)