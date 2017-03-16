# -*- coding: utf-8 -*-

from tkSimpleDialog import *
from tkFileDialog import *
from tkMessageBox import *

__author__ = 'Ivan Kamynin'


class Shutdown(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(expand=YES, fill=BOTH, side=LEFT)

    def quit(self):
        ans = askokcancel('Подтверждение выхода', "Sure you want to Quit?")
        if ans: Frame.quit(self)


class ScrolledText(Frame):

    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.make_widgets()
        self.set_text(text, file)

    def make_widgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = text

    def set_text(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()

    def get_text(self):
        return self.text.get('1.0', END+'-1c')


class ABCTextEditor(ScrolledText):

    def __init__(self, parent=None, file=None):
        frm = Frame(parent)
        frm.pack(fill=X)
        Button(frm, text='Save', command=self.on_save).pack(side=LEFT)
        Button(frm, text='Cut', command=self.on_cut).pack(side=LEFT)
        Button(frm, text='Paste', command=self.on_paste).pack(side=LEFT)
        Shutdown(frm).pack(side=LEFT)
        ScrolledText.__init__(self, parent, file=file)
        self.text.config(font=('courier', 9, 'normal'))

    def on_save(self):
        filename = asksaveasfilename()
        if filename:
            all_text = self.get_text()
            open(filename, 'w').write(all_text)

    def on_cut(self):
        text = self.text.get(SEL_FIRST, SEL_LAST)
        self.text.delete(SEL_FIRST, SEL_LAST)
        self.clipboard_clear()
        self.clipboard_append(text)

    def on_paste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass

if __name__ == '__main__':

    # if there are no cmdline arguments, open a new file.
    if len(sys.argv) > 1:
        ABCTextEditor(file=sys.argv[1]).mainloop()
    else:
        ABCTextEditor().mainloop()