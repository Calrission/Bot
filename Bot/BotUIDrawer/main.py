import pathlib
from pathlib import Path
from tkinter import *
from tkinter import ttk  # Для стилей
from PIL import Image, ImageTk

"""
Класс отрисовки окна приложения.
by Данил Зиновьев и Артемий Струков
created 19/02/22
"""


class Application:
    def __init__(self):
        self.photo = None
        self.photo_dop = None
        self.image_c = None
        self.image_c_dop = None
        self.show_gif_animation = False
        self.root = Tk()
        self.root.title('Бот секретарь школы №15 С УИОП г. Электросталь')
        self.root.geometry('760x600')
        self.root.wm_iconbitmap(bitmap=str(Path(pathlib.Path.cwd(), "media_files", "icon.ico")))
        self.root.resizable(width=False, height=False)
        self.root.configure(bg='#0E1621')  # цвет фона окна
        # self.root.overrideredirect(True) # Убирает рамки windows

        self.style = ttk.Style(self.root)
        self.style.theme_use('winnative')
        self.style.configure('Vertical.TScrollbar', background='#0E1621', arrowcolor='red')

        # top frame
        self.info_frame = Frame(self.root, height=400, padx=0, bg='#0E1621')
        self.info_frame.pack(fill=X, pady=(5, 5))

        self.frame_images = Frame(self.info_frame, width=100, bg='#0E1621')
        self.frame_images.pack(side=LEFT, anchor=N)

        # input  frame
        self.input_frame = Frame(self.root, height=100, pady=10, padx=5, bg='#0E1621', bd=0)
        self.input_frame.pack(fill=X)

        # horizontal scroll frame
        self.hor_scroll_frame_ = Frame(self.root, bg='#0E1621')  # фрейм
        self.hor_scroll_frame_.pack(fill=X, padx=(15, 10))
        self.hor_scroll_frame = Text(self.hor_scroll_frame_, wrap=NONE, height=2, cursor='arrow',
                                     bg='#0E1621', borderwidth=0)  # текстовое поле
        self.hor_scroll_frame.pack(pady=(5, 5), padx=(5, 5), fill=X)

        # Картинка для персонажа
        self.canvas = Canvas(self.frame_images, height=120, width=100, bg='#0E1621', borderwidth=0,
                             highlightthickness=0)
        self.canvas.grid(row=1, pady=(0, 0), padx=(5, 10))

        self.canvas_dop = Canvas(self.frame_images, height=120, width=100, bg='#0E1621', borderwidth=0,
                                 highlightthickness=0)
        self.canvas_dop.grid(row=2, pady=(0, 0), padx=(5, 10))

        self.ent_name = Entry(self.input_frame, font=22, width=68, bg='#17212B', fg='#fff', insertbackground='#fff',
                              bd=0)
        self.ent_name.focus()  # поле ввода сразу становится активным
        self.ent_name.pack(side=LEFT, ipady=10, padx=(20, 0))

        Frame(self.root, width=10).pack(side=LEFT)  # Для отступа между полем ввода и кнопкой

        # send message
        image = Image.open(str(Path(pathlib.Path.cwd(), "media_files", "send_message_btn.png"))) \
            .resize((45, 45), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)
        self.btn_search = Button(self.input_frame, image=self.image, compound=CENTER, bg='#0E1621',
                                 relief='flat', borderwidth=0)
        self.btn_search.pack(side=LEFT, padx=(5, 0))

        # вертикальный scroll фрагмента
        self.scrollbar = ttk.Scrollbar(self.info_frame, style='Vertical.TScrollbar')
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.txt_widget = Text(self.info_frame, yscrollcommand=self.scrollbar.set, font='Courier 12', cursor='arrow',
                               wrap=WORD, bg='#0E1621', fg='#fff', borderwidth=0)
        self.txt_widget.configure(state='disabled')  # для отмены возможности изменения текста
        self.txt_widget.pack(fill='both')
        self.scrollbar.config(command=self.txt_widget.yview)

        # horizontal scroll
        self.hor_scrollbar = ttk.Scrollbar(self.hor_scroll_frame_)
        self.hor_scrollbar.config(command=self.hor_scroll_frame.xview, orient=HORIZONTAL)
        self.hor_scrollbar.pack(side=BOTTOM, fill=X)
        self.hor_scroll_frame.configure(xscrollcommand=self.hor_scrollbar.set)

    def get_text_user_input(self):
        """Получение пользовательского ввода"""
        return self.ent_name.get()

    def set_new_text_user_input(self, text: str):
        """Установка текста в поле ввода пользователя с удалением ранее веденного текста"""
        self.ent_name.delete(0, END)
        self.ent_name.insert(END, text)

    def set_text_user_input(self, text: str):
        """Установка текста в конец поле ввода пользователя"""
        self.ent_name.insert(END, text)

    def new_buttons(self, buttons: list, func):
        """Установка новых кнопок с удалением старых"""
        self.clear_buttons()
        self.add_buttons(buttons, func)

    def add_buttons(self, buttons: list, func):
        """Установка новых кнопок в конец"""
        self.hor_scroll_frame.configure(state=NORMAL)
        for text in buttons:
            frame_button = Frame(self.hor_scroll_frame, bg='#0E1621')
            button = Button(frame_button, text=text, justify='center', bg='#1E2C3A', relief='flat', fg='#fff',
                            font='Candara 9', activebackground='#314050',
                            command=(lambda txt=text: func(name_variant=txt)))
            button.pack(padx=(0, 5), ipady=5, ipadx=5)
            self.hor_scroll_frame.window_create(END, window=frame_button)
        self.hor_scroll_frame.configure(state=DISABLED)

    def clear_buttons(self):
        """Удаление всех кнопок"""
        [i.destroy() for i in self.hor_scroll_frame.winfo_children()]

    def clear_text_user_input(self):
        """Очистка пользовательского ввода"""
        return self.ent_name.delete(0, END)

    def set_text_output(self, text: str):
        """Установка текста в конец поле вывода"""
        self.txt_widget.configure(state='normal')  # для возобновления возможности изменения текста
        self.txt_widget.insert('end', text + "\n")
        self.txt_widget.configure(state='disabled')  # для отмены возможности изменения текста

    def set_new_text_output(self, text: str):
        """Установка текста в поле вывода с удалением старого текста"""
        self.clear_text_output()
        self.set_text_output(text)

    def clear_text_output(self):
        """Очистка поля вывода"""
        self.txt_widget.configure(state='normal')  # для возобновления возможности изменения текста
        self.txt_widget.delete(1.0, END)
        self.txt_widget.configure(state='disabled')  # для отмены возможности изменения текста

    def show_choose_variants(self, variants: list):
        """Показ вариантов переходов по пирамиде в поле вывода"""
        str_list = "\n".join(f"{index + 1} " + variant for index, variant in enumerate(variants))
        self.set_new_text_output(f"Выберите вариант перехода по пирамиде:\n{str_list}")

    def show_object_variant(self, object_str: str):
        """Показ объекта в поле вывода"""
        self.set_new_text_output(object_str)

    def set_click_button_search(self, function):
        """Установка метода на нажатие кнопки поиска"""
        self.btn_search.bind('<Button-1>', function)
        self.ent_name.bind("<Return>", function)

    def set_image(self, image_src: str):
        # Замена картинки персонажа
        self.show_gif_animation = False
        image = Image.open(image_src)
        image = image.resize((90, 90), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.image_c = self.canvas.create_image(50, 55, anchor='center', image=self.photo)

    def set_image_dop(self, image_src: str):
        image = Image.open(image_src)
        image = image.resize((90, 90), Image.ANTIALIAS)
        self.photo_dop = ImageTk.PhotoImage(image)
        self.canvas_dop.delete("all")
        self.image_c_dop = self.canvas_dop.create_image(50, 55, anchor='center', image=self.photo_dop)

    def clear_image_dop(self):
        self.canvas_dop.delete("all")

    def set_image_gif(self, gif_src: str):
        # Замена картинки персонажа на gif
        count_frame = 128
        frames = [PhotoImage(file=gif_src, format='gif -index %i' % i) for i in range(count_frame)]
        self.show_gif_animation = True

        def update(ind):
            frame = frames[ind]
            ind += 8
            if ind >= count_frame:
                ind = 0
            if self.show_gif_animation:
                self.canvas.delete("all")
                self.image_c = self.canvas.create_image(50, 55, anchor='center', image=frame)
                self.root.after(100, update, ind)

        self.root.after(0, update, 0)

    def run_app(self):
        # запуск приложения
        self.root.mainloop()
