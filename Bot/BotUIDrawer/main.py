from tkinter import *

from PIL import Image, ImageTk


class Application:
    def __init__(self):
        self.lbl_right_side = None
        self.root = Tk()
        self.root.title('Секретарь')
        self.root.geometry('700x500')
        self.root.resizable(width=False, height=False)

        # добавление Canvas
        # self.canvas = Canvas(self.root, width=699, height=499)
        # self.canvas.pack()

        # картинка не работает, не видит путь к ней
        # self.pillImage = Image.open('../../media_files/first_face.png')
        # self.image = ImageTk.PhotoImage(self.pillImage)
        # self.image_sprite = self.canvas.create_image(100, 100, image=self.image)

        # top frame
        self.info_frame = Frame(self.root, height=400, padx=15)
        self.info_frame.pack(fill=X, pady=(15, 5))

        # bottom frame
        self.input_frame = Frame(self.root, height=100, pady=10, padx=5)
        self.input_frame.pack(fill=X)

        self.lbl_name = Label(self.input_frame, text='Что вы хотите узнать', font=12)
        self.lbl_name.pack(side=LEFT)

        self.ent_name = Entry(self.input_frame, font=15, width=50)
        self.ent_name.focus()  # поле ввода сразу становится активным
        self.ent_name.pack(side=LEFT)

        Frame(self.root, width=10).pack(side=LEFT)  # Для отступа между полем ввода и кнопкой

        self.btn_search = Button(self.input_frame, text='Узнать', width=10)
        self.btn_search.bind('<Button-1>', self.show_info)
        self.btn_search.pack(side=LEFT)

        # Скролл фрагмента
        self.scrollbar = Scrollbar(self.info_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.txt_widget = Text(self.info_frame, yscrollcommand=self.scrollbar.set, font=15)
        self.txt_widget.configure(state='disabled')  # для отмены возможности изменения текста
        self.txt_widget.pack(fill='both')
        self.scrollbar.config(command=self.txt_widget.yview)

        # запуск приложения
        self.root.mainloop()

    # вывод информации
    def show_info(self, event):

        self.txt_widget.configure(state='normal')  # для возобновления возможности изменения текста
        self.txt_widget.delete('1.0', END)  # очищает поле полностью
        txt = self.ent_name.get().lower()
        if txt == 'адрес':
            self.txt_widget.insert('end', 'ул.Ленина и\nтд и тп')

        if txt == 'номер':
            for i in range(1000):
                self.txt_widget.insert('end', f'{i}\n')  # чтобы переносить строку

        self.ent_name.delete(0, END)  # очищает поле ввода запроса

        self.txt_widget.configure(state='disabled')  # для отмены возможности изменения текста


Application()
