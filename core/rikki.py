import requests
import json
import yaml


'''
Rikki.py · send
处理「satori」协议的信息发送 / API上报
'''

config = yaml.safe_load(open('./config.yml', encoding='utf-8'))


class Rikki:
    @staticmethod
    def send_request(method: str, data: dict, platform: str, self_id: str):
        """
        发送消息到指定频道。

        Parameters:
        method (str): API方法。
        data (dict): 消息内容。
        platform (str): 平台名称。
        self_id (str): 平台账号。

        Returns:
        dict: 包含消息信息的字典，如果发送失败则返回None。
        """

        # 遍历连接配置
        for connection in config["connections"]:
            if self_id in connection["self_ids"]:
                this_connection = connection
                break
        else:
            # 如果未找到匹配的连接配置
            print(f"未找到 self_id 为 {self_id} 的连接配置")
            return None

        # API endpoint
        address = this_connection['address']
        token = this_connection['token']
        http_protocol = this_connection.get('http_protocol', 'http')
        full_address = f'{http_protocol}://{address}/{method}'  # 替换为实际API endpoint

        # 构建请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
            'X-Platform': platform,
            'X-Self-ID': self_id
        }

        # 发送POST请求
        response = requests.post(full_address, data=json.dumps(data), headers=headers, verify=True)

        # 检查响应
        if response.status_code == 200:
            # 解析响应为JSON格式
            response_data = response.json()
            return response_data
        elif response.status_code == 413:
            print('Status code:', response.status_code)
            data_413 = {'channel_id': data["channel_id"], 'content': '55，资源过大，不太好发的说'}
            response2 = requests.post(full_address, data=json.dumps(data_413), headers=headers, verify=True)
            print(response2.status_code)
        else:
            print('Status code:', response.status_code)
            return None


class Bot:
    @staticmethod
    def send(message_content, platform, channel_id, self_id):
        return Rikki.send_request(method='message.create', data={
                'channel_id': channel_id,
                'content': message_content
            }, platform=platform, self_id=self_id)

    @staticmethod
    def call_api(method, data, platform, self_id):
        return Rikki.send_request(method=method, data=data, platform=platform, self_id=self_id)


bot = Bot()





