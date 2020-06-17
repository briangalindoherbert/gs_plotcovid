# encoding=utf-8
"""
cov_gui is a python gui to manage programs which analyze the covid19 epidemic
"""
from tkinter import *
# import matplotlib.animation as animation
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def getpltdata(pdc: pd.DataFrame):
    px = pdc.seq
    py = pdc.newdeaths
    pz = pdc.newcases
    return px,py,pz

class PlotClass:
    """ plotclass prepares a matplotlib chart for display with tk """
    def __init__(self, window, stpdc):
        self.box = Entry(window)
        self.button = Button(window, text="check", command=self.plot)
        self.box.pack()
        self.button.pack()
        self.pdc = stpdc

    def plot(self):
        px, py, pz = getpltdata(self.pdc)

        plt.scatter(py, px, color='red')
        plt.plot(pz, range(2 + max(px)), color='blue')
        plt.gca().invert_yaxis()

        plt.suptitle("Estimation Grid", fontsize=16)
        plt.ylabel("Y", fontsize=14)
        plt.xlabel("X", fontsize=14)
        plt.show()
        plt.gcf().canvas.draw()
        fig = plt.figure()
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().grid(row=1, column=24)
        canvas.draw()

window = Tk()
start = PlotClass(window)
