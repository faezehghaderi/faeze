# Ghaderi, Faezeh
# 1001-552-571
# 2018-10-07
# Assignment-03-01
import Ghaderi_03_02
import sys
import scipy.misc

if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import matplotlib
from sklearn.metrics import confusion_matrix
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import random
import os



class MainWindow(tk.Tk):
    """
    This class creates and controls the main window frames and widgets
    Farhad Kamangar 2018_06_03
    """


    def __init__(self, debug_print_flag=False):
        tk.Tk.__init__(self)
        self.debug_print_flag = debug_print_flag
        self.master_frame = tk.Frame(self)
        self.master_frame.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.rowconfigure(0, weight=1, minsize=500)
        self.columnconfigure(0, weight=1, minsize=500)
        # set the properties of the row and columns in the master frame
        # self.master_frame.rowconfigure(0, weight=1,uniform='xx')
        # self.master_frame.rowconfigure(1, weight=1, uniform='xx')
        self.master_frame.rowconfigure(2, weight=10, minsize=400, uniform='xx')
        self.master_frame.rowconfigure(3, weight=1, minsize=10, uniform='xx')
        self.master_frame.columnconfigure(0, weight=1, minsize=200, uniform='xx')
        ##self.master_frame.columnconfigure(1, weight=1, minsize=200, uniform='xx')
        # create all the widgets
        ##self.menu_bar = MenuBar(self, self.master_frame, background='orange')
        ##self.tool_bar = ToolBar(self, self.master_frame)
        ##self.left_frame = tk.Frame(self.master_frame)
        self.right_frame = tk.Frame(self.master_frame)
        ##self.status_bar = StatusBar(self, self.master_frame, bd=1, relief=tk.SUNKEN)
        # Arrange the widgets
        ##self.menu_bar.grid(row=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        ##self.tool_bar.grid(row=1, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        ##self.left_frame.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.right_frame.grid(row=2, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        ##self.status_bar.grid(row=3, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        # Create an object for plotting graphs in the left frame
        ##self.display_activation_functions = LeftFrame(self, self.left_frame, debug_print_flag=self.debug_print_flag)
        # Create an object for displaying graphics in the right frame
        self.display_graphics = RightFrame(self, self.right_frame, debug_print_flag=self.debug_print_flag)





class RightFrame:
    """
    This class is for creating right frame widgets which are used to draw graphics
    on canvas as well as embedding matplotlib figures in the tkinter.
    Farhad Kamangar 2018_06_03
    """



    def __init__(self, root, master, debug_print_flag=False):
        self.master = master
        self.root = root
        #########################################################################
        #  Set up the constants and default values
        #########################################################################
        self.alpha = 0.1
        self.second_weight = 1
        self.bias = 0.0
        self.error_final=[]
        self.epoch=[]
        self.ep=0.0
        self.xmin = 0
        self.xmax = 10
        self.ymin = 0
        self.ymax = 1
        self.debug_print_flag = debug_print_flag
        self.input_weight = 1
        self.bias = 0.0
        self.activation_type = "Hardlim"
        self.Learning_type = "Smoothing"
        #########################################################################
        #  Set up the plotting frame and controls frame
        #########################################################################
        master.rowconfigure(0, weight=10, minsize=200)
        master.columnconfigure(0, weight=1)
        self.plot_frame = tk.Frame(self.master, borderwidth=10, relief=tk.SUNKEN)
        self.plot_frame.grid(row=0, column=0, columnspan=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.figure = plt.figure(figsize=(8,5))
        self.axes = self.figure.add_axes([0.15, 0.15, 0.6, 0.8])
        # self.axes = self.figure.add_axes()
        self.axes = self.figure.gca()
        # self.axes.margins(0.5)
        self.axes.set_title("")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        # Create a frame to contain all the controls such as sliders, buttons, ...
        self.controls_frame = tk.Frame(self.master)
        self.controls_frame.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        #########################################################################
        #  Set up the control widgets such as sliders and selection boxes
        #########################################################################
        self.alpha_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                     from_=0.001, to_=1.0, resolution=0.01, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", label="Alpha",
                                             command=lambda event: self.alpha_slider_callback())
        self.alpha_slider.set(self.alpha)
        self.alpha_slider.bind("<ButtonRelease-1>", lambda event: self.alpha_slider_callback())
        self.alpha_slider.grid(row=0, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        #########################################################################
        #  Set up the frame for drop down selection
        #########################################################################
        self.label_for_activation_function = tk.Label(self.controls_frame, text="Activation Function Type:",
                                                       justify="center")
        self.label_for_activation_function.grid(row=3, column=4, sticky=tk.N + tk.E + tk.S + tk.W)
        self.activation_function_variable = tk.StringVar()
        self.activation_function_dropdown = tk.OptionMenu(self.controls_frame, self.activation_function_variable,
                                                          "Hardlim", "Tangent", "Linear", command=lambda
                event: self.activation_function_dropdown_callback())
        self.activation_function_variable.set("Hardlim")
        self.activation_function_dropdown.grid(row=3, column=5, sticky=tk.N + tk.E + tk.S + tk.W)

        self.label_for_Learning_method = tk.Label(self.controls_frame, text="learning method:",
                                                       justify="center")
        self.label_for_Learning_method.grid(row=4, column=4, sticky=tk.N + tk.E + tk.S + tk.W)
        self.Learning_method_variable = tk.StringVar()
        self.Learning_method_dropdown = tk.OptionMenu(self.controls_frame, self.Learning_method_variable,
                                                          "Smoothing", "Delta-rule", "Unsupervised-Hebb", command=lambda
                 event: self.Learning_method_dropdown_callback())
        self.Learning_method_variable.set("Smoothing")
        self.Learning_method_dropdown.grid(row=4, column=5, sticky=tk.N + tk.E + tk.S + tk.W)
        #########################################################################
        #  Set up the frame for botton selection
        #########################################################################
        self.Train_button = tk.Button(self.controls_frame, text="Train", fg="red", width=16,
                                     command=self.Training_method_callback)
        self.Randomize_weight_button = tk.Button(self.controls_frame, text="Randomize weight", fg="red", width=16,
                                        command=self.Randomize_callback)
        self.Confusion_matrix_button = tk.Button(self.controls_frame, text="Confusion_matrix", fg="red", width=16,
                                        command=self.Confusion_callback)
        self.Train_button.grid(row=1, column=4)
        self.Randomize_weight_button.grid(row=0, column=4)
        self.Confusion_matrix_button.grid(row=2, column=4)
        self.canvas.get_tk_widget().bind("<ButtonPress-1>", self.left_mouse_click_callback)
        self.canvas.get_tk_widget().bind("<ButtonPress-1>", self.left_mouse_click_callback)
        self.canvas.get_tk_widget().bind("<ButtonRelease-1>", self.left_mouse_release_callback)
        self.canvas.get_tk_widget().bind("<B1-Motion>", self.left_mouse_down_motion_callback)
        self.canvas.get_tk_widget().bind("<ButtonPress-3>", self.right_mouse_click_callback)
        self.canvas.get_tk_widget().bind("<ButtonRelease-3>", self.right_mouse_release_callback)
        self.canvas.get_tk_widget().bind("<B3-Motion>", self.right_mouse_down_motion_callback)
        self.canvas.get_tk_widget().bind("<Key>", self.key_pressed_callback)
        self.canvas.get_tk_widget().bind("<Up>", self.up_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Down>", self.down_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Right>", self.right_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Left>", self.left_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Shift-Up>", self.shift_up_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Shift-Down>", self.shift_down_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Shift-Right>", self.shift_right_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Shift-Left>", self.shift_left_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("f", self.f_key_pressed_callback)
        self.canvas.get_tk_widget().bind("b", self.b_key_pressed_callback)

    def read_one_image_and_convert_to_vector(self,infile):
        img = scipy.misc.imread(infile).astype(np.float32) # read image and convert to float
        return img.reshape(-1,1) # reshape to column vector and return it

    def data(self):

        path = 'Data\\'
        listing = os.listdir(path)
        Input_Vector=[]
        Target_Vector=[]
        Input_Vector_Train=[]
        Input_Vector_Test=[]
        Target_Vector_Train=[]
        Target_Vector_Test=[]
        for infile in listing:
            Target=np.zeros((10,1))
            if infile.endswith('.png'):
                pic1=self.read_one_image_and_convert_to_vector('Data/'+infile)
                pic1=np.append(pic1,[1])
                Input_Vector.append(pic1/127.5-1)
                out=int(infile[0])
                Target[out]=out
                Target_Vector.append(Target)
        X1=random.sample(range(1000), 800)
        X2=list(range(1000))
        for i in X1:
            if i in X2:
                X2.remove(i)
        for i in X1:
            Input_Vector_Train.append(Input_Vector[i])
            Target_Vector_Train.append(Target_Vector[i])
        for i in X2:
            Input_Vector_Test.append(Input_Vector[i])
            Target_Vector_Test.append(Target_Vector[i])
        self.Input_Vectors_Test=Input_Vector_Test
        self.Input_Vectors_Train=Input_Vector_Train
        self.Target_Vectors_Test=Target_Vector_Test
        self.Target_Vectors_Train=Target_Vector_Train




    def alpha_slider_callback(self):
        self.alpha = np.float(self.alpha_slider.get())
       

    def activation_function_dropdown_callback(self):
        self.activation_type = self.activation_function_variable.get()

    def Learning_method_dropdown_callback(self):
        self.Learning_type = self.Learning_method_variable.get()
  

    def Randomize_Weights_bias(self):
        rr=np.random.random((10,785))
        self.Weight=(rr*0.002)-0.001
        #self.axes.cla()
        self.epoch=0
        self.ep=0
        self.epoch=[]
        self.error_final=[]
# =============================================================================
#         self.figure = plt.figure(figsize=(8,5))
#         self.axes = self.figure.add_axes([0.15, 0.15, 0.6, 0.8])
#         self.axes = self.figure.gca()
#         self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
#         self.plot_widget = self.canvas.get_tk_widget()
#         self.plot_widget.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
# 
# =============================================================================
    # Train botton comes here
    def Training(self):
        self.figure = plt.figure(figsize=(8,5))
        self.axes = self.figure.add_axes([0.15, 0.15, 0.6, 0.8])
        self.axes = self.figure.gca()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        j=0
        self.data()

        while (j<10):

            self.ep=self.ep+1
            self.epoch.append(self.ep)
            j=j+1
            if (self.Learning_type=="Smoothing"):
                for idx, item in enumerate(self.Target_Vectors_Train):
                    ret=self.Input_Vectors_Train[idx]
                    ret = ret.reshape(785,1)
                    multiply=np.dot(item, np.transpose(ret))
                    self.Weight=self.Weight*(1-self.alpha)+self.alpha*multiply

                error_count=0
                for k in range(0,200):
                    output=self.Target_Vectors_Test[k]
                    ret=self.Input_Vectors_Test[k]
                    ret = ret.reshape(785,1)
                    actual1=np.dot(self.Weight,ret)
                    actual = Ghaderi_03_02.calculate_activation_function(actual1,
                                                     self.activation_type)
                    max=actual.argmax()
                    if max!=output.argmax():
                        error_count=error_count+1

                error=error_count/200
                self.error_final.append(error)


            elif (self.Learning_type=="Delta-rule"):
                for idx, item in enumerate(self.Target_Vectors_Train):
                    ret=self.Input_Vectors_Train[idx]
                    ret = ret.reshape(785,1)
                    actual1=np.dot(self.Weight,ret)
                    actual = Ghaderi_03_02.calculate_activation_function(actual1,
                                                     self.activation_type)
                    new_item=item-actual
                    multiply=np.dot(new_item, np.transpose(ret))
                    self.Weight=self.Weight+self.alpha*multiply

                error_count=0
                for k in range(0,200):
                    output = self.Target_Vectors_Test[k]
                    ret = self.Input_Vectors_Test[k]
                    ret = ret.reshape(785,1)
                    actual1 = np.dot(self.Weight,ret)
                    actual = Ghaderi_03_02.calculate_activation_function(actual1,
                                                     self.activation_type)

                    max = actual.argmax()
                    if max!=output.argmax():
                        error_count=error_count+1

                error=error_count/200
                self.error_final.append(error)


            elif (self.Learning_type=="Unsupervised-Hebb"):
                for idx, item in enumerate(self.Target_Vectors_Train):
                    ret=self.Input_Vectors_Train[idx]
                    ret = ret.reshape(785,1)
                    actual1=np.dot(self.Weight,ret)
                    actual = Ghaderi_03_02.calculate_activation_function(actual1,
                                                     self.activation_type)
                    multiply=np.dot(actual, np.transpose(ret))
                    self.Weight=self.Weight+self.alpha*multiply

                error_count=0
                for k in range(0,200):
                    output=self.Target_Vectors_Test[k]
                    ret=self.Input_Vectors_Test[k]
                    ret = ret.reshape(785,1)
                    actual1=np.dot(self.Weight,ret)
                    actual = Ghaderi_03_02.calculate_activation_function(actual1,
                                                     self.activation_type)

                    max=actual.argmax()
                    if max!=output.argmax():
                        error_count=error_count+1

                error=error_count/200
                self.error_final.append(error)
                

            self.display_error_epoch()

    def display_error_epoch(self):

        self.axes.cla()

        self.axes.set_xlabel('epoch')
        self.axes.set_ylabel('error')
        self.axes.scatter(self.epoch,self.error_final)
        self.axes.xaxis.set_visible(True)
        plt.xlim(self.xmin, self.ep)
        plt.ylim(self.ymin, self.ymax)
        self.canvas.draw()


    def Show_Confusion_Matrix(self):

        actual_max=[]
        target_max=[]
        for k in range(0,200):
            output=self.Target_Vectors_Test[k]
            ret=self.Input_Vectors_Test[k]
            ret = ret.reshape(785,1)
            actual1=np.dot(self.Weight,ret)
            actual = Ghaderi_03_02.calculate_activation_function(actual1,
                                                     self.activation_type)

            max1=actual.argmax()
            actual_max.append(max1)

            max2=output.argmax()
            target_max.append(max2)

        confusion = confusion_matrix(target_max,actual_max)


        self.axes.cla()

        min_val, max_val = 0, 10
        self.axes.matshow(confusion)
        for i in range(10):
            for j in range(10):
                c = confusion[i][j]
                self.axes.text(i, j, str(c), va='center', ha='center')
        
        self.canvas.draw()

    def key_pressed_callback(self, event):
        self.root.status_bar.set('%s', 'Key pressed')

    def up_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Up arrow was pressed")

    def down_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Down arrow was pressed")

    def right_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Right arrow was pressed")

    def left_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Left arrow was pressed")

    def shift_up_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Shift up arrow was pressed")

    def shift_down_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Shift down arrow was pressed")

    def shift_right_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Shift right arrow was pressed")

    def shift_left_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Shift left arrow was pressed")

    def f_key_pressed_callback(self, event):
        self.root.status_bar.set('%s', "f key was pressed")

    def b_key_pressed_callback(self, event):
        self.root.status_bar.set('%s', "b key was pressed")

    def left_mouse_click_callback(self, event):
        self.root.status_bar.set('%s', 'Left mouse button was clicked. ' + 'x=' + str(event.x) + '   y=' + str(
            event.y))
        self.x = event.x
        self.y = event.y
        self.canvas.focus_set()

    def left_mouse_release_callback(self, event):
        self.root.status_bar.set('%s',
                                 'Left mouse button was released. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
        self.x = None
        self.y = None

    def left_mouse_down_motion_callback(self, event):
        self.root.status_bar.set('%s', 'Left mouse down motion. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
        self.x = event.x
        self.y = event.y

    def right_mouse_click_callback(self, event):
        self.root.status_bar.set('%s', 'Right mouse down motion. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
        self.x = event.x
        self.y = event.y

    def right_mouse_release_callback(self, event):
        self.root.status_bar.set('%s',
                                 'Right mouse button was released. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
        self.x = None
        self.y = None

    def right_mouse_down_motion_callback(self, event):
        self.root.status_bar.set('%s', 'Right mouse down motion. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
        self.x = event.x
        self.y = event.y

    def left_mouse_click_callback(self, event):
        self.root.status_bar.set('%s', 'Left mouse button was clicked. ' + 'x=' + str(event.x) + '   y=' + str(
            event.y))
        self.x = event.x
        self.y = event.y

    # self.focus_set()
    def frame_resized_callback(self, event):
        print("frame resize callback")


    def redisplay(self, event):
        self.create_graphic_objects()

    def Randomize_callback(self):
        self.Randomize_Weights_bias()


    def Confusion_callback(self):
        self.Show_Confusion_Matrix()


    def Training_method_callback(self):
        self.Training()
        #self.root.status_bar.set('%s', "called the draw callback!")


def close_window_callback(root):
    if tk.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()



main_window = MainWindow(debug_print_flag=False)
main_window.geometry("580x600")
##main_window.wm_state('zoomed')
main_window.title('Assignment_01 --  Kamangar')
##main_window.minsize(600, 600)
main_window.protocol("WM_DELETE_WINDOW", lambda root_window=main_window: close_window_callback(root_window))
main_window.mainloop()

