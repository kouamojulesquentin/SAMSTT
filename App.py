import matlab.engine
import tkinter as tk
import customtkinter as ctk
import os
import numpy as np
import sys
from tkinter import filedialog, ttk
import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



from UI_Frame.Identification_frame import Identification_frame
from UI_Frame.Test_frame import Test_frame
from UI_Frame.Pretest_frame import Pretest_frame

from Identification import Identification



class App(ctk.CTk):
    """Main class for the application"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """Initialize the main class"""

        # Window settings
        self.theme = ctk.set_default_color_theme("dark-blue")   
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        self.title("SAMSTT   1.0.0")
        
        # create notebook
        self.notebook = ctk.CTkTabview(self, width=1000, height=800)
        self.notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.notebook.add("Test")
        self.notebook.add("Generate Parameters")

        # Window icon
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(SCRIPT_DIR, "samstt.ico")
        self.iconbitmap(icon_path)

        # Start the MATLAB engine
        self.eng = matlab.engine.start_matlab()
        matlab_files_path = os.path.join(SCRIPT_DIR, "matlab_files")
        self.eng.addpath(matlab_files_path, nargout=0)
       
        # Create the menu bar
        self.create_menu()
        
        self.identification = Identification_frame.identification_frame(self)
        
        self.test = Test_frame.test_frame(self)
        self.pretest = Pretest_frame.generate_parameters_frame(self)

        # Appearance switch
        self.appearance_switch = ctk.CTkSwitch(self, text=" ", command=self.toggle_appearance_mode)
        self.appearance_switch.grid(row=0, column=45, padx=0, pady=0, sticky="n")

        # Execution log frame
        self.log_frame = self.create_scrollable_frame(row=0, column=20)
        self.log_text = tk.Text(self.log_frame, font=("Arial", 15 ), )
        self.log_text.pack(fill=ctk.BOTH, expand=True)
        
        # Redirect stdout and stderr
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def create_scrollable_frame(self, row, column):
        """Create a scrollable frame"""
        frame = ctk.CTkFrame(self, width=100, height=600)
        frame.grid(row=row, column=column, padx=1, pady=1, sticky="nsew")
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", height=600)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

        return scrollable_frame

    def number_of_poles(self):
        """Update the number of poles and zeros"""
        try:
            poles = int(self.pole.get())
            zeros = int(self.zero.get())
        except ValueError:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Invalid input. Please enter numeric values.")
            return

        # Suppression of old entries if they exist
        if hasattr(self.test_frame, "pole_entries"):
            for pole_label, pole_entry_min, pole_entry_max in self.test_frame.pole_entries:
                pole_label.destroy()
                pole_entry_min.destroy()
                pole_entry_max.destroy()

        if hasattr(self.test_frame, "zero_entries"):
            for zero_label, zero_entry_min, zero_entry_max in self.test_frame.zero_entries:
                zero_label.destroy()
                zero_entry_min.destroy()
                zero_entry_max.destroy()

        # Create a list to store the new entries
        self.test_frame.pole_entries = []
        self.test_frame.zero_entries = []
        self.poles_range = []
        self.zeros_range = []

        for i in range(poles+1):
            label_pole = f"A_{i}"
            pole_label = ctk.CTkLabel(self.test_frame, text=label_pole + ":", width=30, height=5)
            pole_label.grid(row=i + 2, column=0, padx=1, pady=1, sticky="n")
            pole_entry_min = ctk.CTkEntry(self.test_frame, width=40, height=5, placeholder_text="Min")
            pole_entry_min.grid(row=i + 2, column=1, padx=1, pady=1, sticky="w")
            pole_entry_max = ctk.CTkEntry(self.test_frame, width=40, height=5, placeholder_text="Max")
            pole_entry_max.grid(row=i + 2, column=2, padx=1, pady=1, sticky="e")

            # Add the new entries to the list of entries plus one box for the pole
            self.test_frame.pole_entries.append((pole_label, pole_entry_min, pole_entry_max))

            
            # Add the entries as attributes of the object for future access
            setattr(self.test_frame, f"entry_A_{i}_min", pole_entry_min)
            setattr(self.test_frame, f"entry_A_{i}_max", pole_entry_max)

        for i in range(zeros+1):
            label_zero = f"B_{i}"
            zero_label = ctk.CTkLabel(self.test_frame, text=label_zero + ":", width=30, height=5)
            zero_label.grid(row=i + 2, column=3, padx=1, pady=1, sticky="n")
            zero_entry_min = ctk.CTkEntry(self.test_frame, width=40, height=5, placeholder_text="Min")
            zero_entry_min.grid(row=i + 2, column=4, padx=1, pady=1, sticky="w")
            zero_entry_max = ctk.CTkEntry(self.test_frame, width=40, height=5, placeholder_text="Max")
            zero_entry_max.grid(row=i + 2, column=5, padx=1, pady=1, sticky="e")

            # Add the new entries to the list of entries plus one box for the zero
            self.test_frame.zero_entries.append((zero_label, zero_entry_min, zero_entry_max))

            # Add the entries as attributes of the object for future access
            setattr(self.test_frame, f"entry_B_{i}_min", zero_entry_min)
            setattr(self.test_frame, f"entry_B_{i}_max", zero_entry_max)

        # update list of ranges after creating all entries
        self.update_ranges()

    def update_ranges(self):
        """Update the ranges for poles and zeros"""
        self.poles_range = [(entry[1].get(), entry[2].get()) for entry in self.test_frame.pole_entries]
        self.zeros_range = [(entry[1].get(), entry[2].get()) for entry in self.test_frame.zero_entries]

    def compare_parameters(self):
        """Compare the identified parameters with the specified ranges"""
        self.update_ranges()
        if not hasattr(self, 'identification_parameters'):
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Please identify the parameters first.")
            return

        identified_params = np.array(self.identification_parameters, dtype=float)

        # Debug: Print identified parameters
        print("Identified parameters:", identified_params)

        # Ensure identified_params is a 1D array for easy slicing
        if identified_params.ndim > 1:
            identified_params = identified_params.flatten()

        # Debug: Print the flattened identified parameters
        print("Flattened identified parameters:", identified_params)

        # Ensure identified_params has an even length
        if len(identified_params) % 2 != 0:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Invalid number of identified parameters.")
            return

        # Extract zeros and poles assuming first half are zeros and second half are poles
        num_zeros = len(identified_params) // 2
        zeros_identified = identified_params[:num_zeros]
        poles_identified = identified_params[num_zeros:]

        # Debug: Print zeros and poles
        print("Identified zeros:", zeros_identified)
        print("Identified poles:", poles_identified)

        reference_pole_length = int(self.pole.get()) + 1
        reference_zero_length = int(self.zero.get()) + 1

        results = []
        inside_pole_params = []
        inside_zero_params = []
        outside_pole_params = []
        outside_zero_params = []

        for i in range(reference_pole_length):
            min_range = float(self.poles_range[i][0])
            max_range = float(self.poles_range[i][1])

            # Debug: Print comparison details for poles
            print(f"Pole {i + 1}: {poles_identified[i]} (Range: {min_range} - {max_range})")

            if min_range <= poles_identified[i] <= max_range:
                results.append(True)
                inside_pole_params.append((i, poles_identified[i], min_range, max_range))
            else:
                results.append(False)
                outside_pole_params.append((i, poles_identified[i], min_range, max_range))

        for i in range(reference_zero_length):
            min_range = float(self.zeros_range[i][0])
            max_range = float(self.zeros_range[i][1])

            # Debug: Print comparison details for zeros
            print(f"Zero {i + 1}: {zeros_identified[i]} (Range: {min_range} - {max_range})")

            if min_range <= zeros_identified[i] <= max_range:
                results.append(True)
                inside_zero_params.append((i, zeros_identified[i], min_range, max_range))
            else:
                results.append(False)
                outside_zero_params.append((i, zeros_identified[i], min_range, max_range))

        self.result_text.delete("1.0", tk.END)
        if inside_pole_params:
            self.result_text.insert(tk.END, "Poles inside their ranges:\n")
            for i, param, min_range, max_range in inside_pole_params:
                self.result_text.insert(tk.END, f"Pole {i}: {param} (Range: {min_range} - {max_range})\n")

        if outside_pole_params:
            self.result_text.insert(tk.END, "\nPoles outside their ranges:\n")
            for i, param, min_range, max_range in outside_pole_params:
                self.result_text.insert(tk.END, f"Pole {i}: {param} (Range: {min_range} - {max_range})\n")

        if inside_zero_params:
            self.result_text.insert(tk.END, "Zeros inside their ranges:\n")
            for i, param, min_range, max_range in inside_zero_params:
                self.result_text.insert(tk.END, f"Zero {i}: {param} (Range: {min_range} - {max_range})\n")

        if outside_zero_params:
            self.result_text.insert(tk.END, "\nZeros outside their ranges:\n")
            for i, param, min_range, max_range in outside_zero_params:
                self.result_text.insert(tk.END, f"Zero {i}: {param} (Range: {min_range} - {max_range})\n")

        if all(results):
            self.result_text.insert(tk.END, "\nAll parameters are within their ranges.")
            self.test_result.configure(text="Good circuit", text_color="green")
        else:
            self.result_text.insert(tk.END, "\nSome parameters are outside their ranges.")
            self.test_result.configure(text="Defect circuit", text_color="red")

    

    

    def display_params(self, selected_method):
        """Display parameters based on the selected identification method"""
        print("Running MATLAB script for model identification...")
        
        self.params = Identification.option_identification_callback(self, selected_method)
        if self.params:
            self.display_params_in_columns(self.params)
            print("Parameters identified.", self.params)
        print("Execution finished.")

   

    def display_params_in_columns(self, params):
        """Display parameters in columns"""
        self.result_textID.delete(1.0, tk.END)  # Clear previous text
        self.identification_parameters = []
        for param in params:
            self.result_textID.insert(tk.END, f"{param}\n")
            self.identification_parameters.append(param)
      
    

       
  


   

    def run_simulation(self):
        """Run the MATLAB simulation with the input parameters"""
        try:
            R = float(self.generate_parameters_frame.entry_r.get())
            L = float(self.generate_parameters_frame.entry_l.get())
            C = float(self.generate_parameters_frame.entry_c.get())
            alpha = float(self.generate_parameters_frame.entry_alpha.get())
            nbSimulations = int(self.generate_parameters_frame.entry_number_of_simulations.get())
        except ValueError:
            self.result_parameters.delete("1.0", tk.END)
            self.result_parameters.insert(tk.END, "Invalid input. Please enter numeric values.")
            return

        # Create the structure for valeursNominales
        valeursNominales = {'R': R, 'L': L, 'C': C}

        try:
            # Call the MATLAB function
            self.boitesTolerance = self.eng.expected_parameters(valeursNominales, alpha, nbSimulations, nargout=1)

            # Display the results
            self.result_parameters.delete("1.0", tk.END)
            self.result_parameters.insert(tk.END, "Boîtes de tolerance :\n")
            values_to_send = []
            for key, value in self.boitesTolerance.items():
                values_to_send.append(value)
                self.result_parameters.insert(tk.END, f"{key}: {value}\n")
           
            # convert the values to a numpy array
            self.parameters_range = np.array(values_to_send)
            print(self.parameters_range)   
            print("Simulation finished.") 
        except Exception as e:
            self.result_parameters.delete("1.0", tk.END)
            self.result_parameters.insert(tk.END, f"An error occurred during simulation: {e}")

    def import_data(self):
            """Import data from a file"""
            print("Importing data...")
            self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if  self.file_path:
                self.display_csv_data(self.file_path)
                self.plot_data()

    def display_csv_data(self, file_path):
            """Display data in a table"""
            print(f"Displaying data from {file_path}")
            for widget in self.data_frame.winfo_children():
                widget.destroy()
            df = pd.read_csv(file_path)
            tree = ttk.Treeview(self.data_frame)
            tree.pack(fill=ctk.BOTH, expand=True)
            tree["column"] = list(df.columns)
            tree["show"] = "headings"
            for column in tree["column"]:
                tree.heading(column, text=column)
            for row in df.to_numpy().tolist():
                tree.insert("", "end", values=row)
   
    def plot_data(self):
        """Display a plot of the data"""
        print("Plotting data...")
        if hasattr(self, 'file_path'):
            for widget in self.plot_frame.winfo_children():
                widget.destroy()
            df = pd.read_csv(self.file_path)
            if 'time' in df.columns and 'V_in' in df.columns and 'V_out' in df.columns:
                # Plot for input data
                fig1, ax1 = plt.subplots(figsize=(6, 3))
                ax1.plot(df['time'], df['V_in'])
                ax1.set_title('V_in')
                ax1.set_xlabel('time')
                ax1.set_ylabel('V_in')
                canvas1 = FigureCanvasTkAgg(fig1, master=self.plot_frame)
                canvas1.draw()
                canvas1.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=False)

                # Plot for output data
                fig2, ax2 = plt.subplots(figsize=(6, 3))
                ax2.plot(df['time'], df['V_out'])
                ax2.set_title('V_out')
                ax2.set_xlabel('time')
                ax2.set_ylabel('V_out')
                canvas2 = FigureCanvasTkAgg(fig2, master=self.plot_frame)
                canvas2.draw()
                canvas2.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=False)

 

    def write(self, message):
        """Write a message to the log text widget"""
        self.log_text.insert(tk.END, message)

    def create_menu(self):
        """Create the menu bar"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About")

         # 
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tool", menu=help_menu)
        help_menu.add_command(label="tools")



    def toggle_appearance_mode(self):
        """Toggle between light and dark mode"""
        if self.appearance_switch.get() == 1:
            ctk.set_appearance_mode("dark")
            self.appearance_switch.configure(text=" ")
        else:
            ctk.set_appearance_mode("light")
            self.appearance_switch.configure(text=" ")

    def destroy(self):
        self.quit()
        super().destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
