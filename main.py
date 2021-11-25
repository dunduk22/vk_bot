import vk_api
import secret_constants
from vk_api.longpoll import VkLongPoll, VkEventType

from cities import Cities
from correct_cities import correct_cities

vk_session = vk_api.VkApi(token=secret_constants.TOKEN)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

players_in_game = []
active_games = []


def is_correct_event(event):
    return event.to_me and event.type == VkEventType.MESSAGE_NEW


def send_message(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id,
                                        'message': message,
                                        'random_id': 0})

def is_play_game(event):
    game_command = ['начали','lets go','города']
    return event.text.lower() in game_command

def kill_game(game):
    user_ids = game
    active_games.pop(active_games.index(game))
    players_in_game.remove(user_ids[0])
    players_in_game.remove(user_ids[1])

def main():
    for event in longpoll.listen():
        if is_correct_event(event):
            if event.text == 'hi':
                send_message(event.user_id, 'Hi friend!')


def main():
    user_in_queue = None
    for event in longpoll.listen():
        if is_correct_event(event):
            if event.text == 'hi':
                send_message(event.user_id, 'Hi friend!')
            elif is_play_game(event):
                if user_in_queue is None:
                    send_message(event.user_id, 'Мы нашли вам оппонента')
                    send_message(event.user_id, 'Оппонент ожидает вас')
                    active_games.append(Cities(user_in_queue, event.user_id))
                    players_in_game.append(user_in_queue)
                    players_in_game.append(event.user_id)
                    first_user = active_games[-1].user_ids[active_games[-1].courrent_step]
                    send_message(first_user, 'Вы ходите первый! Назовите город на любую букву.')
                    user_in_queue = None
            elif event.user_id in players_in_game:
                bad = False
                igra=''
                for game in active_games:
                    if event.user_id in game.user_ids:
                        if game.user_ids.index(event.user_id) != game.current_step:
                            bad = True
                            break
                        else:
                            igra = game
                    if bad:
                        send_message(event.user_id, 'Сейчас не ваш ход!')
                        continue
                    user1 = event.user_id
                    user2 = igra.user_ids[1 - igra.current_step]
                    if not igra.is_correct_first_char(event.text(0).upper()):
                        send_message(user1, 'Вы назвали город не на ту букву и проиграли! Игра окончена!')
                        send_message(user2, 'Вы победили!')
                        kill_game(igra)
                        continue
                    city = event.text.capitalize()
                    if city not in correct_cities:
                        send_message(user1, 'Такого города нет в нашем списке городов!')
                        send_message(user2, 'Вы победили!')
                        kill_game(igra)
                        continue
                    if igra.is_unused_city(city):
                        send_message(user1, 'Такой город уже назывался. Увы, вы проиграли!')
                        send_message(user2, 'Вы победили!')
                        kill_game(igra)
                        continue
                    igra.used_cities.append(city)
                    igra.change_last_char(city)
                    igra.change_last_char(city)
                    send_message(user2, "Ваш ход! Оппонент назвал город: " + city + '. \nBan Ha бykвy: ')


