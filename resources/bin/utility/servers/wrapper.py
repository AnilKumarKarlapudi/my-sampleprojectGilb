import threading
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk

from libs.infra.remote import configurator
from libs.infra.remote import persistence
from libs.infra.remote.models import Instance
from libs.infra.remote.models import Service


def waiting(win: tkinter.Tk):
    mainframe = win.nametowidget('mainFrame')
    mainframe.pack_forget()

    loading = win.nametowidget('loadingFrame')
    loading.pack()

    progress = win.nametowidget('loadingFrame.progress')
    progress.start()

    win.update()


def hide_loading(win: tkinter.Tk):
    loading = win.nametowidget('loadingFrame')
    loading.pack_forget()

    mainframe = win.nametowidget('mainFrame')
    mainframe.pack()

    progress = win.nametowidget('loadingFrame.progress')
    progress.stop()

    win.update()


def import_json(win: tkinter.Tk):
    def __inner__():
        fp_config = tkinter.filedialog.askopenfile(mode='r', filetypes=[("JSON Files", "*.json")])

        if not fp_config:
            return

        try:
            waiting(win)
            task = threading.Thread(target=configurator.loads, args=(fp_config,))
            task.start()
            while task.is_alive():
                win.update()

            hide_loading(win)
            tkinter.messagebox.showinfo("JSON Configurations", "Configurations loaded!")
        except Exception as ex:
            hide_loading(win)
            tkinter.messagebox.showerror("An error has occurred", f"Cannot import configurations due to: {ex}")
            raise ex

    return __inner__


def show_configurations():
    try:
        fp_report = tkinter.filedialog.asksaveasfile(mode='w',
                                                     initialfile='ip-setup-configuration',
                                                     defaultextension="*.json",
                                                     filetypes=[("JSON", "*.json")])
        if not fp_report:
            return

        configurator.report(fp_report)
        tkinter.messagebox.showinfo("Report", "New configuration report was created successfully!")
    except Exception as ex:
        tkinter.messagebox.showerror("An error has occurred", f"Cannot export configuration due to: {ex}")


def check_exit(win: tkinter.Tk):
    def __inner__():
        db = persistence.get_connection()
        tables = db.get_tables()
        if not all([table in tables for table in ['instance', 'service']]):
            tkinter.messagebox.showerror("Cannot exit!", "No IP configuration was found!")
            return
        elif Instance.select().count() == 0 or Service.select().count() == 0:
            tkinter.messagebox.showerror("Cannot exit!", "Empty configuration tables!")
            return
        else:
            win.destroy()
    return __inner__
