import pathlib
from pathlib import Path
from tkinter import *

from PIL import Image, ImageTk


class Application:
    def __init__(self):
        self.root = Tk()
        self.root.title('Бот секретарь школы №15 С УИОП г. Электросталь')
        self.root.geometry('820x550')
        self.root.wm_iconbitmap(bitmap=str(Path(pathlib.Path.cwd(), "media_files", "icon.ico")))
        self.root.resizable(width=False, height=False)

        # картинка
        self.image = Image.open(str(Path(pathlib.Path.cwd(), "media_files", "face1.png")))
        self.image = self.image.resize((82,82), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = Canvas(self.root, height=82, width=82)
        self.c_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.pack(side=LEFT, anchor=NW)

        # info frame
        self.info_frame = Frame(self.root, height=400, padx=15)
        self.info_frame.pack(fill=X, pady=(15, 5))

        # input frame
        self.input_frame = Frame(self.root, height=100, pady=10, padx=5)
        self.input_frame.pack(fill=X)

        # horizontal scroll frame
        self.hor_scroll_frame = Frame(self.root)
        self.hor_scroll_frame.pack(pady=(10, 0), padx=(0, 30), fill=X)

        self.lbl_name = Label(self.input_frame, text='Что вы хотите узнать', font=12)
        self.lbl_name.pack(side=LEFT)

        self.ent_name = Entry(self.input_frame, font=15, width=50)
        self.ent_name.focus()  # поле ввода сразу становится активным
        self.ent_name.pack(side=LEFT)

        Frame(self.root, width=10).pack(side=LEFT)  # Для отступа между полем ввода и кнопкой

        self.btn_search = Button(self.input_frame, text='Узнать', width=10)
        self.btn_search.pack(side=LEFT)

        # вертикальный скролл фрагмента
        self.scrollbar = Scrollbar(self.info_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.txt_widget = Text(self.info_frame, yscrollcommand=self.scrollbar.set, font=15, wrap=WORD)
        self.txt_widget.configure(state='disabled')  # для отмены возможности изменения текста
        self.txt_widget.pack(fill='both')
        self.scrollbar.config(command=self.txt_widget.yview)

        # горизонтальный скролл фрагмента
        self.hor_scrollbar = Scrollbar(self.hor_scroll_frame)
        self.hor_txt_widget = Text(self.hor_scroll_frame, height=1, font=12, wrap=NONE)
        self.hor_txt_widget.configure(xscrollcommand=self.hor_scrollbar.set)
        self.hor_txt_widget.configure(state='normal')  # для отмены возможности изменения текста
        self.hor_txt_widget.pack(fill='both')
        self.hor_scrollbar.config(command=self.hor_txt_widget.xview, orient=HORIZONTAL)
        self.hor_scrollbar.pack(side=BOTTOM, fill=X)

    def get_text_user_input(self):
        return self.ent_name.get()

    def clear_text_user_input(self):
        return self.ent_name.delete(0, END)

    def set_text_output(self, text: str):
        self.txt_widget.configure(state='normal')  # для возобновления возможности изменения текста
        self.txt_widget.insert('end', text + "\n")
        self.txt_widget.configure(state='disabled')  # для отмены возможности изменения текста

        # для горизонтального скролла
    def set_text_hor_scrollbar(self, text: str):
        self.hor_txt_widget.configure(state='normal')  # для возобновления возможности изменения текста
        self.hor_txt_widget.insert('end', text + "\n")
        self.hor_txt_widget.configure(state='disabled')  # для отмены возможности изменения текста

    def set_new_text_output(self, text: str):
        self.clear_text_output()
        self.set_text_output(text)

    def clear_text_output(self):
        self.txt_widget.configure(state='normal')  # для возобновления возможности изменения текста
        self.txt_widget.delete(1.0, END)
        self.txt_widget.configure(state='disabled')  # для отмены возможности изменения текста

    def show_choose_variants(self, variants: list):
        str_list = "\n".join(f"{index + 1} " + variant for index, variant in enumerate(variants))
        self.set_new_text_output(f"Выберите вариант перехода по пирамиде:\n{str_list}")

    def show_object_variant(self, object_str: str):
        self.set_new_text_output(object_str)

    def set_click_button(self, function):
        self.btn_search.bind('<Button-1>', function)
        self.ent_name.bind("<Return>", function)

    def set_image(self, image_src: str):
        # Замена картинки персонажа
        pass

    def set_image_gif(self, gif_src: str):
        # Замена картинки персонажа на gif
        pass

    def run_app(self):
        # запуск приложения
        self.root.mainloop()
