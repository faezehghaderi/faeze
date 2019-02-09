# Ghaderi, Faezeh
# 1001-552-571
# 2018-10-29
# Assignment-04-01

import sys
import scipy.misc
import math

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
        self.ep=0.0
        self.xmin = 0
        self.xmax = 10
        self.ymin = 0
        self.ymax = 2
        self.debug_print_flag = debug_print_flag
        self.Number_of_Delayed_Elements = 10
        self.Learning_Rate=0.1
        self.Training_Sample_Size = 80
        self.Stride=1
        self.Number_of_Iterations=10
 
        #########################################################################
        #  Set up the plotting frame and controls frame
        #########################################################################
        master.rowconfigure(0, weight=10, minsize=200)
        master.columnconfigure(0, weight=1)
        self.plot_frame = tk.Frame(self.master, borderwidth=10, relief=tk.SUNKEN)
        self.plot_frame.grid(row=0, column=0, columnspan=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.figure = plt.figure(figsize=(6,4))
        self.plot_frame1 = tk.Frame(self.master, borderwidth=10, relief=tk.SUNKEN)
        self.plot_frame1.grid(row=0, column=1, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.figure1 = plt.figure(figsize=(6,4))
        self.axes = self.figure.add_axes([0.15, 0.15, 0.6, 0.8])
        self.axes = self.figure.add_axes()
        self.axes = self.figure.gca()
        
        self.axes1 = self.figure1.add_axes([0.15, 0.15, 0.6, 0.8])
        self.axes1 = self.figure1.add_axes()
        self.axes1 = self.figure1.gca()
        # self.axes.margins(0.5)
        self.axes.set_title("MSE")
        self.axes1.set_title("MAE")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas1 = FigureCanvasTkAgg(self.figure1, master=self.plot_frame)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        
        self.plot_widget = self.canvas1.get_tk_widget()
        self.plot_widget.grid(row=0, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
 
        # Create a frame to contain all the controls such as sliders, buttons, ...
        self.controls_frame = tk.Frame(self.master)
        self.controls_frame.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        #########################################################################
        #  Set up the control widgets such as sliders and selection boxes
        #########################################################################
        self.Number_of_Delayed_Elements_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                     from_=0.0, to_=100, resolution=1, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", label="Number of Delayed Elements",
                                             command=lambda event: self.Number_of_Delayed_Elements_slider_callback())
        self.Number_of_Delayed_Elements_slider.set(self.Number_of_Delayed_Elements)
        self.Number_of_Delayed_Elements_slider.bind("<ButtonRelease-1>", lambda event: self.Number_of_Delayed_Elements_slider_callback())
        self.Number_of_Delayed_Elements_slider.grid(row=0, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        #-------------------------------
        self.Learning_Rate_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                     from_=0.001, to_=1.0, resolution=0.01, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", label="Learning Rate",
                                             command=lambda event: self.Learning_Rate_slider_callback())
        self.Learning_Rate_slider.set(self.Learning_Rate)
        self.Learning_Rate_slider.bind("<ButtonRelease-1>", lambda event: self.Learning_Rate_slider_callback())
        self.Learning_Rate_slider.grid(row=1, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        #-------------------------------
        self.Training_Sample_Size_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                     from_=0, to_=100, resolution=1, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", label="Training Sample Size",
                                             command=lambda event: self.Training_Sample_Size_slider_callback())
        self.Training_Sample_Size_slider.set(self.Training_Sample_Size)
        self.Training_Sample_Size_slider.bind("<ButtonRelease-1>", lambda event: self.Training_Sample_Size_slider_callback())
        self.Training_Sample_Size_slider.grid(row=3, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        #-------------------------------
        self.Stride_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                     from_=1, to_=100, resolution=1, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", label="Stride",
                                             command=lambda event: self.Stride_slider_callback())
        self.Stride_slider.set(self.Stride)
        self.Stride_slider.bind("<ButtonRelease-1>", lambda event: self.Stride_slider_callback())
        self.Stride_slider.grid(row=4, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        #-------------------------------
        self.Number_of_Iterations_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                     from_=1, to_=100, resolution=1, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", label="Number of Iterations",
                                             command=lambda event: self.Number_of_Iterations_slider_callback())
        self.Number_of_Iterations_slider.set(self.Number_of_Iterations)
        self.Number_of_Iterations_slider.bind("<ButtonRelease-1>", lambda event: self.Number_of_Iterations_slider_callback())
        self.Number_of_Iterations_slider.grid(row=5, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        #-------------------------------        
        #########################################################################
        #  Set up the frame for botton selection
        #########################################################################
        self.Set_Weights_to_Zero_button = tk.Button(self.controls_frame, text="Set Weights to Zero", fg="red", width=16,
                                     command=self.Set_Weights_to_Zero_callback)
        self.Adjust_Weights_LMS_button = tk.Button(self.controls_frame, text="Adjust Weights (LMS)", fg="red", width=16,
                                        command=self.Adjust_Weights_LMS_callback)
        self.Adjust_Weights_Direct_button = tk.Button(self.controls_frame, text="Adjust Weights(Direct)", fg="red", width=16,
                                        command=self.Adjust_Weights_Direct_callback)
        self.Set_Weights_to_Zero_button.grid(row=0, column=4)
        self.Adjust_Weights_LMS_button.grid(row=1, column=4)
        self.Adjust_Weights_Direct_button.grid(row=2, column=4)
        
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

    def read_csv_as_matrix(self,file_name):
        # Each row of data in the file becomes a row in the matrix
        # So the resulting matrix has dimension [num_samples x sample_dimension]
        data = np.loadtxt(file_name, skiprows=1, delimiter=',', dtype=np.float32)
       
        return data

    def data_price_volume(self):
        data = self.read_csv_as_matrix('data.csv')
        self.data_normalize = 2*((data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0)))-1

    def data(self):

        self.data_price_volume()
        #dividing data into training and test parts based on training sample size
        s=int(self.data_normalize.shape[0]*self.Training_Sample_Size/100)
        data_train=np.array_split(self.data_normalize, [s])
        self.train=data_train[0]
        self.test=data_train[1]
        
        self.Target_Vectors_Train=[]
        self.Input_Vectors_Train=[]
        self.Target_Vectors_Test=[]
        self.Input_Vectors_Test=[]
        #creating one sample input for train and test 
        r=int((self.train.shape[0]-self.Number_of_Delayed_Elements-1)/self.Stride)
        for k in range(0,r):
            current=self.Number_of_Delayed_Elements+(k*self.Stride)
            self.Target_Vectors_Train.append(self.train[current+1,0])        
            input_train=[]
            
            for i in range(0,self.Number_of_Delayed_Elements+1):
                input_train.append(self.train[current-i,0])
                input_train.append(self.train[current-i,1])            
            input_train.append(1)
            self.Input_Vectors_Train.append(input_train)
        #-----------------------------------
        r=(self.test.shape[0]-self.Number_of_Delayed_Elements-1)
        for k in range(0,r):
            current=self.Number_of_Delayed_Elements+k
            self.Target_Vectors_Test.append(self.test[current+1,0])        
            input_test=[]
            for i in range(0,self.Number_of_Delayed_Elements+1):
                input_test.append(self.test[current-i,0])
                input_test.append(self.test[current-i,1])            
            input_test.append(1)
            self.Input_Vectors_Test.append(input_test)
        



    def Number_of_Delayed_Elements_slider_callback(self):
        self.Number_of_Delayed_Elements = np.int(self.Number_of_Delayed_Elements_slider.get())

    def Learning_Rate_slider_callback(self):
        self.Learning_Rate = np.float(self.Learning_Rate_slider.get())
        
    def Training_Sample_Size_slider_callback(self):
        self.Training_Sample_Size = np.int(self.Training_Sample_Size_slider.get())

    def Stride_slider_callback(self):
        self.Stride = np.int(self.Stride_slider.get())

    def Number_of_Iterations_slider_callback(self):
        self.Number_of_Iterations = np.int(self.Number_of_Iterations_slider.get())



    def Set_Weights_to_Zero_callback(self):
        self.Set_Weights_to_Zero()


    def Adjust_Weights_LMS_callback(self):
        self.Adjust_Weights_LMS()


    def Adjust_Weights_Direct_callback(self):
        self.Adjust_Weights_Direct()



    def Set_Weights_to_Zero(self):
        #added with biases
        self.No_of_samples=self.Number_of_Delayed_Elements*2+2
        s=(1,self.No_of_samples+1) 
        self.Weight=np.zeros(s)



    def Adjust_Weights_LMS(self):
        self.data()
        j=0
        self.ep=[]
        self.error_MSE=[]
        self.error_MAE=[]
        while (j<self.Number_of_Iterations):
            for i in range(0,len(self.Input_Vectors_Train)):
                a=np.dot(self.Weight,self.Input_Vectors_Train[i])
                e=self.Target_Vectors_Train[i]-a
                self.Weight=self.Weight+2*self.Learning_Rate*e*np.transpose(self.Input_Vectors_Train[i])
            j=j+1
            self.ep.append(j)
            #calculating error
            error_MSE=[]
            error_MAE=[]
            for i in range(0,len(self.Input_Vectors_Test)):
                a=np.dot(self.Weight,self.Input_Vectors_Test[i])
                e=self.Target_Vectors_Test[i]-a
                error_MSE.append(math.pow(e,2))
                error_MAE.append(e)
            error_MSE=np.mean(error_MSE)
            error_MAE=np.max(error_MAE)
            self.error_MSE.append(error_MSE)
            self.error_MAE.append(error_MAE)
            
            self.display_error_epoch()
        print ('self.error_MSE-LMS',self.error_MSE)
        print ('self.error_MAE-LMS',self.error_MAE)
    def Adjust_Weights_Direct(self):
        self.data()
        h_train=[]
        R_train=[]
        self.ep=[1]
        #calculating list of tz and zz
        for i in range(0,int(len(self.Input_Vectors_Train))):
            h=self.Target_Vectors_Train[i]*np.transpose(self.Input_Vectors_Train[i])
            
            h_train.append(h)
            self.Input_Vectors_Train[i]=np.reshape(self.Input_Vectors_Train[i],(self.Number_of_Delayed_Elements*2+3,1))
            R=np.dot(self.Input_Vectors_Train[i],np.transpose(self.Input_Vectors_Train[i]))
            R_train.append(R)
        
        #calculating h=e[tz]
        mean_tz=[]
        for k in range(0,self.Number_of_Delayed_Elements*2+3):
            sum=0
            for e in range(0,int(len(self.Input_Vectors_Train))):
            
                s=h_train[e]
                
                sum=sum+s[k]
            mean_tz.append(sum/len(self.Input_Vectors_Train)) 
        mean_tz=np.reshape(mean_tz,(self.Number_of_Delayed_Elements*2+3,1))    
        
        #calculating R=e[zz]
        mean_zz=np.zeros((self.Number_of_Delayed_Elements*2+3, self.Number_of_Delayed_Elements*2+3))
        for k in range(0,self.Number_of_Delayed_Elements*2+3):
            for o in range(0,self.Number_of_Delayed_Elements*2+3):
                sum=0
                for g in range(0,int(len(self.Input_Vectors_Train))):
            
                    sg=R_train[g]
                
                    sum=sum+sg[k,o]
                mean_zz[k,o]=(sum/len(self.Input_Vectors_Train)) 
        
        #calculating W=R(-1).h
        R_inv=np.linalg.inv(mean_zz)
        self.Weight=np.transpose( np.dot(R_inv,mean_tz))
        #calculating error
        error_MAE=[]
        error_MSE=[]
        for i in range(0,int(len(self.Input_Vectors_Test))):
            a=np.dot(self.Weight,np.transpose(self.Input_Vectors_Test[i]))
            e=self.Target_Vectors_Test[i]-a  
            error_MSE.append(math.pow(e,2))
            error_MAE.append(e)
        error_MSE=np.mean(error_MSE)
        error_MAE=np.max(error_MAE)
        self.error_MSE=[error_MSE]
        self.error_MAE=[error_MAE]
        self.display_error_epoch()
        print ('self.error_MSE-direct',self.error_MSE)
        print ('self.error_MAE-direct',self.error_MAE)

    def display_error_epoch(self):

        self.axes.cla()
        
        self.axes.set_title("MSE")
        self.axes.set_xlabel('epoch')
        self.axes.set_ylabel('error')
        self.axes.scatter(self.ep,self.error_MSE)
        self.axes.xaxis.set_visible(True)
        self.axes.set_ylim([0,2])
        self.canvas.draw()
        
        self.axes1.cla()
        self.axes1.set_title("MAE")
        self.axes1.set_xlabel('epoch')
        self.axes1.set_ylabel('error')
        self.axes1.scatter(self.ep,self.error_MAE)
        self.axes1.xaxis.set_visible(True)
        self.axes1.set_ylim([0,2])

        self.canvas1.draw()


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




def close_window_callback(root):
    if tk.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()



main_window = MainWindow(debug_print_flag=False)
main_window.geometry("900x700")
##main_window.wm_state('zoomed')
main_window.title('Assignment_01 --  Kamangar')
##main_window.minsize(600, 600)
main_window.protocol("WM_DELETE_WINDOW", lambda root_window=main_window: close_window_callback(root_window))
main_window.mainloop()

