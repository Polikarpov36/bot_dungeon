import vk_api.vk_api
from random import randint
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from threading import Thread

list_of_users = []

class Server:
    def __init__(self, api_token, group_id, server_name: str = 'Empty'):
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token)
        self.long_pool = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()

    def send_msg_keyboard(self, send_id, message, process):
        self.vk_api.messages.send(peer_id=send_id, message=message,
                                  random_id=randint(600000000 ** 2, 777777777777777 ** 2),
                                  keyboard=open('keyboard.json', 'r', encoding='UTF-8').read())
        for el in self.long_pool.listen():
            if el.type == VkBotEventType.MESSAGE_NEW:
                if el.object.from_id != send_id and el.object.from_id not in list_of_users:
                    Thread(target=process, args=(el.object.from_id,)).start()
                    list_of_users.append(el.object.from_id)
                    pass
                if el.object.from_id == send_id:
                    return el.object.text

    def send_msg(self, send_id, message):
        self.vk_api.messages.send(peer_id=send_id, message=message, random_id=randint(600000000573478563856 ** 2, 37777777777777779999999999999999999 ** 2))

    def vk_mes(self, send_id, message, process):
        global list_of_users
        self.send_msg(send_id, message)
        for el in self.long_pool.listen():
            if el.type == VkBotEventType.MESSAGE_NEW:
                if el.object.from_id != send_id and el.object.from_id not in list_of_users:
                    Thread(target=process, args=(el.object.from_id,)).start()
                    list_of_users.append(el.object.from_id)
                    continue
                if send_id == el.object.from_id:
                    return el.object.text

    def test(self):
        self.send_msg(457063923, 'Приветик')

    def start(self):
        for event in self.long_pool.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object.from_id not in list_of_users:
                    list_of_users.append(event.object.from_id)
                    return event.object.from_id


