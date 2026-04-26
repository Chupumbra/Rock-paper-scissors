from tkinter import *

# экран и его настройка
root = Tk()
root.title('Камень, Ножницы, Бумага')
root.attributes("-fullscreen", True) # весь экран
icon_image = PhotoImage(file='img/logo.png') # создание иконки
root.iconphoto(False, icon_image)

# создание фона
img_bg = PhotoImage(file='img/блюр_экрана.png')
bg_label = Label(root, image=img_bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1) # на задний план

# меню для входа
# фрейм для элементов меню
frame_elems = Label(root, width=50, height=30, bg='white', highlightbackground='#022F64',
                    highlightthickness=3) # толщина обводки
frame_elems.place(relx=0.5, rely=0.5, anchor='center')
# надпись вход
log_lb = Label(frame_elems, text='Вход', font=('Inter', 30), bg='white', fg='#022F64',
               highlightbackground='#022F64')
log_lb.place(relx=0.413, rely=0.05)
# кнопка почта
email_but = Button(frame_elems, text='Почта', font=('Inter', 30), bg='white', fg='#5c7899',
                   highlightbackground='#022F64', width=18, height=1, anchor='w', padx= 10)
# anchor='w' - по левому краю, padx - отступы текста
email_but.place(relx=0.06, rely=0.2)
# кнопка пароль
password_but = Button(frame_elems, text='Пароль', font=('Inter', 30), bg='white', fg='#5c7899',
                   highlightbackground='#022F64', width=18, height=1, anchor='w', padx=10)
password_but.place(relx=0.06, rely=0.34)
# кнопка войти
login_but = Button(frame_elems, text='Войти', font=('Inter', 30), bg='white', fg='#022F64',
                   highlightbackground='#022F64')
login_but.place(relx=0.37, rely=0.48)
# кнопка глаз
show_pas_img = PhotoImage(file='img/show_pass.png')
show_pas_but = Button(password_but, image=show_pas_img, borderwidth=0)
show_pas_but.place(in_=password_but, relx=0.94, rely=0.5, anchor='center', highlightthickness=0)
# кнопка зарегистрироваться
reg_but = Button(frame_elems, text='Регистрация', font=('Inter', 30), bg='white', fg='#022F64',
                   highlightbackground='#022F64', width=11)
reg_but.place(relx=0.06, rely=0.837)
# кнопка гость
guest_but = Button(frame_elems, text='Гость', font=('Inter', 30), bg='white', fg='#022F64',
                   highlightbackground='#022F64', width=5)
guest_but.place(relx=0.646, rely=0.837)




root.mainloop() # запуск приложения