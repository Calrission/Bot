import pathlib
from pathlib import Path
from tkinter import *

from PIL import Image, ImageTk


class Application:
    def __init__(self):
        self.photo = None
        self.image_c = None
        self.show_gif_animation = False
        self.root = Tk()
        self.root.title('Бот секретарь школы №15 С УИОП г. Электросталь')
        self.root.geometry('700x500')
        self.root.wm_iconbitmap(bitmap=str(Path(pathlib.Path.cwd(), "media_files", "icon.ico")))
        self.root.resizable(width=False, height=False)
        # self.root.wm_attributes('-transparentcolor', '#ab23ff')

        self.label = Label(self.root, width=100, height=100, bg="red")  # задний frame
        self.label.pack()

        # top frame
        self.info_frame = Frame(self.label, height=400, padx=0, bg="")
        self.info_frame.pack(fill=X, pady=(5, 5))

        # bottom frame
        self.input_frame = Frame(self.label, height=100, pady=10, padx=5, bg="")
        self.input_frame.pack(fill=X)

        self.canvas = Canvas(self.info_frame, height=120, width=100)
        self.canvas.pack(side=LEFT, anchor=NW, padx=(5, 0), pady=(0, 0))

        self.ent_name = Entry(self.input_frame, font=15, width=68)
        self.ent_name.focus()  # поле ввода сразу становится активным
        self.ent_name.pack(side=LEFT)

        Frame(self.label, width=10).pack(side=LEFT)  # Для отступа между полем ввода и кнопкой

        self.btn_search = Button(self.input_frame, text='Узнать', width=10)
        self.btn_search.pack(side=LEFT)

        # Скролл фрагмента
        self.scrollbar = Scrollbar(self.info_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.txt_widget = Text(self.info_frame, yscrollcommand=self.scrollbar.set, font=15, wrap=WORD)
        self.txt_widget.configure(state='disabled')  # для отмены возможности изменения текста
        self.txt_widget.pack(fill='both')
        self.scrollbar.config(command=self.txt_widget.yview)

    def get_text_user_input(self):
        return self.ent_name.get()

    def clear_text_user_input(self):
        return self.ent_name.delete(0, END)

    def set_text_output(self, text: str):
        self.txt_widget.configure(state='normal')  # для возобновления возможности изменения текста
        self.txt_widget.insert('end', text + "\n")
        self.txt_widget.configure(state='disabled')  # для отмены возможности изменения текста

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
        self.show_gif_animation = False
        image = Image.open(image_src)
        image = image.resize((90, 90), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.delete("all")
        self.image_c = self.canvas.create_image(50, 55, anchor='center', image=self.photo)

    def set_image_gif(self, gif_src: str):
        # Замена картинки персонажа на gif
        count_frame = 128
        frames = [PhotoImage(file=gif_src, format='gif -index %i' % i) for i in range(count_frame)]
        self.show_gif_animation = True

        def update(ind):
            frame = frames[ind]
            ind += 5
            if ind >= count_frame:
                ind = 0
            if self.show_gif_animation:
                self.canvas.delete("all")
                self.image_c = self.canvas.create_image(50, 55, anchor='center', image=frame)
                self.root.after(100, update, ind)
        self.root.after(0, update, 0)

    def set_background_gif(self, gif_src: str):
        count_frame = 128
        frames = [PhotoImage(file=gif_src, format='gif -index %i' % i) for i in range(count_frame)]
        self.show_gif_animation = True

        def update(ind):
            frame = frames[ind]
            ind += 5
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
