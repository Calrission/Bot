from tkinter import *


class Application:
    def __init__(self):
        self.root = Tk()
        self.root.title('Секретарь')
        self.root.geometry('700x500')
        self.root.resizable(width=False, height=False)

        # top frame
        self.input_frame = Frame(self.root, height=100, pady=25, padx=5)
        self.input_frame.pack(fill=X)

        # bottom frame
        self.info_frame = Frame(self.root, height=400, padx=15)
        self.info_frame.pack(fill=X)

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
        # появляется после нажатия кнопки
        # self.scrollbar = Scrollbar(self.info_frame)
        # self.scrollbar.pack(side=RIGHT, fill=Y)
        # self.listbox = Listbox(self.info_frame, yscrollcommand=self.scrollbar.set, font=15)
        # self.listbox.pack(fill='both')
        # self.scrollbar.config(command=self.listbox.yview)

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