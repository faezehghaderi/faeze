# Ghaderi, Faezeh
# 1001-552-571
# 2018-11-25
# Assignment-05-01
import Ghaderi_05_02
import sys
import scipy.misc
import math
import sklearn.datasets
from sklearn.cluster import AgglomerativeClustering

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
import tensorflow as tf
import numpy.random as nprnd
#import tfgraphviz as tfg
import matplotlib as mpl


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
        self.Alpha = 1
        self.Learning_Rate=0.1
        self.Number_of_Nodes_in_Hidden_Layer = 100
        self.Number_of_Samples=20
        self.Numbe_of_Classes=4
        self.Lambda=0.01
        self.activation_type = "Relu"
        self.Type_of_generated_data= "s_curve"
 
    
        #########################################################################
        #  Set up the plotting frame and controls frame
        #########################################################################
        master.rowconfigure(0, weight=10, minsize=200)
        master.columnconfigure(0, weight=1)
        self.plot_frame = tk.Frame(self.master, borderwidth=10, relief=tk.SUNKEN)
        self.plot_frame.grid(row=0, column=0, columnspan=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.figure = plt.figure(figsize=(9.5,5))
        
        
    

        self.axes = self.figure.add_axes([0.15, 0.15, 0.6, 0.8])
        #self.axes = self.figure.add_axes()
        self.axes = self.figure.gca()
        
        # self.axes.margins(0.5)
        #self.axes.set_title("MSE")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)      
       
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        
        # Create a frame to contain all the controls such as sliders, buttons, ...
        self.controls_frame = tk.Frame(self.master)
        self.controls_frame.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        
        
        

        #########################################################################
        #  Set up the control widgets such as sliders and selection boxes
        #########################################################################
        self.Alpha_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                     from_=0.1, to_=1.0, resolution=.001, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", label="Alpha",
                                             command=lambda event: self.Alpha_slider_callback())
        self.Alpha_slider.set(self.Alpha)
        self.Alpha_slider.bind("<ButtonRelease-1>", lambda event: self.Alpha_slider_callback())
        self.Alpha_slider.grid(row=0, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        #-------------------------------
        self.Lambda = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                     from_=0.0, to_=1.0, resolution=0.01, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", label="Lambda",
                                             command=lambda event: self.Lambda_callback())
        self.Lambda.set(self.Learning_Rate)
        self.Lambda.bind("<ButtonRelease-1>", lambda event: self.Lambda_callback())
        self.Lambda.grid(row=1, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        #-------------------------------
        self.Number_of_Nodes_in_Hidden_Layer_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                     from_=1, to_=500, resolution=1, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", label="Num. of Nodes in Hidden Layer",
                                             command=lambda event: self.Number_of_Nodes_in_Hidden_Layer_slider_callback())
        self.Number_of_Nodes_in_Hidden_Layer_slider.set(self.Number_of_Nodes_in_Hidden_Layer)
        self.Number_of_Nodes_in_Hidden_Layer_slider.bind("<ButtonRelease-1>", lambda event: self.Number_of_Nodes_in_Hidden_Layer_slider_callback())
        self.Number_of_Nodes_in_Hidden_Layer_slider.grid(row=3, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        #-------------------------------
        self.Number_of_Samples_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                     from_=4, to_=1000, resolution=1, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", label="Number of Samples",
                                             command=lambda event: self.Number_of_Samples_slider_callback())
        self.Number_of_Samples_slider.set(self.Number_of_Samples)
        self.Number_of_Samples_slider.bind("<ButtonRelease-1>", lambda event: self.Number_of_Samples_slider_callback())
        self.Number_of_Samples_slider.grid(row=4, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        #-------------------------------
        self.Numbe_of_Classes_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                     from_=2, to_=10, resolution=1, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", label="Number of Classes",
                                             command=lambda event: self.Numbe_of_Classes_slider_callback())
        self.Numbe_of_Classes_slider.set(self.Numbe_of_Classes)
        self.Numbe_of_Classes_slider.bind("<ButtonRelease-1>", lambda event: self.Numbe_of_Classes_slider_callback())
        self.Numbe_of_Classes_slider.grid(row=5, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        #-------------------------------        
        #########################################################################
        #  Set up the frame for botton selection
        #########################################################################
        self.Adjust_Weights_button = tk.Button(self.controls_frame, text="Adjust Weights", fg="red", width=16,
                                     command=self.Adjust_Weights_callback)
        self.Reset_Weights_button = tk.Button(self.controls_frame, text="Reset Weights", fg="red", width=16,
                                        command=self.Reset_Weights_callback)

        self.Adjust_Weights_button.grid(row=0, column=4)
        self.Reset_Weights_button.grid(row=1, column=4)


        #########################################################################
        #  Set up the frame for drop down selection
        #########################################################################
        self.label_for_activation_function = tk.Label(self.controls_frame, text="Activation Function Type:",
                                                       justify="center")
        self.label_for_activation_function.grid(row=3, column=4, sticky=tk.N + tk.E + tk.S + tk.W)
        self.activation_function_variable = tk.StringVar()
        self.activation_function_dropdown = tk.OptionMenu(self.controls_frame, self.activation_function_variable,
                                                          "Relu", "Sigmoid", command=lambda
                event: self.activation_function_dropdown_callback())
        self.activation_function_variable.set("Relu")
        self.activation_function_dropdown.grid(row=3, column=5, sticky=tk.N + tk.E + tk.S + tk.W)



        self.label_for_Type_of_generated_data = tk.Label(self.controls_frame, text="Type of generated data:",
                                                       justify="center")
        self.label_for_Type_of_generated_data.grid(row=4, column=4, sticky=tk.N + tk.E + tk.S + tk.W)
        self.Type_of_generated_data_variable = tk.StringVar()
        self.Type_of_generated_data_dropdown = tk.OptionMenu(self.controls_frame, self.Type_of_generated_data_variable,
                                                          "s_curve", "blobs", "swiss_roll", "moons", command=lambda
                 event: self.Type_of_generated_data_dropdown_callback())
        self.Type_of_generated_data_variable.set("s_curve")
        self.Type_of_generated_data_dropdown.grid(row=4, column=5, sticky=tk.N + tk.E + tk.S + tk.W)


        
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
        self.initial_data()



     



    def Alpha_slider_callback(self):
        self.Alpha = np.int(self.Alpha_slider.get())

    def Lambda_callback(self):
        self.Learning_Rate = np.float(self.Lambda.get())
        
    def Number_of_Nodes_in_Hidden_Layer_slider_callback(self):
        self.Number_of_Nodes_in_Hidden_Layer = np.int(self.Number_of_Nodes_in_Hidden_Layer_slider.get())

    def Number_of_Samples_slider_callback(self):
        self.Number_of_Samples = np.int(self.Number_of_Samples_slider.get())

    def Numbe_of_Classes_slider_callback(self):
        self.Numbe_of_Classes = np.int(self.Numbe_of_Classes_slider.get())



    def Adjust_Weights_callback(self):
        self.Adjust_Weights()


    def Reset_Weights_callback(self):
        self.Reset_Weights()


    def Adjust_Weights_Direct_callback(self):
        self.Adjust_Weights_Direct()

    def activation_function_dropdown_callback(self):
        self.activation_type = self.activation_function_variable.get()

    def Type_of_generated_data_dropdown_callback(self):
        self.Type_of_generated_data = self.Type_of_generated_data_variable.get()
        
        
        
       
        
                      
    def generate_data(self,dataset_name, n_samples, n_classes):
        if dataset_name == 'swiss_roll':
            data = sklearn.datasets.make_swiss_roll(n_samples, noise=1.5, random_state=99)[0]
            data = data[:, [0, 2]]
        if dataset_name == 'moons':
            data = sklearn.datasets.make_moons(n_samples=n_samples, noise=0.15)[0]
        if dataset_name == 'blobs':
            data = sklearn.datasets.make_blobs(n_samples=n_samples, centers=n_classes*2, n_features=2, cluster_std=0.85*np.sqrt(n_classes), random_state=100)
            return data[0]/10., [i % n_classes for i in data[1]]
        if dataset_name == 's_curve':
            data = sklearn.datasets.make_s_curve(n_samples=n_samples, noise=0.15, random_state=100)[0]
            data = data[:, [0,2]]/3.0

    
        ward = AgglomerativeClustering(n_clusters=n_classes*2, linkage='ward').fit(data)
        return data[:]+np.random.randn(*data.shape)*0.03, [i % n_classes for i in ward.labels_]
    
    
    def initial_data(self):
        
        self.X, self.y = self.generate_data(self.Type_of_generated_data, self.Number_of_Samples, self.Numbe_of_Classes )
        min_x=np.amin(self.X, axis=0)
        max_x=np.amax(self.X, axis=0)
        self.min_x = min_x[0]
        self.max_x = max_x[0]
        self.min_y = min_x[1]
        self.max_y = max_x[1]
        self.display_error_epoch()

        
    def Reset_Weights(self):  
        self.axes.cla()
        self.initial_data() 
        self.Weight1 =self.init1
        self.Weight2 = self.init2
        self.bias1 = self.init_bias1
        self.bias2 = self.init_bias2
        
        
    def Adjust_Weights(self):
        self.axes.cla()
    
        #### initialize weights and biases
        tf.reset_default_graph()
        init1=np.random.uniform(size=2*self.Number_of_Nodes_in_Hidden_Layer)
        self.init1=np.reshape(init1,(self.Number_of_Nodes_in_Hidden_Layer,2))
        
        init2=np.random.uniform(size=self.Number_of_Nodes_in_Hidden_Layer*self.Numbe_of_Classes)
        self.init2=np.reshape(init2,(self.Numbe_of_Classes,self.Number_of_Nodes_in_Hidden_Layer))
        
        init_bias1=np.random.uniform(size=self.Number_of_Nodes_in_Hidden_Layer)
        self.init_bias1=np.reshape(init_bias1,(self.Number_of_Nodes_in_Hidden_Layer,1))
        
        init_bias2=np.random.uniform(size=self.Numbe_of_Classes)
        self.init_bias2=np.reshape(init_bias2,(self.Numbe_of_Classes,1))
        
        
        ######    Declaring placeholders and variables
        Train_input = tf.placeholder(dtype=tf.float64)
        Train_target = tf.placeholder(tf.int64)
       

        self.Weight1 = tf.Variable(self.init1, dtype=np.float64)
        self.Weight2 = tf.Variable(self.init2, dtype=np.float64)
        self.bias1 = tf.Variable(self.init_bias1, dtype=np.float64)
        self.bias2 = tf.Variable(self.init_bias2, dtype=np.float64)
        Alpha = tf.placeholder(dtype=np.float64)
        lamda= tf.placeholder(dtype=np.float64)
        
        ###### Calculations for training
        output1 = tf.matmul(self.Weight1, Train_input) + self.bias1

        actual = Ghaderi_05_02.calculate_activation_function(output1,self.activation_type)
        output2 = tf.matmul(self.Weight2, actual) + self.bias2
        

        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Train_target,logits=output2))
        regularizer= tf.nn.l2_loss(self.Weight2) +  tf.nn.l2_loss(self.Weight1)
        loss=tf.reduce_mean(loss + lamda*regularizer)
        optimizer=tf.train.GradientDescentOptimizer(Alpha).minimize(loss)
        train_prediction = tf.nn.softmax(output2)
        final_answer = tf.argmax(train_prediction)
        
        ###### meshgrid coordinates for testing the network
        res = 100;
 
        telorance_x = (self.max_x - self.min_x ) /20 
        telorance_y = (self.max_y - self.min_y ) /20 
        yy=np.linspace( self.min_y - telorance_y,  self.max_y + telorance_y, res)
        xx=np.linspace( self.min_x - telorance_x,  self.max_x + telorance_x, res)

        self.xx,self.yy= np.meshgrid(xx, yy)
    
        xx1=np.reshape(self.xx,(1,res*res))
        yy1=np.reshape(self.yy,(1,res*res))
        input_test=np.concatenate((xx1, yy1))


       ###### Testing and obtain the colors
        output_test1 = tf.matmul(self.Weight1, input_test) + self.bias1
        
        actual_test = Ghaderi_05_02.calculate_activation_function(output_test1,self.activation_type)
        output_test2 = tf.matmul(self.Weight2, actual_test) + self.bias2
    
        test_prediction =  tf.nn.softmax(output_test2)
        final_answer_test = tf.argmax(test_prediction)
        
        
        sess=tf.Session()
        # Run the initializer
        sess.run(tf.global_variables_initializer())
        with sess.as_default():
        
            input=np.transpose(self.X)
    
        
        #####   Running
            for i in range(40):
                opt,final=sess.run([optimizer,final_answer_test], feed_dict={Train_input: input, Train_target: self.y ,lamda : self.Learning_Rate, Alpha:self.Alpha})
                
    
                self.final_color=np.reshape(final,(res,res))
                
                print('yyyyyyyyyyyyyyy123',final) 
                print('final_color',self.final_color) 
                self.display_error_epoch1()
                self.display_error_epoch()
                
            sess.close()
            
        
        
        
    def display_error_epoch1(self):
        self.axes.cla()
        cmap = plt.get_cmap('PiYG') 
        self.axes.pcolormesh(self.xx, self.yy,  self.final_color, cmap=cmap)
        self.canvas.draw()        
   
    def display_error_epoch(self):
   
        X=self.X
        y=self.y
        
        self.axes.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Accent)
        plt.suptitle(self.Type_of_generated_data,fontsize=20)
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




def close_window_callback(root):
    if tk.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()



main_window = MainWindow(debug_print_flag=False)
main_window.geometry("700x900")
##main_window.wm_state('zoomed')
main_window.title('Assignment_05 --  Ghaderi')
##main_window.minsize(600, 600)
main_window.protocol("WM_DELETE_WINDOW", lambda root_window=main_window: close_window_callback(root_window))
main_window.mainloop()

