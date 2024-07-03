import tkinter as tk
import customtkinter as ctk
import numpy as np

class Test_frame:
    """Test class for the Test of the CUT"""
    def test_frame(self):
            """Create the Test frame"""
            self.test_frame = ctk.CTkFrame(self.notebook.tab("Test"))
            self.test_frame.grid(row=0, column=5, padx=10, pady=10, sticky="n")
            self.test_frame.grid_rowconfigure(0, weight=1)
            self.test_frame.grid_columnconfigure(0, weight=1)

            # Title
            self.label = ctk.CTkLabel(self.test_frame, text="Test", font=("Arial", 25))
            self.label.grid(row=0, column=1, padx=10, pady=10, sticky="n")


            self.result_text = tk.Text(self.test_frame, width=60, height=25)
            self.result_text.grid(row=8, column=0, padx=10, pady=10)
            self.test_result = ctk.CTkLabel(self.test_frame, text="Test Result", font=("calibri", 25), width=100, height=50)
            self.test_result.grid(row=8, column=1, padx=1, pady=1, sticky="ew")
        


            
            self.button_test = ctk.CTkButton(self.test_frame, text="Enter ranges", command=self.number_of_poles)
            self.button_test.grid(row=6, column=0, padx=1, pady=1, sticky="n")
        

            self.button_test = ctk.CTkButton(self.test_frame, text="TEST", command=self.compare_parameters)
            self.button_test.grid(row=12, column=0, padx=1, pady=1, sticky="n")

            self.number_of_zero = ctk.CTkLabel(self.test_frame, text="Zeros", width=10, height=5)
            self.number_of_zero.grid(row=1, column=2, padx=1, pady=1, sticky="w")
            self.zero = ctk.CTkEntry(self.test_frame)
            self.zero.grid(row=1, column=3, padx=1, pady=1, sticky="n")


            self.number_of_pole = ctk.CTkLabel(self.test_frame, text="Poles", width=10, height=5)
            self.number_of_pole.grid(row=1, column=0, padx=1, pady=1, sticky="e")
            self.pole = ctk.CTkEntry(self.test_frame)
            self.pole.grid(row=1, column=1, padx=1, pady=1, sticky="w")



    