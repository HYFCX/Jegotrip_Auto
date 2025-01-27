import requests
import pprint
import os


class JegoTrip():
    user_id: str

    def __init__(self, user_id):
        self.user_id = user_id

    def task(self):
        resp = requests.get(f'https://app.jegotrip.com.cn/api/service/v1/mission/sign/userSign?token=={self.user_id}')
        data = resp.json()
        # pprint.pprint(data)
        return data['rtn']['tasks']

    def sign(self, task_id) -> bool:
        resp = requests.post('https://app.jegotrip.com.cn/api/service/v1/mission/sign',
                             json={
                                 'userid': self.user_id,
                                 'taskId': task_id    # 此处`I`要大写
                             },
                             headers={
                                 'Accept-Encoding': 'gzip, deflate, br',
                                 'Origin': ' https://cdn.jegotrip.com.cn',
                                 'Content-Type': 'application/json',
                                 'Connection': 'keep-alive',
                                 'Host': 'app.jegotrip.com.cn',
                                 'Content-Length': '112',
                                 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip',
                                 'Accept-Language': 'zh-cn',
                                 'Referer': 'https://cdn.jegotrip.com.cn/static/missioncenter/index.html'
                             })

        data = resp.json()
        # pprint.pprint(data)
        return data['result']

    def verify_result(self):
        tasks = self.task()
        for task in tasks.get('日常任务', []):
            if task.get('name') == '每日签到奖励':
                return True if task.get('triggerAction') == '已签到' else False


def main():
    _user_id = os.getenv('USERID')
    cli = JegoTrip(_user_id)
    for task in cli.task().get('日常任务', []):
        if task.get('name') == '每日签到奖励':
            if task.get('triggerAction') == '签到':
                result = cli.sign(task['id'])
                if result:
                    print('签到成功' if cli.verify_result() else '签到失败:未知')

            elif task.get('triggerAction') == '已签到':
                print('签到失败:今日已签到‼️')


if __name__ == '__main__':
    main()
