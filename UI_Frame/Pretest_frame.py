import tkinter as tk
import customtkinter as ctk


class Pretest_frame:
      """ Pretest class for the Pretest of the CUT"""
      def generate_parameters_frame(self):
            """Create the Test frame"""
            self.generate_parameters_frame = ctk.CTkFrame(self.notebook.tab("Generate Parameters"))
            self.generate_parameters_frame.grid(row=0, column=5, padx=10, pady=10, sticky="n")
            self.generate_parameters_frame.grid_rowconfigure(0, weight=1)
            self.generate_parameters_frame.grid_columnconfigure(0, weight=1)

            # Title
            self.label = ctk.CTkLabel(self.generate_parameters_frame, text="BAND PASS FILTER", font=("Arial", 25))
            self.label.grid(row=0, column=0, padx=10, pady=10, sticky="n")

            entries = [("R", 1), ("L", 2), ("C", 3), ("Alpha", 4), ("Number of Simulations", 5)]
            for label_text, row in entries:
                label = ctk.CTkLabel(self.generate_parameters_frame, text=label_text + ":")
                label.grid(row=row, column=0, padx=1, pady=1, sticky="n")
                entry = ctk.CTkEntry(self.generate_parameters_frame)
                entry.grid(row=row, column=1, padx=1, pady=1, sticky="n")
                setattr(self.generate_parameters_frame, f"entry_{label_text.lower().replace(' ', '_')}", entry)

            # Widgets
            self.button_simulation = ctk.CTkButton(self.generate_parameters_frame, text="Run Simulation", command=self.run_simulation)
            self.button_simulation.grid(row=6, column=0, padx=10, pady=10, sticky="n")


            # Text widget to display the results
            self.result_parameters = tk.Text(self.generate_parameters_frame, width=60, height=15)
            self.result_parameters.grid(row=8, column=0, padx=10, pady=10)