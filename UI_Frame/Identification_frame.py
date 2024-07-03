import tkinter as tk
import customtkinter as ctk


class Identification_frame:
     """ Identification class for the identification of the system"""   
     def identification_frame(self):
            """Create the Identification frame"""
            self.identification_frame = ctk.CTkFrame(self.notebook.tab("Test"))
            self.identification_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        

            self.label = ctk.CTkLabel(self.identification_frame, text="Identification", font=("Arial", 25), width=100, height=5)
            self.label.grid(row=1, column=0, padx=10, pady=10, sticky="n")

            # Widgets
            self.button_input_data = ctk.CTkButton(self.identification_frame, text="Collect data", command=self.import_data)
            self.button_input_data.grid(row=2, column=0, padx=1, pady=1, sticky="w")

            self.option_identification = ctk.CTkOptionMenu(self.identification_frame, 
                                                        values=["Select identification method", "ARX", "ARMAX", "OE", "BJ"],
                                                        command=self.display_params)
            self.option_identification.grid(row=3, column=0, padx=1, pady=1, sticky="w")

            # Use Text widget instead of Label for result display
            self.result_textID = tk.Text(self.identification_frame, width=50, height=10)
            self.result_textID.grid(row=4, column=0, padx=20, pady=10)

            # Data and plot frames
            self.data_frame = ctk.CTkFrame(self.identification_frame, width=150, height=120)
            self.data_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
            self.data_frame.grid_rowconfigure(0, weight=0)
            self.data_frame.grid_columnconfigure(0, weight=0)
            self.plot_frame = ctk.CTkFrame(self.identification_frame)
            self.plot_frame.grid(row=3, column=1, padx=1, pady=1, sticky="nsew")
            self.plot_frame.grid_rowconfigure(0, weight=1)