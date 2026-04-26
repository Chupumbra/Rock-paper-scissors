from tkinter import *

# экран и его настройка
root = Tk()
root.title('Камень, Ножницы, Бумага')
root.attributes("-fullscreen", True) # весь экран
icon_image = PhotoImage(file='img/logo.png') # создание иконки
root.iconphoto(False, icon_image)

# создание фона
img_bg = PhotoImage(file='img/изображение_экрана.png')
bg_label = Label(root, image=img_bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1) # на задний план

# кнопка "играть"
play_bt = Button(root, text='ИГРАТЬ', font=('Inter', 30), highlightbackground='#022F64', # цвет обводки
                 fg='#022F64', width=8, height=2, )
play_bt.place(relx=0.5, rely=0.5, anchor='center')  # по центру

root.mainloop() # запуск приложения
