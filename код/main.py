from tkinter import *
from tkinter import messagebox  # для отображения ошибок при входе / регистрации пользователя и другеи сообдщения
from random import choice, random
import re   # для проверки на соответствие почты
import datetime    # показ даты и времени
import os   # доступ к функциям операционной системы (работа с файлами)


# глобальные переменные для отслеживания состояния пользователя
current_user_id = None
current_username = None
user_is_logged_in = False


# ДЛЯ УПРАВЛЕНИЯ ДАННЫМИ

class UserManager:
    """Класс для управления пользователями и статистикой"""

    def __init__(self):
        self.USERS_DB = {}  # email: {username, password, gender, age, user_id}
        self.GAME_STATS = {}  # user_id: {username, total_games, wins, losses, draws}
        self.GAME_HISTORY = []  # список словарей с историей игр
        self.USER_ID_COUNTER = 1
        self.load_data()    # отображение даты и времени

    def load_data(self):
        """Загрузка данных из текстового файла"""
        try:
            # Проверка существования файла
            if not os.path.exists('game_data.txt'):
                print("Файл game_data.txt не найден, создается новый")  # сообщения сделаны для отладки в консоли
                return

            with open('game_data.txt', 'r', encoding='utf-8') as f:
                content = f.read()

            if not content:
                print("Файл game_data.txt пустой")
                return

            # обновление структур
            self.USERS_DB = {}
            self.GAME_STATS = {}
            self.GAME_HISTORY = []

            sections = content.split('\n\n')

            for section in sections:
                lines = section.strip().split('\n')
                if not lines:
                    continue

                if lines[0] == '[USERS]':   # после с пользователем
                    for line in lines[1:]:
                        if ':' in line:
                            email, data = line.split(':', 1)
                            try:
                                user_data = eval(data)
                                self.USERS_DB[email] = user_data
                                self.USER_ID_COUNTER = max(self.USER_ID_COUNTER, user_data.get('user_id', 0) + 1)
                            except:
                                continue

                elif lines[0] == '[STATS]':  # поле со статистикой
                    for line in lines[1:]:
                        if ':' in line:
                            user_id_str, data = line.split(':', 1)
                            try:
                                user_id = int(user_id_str)
                                self.GAME_STATS[user_id] = eval(data)
                            except:
                                continue

                elif lines[0] == '[HISTORY]':   # после с историей совершённых ходов и действий
                    for line in lines[1:]:
                        if line.startswith('{'):
                            try:
                                self.GAME_HISTORY.append(eval(line))
                            except:
                                continue

            print(f"Данные загружены: {len(self.USERS_DB)} пользователей, {len(self.GAME_STATS)} записей статистики")

        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            self.USERS_DB = {}
            self.GAME_STATS = {}
            self.GAME_HISTORY = []

    def save_data(self):
        """Сохранение данных в текстовый файл"""
        try:
            with open('game_data.txt', 'w', encoding='utf-8') as f: # открытие файла с контекстным менеджером
                # Сохранение пользователей
                f.write('[USERS]\n')
                for email, user_data in self.USERS_DB.items():
                    f.write(f'{email}:{user_data}\n')

                # Сохранение статистики
                f.write('\n[STATS]\n')
                for user_id, stats in self.GAME_STATS.items():
                    f.write(f'{user_id}:{stats}\n')

                # Сохранение истории
                f.write('\n[HISTORY]\n')
                for record in self.GAME_HISTORY:
                    f.write(f'{record}\n')

            print(f"Данные сохранены: {len(self.USERS_DB)} пользователей, {len(self.GAME_STATS)} записей статистики")
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

    def save_user_stats_to_file(self, user_id, username, rock_cnt, shear_cnt, paper_cnt, losses, wins, draws,
                                total_games):
        """Сохранение статистики пользователя в отдельный файл в отсортированном виде"""
        try:
            # Создаем словарь со статистикой
            user_stats = {
                "username": username,
                "statistics": {
                    "Поражений": losses,
                    "Побед": wins,
                    "Ничьих": draws,
                    "Камень": rock_cnt,
                    "Ножницы": shear_cnt,
                    "Бумага": paper_cnt,
                    "Всего игр": total_games
                }
            }

            # сохранение в файл с именем пользователя
            filename = f"stats_{username.replace(' ', '_')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                # Записываем в отсортированном виде
                f.write(f"Статистика пользователя: {username}\n")
                f.write("=" * 50 + "\n")

                # Статистика в нужном порядке
                f.write(f"Поражений: {losses}\n")
                f.write(f"Побед: {wins}\n")
                f.write(f"Ничьих: {draws}\n")
                f.write(f"Камень: {rock_cnt}\n")
                f.write(f"Ножницы: {shear_cnt}\n")
                f.write(f"Бумага: {paper_cnt}\n")
                f.write(f"Всего игр: {total_games}\n")

            print(f"Статистика пользователя сохранена в файл: {filename}")
            return filename
        except Exception as e:
            print(f"Ошибка сохранения статистики пользователя: {e}")
            return None

    def save_all_stats_to_file(self, all_stats_list):
        """Сохранение всей статистики в файл"""
        try:
            filename = "all_users_stats.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Общая статистика всех пользователей\n")
                f.write("=" * 50 + "\n")

                # обход по всем полям статистики и запись
                for idx, (user_id, username, total, wins, losses, draws) in enumerate(all_stats_list, 1):
                    f.write(f"\n{idx}. {username}:\n")
                    f.write(f"   Всего игр: {total}\n")
                    f.write(f"   Побед: {wins}\n")
                    f.write(f"   Поражений: {losses}\n")
                    f.write(f"   Ничьих: {draws}\n")
                    f.write(f"   Процент побед: {wins / total * 100:.1f}%\n" if total > 0 else "   Процент побед: 0%\n")

            print(f"Общая статистика сохранена в файл: {filename}")
            return filename
        except Exception as e:
            print(f"Ошибка сохранения общей статистики: {e}")
            return None

    def add_user(self, username, email, password, gender=None, age=None):
        """Добавление нового пользователя"""
        if email in self.USERS_DB:
            return False

        user_id = self.USER_ID_COUNTER
        self.USER_ID_COUNTER += 1

        self.USERS_DB[email] = {
            'username': username,
            'password': password,
            'gender': gender,
            'age': age,
            'user_id': user_id
        }

        self.GAME_STATS[user_id] = {
            'username': username,
            'total_games': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0
        }

        self.save_data()    # сохранение даты
        return True

    def check_user(self, email, password):
        """Проверка пользователя при входе"""
        if email in self.USERS_DB:
            user_data = self.USERS_DB[email]
            if user_data['password'] == password:
                return (user_data['user_id'], user_data['username'])
        return None

    def update_user(self, user_id, username=None, email=None, password=None, gender=None, age=None):
        """Обновление данных пользователя"""
        old_email = None
        for email_key, user_data in self.USERS_DB.items():
            if user_data['user_id'] == user_id:
                old_email = email_key
                break

        if not old_email:
            return False

        user_data = self.USERS_DB[old_email]

        if username:
            user_data['username'] = username
            if user_id in self.GAME_STATS:
                self.GAME_STATS[user_id]['username'] = username

        if password:
            user_data['password'] = password

        if gender:
            user_data['gender'] = gender

        if age is not None:
            user_data['age'] = age

        if email and email != old_email:
            if email in self.USERS_DB:
                return False

            self.USERS_DB[email] = user_data
            del self.USERS_DB[old_email]

        self.save_data()
        return True

    def save_game_result(self, user_id, player_move, bot_move, result):
        """Сохранение результата игры"""
        self.GAME_HISTORY.append({
            'user_id': user_id,
            'player_move': player_move,
            'bot_move': bot_move,
            'result': result,
            'timestamp': datetime.datetime.now().isoformat()
        })

        if user_id in self.GAME_STATS:
            stats = self.GAME_STATS[user_id]
            stats['total_games'] += 1

            if result == 'win':
                stats['wins'] += 1
            elif result == 'lose':
                stats['losses'] += 1
            else:
                stats['draws'] += 1

        self.save_data()

    def get_user_stats(self, user_id):
        """Получение статистики пользователя"""
        if user_id in self.GAME_STATS:
            stats = self.GAME_STATS[user_id]
            return (stats['total_games'], stats['wins'], stats['losses'], stats['draws'])
        return (0, 0, 0, 0)

    def get_all_stats_sorted(self):
        """Получение всей статистики, отсортированной по победам"""
        stats_list = []
        for user_id, stats in self.GAME_STATS.items():
            if stats['total_games'] > 0:  # только пользователи с играми
                stats_list.append((
                    user_id,
                    stats['username'],
                    stats['total_games'],
                    stats['wins'],
                    stats['losses'],
                    stats['draws']
                ))

        # Сортировка по победам (от большего к меньшему)
        stats_list.sort(key=lambda x: x[3], reverse=True)
        return stats_list

    def save_specific_user_stats_to_file(self, user_id):
        """Сохранение статистики конкретного пользователя в файл"""
        try:
            # Проверка наличия пользователя в статистике
            if user_id not in self.GAME_STATS:
                print(f"Пользователь с ID {user_id} не найден в статистике")
                return None

            # Получение данных пользователя
            stats = self.GAME_STATS[user_id]
            username = stats['username']

            # Поиск email пользователя
            user_email = None
            for email, user_data in self.USERS_DB.items():
                if user_data['user_id'] == user_id:
                    user_email = email
                    break

            # Создание имени файла
            filename = f"user_{user_id}_{username.replace(' ', '_')}_stats.txt"

            # Получение дополнительных данных пользователя
            user_data = None
            if user_email:
                user_data = self.USERS_DB.get(user_email)

            # Запись в файл
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"СТАТИСТИКА ПОЛЬЗОВАТЕЛЯ\n")
                f.write("=" * 50 + "\n")
                f.write(f"ID пользователя: {user_id}\n")
                f.write(f"Имя пользователя: {username}\n")

                if user_email:
                    f.write(f"Email: {user_email}\n")

                if user_data:
                    if user_data.get('gender'):
                        f.write(f"Пол: {user_data['gender']}\n")
                    if user_data.get('age') is not None:
                        f.write(f"Возраст: {user_data['age']}\n")

                f.write("=" * 50 + "\n")
                f.write(f"ИГРОВАЯ СТАТИСТИКА:\n")
                f.write(f"Всего игр: {stats['total_games']}\n")
                f.write(f"Побед: {stats['wins']}\n")
                f.write(f"Поражений: {stats['losses']}\n")
                f.write(f"Ничьих: {stats['draws']}\n")

                # Расчет процентов
                if stats['total_games'] > 0:
                    win_percentage = (stats['wins'] / stats['total_games']) * 100
                    loss_percentage = (stats['losses'] / stats['total_games']) * 100
                    draw_percentage = (stats['draws'] / stats['total_games']) * 100

                    f.write("=" * 50 + "\n")
                    f.write(f"ПРОЦЕНТНОЕ СООТНОШЕНИЕ:\n")
                    f.write(f"Процент побед: {win_percentage:.1f}%\n")
                    f.write(f"Процент поражений: {loss_percentage:.1f}%\n")
                    f.write(f"Процент ничьих: {draw_percentage:.1f}%\n")

                # Получение истории игр пользователя
                user_games = []
                for game in self.GAME_HISTORY:
                    if game['user_id'] == user_id:
                        user_games.append(game)

                if user_games:
                    f.write("=" * 50 + "\n")
                    f.write(f"ИСТОРИЯ ИГР (последние {min(20, len(user_games))} игр):\n")

                    # Сортировка по времени (новые сначала)
                    user_games.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

                    for i, game in enumerate(user_games[:20], 1):
                        f.write(f"\nИгра #{i}:\n")
                        f.write(f"  Ход игрока: {game.get('player_move', 'неизвестно')}\n")
                        f.write(f"  Ход бота: {game.get('bot_move', 'неизвестно')}\n")
                        f.write(f"  Результат: {game.get('result', 'неизвестно')}\n")
                        if 'timestamp' in game:
                            try:
                                dt = datetime.datetime.fromisoformat(game['timestamp'])
                                f.write(f"  Время: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
                            except:
                                f.write(f"  Время: {game['timestamp']}\n")

                f.write("=" * 50 + "\n")
                f.write(f"Файл создан: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            print(f"Статистика пользователя {username} сохранена в файл: {filename}")
            return filename

        except Exception as e:
            print(f"Ошибка сохранения статистики пользователя {user_id}: {e}")
            return None


# Создание менеджера пользователей
user_manager = UserManager()


# ГЛАВНОЕ ОКНО
def open_start_window():
    """Главное окно"""
    global root, icon_image
    # экран и его настройка
    root = Tk()
    root.title('Камень, Ножницы, Бумага')
    root.attributes("-fullscreen", True)  # весь экран
    icon_image = PhotoImage(file='img/logo.png')  # создание иконки
    root.iconphoto(False, icon_image)

    # создание фона
    img_bg = PhotoImage(file='img/изображение_экрана.png')
    bg_label = Label(root, image=img_bg)
    bg_label.image = img_bg
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # на задний план

    # кнопка "играть"
    def play_action():
        global user_is_logged_in, current_user_id, current_username
        if user_is_logged_in and current_user_id is not None:
            # Пользователь уже в системе - открыть игру напрямую
            open_game_window(current_user_id, current_username)
        else:
            # Пользователь не в системе - открыть окно входа
            open_login_window()

    play_bt = Button(root, text='ИГРАТЬ', font=('Inter', 30), highlightbackground='#022F64',  # цвет обводки
                     fg='#022F64', width=8, height=2, command=play_action)
    play_bt.place(relx=0.5, rely=0.5, anchor='center')  # по центру

    root.mainloop()


# ФУНКЦИИ ОТКРЫТИЯ ОКОН
def open_login_window():
    """Открытие окна входа"""
    global user_is_logged_in, current_user_id, current_username

    login_window = Toplevel(root)
    login_window.title('Вход')
    login_window.attributes("-fullscreen", True)  # весь экран
    login_window.iconphoto(False, icon_image)

    # создание фона
    img_bg_login = PhotoImage(file='img/блюр_экрана.png')
    bg_label_login = Label(login_window, image=img_bg_login)
    bg_label_login.image = img_bg_login
    bg_label_login.place(x=0, y=0, relwidth=1, relheight=1)

    # меню для входа
    # фрейм для элементов меню
    frame_elems = Label(login_window, width=50, height=30, bg='white', highlightbackground='#022F64',
                        highlightthickness=3)
    frame_elems.place(relx=0.5, rely=0.5, anchor='center')

    # надпись вход
    log_lb = Label(frame_elems, text='Вход', font=('Inter', 30), bg='white', fg='#022F64',
                   highlightbackground='#022F64')
    log_lb.place(relx=0.413, rely=0.05)

    # поля для ввода
    email_var = StringVar()
    email_entry = Entry(frame_elems, font=('Inter', 30), bg='white', fg='#5c7899',
                        highlightbackground='#022F64', highlightthickness=2,
                        width=20)
    email_entry.insert(0, 'Почта')
    email_entry.place(relx=0.06, rely=0.2)

    password_var = StringVar()
    password_entry = Entry(frame_elems, font=('Inter', 30), bg='white', fg='#5c7899',
                           highlightbackground='#022F64', highlightthickness=2,
                           width=20, show='*')
    password_entry.insert(0, 'Пароль')
    password_entry.place(relx=0.06, rely=0.34)

    # метки для ошибок
    email_error = Label(frame_elems, text='', font=('Inter', 20), bg='white', fg='red')
    email_error.place(relx=0.06, rely=0.27)

    password_error = Label(frame_elems, text='', font=('Inter', 20), bg='white', fg='red')
    password_error.place(relx=0.06, rely=0.41)

    # функция входа
    def login():
        global user_is_logged_in, current_user_id, current_username

        email = email_entry.get()
        password = password_entry.get()

        # сброс ошибок
        email_error.config(text='')
        password_error.config(text='')

        # проверка валидности почты
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            email_error.config(text='Неверный формат!')
            return

        # проверка пользователя
        user = user_manager.check_user(email, password)
        if user:
            # Устанавливаем флаг и сохраняем данные пользователя
            user_is_logged_in = True
            current_user_id = user[0]
            current_username = user[1]

            login_window.destroy()
            open_game_window(user[0], user[1])
        else:
            password_error.config(text='Неверные данные!')

    # кнопка войти
    login_but = Button(frame_elems, text='Войти', font=('Inter', 30), bg='white', fg='#022F64',
                       highlightbackground='#022F64', command=login)
    login_but.place(relx=0.37, rely=0.48)

    # кнопка глаз
    show_pass_var = BooleanVar(value=False)

    def toggle_password():
        if show_pass_var.get():
            password_entry.config(show='')
        else:
            password_entry.config(show='*')
        show_pass_var.set(not show_pass_var.get())

    show_pas_img = PhotoImage(file='img/show_pass.png')
    show_pas_but = Button(frame_elems, image=show_pas_img, borderwidth=0,
                          highlightthickness=0, command=toggle_password)
    show_pas_but.image = show_pas_img
    show_pas_but.place(in_=password_entry, relx=0.94, rely=0.5, anchor='center')

    # кнопка зарегистрироваться
    def open_reg_from_login():
        login_window.destroy()
        open_registration_window()

    reg_but = Button(frame_elems, text='Регистрация', font=('Inter', 30), bg='white', fg='#022F64',
                     highlightbackground='#022F64', width=11, command=open_reg_from_login)
    reg_but.place(relx=0.06, rely=0.837)

    # кнопка гость
    def play_as_guest():
        global user_is_logged_in, current_user_id, current_username

        # Для гостя флаг не устанавливается
        user_is_logged_in = False
        current_user_id = None
        current_username = 'Гость'

        login_window.destroy()
        open_game_window(None, 'Гость')

    guest_but = Button(frame_elems, text='Гость', font=('Inter', 30), bg='white', fg='#022F64',
                       highlightbackground='#022F64', width=5, command=play_as_guest)
    guest_but.place(relx=0.646, rely=0.837)

    # кнопка закрыть
    Button(login_window, text='✕', font=('Inter', 24), bg='red', fg='#4A0112',
           command=login_window.destroy).place(x=20, y=20)


def open_registration_window():
    """Открытие окна регистрации"""
    reg_window = Toplevel(root)
    reg_window.title('Регистрация')
    reg_window.attributes("-fullscreen", True)
    reg_window.iconphoto(False, icon_image)

    # создание фона
    img_bg_reg = PhotoImage(file='img/блюр_экрана.png')
    bg_label_reg = Label(reg_window, image=img_bg_reg)
    bg_label_reg.image = img_bg_reg
    bg_label_reg.place(x=0, y=0, relwidth=1, relheight=1)

    # меню для регистрации
    frame_elems = Label(reg_window, width=50, height=38, bg='white', highlightbackground='#022F64',
                        highlightthickness=3)
    frame_elems.place(relx=0.5, rely=0.5, anchor='center')

    # надпись регистрация
    reg_lb = Label(frame_elems, text='Регистрация', font=('Inter', 30), bg='white', fg='#022F64',
                   highlightbackground='#022F64')
    reg_lb.place(relx=0.32, rely=0.05)

    # поля для ввода
    username_entry = Entry(frame_elems, font=('Inter', 30), bg='white', fg='#5c7899',
                           highlightbackground='#022F64', highlightthickness=2,
                           width=20)
    username_entry.insert(0, 'Имя пользователя')
    username_entry.place(relx=0.06, rely=0.17)

    password_entry = Entry(frame_elems, font=('Inter', 30), bg='white', fg='#5c7899',
                           highlightbackground='#022F64', highlightthickness=2,
                           width=20, show='*')
    password_entry.insert(0, 'Пароль')
    password_entry.place(relx=0.06, rely=0.28)

    password2_entry = Entry(frame_elems, font=('Inter', 30), bg='white', fg='#5c7899',
                            highlightbackground='#022F64', highlightthickness=2,
                            width=20, show='*')
    password2_entry.insert(0, 'Пароль ещё раз')
    password2_entry.place(relx=0.06, rely=0.39)

    email_entry = Entry(frame_elems, font=('Inter', 30), bg='white', fg='#5c7899',
                        highlightbackground='#022F64', highlightthickness=2,
                        width=20)
    email_entry.insert(0, 'Почта')
    email_entry.place(relx=0.06, rely=0.5)

    # метки для ошибок
    username_error = Label(frame_elems, text='', font=('Inter', 20), bg='white', fg='red')
    username_error.place(relx=0.06, rely=0.23)

    password_error = Label(frame_elems, text='', font=('Inter', 20), bg='white', fg='red')
    password_error.place(relx=0.06, rely=0.34)

    password2_error = Label(frame_elems, text='', font=('Inter', 20), bg='white', fg='red')
    password2_error.place(relx=0.06, rely=0.45)

    email_error = Label(frame_elems, text='', font=('Inter', 20), bg='white', fg='red')
    email_error.place(relx=0.06, rely=0.56)

    # кнопка глаз
    show_pass_var = BooleanVar(value=False)

    def toggle_password():
        if show_pass_var.get():
            password_entry.config(show='')
            password2_entry.config(show='')
        else:
            password_entry.config(show='*')
            password2_entry.config(show='*')
        show_pass_var.set(not show_pass_var.get())

    show_pas_img = PhotoImage(file='img/show_pass.png')
    show_pas_but = Button(password_entry, image=show_pas_img, borderwidth=0,
                          highlightthickness=0, command=toggle_password)
    show_pas_but.image = show_pas_img
    show_pas_but.place(in_=password_entry, relx=0.94, rely=0.5, anchor='center')

    # кнопка пол
    gender_var = StringVar(value='')
    gender_options = ['', 'Мужской', 'Женский', 'Другой']
    gender_menu = OptionMenu(frame_elems, gender_var, *gender_options)
    gender_menu.config(font=('Inter', 30), bg='white', fg='#5c7899',
                       highlightbackground='#022F64', width=7, anchor='w')
    gender_menu.place(relx=0.06, rely=0.61)

    # поле для возраста
    age_entry = Entry(frame_elems, font=('Inter', 30), bg='white', fg='#5c7899',
                      highlightbackground='#022F64', highlightthickness=2,
                      width=7)
    age_entry.insert(0, 'Возраст')
    age_entry.place(relx=0.52, rely=0.61)

    # функция регистрации
    def register():
        global user_is_logged_in, current_user_id, current_username

        # сброс ошибок
        username_error.config(text='')
        password_error.config(text='')
        password2_error.config(text='')
        email_error.config(text='')

        username = username_entry.get()
        password = password_entry.get()
        password2 = password2_entry.get()
        email = email_entry.get()
        gender = gender_var.get() if gender_var.get() else None
        age = age_entry.get() if age_entry.get().isdigit() else None

        # валидация
        errors = False

        if not username or username == 'Имя пользователя':
            username_error.config(text='Заполните поле!')
            errors = True

        if not password or password == 'Пароль':
            password_error.config(text='Заполните поле!')
            errors = True

        if password != password2:
            password2_error.config(text='Пароли не совпадают!')
            errors = True

        if not email or email == 'Почта':
            email_error.config(text='Заполните поле!')
            errors = True
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            email_error.config(text='Неверный формат!')
            errors = True

        if errors:
            return

        # регистрация пользователя
        if user_manager.add_user(username, email, password, gender, age):
            # После регистрации автоматически входить в систему
            user = user_manager.check_user(email, password)
            if user:
                user_is_logged_in = True
                current_user_id = user[0]
                current_username = user[1]

                messagebox.showinfo('Успех', 'Регистрация прошла успешно! Вы вошли в систему.')
                reg_window.destroy()
                open_game_window(user[0], user[1])
        else:
            email_error.config(text='Эта почта уже занята!')

    # кнопка зарегистрироваться
    reg_but = Button(frame_elems, text='Зарегистрироваться', font=('Inter', 30), bg='white', fg='#022F64',
                     highlightbackground='#022F64', width=19, command=register)
    reg_but.place(relx=0.06, rely=0.72)

    # кнопка вход
    def open_login_from_reg():
        reg_window.destroy()
        open_login_window()

    log_but = Button(frame_elems, text='Вход', font=('Inter', 30), bg='white', fg='#022F64',
                     highlightbackground='#022F64', width=8, command=open_login_from_reg)
    log_but.place(relx=0.06, rely=0.89)

    # кнопка гость
    def play_as_guest_from_reg():
        global user_is_logged_in, current_user_id, current_username

        # Для гостя флаг не устанавливается
        user_is_logged_in = False
        current_user_id = None
        current_username = 'Гость'

        reg_window.destroy()
        open_game_window(None, 'Гость')

    guest_but = Button(frame_elems, text='Гость', font=('Inter', 30), bg='white', fg='#022F64',
                       highlightbackground='#022F64', width=8, command=play_as_guest_from_reg)
    guest_but.place(relx=0.52, rely=0.89)

    # кнопка закрыть
    Button(reg_window, text='✕', font=('Inter', 24), bg='red', fg='#4A0112',
           command=reg_window.destroy).place(x=20, y=20)


def open_game_window(user_id=None, username='Гость'):
    """Открытие игрового окна"""
    global user_is_logged_in, current_user_id, current_username

    # Обновляем глобальные переменные
    if user_id is not None:
        user_is_logged_in = True
        current_user_id = user_id
        current_username = username
    else:
        user_is_logged_in = False
        current_user_id = None
        current_username = username

    game_window = Toplevel(root)
    game_window.title('Игра')
    game_window.attributes("-fullscreen", True)
    game_window.iconphoto(False, icon_image)

    # создание фона
    img_bg_game = PhotoImage(file='img/основной_фон.png')
    bg_label_game = Label(game_window, image=img_bg_game)
    bg_label_game.image = img_bg_game
    bg_label_game.place(x=0, y=0, relwidth=1, relheight=1)

    # окно хода компьютера
    window_computer = Label(game_window, text='\nВыбери камень/ножницы/бумагу!', width=35, height=15,
                            font=('Inter', 30),
                            fg='#022F64', borderwidth=1, relief='sunken', anchor='n', bg='white',
                            highlightbackground='#022F64', highlightthickness=2)
    window_computer.place(relx=0.27, rely=0.02)

    # плашка "вы"
    player_label = Label(game_window, text='Вы', font=('Inter', 24),
                         fg='#022F64', borderwidth=0, relief='sunken', bg='white',
                         highlightbackground='#022F64', highlightthickness=0, width=8, height=1)
    player_label.place(relx=0.4, rely=0.17, anchor='center')

    # плашка "робот"
    robot_label = Label(game_window, text='Робот', font=('Inter', 24),
                        fg='#022F64', borderwidth=0, relief='sunken', bg='white',
                        highlightbackground='#022F64', highlightthickness=0, width=8, height=1)
    robot_label.place(relx=0.6, rely=0.17, anchor='center')

    # камень
    img_rock = PhotoImage(file='img/rock.png')
    rock = Button(game_window, width=200, height=195, image=img_rock, bg='white', highlightbackground='#022F64',
                  highlightthickness=0)
    rock.image = img_rock
    rock.place(relx=0.34, rely=0.766, anchor='center')
    # бумага
    img_paper = PhotoImage(file='img/paper.png')
    paper = Button(game_window, width=200, height=195, image=img_paper, bg='white', highlightbackground='#022F64',
                   highlightthickness=0)
    paper.image = img_paper
    paper.place(relx=0.504, rely=0.766, anchor='center')
    # ножницы
    img_shear = PhotoImage(file='img/shear.png')
    shear = Button(game_window, width=200, height=195, image=img_shear, bg='white', highlightbackground='#022F64',
                   highlightthickness=0)
    shear.image = img_shear
    shear.place(relx=0.666, rely=0.766, anchor='center')

    # раунд
    round_label = Label(game_window, text='Раунд: 0',
                        highlightbackground='#4A0112', highlightthickness=2,
                        font=('Inter', 24), fg='#4A0112', bg='white',
                        width=16, height=2)
    round_label.place(relx=0.014, rely=0.02)

    # заработано очков
    point_lb = Label(game_window, text='Заработано очков: 0',
                     highlightbackground='#4A0112', highlightthickness=2,
                     font=('Inter', 24), fg='#4A0112', bg='white',
                     width=16, height=2)
    point_lb.place(relx=0.014, rely=0.11)

    # статистика
    statics_but = Label(game_window, text='Статистика: ',
                        highlightbackground='#4A0112', highlightthickness=2,
                        font=('Inter', 24), fg='#4A0112', bg='white',
                        width=16, height=2)
    statics_but.place(relx=0.014, rely=0.2)

    # показать статистику
    show_stat_img = PhotoImage(file='img/open_stats.png')
    show_stat_but = Button(statics_but, image=show_stat_img,
                           borderwidth=0, highlightthickness=0)
    show_stat_but.image = show_stat_img
    show_stat_but.place(in_=statics_but, relx=0.96, rely=0.87, anchor='center')

    # показать общую статистику
    show_all_statistic = Button(game_window, text='Статистика по всем\nпользователям', width=16, height=2,
                                bg='white', font=('Inter', 24),
                                highlightbackground='#022F64', highlightthickness=0,
                                fg='#022F64')
    show_all_statistic.place(relx=0.014, rely=0.9)

    # сброс счёта
    reset_but = Button(game_window, text='Сброс счёта', width=16, height=2,
                       bg='white', font=('Inter', 24),
                       highlightbackground='#022F64', highlightthickness=0,
                       fg='#022F64')
    reset_but.place(relx=0.795, rely=0.9)

    # настройки
    settings_lb = Label(game_window, text='Настройки', width=13, height=2,
                        font=('Inter', 24), fg='#022F64', bg='white',
                        anchor='w', padx=30, highlightbackground='#022F64',
                        highlightthickness=2)
    settings_lb.place(relx=0.805, rely=0.02)

    # иконка настроек (кнопка)
    settings_img = PhotoImage(file='img/settings.png')
    settings_but = Button(settings_lb, image=settings_img,
                          highlightbackground='#022F64', highlightthickness=0,
                          anchor='center', borderwidth=0)
    settings_but.image = settings_img
    settings_but.place(relx=0.72, rely=0.1)

    # ВНУТРЕННИЕ ФУНКЦИИ ИГРЫ

    # Переменные для этой игровой сессии
    but_next = None
    current_lb = None
    flag_static = False
    static_widget = None

    # Игровые счётчики (только для текущей сессии)
    cnt_win = 0
    cnt_lose = 0
    total_game = 0
    rock_cnt = 0
    shear_cnt = 0
    paper_cnt = 0

    def rock_click():
        nonlocal rock_cnt
        rock_cnt += 1
        play_game('камень')

    def shear_click():
        nonlocal shear_cnt
        shear_cnt += 1
        play_game('ножницы')

    def paper_click():
        nonlocal paper_cnt
        paper_cnt += 1
        play_game('бумага')

    rock['command'] = rock_click
    shear['command'] = shear_click
    paper['command'] = paper_click

    # пользовательская статистика
    def open_close_statistic():
        nonlocal flag_static, static_widget

        if flag_static:
            if static_widget:
                static_widget.destroy()
            flag_static = False
            hide_smile()
        else:
            # Получение статистики из базы и текущей сессии
            if user_id:
                db_total, db_wins, db_losses, db_draws = user_manager.get_user_stats(user_id)
                # Используем только статистику из базы данных, так как текущая сессия уже сохранена
                total_games = db_total
                wins = db_wins
                losses = db_losses
                draws = db_draws
            else:
                # Для гостя используем только текущую сессию
                total_games = total_game
                wins = cnt_win
                losses = cnt_lose
                draws = total_game - cnt_win - cnt_lose

            st_text = (f'Камень - {rock_cnt}\n\nНожницы - {shear_cnt}\n\nБумага - {paper_cnt}\n\n'
                       f'Поражений - {losses}\n\nПобед - {wins}\n\nНичьих - {draws}\n\n'
                       f'Кол-во игр - {total_games}\n\nПользователь:\n{username}')

            static_widget = Label(game_window, text=f"\n{st_text}", height=18, width=16,
                                  font=('Inter', 24), anchor='n',
                                  highlightbackground='#4A0112', highlightthickness=2,
                                  fg='#4A0112', bg='white')
            static_widget.place(relx=0.014, rely=0.27)

            # Добавление маленькой кнопки сортировки в правый верхний угол
            sort_button = Button(static_widget, text='↑↓', font=('Inter', 12),
                                 bg='#4A0112', fg='white',
                                 width=2, height=1,
                                 command=lambda: sort_personal_stats())
            sort_button.place(relx=0.88, rely=0.03, anchor='center')

            flag_static = True

            # Функция сортировки личной статистики
            def sort_personal_stats():
                # Создается список элементов статистики для сортировки
                stats_items = [
                    ('Камень', rock_cnt),
                    ('Ножницы', shear_cnt),
                    ('Бумага', paper_cnt),
                    ('Поражений', losses),
                    ('Побед', wins),
                    ('Ничьих', draws),
                    ('Кол-во игр', total_games)
                ]

                # Используется атрибут функции для хранения состояния сортировки между нажатиями
                if not hasattr(sort_personal_stats, 'reverse_sort'):
                    sort_personal_stats.reverse_sort = False

                # Переключается направление сортировки
                sort_personal_stats.reverse_sort = not sort_personal_stats.reverse_sort

                # Сортировка выполняется по значениям (второй элемент кортежа)
                stats_items.sort(key=lambda x: x[1], reverse=sort_personal_stats.reverse_sort)

                # Формируется новый текст статистики
                new_st_text = "\n"
                for item_name, item_value in stats_items:
                    new_st_text += f'{item_name} - {item_value}\n\n'
                new_st_text += f'Пользователь:\n{username}'

                # Обновляется отображение
                static_widget.config(text=new_st_text)

                # Меняется текст кнопки для отображения направления сортировки
                sort_button.config(text='↓↑' if sort_personal_stats.reverse_sort else '↑↓')

    show_stat_but['command'] = open_close_statistic

    # Функция для показа общей статистики всех пользователей
    def show_all_users_stats():
        stats_window = Toplevel(game_window)
        stats_window.title("Общая статистика всех пользователей")
        stats_window.attributes("-fullscreen", True)
        stats_window.iconphoto(False, icon_image)

        # создание фона
        img_bg_stats = PhotoImage(file='img/основной_фон.png')
        bg_label_stats = Label(stats_window, image=img_bg_stats)
        bg_label_stats.image = img_bg_stats
        bg_label_stats.place(x=0, y=0, relwidth=1, relheight=1)

        # Заголовок
        title_label = Label(stats_window, text='ОБЩАЯ СТАТИСТИКА ВСЕХ ПОЛЬЗОВАТЕЛЕЙ',
                            font=('Inter', 30), bg='white', fg='#022F64',
                            highlightbackground='#022F64', highlightthickness=3,
                            width=40, height=2)
        title_label.place(relx=0.5, rely=0.05, anchor='center')

        # Получение отсортированной статистики
        all_stats = user_manager.get_all_stats_sorted()

        # Фрейм для таблицы
        table_frame = Frame(stats_window, bg='white', highlightbackground='#022F64', highlightthickness=3)
        table_frame.place(relx=0.5, rely=0.5, anchor='center', width=1000, height=500)

        # Заголовки таблицы со стилями
        headers = ["№", "ИГРОК", "ВСЕГО ИГР", "ПОБЕД", "ПОРАЖЕНИЙ", "НИЧЬИХ", "% ПОБЕД"]

        # Создание заголовков
        for col, header in enumerate(headers):
            header_label = Label(table_frame, text=header, font=('Inter', 18, 'bold'),
                                 fg='#022F64', bg='#e0e0e0', width=15, height=2,
                                 relief='solid', borderwidth=2, highlightbackground='#022F64')
            header_label.grid(row=0, column=col, sticky='nsew', padx=1, pady=1)

        # Переменная для хранения текущего способа сортировки
        current_sort_by = 'wins'  # По умолчанию сортировка по победам
        sort_reverse = True  # По убыванию

        # Функция для обновления отображения таблицы
        def update_table(stats_data):
            # Очистка старых данных (кроме заголовков)
            for widget in table_frame.winfo_children():
                if widget.grid_info() and widget.grid_info()['row'] > 0:
                    widget.destroy()

            # Данные таблицы с нумерацией
            if stats_data:
                for idx, (user_id, username, total, wins, losses, draws) in enumerate(stats_data, 1):
                    # Вычисление процента побед
                    win_percentage = wins / total * 100 if total > 0 else 0

                    # № (позиция)
                    num_label = Label(table_frame, text=str(idx), font=('Inter', 16),
                                      relief='solid', borderwidth=2, bg='#022F64', highlightbackground='#022F64',
                                      width=15, height=2, fg='#022F64')
                    num_label.grid(row=idx, column=0, sticky='nsew', padx=1, pady=1)

                    # Имя пользователя
                    name_label = Label(table_frame, text=username, font=('Inter', 16),
                                       relief='solid', borderwidth=2, highlightbackground='#022F64',
                                       width=15, height=2, fg='#022F64')
                    name_label.grid(row=idx, column=1, sticky='nsew', padx=1, pady=1)

                    # Всего игр
                    total_label = Label(table_frame, text=str(total), font=('Inter', 16),
                                        relief='solid', borderwidth=2, highlightbackground='#022F64',
                                        width=15, height=2, fg='#022F64')
                    total_label.grid(row=idx, column=2, sticky='nsew', padx=1, pady=1)

                    # Побед
                    wins_label = Label(table_frame, text=str(wins), font=('Inter', 16),
                                       relief='solid', borderwidth=2, highlightbackground='#022F64',
                                       width=15, height=2, fg='#022F64')
                    wins_label.grid(row=idx, column=3, sticky='nsew', padx=1, pady=1)

                    # Поражений
                    losses_label = Label(table_frame, text=str(losses), font=('Inter', 16),
                                         relief='solid', borderwidth=2, highlightbackground='#022F64',
                                         width=15, height=2, fg='#022F64')
                    losses_label.grid(row=idx, column=4, sticky='nsew', padx=1, pady=1)

                    # Ничьих
                    draws_label = Label(table_frame, text=str(draws), font=('Inter', 16),
                                        relief='solid', borderwidth=2, highlightbackground='#022F64',
                                        width=15, height=2, fg='#022F64')
                    draws_label.grid(row=idx, column=5, sticky='nsew', padx=1, pady=1)

                    # Процент побед
                    percent_label = Label(table_frame, text=f"{win_percentage:.1f}%", font=('Inter', 16),
                                          relief='solid', borderwidth=2, highlightbackground='#022F64',
                                          width=15, height=2, fg='#022F64')
                    percent_label.grid(row=idx, column=6, sticky='nsew', padx=1, pady=1)

                    # Раскрашивание строк
                    if idx % 2 == 0:
                        bg_color = '#f0f0f0'
                    else:
                        bg_color = 'white'

                    for widget in [num_label, name_label, total_label, wins_label, losses_label, draws_label,
                                   percent_label]:
                        widget.config(bg=bg_color)

        # Функция сортировки общей статистики
        def sort_all_stats():
            nonlocal all_stats, current_sort_by, sort_reverse

            # Определяем следующий критерий сортировки
            sort_order = ['wins', 'total', 'losses', 'draws', 'percent', 'name']
            current_index = sort_order.index(current_sort_by) if current_sort_by in sort_order else 0

            # Переходим к следующему критерию или меняем направление
            if not sort_reverse:
                # Меняем критерий сортировки
                current_index = (current_index + 1) % len(sort_order)
                current_sort_by = sort_order[current_index]
                sort_reverse = True
            else:
                # Меняем направление сортировки для текущего критерия
                sort_reverse = False

            # Создаем копию для сортировки
            stats_to_sort = all_stats.copy()

            # Сортировка в зависимости от критерия
            if current_sort_by == 'wins':
                stats_to_sort.sort(key=lambda x: x[3], reverse=sort_reverse)
                sort_button.config(text='П↓' if sort_reverse else 'П↑')
            elif current_sort_by == 'total':
                stats_to_sort.sort(key=lambda x: x[2], reverse=sort_reverse)
                sort_button.config(text='И↓' if sort_reverse else 'И↑')
            elif current_sort_by == 'losses':
                stats_to_sort.sort(key=lambda x: x[4], reverse=sort_reverse)
                sort_button.config(text='Пор↓' if sort_reverse else 'Пор↑')
            elif current_sort_by == 'draws':
                stats_to_sort.sort(key=lambda x: x[5], reverse=sort_reverse)
                sort_button.config(text='Н↓' if sort_reverse else 'Н↑')
            elif current_sort_by == 'percent':
                stats_to_sort.sort(key=lambda x: x[3] / x[2] if x[2] > 0 else 0, reverse=sort_reverse)
                sort_button.config(text='%↓' if sort_reverse else '%↑')
            elif current_sort_by == 'name':
                stats_to_sort.sort(key=lambda x: x[1].lower(), reverse=sort_reverse)
                sort_button.config(text='Имя↓' if sort_reverse else 'Имя↑')

            # Обновление отображения
            update_table(stats_to_sort)

        # Инициализация отображения таблицы
        update_table(all_stats)

        # Если нет статистики
        if not all_stats:
            no_data_label = Label(table_frame,
                                  text="Нет данных для отображения\n\nСыграйте несколько игр,\nчтобы увидеть статистику",
                                  font=('Inter', 24), fg='gray', bg='white', justify='center')
            no_data_label.place(relx=0.5, rely=0.5, anchor='center')

        # Добавление кнопки сортировки справа во фрейме
        sort_button = Button(table_frame, text='П↓', font=('Inter', 12),
                             bg='#022F64', fg='white',
                             width=1, height=1,
                             command=sort_all_stats)
        sort_button.place(relx=0.05, rely=0.02, anchor='ne')

        # Настройка весов столбцов
        for i in range(7):
            table_frame.grid_columnconfigure(i, weight=1)

        # Кнопка закрытия
        close_btn = Button(stats_window, text="ЗАКРЫТЬ", font=('Inter', 24), bg='white', fg='#022F64',
                           highlightbackground='#022F64', highlightthickness=1,
                           width=15, height=2, command=stats_window.destroy)
        close_btn.place(relx=0.5, rely=0.92, anchor='center')

        # кнопка закрыть
        Button(stats_window, text='✕', font=('Inter', 24), bg='red', fg='#4A0112',
               command=stats_window.destroy).place(x=20, y=20)

    # Привязываем функцию к кнопке
    show_all_statistic['command'] = show_all_users_stats

    def play_again():
        nonlocal but_next
        clear_program_move()
        rock['state'] = 'normal'
        paper['state'] = 'normal'
        shear['state'] = 'normal'
        hide_smile()
        window_computer['text'] = '\nВыбери камень/ножницы/бумагу!'
        if but_next:
            but_next.destroy()
            but_next = None

    def show_moves(player_choice, robot_choice):
        for widget in window_computer.winfo_children():
            if isinstance(widget, Label) and widget != window_computer:
                widget.destroy()

        # Ход игрока
        if player_choice == 'камень':
            player_img = img_rock
        elif player_choice == 'бумага':
            player_img = img_paper
        else:
            player_img = img_shear

        player_move = Label(window_computer, image=player_img, bg='white')
        player_move.place(relx=0.3, rely=0.53, anchor='center')

        # Ход робота
        if robot_choice == 'камень':
            robot_img = img_rock
        elif robot_choice == 'бумага':
            robot_img = img_paper
        else:
            robot_img = img_shear

        robot_move = Label(window_computer, image=robot_img, bg='white')
        robot_move.place(relx=0.71, rely=0.53, anchor='center')

    def clear_program_move():
        for widget in window_computer.winfo_children():
            if isinstance(widget, Label) and widget != window_computer:
                widget.destroy()

    def chance():
        max_way = max([rock_cnt, shear_cnt, paper_cnt])
        if max_way != 0:
            if random() < 0.8:
                if max_way == rock_cnt:
                    return 'бумага'
                elif max_way == shear_cnt:
                    return 'камень'
                else:
                    return 'ножницы'
            return 0
        return 0

    def show_message(msg_type):
        nonlocal current_lb
        if current_lb:
            current_lb.destroy()

        if msg_type == 'happy':
            lb_state = Label(game_window, text='Вы победили! :)', width=41, height=2,
                             font=('Inter', 24), fg='#022F64', bg='#78DC66',
                             anchor='w', padx=30, highlightbackground='#022F64',
                             highlightthickness=2.5)
        elif msg_type == 'puzzled':
            lb_state = Label(game_window, text='Ничья! :|', width=41, height=2,
                             font=('Inter', 24), fg='#022F64', bg='#7e92ac',
                             anchor='w', padx=30, highlightbackground='#022F64',
                             highlightthickness=2.5)
        else:
            lb_state = Label(game_window, text='Вы проиграли! :(', width=41, height=2,
                             font=('Inter', 24), fg='#022F64', bg='#F16767',
                             anchor='w', padx=30, highlightbackground='#022F64',
                             highlightthickness=2.5)

        lb_state.place(relx=0.504, rely=0.937, anchor='center')
        current_lb = lb_state

    def hide_smile():
        nonlocal current_lb
        if current_lb:
            current_lb.destroy()
            current_lb = None

    def reset_score():
        nonlocal cnt_win, cnt_lose, total_game, rock_cnt, shear_cnt, paper_cnt
        # Полностью сбрасываем всю статистику для текущей сессии
        cnt_win = cnt_lose = total_game = 0
        rock_cnt = shear_cnt = paper_cnt = 0

        # Если пользователь авторизован, сбрасываем его статистику в базе данных
        if user_id:
            # Обнуляем статистику в базе данных
            if user_id in user_manager.GAME_STATS:
                user_manager.GAME_STATS[user_id] = {
                    'username': username,
                    'total_games': 0,
                    'wins': 0,
                    'losses': 0,
                    'draws': 0
                }
                user_manager.save_data()

        # Обновляем отображение
        round_label['text'] = 'Раунд: 0'
        point_lb['text'] = 'Заработано очков: 0'
        clear_program_move()
        hide_smile()
        window_computer['text'] = '\nВыбери камень/ножницы/бумагу!'

        # Если статистика открыта, закрываем ее
        nonlocal flag_static, static_widget
        if flag_static and static_widget:
            static_widget.destroy()
            flag_static = False

        messagebox.showinfo("Сброс статистики", "Вся статистика была сброшена!")

    reset_but['command'] = reset_score

    def play_game(choice_user):
        nonlocal but_next, cnt_win, cnt_lose, total_game

        rock['state'] = 'disabled'
        paper['state'] = 'disabled'
        shear['state'] = 'disabled'

        ls_of_moves = {'камень': 2, 'ножницы': 1, 'бумага': 0}
        chance_player = chance()
        choice_program = chance_player if chance_player != 0 else choice(['камень', 'ножницы', 'бумага'])

        show_moves(choice_user, choice_program)
        res = (ls_of_moves[choice_program] - ls_of_moves[choice_user]) % 3

        if res == 1:
            cnt_lose += 1
            result = 'lose'
            show_message('sad')
        elif res == 0:
            result = 'draw'
            show_message('puzzled')
        else:
            cnt_win += 1
            result = 'win'
            show_message('happy')

        # Сохранение в базу данных если пользователь авторизован
        if user_id:
            user_manager.save_game_result(user_id, choice_user, choice_program, result)

        # Обновление счётчиков
        total_game += 1
        round_label['text'] = f'Раунд: {total_game}'
        point_lb['text'] = f'Заработано очков: {cnt_win}'

        if but_next:
            but_next.destroy()

        but_next = Button(game_window, text='Играть ещё раз', width=11, height=2,
                          font=('Inter', 24), highlightbackground='#022F64',
                          highlightthickness=0, fg='#022F64', bg='white')
        but_next.place(relx=0.435, rely=0.9011)
        but_next['command'] = play_again

    # функция открытия настроек
    def open_settings_from_game():
        game_window.destroy()
        open_settings_window(user_id, username)

    settings_but['command'] = open_settings_from_game

    # кнопка закрыть
    Button(game_window, text='✕', font=('Inter', 24), bg='red', fg='#4A0112',
           command=game_window.destroy).place(x=20, y=20)


def open_settings_window(user_id=None, username='Гость'):
    """Открытие окна настроек"""
    global user_is_logged_in, current_user_id, current_username

    settings_window = Toplevel(root)
    settings_window.title('Настройки')
    settings_window.attributes("-fullscreen", True)
    settings_window.iconphoto(False, icon_image)

    # создание фона
    img_bg_settings = PhotoImage(file='img/основной_фон.png')
    bg_label_settings = Label(settings_window, image=img_bg_settings)
    bg_label_settings.image = img_bg_settings
    bg_label_settings.place(x=0, y=0, relwidth=1, relheight=1)

    # кнопка меню
    def menu_action():
        settings_window.destroy()
        # Закрываем все окна и возвращаемся в главное меню
        root.destroy()
        open_start_window()

    menu_but = Button(settings_window, text='Меню', font=('Inter', 24), bg='white', fg='#4A0112',
                      highlightbackground='#4A0112', borderwidth=2, width=10, height=2,
                      command=menu_action)
    menu_but.place(relx=0.014, rely=0.014)

    # надпись приветствия
    hello_text = f'Добро пожаловать, {username}!' if user_id else 'Добро пожаловать, Гость!'
    hello_lb = Label(settings_window, text=hello_text, font=('Inter', 24), bg='white', fg='#4A0112',
                     highlightbackground='#4A0112', highlightthickness=3, width=25, height=2)
    hello_lb.place(relx=0.367, rely=0.013)

    # кнопка назад к игре
    def back_to_game():
        settings_window.destroy()
        if user_id:
            open_game_window(user_id, username)
        else:
            open_game_window(None, 'Гость')

    back_to_game_but = Button(settings_window, text='Назад к игре', font=('Inter', 24), bg='white', fg='#022F64',
                              highlightbackground='#022F64', borderwidth=2, width=10, height=2,
                              command=back_to_game)
    back_to_game_but.place(relx=0.856, rely=0.014)

    # фрейм для настроек
    frame_elems = Label(settings_window, width=50, height=37, bg='white', highlightbackground='#022F64',
                        highlightthickness=3)
    frame_elems.place(relx=0.5, rely=0.5, anchor='center')
    # надпись настройки
    settings_lb = Label(frame_elems, text='Настройки', bg='white', borderwidth=0, font=('Inter', 24), fg='#022F64')
    settings_lb.place(relx=0.37, rely=0.05)

    if user_id:
        # Получение текущих данных пользователя
        current_email = None
        current_gender = None
        current_age = None

        for email, user_data in user_manager.USERS_DB.items():
            if user_data['user_id'] == user_id:
                current_email = email
                current_gender = user_data.get('gender', '')
                current_age = user_data.get('age', '')
                break

        # ПОЛЕ ДЛЯ ИЗМЕНЕНИЯ ИМЕНИ (с кнопкой сохранения прямо в поле)
        new_name_var = StringVar(value=username)

        # Фрейм для имени с кнопкой
        name_frame = Frame(frame_elems, bg='white')
        name_frame.place(relx=0.025, rely=0.14, relwidth=0.95, height=50)

        Label(name_frame, text='Имя:', font=('Inter', 24), bg='white', fg='#022F64').pack(side=LEFT, padx=(0, 10))

        rename_entry = Entry(name_frame, font=('Inter', 24), bg='white', fg='#5c7899',
                             highlightbackground='#022F64', highlightthickness=2,
                             width=18, textvariable=new_name_var)
        rename_entry.pack(side=LEFT, padx=(0, 10))

        def save_new_name():
            new_name = new_name_var.get().strip()
            if not new_name:
                messagebox.showerror("Ошибка", "Имя не может быть пустым!")
                return

            if user_manager.update_user(user_id, username=new_name):
                messagebox.showinfo("Успех", "Имя пользователя изменено!")
                settings_window.destroy()
                open_settings_window(user_id, new_name)
            else:
                messagebox.showerror("Ошибка", "Не удалось изменить имя!")

        # Кнопка с галочкой
        save_name_img = PhotoImage(file='img/check.png') if os.path.exists('img/check.png') else None
        if save_name_img:
            rename_save_but = Button(name_frame, image=save_name_img,
                                     borderwidth=0, highlightthickness=0,
                                     command=save_new_name, bg='white')
            rename_save_but.image = save_name_img
        else:
            rename_save_but = Button(name_frame, text='✓', font=('Inter', 20),
                                     bg='#022F64', fg='white',
                                     command=save_new_name, width=2, height=1)

        rename_save_but.pack(side=LEFT)

        # ПОЛЕ ДЛЯ ИЗМЕНЕНИЯ ПОЧТЫ (с кнопкой сохранения прямо в поле)
        new_email_var = StringVar(value=current_email if current_email else '')

        # Фрейм для почты с кнопкой
        email_frame = Frame(frame_elems, bg='white')
        email_frame.place(relx=0.025, rely=0.23, relwidth=0.95, height=50)

        Label(email_frame, text='Почта:', font=('Inter', 24), bg='white', fg='#022F64').pack(side=LEFT, padx=(0, 10))

        change_email_entry = Entry(email_frame, font=('Inter', 24), bg='white', fg='#5c7899',
                                   highlightbackground='#022F64', highlightthickness=2,
                                   width=18, textvariable=new_email_var)
        change_email_entry.pack(side=LEFT, padx=(0, 10))

        def save_new_email():
            new_email = new_email_var.get().strip()
            if not new_email:
                messagebox.showerror("Ошибка", "Почта не может быть пустой!")
                return

            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', new_email):
                messagebox.showerror("Ошибка", "Неверный формат почты!")
                return

            if user_manager.update_user(user_id, email=new_email):
                messagebox.showinfo("Успех", "Почта изменена!")
                settings_window.destroy()
                open_settings_window(user_id, username)
            else:
                messagebox.showerror("Ошибка", "Эта почта уже занята!")

        # Кнопка с галочкой
        if save_name_img:
            email_save_but = Button(email_frame, image=save_name_img,
                                    borderwidth=0, highlightthickness=0,
                                    command=save_new_email, bg='white')
            email_save_but.image = save_name_img
        else:
            email_save_but = Button(email_frame, text='✓', font=('Inter', 20),
                                    bg='#022F64', fg='white',
                                    command=save_new_email, width=2, height=1)

        email_save_but.pack(side=LEFT)

        # ПОЛЕ ДЛЯ ИЗМЕНЕНИЯ ПАРОЛЯ (с кнопкой сохранения прямо в поле)
        new_password_var = StringVar()

        # Фрейм для пароля с кнопкой
        password_frame = Frame(frame_elems, bg='white')
        password_frame.place(relx=0.025, rely=0.32, relwidth=0.95, height=50)

        Label(password_frame, text='Пароль:', font=('Inter', 24), bg='white', fg='#022F64').pack(side=LEFT,
                                                                                                 padx=(0, 10))

        change_password_entry = Entry(password_frame, font=('Inter', 24), bg='white', fg='#5c7899',
                                      highlightbackground='#022F64', highlightthickness=2,
                                      width=18, textvariable=new_password_var, show='*')
        change_password_entry.pack(side=LEFT, padx=(0, 10))

        def save_new_password():
            new_password = new_password_var.get()
            if not new_password:
                messagebox.showerror("Ошибка", "Пароль не может быть пустым!")
                return

            if user_manager.update_user(user_id, password=new_password):
                messagebox.showinfo("Успех", "Пароль изменен!")
                settings_window.destroy()
                open_settings_window(user_id, username)
            else:
                messagebox.showerror("Ошибка", "Не удалось изменить пароль!")

        # Кнопка с галочкой
        if save_name_img:
            password_save_but = Button(password_frame, image=save_name_img,
                                       borderwidth=0, highlightthickness=0,
                                       command=save_new_password, bg='white')
            password_save_but.image = save_name_img
        else:
            password_save_but = Button(password_frame, text='✓', font=('Inter', 20),
                                       bg='#022F64', fg='white',
                                       command=save_new_password, width=2, height=1)

        password_save_but.pack(side=LEFT)

        # ПОЛЕ ДЛЯ ИЗМЕНЕНИЯ ПОЛА (с кнопкой сохранения прямо в поле)
        gender_options = ['', 'Мужской', 'Женский', 'Другой']
        gender_var = StringVar(value=current_gender if current_gender else '')

        # Фрейм для пола с кнопкой
        gender_frame = Frame(frame_elems, bg='white')
        gender_frame.place(relx=0.025, rely=0.41, relwidth=0.95, height=50)

        Label(gender_frame, text='Пол:', font=('Inter', 24), bg='white', fg='#022F64').pack(side=LEFT, padx=(0, 10))

        gender_menu = OptionMenu(gender_frame, gender_var, *gender_options)
        gender_menu.config(font=('Inter', 20), bg='white', fg='#5c7899',
                           highlightbackground='#022F64', width=10, anchor='w')
        gender_menu.pack(side=LEFT, padx=(0, 10))

        def save_new_gender():
            new_gender = gender_var.get() if gender_var.get() else None
            if user_manager.update_user(user_id, gender=new_gender):
                messagebox.showinfo("Успех", "Пол изменен!")
                settings_window.destroy()
                open_settings_window(user_id, username)
            else:
                messagebox.showerror("Ошибка", "Не удалось изменить пол!")

        # Кнопка с галочкой
        if save_name_img:
            gender_save_but = Button(gender_frame, image=save_name_img,
                                     borderwidth=0, highlightthickness=0,
                                     command=save_new_gender, bg='white')
            gender_save_but.image = save_name_img
        else:
            gender_save_but = Button(gender_frame, text='✓', font=('Inter', 20),
                                     bg='#022F64', fg='white',
                                     command=save_new_gender, width=2, height=1)

        gender_save_but.pack(side=LEFT)

        # ПОЛЕ ДЛЯ ИЗМЕНЕНИЯ ВОЗРАСТА (с кнопкой сохранения прямо в поле)
        age_var = StringVar(value=str(current_age) if current_age else '')

        # Фрейм для возраста с кнопкой
        age_frame = Frame(frame_elems, bg='white')
        age_frame.place(relx=0.025, rely=0.5, relwidth=0.95, height=50)

        Label(age_frame, text='Возраст:', font=('Inter', 24), bg='white', fg='#022F64').pack(side=LEFT, padx=(0, 10))

        age_entry = Entry(age_frame, font=('Inter', 24), bg='white', fg='#5c7899',
                          highlightbackground='#022F64', highlightthickness=2,
                          width=10, textvariable=age_var)
        age_entry.pack(side=LEFT, padx=(0, 10))

        def save_new_age():
            new_age = age_var.get().strip()
            if not new_age:
                new_age = None
            elif not new_age.isdigit():
                messagebox.showerror("Ошибка", "Возраст должен быть числом!")
                return
            else:
                new_age = int(new_age)

            if user_manager.update_user(user_id, age=new_age):
                messagebox.showinfo("Успех", "Возраст изменен!")
                settings_window.destroy()
                open_settings_window(user_id, username)
            else:
                messagebox.showerror("Ошибка", "Не удалось изменить возраст!")

        # Кнопка с галочкой
        if save_name_img:
            age_save_but = Button(age_frame, image=save_name_img,
                                  borderwidth=0, highlightthickness=0,
                                  command=save_new_age, bg='white')
            age_save_but.image = save_name_img
        else:
            age_save_but = Button(age_frame, text='✓', font=('Inter', 20),
                                  bg='#022F64', fg='white',
                                  command=save_new_age, width=2, height=1)

        age_save_but.pack(side=LEFT)

    # кнопка сохранить статистику
    def save_stats():
        # Получаем статистику из базы данных
        if user_id:
            db_total, db_wins, db_losses, db_draws = user_manager.get_user_stats(user_id)

            # Здесь нужно получить счетчики ходов из игрового окна
            # В реальном приложении эти счетчики должны передаваться или храниться глобально
            # Для демонстрации используем заглушки
            rock_cnt = 0
            shear_cnt = 0
            paper_cnt = 0

            # Получаем общую статистику
            total_games = db_total
            wins = db_wins
            losses = db_losses
            draws = db_draws

            # Сохраняем статистику пользователя
            user_filename = user_manager.save_user_stats_to_file(
                user_id, username, rock_cnt, shear_cnt, paper_cnt,
                losses, wins, draws, total_games
            )

            # Получаем и сохраняем общую статистику всех пользователей
            all_stats = user_manager.get_all_stats_sorted()
            all_filename = user_manager.save_all_stats_to_file(all_stats)

            if user_filename and all_filename:
                messagebox.showinfo("Сохранение статистики",
                                    f"Статистика сохранена в файлы:\n"
                                    f"1. {user_filename} (ваша статистика)\n"
                                    f"2. {all_filename} (статистика всех пользователей)")
            else:
                messagebox.showwarning("Внимание", "Статистика сохранена не полностью!")
        else:
            messagebox.showinfo("Сохранение статистики",
                                "Для сохранения статистики необходимо войти в систему!")

    save_static_but = Button(frame_elems, text='Сохранить статистику\nи прогресс', font=('Inter', 24), bg='white',
                             fg='#022F64',
                             highlightbackground='#022F64', width=26, height=2, command=save_stats)
    save_static_but.place(relx=0.025, rely=0.7)

    # кнопка выйти
    def logout():
        global user_is_logged_in, current_user_id, current_username

        # Сбрасываем флаги
        user_is_logged_in = False
        current_user_id = None
        current_username = None

        settings_window.destroy()
        root.destroy()
        open_start_window()

    logout_but = Button(frame_elems, text='ВЫЙТИ', font=('Inter', 24), bg='white', fg='#4A0112',
                        highlightbackground='#4A0112', width=26, height=2, command=logout)
    logout_but.place(relx=0.025, rely=0.86)

    # кнопка закрыть
    Button(settings_window, text='✕', font=('Inter', 24), bg='red', fg='#4A0112',
           command=settings_window.destroy).place(x=20, y=16)


# ЗАПУСК
if __name__ == "__main__":
    open_start_window()