import time

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint

fileApi = open("token.api", "r")
tokenVK = fileApi.read()
print(tokenVK)

vk_session = vk_api.VkApi(token=tokenVK)
vk_longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
upload = vk_api.VkUpload(vk_session)
# Добавить все картинки из папки где лежит файл с расширением py
images = ['images/1.jpg', 'images/2.jpg', 'images/3.jpg', 'images/4.jpg', 'images/5.jpg', 'images/6.jpg', 'images/7.jpg', 'images/8.jpg', 'images/9.jpg', 'images/10.jpg']
# Создать пустой список для данных о картинках
data = []
# Организовать цикл для всех картинок из списка
for image in images:
    # Получить url для каждой картинки
    url = upload.photo_messages(photos=image)[0]
    # И добавить его к списку для данных
    data.append(f'photo{url["owner_id"]}_{url["id"]}')

phrases = [
    'Сорванный цветок должен быть подарен, начатое стихотворение — дописано, а любимая женщина — счастлива, иначе и не стоило браться за то, что тебе не по силам.',
    'Слушай, что говорит твой враг, потому что только он знает все твои ошибки.',
    'Мы живем в мире, которым управляет вера. Во что вы поверите, то и сработает.',
    'Вокзал видел больше искренних поцелуев, чем загс. А стены больницы слышали больше искренних слов, чем церковь.',
    'Жизнь не обязана давать нам то, чего мы ждём. Надо брать то, что она даёт, и быть благодарным уже за то, что это так, а не хуже.',
    'Самая большая человеческая глупость — боязнь. Боязнь совершить поступок, поговорить, признаться. Мы всегда боимся, и потому так часто проигрываем.',
    'И запомни: никогда ничего не добьешься, пока не научишься определять, что для тебя в данный момент самое главное. - Роберт Хайнлайн.',
    'В любимом человеке нравятся даже недостатки, а в нелюбимом раздражают даже достоинства.',
    'К вам притягивается и от вас исходит только то, что соответствует вашему внутреннему состоянию. - Экхарт Толле.',
    'Иногда стоит совершить ошибку, хотя бы ради того, чтобы знать почему ее не следовало совершать.',
    'Я не боюсь того, кто изучает 10,000 различных ударов. Я боюсь того, кто изучает один удар 10,000 раз.',
    'Мерзко, когда в словах человека — высокие убеждения, а в действиях — низкие поступки.',
    'Некоторые полагают, что ты становишься сильнее держась за что-то, но сильнее становишься только отпустив.',
    'Все всегда заканчивается хорошо. Если все закончилось плохо, значит это еще не конец!',
    'Принимайте все так, как приходит. Даже если ничего не приходит — все равно принимайте.',
    'Всё идет своим чередом. Не торопись, будь спокоен: жизнь мудрее нас. Всё идёт так как должно идти.'

]

users = {}  # Словарь пользователей. id - remember

halloweenState = {}  # Храним состояние

whoIsPlaying = {}  # Храним пользователей, которые играют

while True:
    try:
        for event in vk_longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:

                    response = ''
                    if event.user_id in whoIsPlaying:
                        if 'стоп' in event.text.lower():
                            response = 'Ладно закончили. Число было = ' + str(whoIsPlaying[event.user_id])
                            del whoIsPlaying[event.user_id]
                        else:
                            try:
                                num = int(event.text)
                                remNum = whoIsPlaying[event.user_id]
                                if num == remNum:
                                    response = 'Ты угадал! Супер!'
                                    del whoIsPlaying[event.user_id]
                                else:
                                    response = 'Нет, не оно.'
                            except ValueError:
                                response = 'Не похоже на число. Пробуй еще'

                        vk.messages.send(user_id=event.user_id, random_id=randint(0, 2 ** 32), message=response)
                        continue  # возвращает в начало for
                    else:

                        if 'привет' in event.text.lower():
                            response = 'И тебе привет!'
                        elif event.text.lower() == 'как дела?':
                            response = 'Я умею присылать картинки. Пиши "Картинка" или "мысль"'
                        elif 'картинка' in event.text.lower() or 'хэллоуин' in event.text.lower() or 'хэлоуин' in event.text.lower() or 'хэлоин' in event.text.lower() or 'хэлуин' in event.text.lower() or 'халлоуин' in event.text.lower():
                            halloweenState[event.user_id] = True
                            response = 'Сладость или гадость?'
                        elif 'сладость' in event.text.lower():
                            if event.user_id in halloweenState:
                                response = 'Держи'  # картинка
                                vk.messages.send(user_id=event.user_id, random_id=randint(0, 2 ** 32),
                                                 attachment=data[randint(0, 4)])
                                del halloweenState[event.user_id]
                            else:
                                response = 'Ты о чем это?'
                        elif 'гадость' in event.text.lower():
                            if event.user_id in halloweenState:
                                response = 'Держи'  # картинка
                                vk.messages.send(user_id=event.user_id, random_id=randint(0, 2 ** 32),
                                                 attachment=data[randint(5, len(data) - 1)])
                                del halloweenState[event.user_id]
                            else:
                                response = 'Ты о чем это?'
                        elif 'мысль' in event.text.lower():
                            response = phrases[randint(0, len(phrases) - 1)]
                        elif 'запомни' in event.text.lower():
                            if event.user_id in users:
                                rembr = users[event.user_id]
                                rembr.append(event.text[7:])
                            else:
                                rembr = []
                                rembr.append(event.text[7:])
                                users[event.user_id] = rembr
                            response = 'Запомнил!'
                        elif 'что нового' in event.text.lower() or 'напомни' in event.text.lower():
                            if event.user_id in users:
                                rembr = users[event.user_id]
                                if len(rembr) > 0:
                                    i = 1
                                    for r in rembr:
                                        response = response + str(i) + ") " + r + '\n'
                                        i = i + 1
                                else:
                                    response = 'Я еще ничего не запоминал.'
                            else:
                                response = 'Ничего не помню :('
                        elif 'забудь' in event.text.lower():
                            try:
                                num = int(event.text[7:])
                                if event.user_id in users:
                                    rembr = users[event.user_id]
                                    if len(rembr) >= num:
                                        del rembr[num - 1]
                                        response = 'Забыл :('
                                    else:
                                        response = 'Я такого не помню.'
                                else:
                                    response = 'Я еще ничего не запоминал.'
                            except ValueError:
                                response = 'Такое я не забуду!'
                        elif 'игра' in event.text.lower():
                            response = 'Я загадал цифру от 1 до 10. Угадаешь? Пиши стоп, если не сможешь.'
                            whoIsPlaying[event.user_id] = randint(0, 10)
                        else:
                            response = 'Не поняяятно. \n' \
                                       'Я понимаю такие команды:\n' \
                                       '1) Привет\n' \
                                       '2) Картинка\n' \
                                       '3) Мысль\n' \
                                       '4) Запомни <текст>\n' \
                                       '5) Напомни\n' \
                                       '6) Забудь <номер строки>\n' \
                                       '7) Хэллоуин\n' \
                                       '8) Игра'

                    vk.messages.send(user_id=event.user_id, random_id=randint(0, 2 ** 32), message=response)

                    print(f'Получено сообщение {event.text} от {event.user_id}')
    except:
        print("read timeout")
        time.sleep(60 * 5)
