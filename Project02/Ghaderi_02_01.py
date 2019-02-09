# Ghaderi, Faezeh
# 1001-552-571
# 2018-09-24
# Assignment-02-01
import Ghaderi_02_02
import sys

if sys.version_info[0] < 3:
	import Tkinter as tk
else:
	import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt  # Required import
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.backends.tkagg as tkagg
import random 
import numpy as np
import matplotlib.pyplot as plt
import time


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
		self.root = root
		self.master = master
		self.first_weight = 1
		self.second_weight = 1
		self.bias = 0.0
		self.debug_print_flag = debug_print_flag
		width_px = root.winfo_screenwidth()
		height_px = root.winfo_screenheight()
		width_mm = root.winfo_screenmmwidth()
		height_mm = root.winfo_screenmmheight()
		# 2.54 cm = in
		width_in = width_mm / 25.4
		height_in = height_mm / 25.4
		width_dpi = width_px / width_in
		height_dpi = height_px / height_in
		self.activation_type = "Hardlim"        
		if self.debug_print_flag:
			print('Width: %i px, Height: %i px' % (width_px, height_px))
			print('Width: %i mm, Height: %i mm' % (width_mm, height_mm))
			print('Width: %f in, Height: %f in' % (width_in, height_in))
			print('Width: %f dpi, Height: %f dpi' % (width_dpi, height_dpi))
		# self.canvas = self.master.canvas
		#########################################################################
		#  Set up the plotting frame and controls frame
		#########################################################################
		master.rowconfigure(0, weight=100, minsize=200)
		master.columnconfigure(0, weight=1)
		master.rowconfigure(1, weight=1, minsize=20)
		self.right_frame = tk.Frame(self.master, borderwidth=1, relief='sunken')
		self.right_frame.grid(row=0, column=0, columnspan=1, sticky=tk.N + tk.E + tk.S + tk.W)
		self.matplotlib_width_pixel = self.right_frame.winfo_width()
		self.matplotlib_height_pixel = self.right_frame.winfo_height()
		# set up the frame which contains controls such as sliders and buttons
		self.controls_frame = tk.Frame(self.master)
		self.controls_frame.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
		self.controls_frame.rowconfigure(1, weight=1, minsize=20)
		#########################################################################
		#  Set up the control widgets such as sliders and selection boxes  form left side 
		#########################################################################
		self.first_weight_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
		                                    from_=-10.0, to_=10.0, resolution=0.01, bg="#DDDDDD",
		                                    activebackground="#FF0000", highlightcolor="#00FFFF", label="first weight",
		                                    command=lambda event: self.first_weight_slider_callback())
		self.first_weight_slider.set(self.first_weight)
		self.first_weight_slider.bind("<ButtonRelease-1>", lambda event: self.first_weight_slider_callback())
		self.first_weight_slider.grid(row=0, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
		self.second_weight_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
		                                    from_=-10.0, to_=10.0, resolution=0.01, bg="#DDDDDD",
		                                    activebackground="#FF0000", highlightcolor="#00FFFF", label="second weight",
		                                    command=lambda event: self.second_weight_slider_callback())
		self.second_weight_slider.set(self.second_weight)
		self.second_weight_slider.bind("<ButtonRelease-1>", lambda event: self.second_weight_slider_callback())
		self.second_weight_slider.grid(row=1, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
		self.bias_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL, from_=-10.0,
		                            to_=10.0, resolution=0.01, bg="#DDDDDD", activebackground="#FF0000",
		                            highlightcolor="#00FFFF", label="Bias",
		                            command=lambda event: self.bias_slider_callback())
		self.bias_slider.set(self.bias)
		self.bias_slider.bind("<ButtonRelease-1>", lambda event: self.bias_slider_callback())
		self.bias_slider.grid(row=2, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
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
		##################################################################################
		self.Train_button = tk.Button(self.controls_frame, text="Train", fg="red", width=16,
		                             command=self.graphics_draw_callback)
		self.create_sample_button = tk.Button(self.controls_frame, text="Create Sample Data", fg="red", width=16,
		                                command=self.matplotlib_plot_2d_callback)
		self.Train_button.grid(row=0, column=4)
		self.create_sample_button.grid(row=1, column=4)
		self.right_frame.update()
		#self.canvas = tk.Canvas(self.right_frame, relief='ridge', width=self.right_frame.winfo_width() - 50,
		#                        height=self.right_frame.winfo_height())        
		self.canvas = tk.Canvas(self.right_frame, relief='ridge', width=1100,
		                        height=800)
		self.canvas.rowconfigure(0, weight=1)
		self.canvas.columnconfigure(0, weight=1)
		self.canvas.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
		self.canvas.bind("<ButtonPress-1>", self.left_mouse_click_callback)
		self.canvas.bind("<ButtonRelease-1>", self.left_mouse_release_callback)
		self.canvas.bind("<B1-Motion>", self.left_mouse_down_motion_callback)
		self.canvas.bind("<ButtonPress-3>", self.right_mouse_click_callback)
		self.canvas.bind("<ButtonRelease-3>", self.right_mouse_release_callback)
		self.canvas.bind("<B3-Motion>", self.right_mouse_down_motion_callback)
		self.canvas.bind("<Key>", self.key_pressed_callback)
		self.canvas.bind("<Up>", self.up_arrow_pressed_callback)
		self.canvas.bind("<Down>", self.down_arrow_pressed_callback)
		self.canvas.bind("<Right>", self.right_arrow_pressed_callback)
		self.canvas.bind("<Left>", self.left_arrow_pressed_callback)
		self.canvas.bind("<Shift-Up>", self.shift_up_arrow_pressed_callback)
		self.canvas.bind("<Shift-Down>", self.shift_down_arrow_pressed_callback)
		self.canvas.bind("<Shift-Right>", self.shift_right_arrow_pressed_callback)
		self.canvas.bind("<Shift-Left>", self.shift_left_arrow_pressed_callback)
		self.canvas.bind("f", self.f_key_pressed_callback)
		self.canvas.bind("b", self.b_key_pressed_callback)
		# Create a figure for 2d plotting
		self.matplotlib_2d_fig = mpl.figure.Figure()
		self.matplotlib_2d_fig.set_size_inches(4.4,3.4)
		self.matplotlib_2d_fig.set_size_inches((self.right_frame.winfo_width() / width_dpi) - 0.5,
		                                      self.right_frame.winfo_height() / height_dpi)
		self.matplotlib_2d_ax = self.matplotlib_2d_fig.add_axes([.1, .1, .7, .7])
		if self.debug_print_flag:
			print("Matplotlib figsize in inches: ", (self.right_frame.winfo_width() / width_dpi) - 0.5,
			      self.right_frame.winfo_height() / height_dpi)
		self.matplotlib_2d_fig_x, self.matplotlib_2d_fig_y = 0, 0
		self.matplotlib_2d_fig_loc = (self.matplotlib_2d_fig_x, self.matplotlib_2d_fig_y)
		# fig = plt.figure()
		# ax = fig.gca(projection='3d')
		

	def first_weight_slider_callback(self):
		self.first_weight = np.float(self.first_weight_slider.get())          
		self.display_matplotlib_figure_on_tk_canvas()

	def second_weight_slider_callback(self):
		self.second_weight = np.float(self.second_weight_slider.get())          
		self.display_matplotlib_figure_on_tk_canvas()

	def bias_slider_callback(self):
		self.first_weight = np.float(self.bias_slider.get())          
		self.display_matplotlib_figure_on_tk_canvas()        

	def activation_function_dropdown_callback(self):
		self.activation_type = self.activation_function_variable.get()
		#self.display_activation_function()       

	def sample_point_creation(self):

		self.X1 = np.random.uniform(-10, 10, size=2)
		self.Y1 = np.random.uniform(-10, 10, size=2)
		self.X2 = np.random.uniform(-10, 10, size=2)
		self.Y2 = np.random.uniform(-10, 10, size=2)

	def initialize_points(self):

		self.matplotlib_2d_ax.scatter(self.X1, self.Y1,7)
		self.matplotlib_2d_ax.scatter(self.X2, self.Y2,8)
		self.X_points = np.concatenate([self.X1, self.X2])
		self.Y_points = np.concatenate([self.Y1, self.Y2])
		self.matplotlib_2d_ax.set_xlim([-10, 10])
		self.matplotlib_2d_ax.set_ylim([-10, 10])
		# plt.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)
		# Place the matplotlib figure on canvas and display it
		self.matplotlib_2d_figure_canvas_agg = FigureCanvasAgg(self.matplotlib_2d_fig)
		self.matplotlib_2d_figure_canvas_agg.draw()
		self.matplotlib_2d_figure_x, self.matplotlib_2d_figure_y, self.matplotlib_2d_figure_w, \
		self.matplotlib_2d_figure_h = self.matplotlib_2d_fig.bbox.bounds
		self.matplotlib_2d_figure_w, self.matplotlib_2d_figure_h = int(self.matplotlib_2d_figure_w), int(
			self.matplotlib_2d_figure_h)
		self.photo = tk.PhotoImage(master=self.canvas, width=self.matplotlib_2d_figure_w,
		                           height=self.matplotlib_2d_figure_h)
		
	
	
	# Position: convert from top-left anchor to center anchor
		self.canvas.create_image(self.matplotlib_2d_fig_loc[0] + self.matplotlib_2d_figure_w / 2,
		                         self.matplotlib_2d_fig_loc[1] + self.matplotlib_2d_figure_h / 2, image=self.photo)
								 
								 
		tkagg.blit(self.photo, self.matplotlib_2d_figure_canvas_agg.get_renderer()._renderer, colormode=2)
	
	
	
	
	
	def display_matplotlib_figure_on_tk_canvas(self):
		
		fig = plt.figure()
		ax = fig.gca()

		#self.matplotlib_2d_ax.clear()
		
		w0 = self.first_weight
		w1 = self.second_weight
		bias = self.bias
		
		xx=np.linspace(-10., 10, 200)
		yy=np.linspace(-10., 10, 200)

		xx,yy= np.meshgrid(xx, yy)
		colors=["red", "green"]
		cmap = matplotlib.colors.ListedColormap(colors)
		input_values=w0*xx+w1*yy+bias
		activation2 = Ghaderi_02_02.calculate_activation_function(input_values,
		                                                          self.activation_type)
		self.matplotlib_2d_ax.pcolormesh(xx, yy, activation2, cmap=cmap)     
		self.sample_point_creation()
		self.initialize_points()
		
		self.matplotlib_2d_ax.set_xlim([-10, 10])
		self.matplotlib_2d_ax.set_ylim([-10, 10])
		
		# plt.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)
		# Place the matplotlib figure on canvas and display it
		self.matplotlib_2d_figure_canvas_agg = FigureCanvasAgg(self.matplotlib_2d_fig)
		self.matplotlib_2d_figure_canvas_agg.draw()
		
		self.matplotlib_2d_figure_x, self.matplotlib_2d_figure_y, self.matplotlib_2d_figure_w, \
		self.matplotlib_2d_figure_h = self.matplotlib_2d_fig.bbox.bounds
		self.matplotlib_2d_figure_w, self.matplotlib_2d_figure_h = int(self.matplotlib_2d_figure_w), int(
			self.matplotlib_2d_figure_h)
		self.photo = tk.PhotoImage(master=self.canvas, width=self.matplotlib_2d_figure_w,
		                           height=self.matplotlib_2d_figure_h)
		
	
	
	# Position: convert from top-left anchor to center anchor
		self.canvas.create_image(self.matplotlib_2d_fig_loc[0] + self.matplotlib_2d_figure_w / 2,
		                         self.matplotlib_2d_fig_loc[1] + self.matplotlib_2d_figure_h / 2, image=self.photo)
								 
								 
		tkagg.blit(self.photo, self.matplotlib_2d_figure_canvas_agg.get_renderer()._renderer, colormode=2)
		
		#self.matplotlib_2d_fig_w, self.matplotlib_2d_fig_h = self.photo.width(), self.photo.height()

		#		self.canvas.create_text(0, 0, text="Sin Wave", anchor="nw")
		
		#self.decision_boundary()


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
        
   def plotline(self):
       x = np.linspace(-20,20,5) # Create 100 linearly spaced numbers from -2 to 2
       y = x**2 # y is a function of x (y=x**2)
       z = 100*np.sin(x) # z is also a function of x (z=x**3)
       plt.plot(x,y) # Plot y vs x
       plt.plot(x,z) # Plot z vs x on the same plot
       plt.show()  # Show the plot

	def plotLine(self):

		xx=np.linspace(-10., 10, 200)
		yy=np.linspace(-10., 10, 200)
		xx,yy= np.meshgrid(xx, yy)

		input_values=self.first_weight0*xx-self.second_weight1*yy+self.bias0
		activation = Ghaderi_02_02.calculate_activation_function(input_values,
                                                          self.activation_type)
		colors=["red", "green"]
		cmap = matplotlib.colors.ListedColormap(colors)
		#input_values=w0*xx+w1*yy+bias
		self.matplotlib_2d_ax.pcolormesh(xx, yy, activation, cmap=cmap)

		self.initialize_points()


		self.matplotlib_2d_ax.set_xlim([-10, 10])
		self.matplotlib_2d_ax.set_ylim([-10, 10])
		
		
		self.matplotlib_2d_figure_canvas_agg = FigureCanvasAgg(self.matplotlib_2d_fig)
		self.matplotlib_2d_figure_canvas_agg.draw()
		
		self.matplotlib_2d_figure_x, self.matplotlib_2d_figure_y, self.matplotlib_2d_figure_w, \
		self.matplotlib_2d_figure_h = self.matplotlib_2d_fig.bbox.bounds
		self.matplotlib_2d_figure_w, self.matplotlib_2d_figure_h = int(self.matplotlib_2d_figure_w), int(
		self.matplotlib_2d_figure_h)
		self.photo = tk.PhotoImage(master=self.canvas, width=self.matplotlib_2d_figure_w,
    		                       height=self.matplotlib_2d_figure_h)

		self.canvas.create_image(self.matplotlib_2d_fig_loc[0] + self.matplotlib_2d_figure_w / 2,
		                         self.matplotlib_2d_fig_loc[1] + self.matplotlib_2d_figure_h / 2, image=self.photo)
						 
						 
		tkagg.blit(self.photo, self.matplotlib_2d_figure_canvas_agg.get_renderer()._renderer, colormode=2)


        
        
	def create_graphic_objects(self):
		j=0
		alpha=0.001
		w0 = self.first_weight
		w1 = self.second_weight
		bias = self.bias
		while (j<100):          
			j=j+1
			for i in range (0,4):

				TT = w0 * self.X_points - w1 * self.Y_points + bias

				activation = Ghaderi_02_02.calculate_activation_function(TT,
                                                     self.activation_type)
				one = [1, 1, -1, -1]
				e=one-activation
				w0 = w0 + alpha * e[i] * self.X_points[i]
				w1 = w1 + alpha * e[i] * self.Y_points[i]
				bias = bias + 0.01 * e[i]

		self.first_weight0 = w0
		self.second_weight1 = w1
		self.bias0 = bias
		self.plotLine()
    
    

	def redisplay(self, event):
		self.create_graphic_objects()

	def matplotlib_plot_2d_callback(self):
		self.display_matplotlib_figure_on_tk_canvas()
		#self.root.status_bar.set('%s', "called matplotlib_plot_2d_callback callback!")

	def matplotlib_plot_3d_callback(self):
		self.display_matplotlib_3d_figure_on_tk_canvas()
		self.root.status_bar.set('%s', "called matplotlib_plot_3d_callback callback!")

	def graphics_draw_callback(self):
		self.create_graphic_objects()
		#self.root.status_bar.set('%s', "called the draw callback!")


def close_window_callback(root):
	if tk.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
		root.destroy()

  

main_window = MainWindow(debug_print_flag=False)
main_window.geometry("450x600")
##main_window.wm_state('zoomed')
main_window.title('Assignment_02 --  ghaderi')
##main_window.minsize(600, 600)
main_window.protocol("WM_DELETE_WINDOW", lambda root_window=main_window: close_window_callback(root_window))
main_window.mainloop()

