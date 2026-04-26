from tkinter import *

# экран и его настройка
root = Tk()
root.title('Камень, Ножницы, Бумага')
root.attributes("-fullscreen", True) # весь экран
icon_image = PhotoImage(file='img/logo.png') # создание иконки
root.iconphoto(False, icon_image)

# создание фона
img_bg = PhotoImage(file='img/основной_фон.png')
bg_label = Label(root, image=img_bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1) # на задний план

# кнопка меню
menu_but = Button(root, text='Меню', font=('Inter', 24), bg='white', fg='#4A0112',
               highlightbackground='#4A0112', borderwidth=2, width=10, height=2)
menu_but.place(relx=0.014, rely=0.014)
# надпись приветствия
hello_lb = Label(root, text='Добро пожаловать, юзер!', font=('Inter', 24), bg='white', fg='#4A0112',
               highlightbackground='#4A0112', highlightthickness=3, width=25, height=2)
hello_lb.place(relx=0.367, rely=0.013)
# кнопка назад к игре
back_to_game_but = Button(root, text='Назад к игре', font=('Inter', 24), bg='white', fg='#022F64',
               highlightbackground='#022F64', borderwidth=2, width=10, height=2)
back_to_game_but.place(relx=0.856, rely=0.014)
# фрейм для настроек
frame_elems = Label(root, width=50, height=21, bg='white', highlightbackground='#022F64',
                    highlightthickness=3)
frame_elems.place(relx=0.5, rely=0.5, anchor='center')
# изменить имя
rename_but = Button(frame_elems, text='Изменить имя', font=('Inter', 24), bg='white', fg='#5c7899',
               highlightbackground='#022F64', width=25, height=2, anchor='w', padx=10)
rename_but.place(relx=0.025, rely=0.035)
# изменить почту
change_email_but = Button(frame_elems, text='Изменить почту', font=('Inter', 24), bg='white', fg='#5c7899',
               highlightbackground='#022F64', width=25, height=2, anchor='w', padx=10)
change_email_but.place(relx=0.025, rely=0.28)
# кнопка скачать статистику
save_static_but = Button(frame_elems, text='Скачать статистику', font=('Inter', 24), bg='white', fg='#022F64',
               highlightbackground='#022F64', width=26, height=2)
save_static_but.place(relx=0.025, rely=0.52)
# кнопка выйти
logout_but = Button(frame_elems, text='ВЫЙТИ', font=('Inter', 24), bg='white', fg='#4A0112',
               highlightbackground='#4A0112', width=26, height=2)
logout_but.place(relx=0.025, rely=0.76)

root.mainloop()