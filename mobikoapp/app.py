import tkinter as tk
from mobikoapp import version
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from tkinter import ttk
from PIL import Image
import time
import os


the_text = """
Select a PNG file of the size of 1024x1024 pixels.
"""

default_template = [
    (20, 1),
    (20, 2),
    (20, 3),
    (29, 1),
    (29, 2),
    (29, 3),
    (40, 1),
    (40, 2),
    (40, 3),
    (60, 2),
    (60, 3),
    (76, 1),
    (76, 2),
    (83.5, 2),
]


class App(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master,
            width=640,
            height=350,
            padding=32
            )

        self.style = ttk.Style()
        self.style.map("C.TButton",
            foureground=[('pressed', 'red'), ('active', 'blue')],
            backgroud=[('pressed', '!disabled', 'black'), ('active', 'white')]
            )

        self.total_steps = len(default_template)
        self.current_step = 0

        # Information of the process
        self.dirname = None

        self.grid()
        self.grid_propagate(0)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.columnconfigure(0, weight=1)

        self.label_text = ttk.Label(self, text=the_text)
        self.button_select = ttk.Button(self, text='Select image',
                                       command=self.select_file,
                                       style="C.TButton",
                                       )
        self.progress = ttk.Progressbar(self, length=350, mode='determinate')

        self.label_text.grid(sticky=tk.N)
        self.button_select.grid()
        #self.progress.grid()

    def select_file(self):
        self.filename = askopenfilename()

        if self.filename:
            self.process_template()

    def process_template(self):
        self.progress.grid()
        self.tmax = len(default_template)
        self.progress.maximum = 1.0
        
        self.dirname = os.path.dirname(self.filename)
        template = default_template
        basename = os.path.basename(self.filename)
        self.noextname = basename.split('.')[0]

        self.image = Image.open(self.filename)
        self.progress.grid()
        self.after(0, self.process_step)

    def process_step(self):
        t = default_template[self.current_step]
        size, scale = t
        absize = size * scale
        outfile = os.path.join(self.dirname, '{}-{}@{}x.png'\
                    .format(self.noextname, size, scale)
                  )

        img = self.image.resize((int(absize), int(absize)), Image.ANTIALIAS)
        img.save(outfile)

        self.progress.step(self.tmax)
        self.current_step += 1

        if self.current_step < self.total_steps - 1:
            self.after(25, self.process_step)

        else:
            showinfo('Finished', 'Conversion completed.')
            self.progress.grid_remove()




app = App()
app.master.title('Mobiko {}'.format(version))
app.master.resizable(False, False)
app.mainloop()