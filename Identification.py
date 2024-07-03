class Identification:
     """ Identification class for the identification of the system"""

     
     def option_identification_callback(self, value):
            """Callback for the identification method option menu"""
            print(f"Selected identification method: {value}")
            try:
                if value == "ARX":

                    return self.eng.identify_arx_model(self.file_path, float(self.pole.get()), float(self.zero.get()))
                
                elif value == "ARMAX":
                    return self.eng.identify_armax_model(self.file_path, float(self.pole.get()), float(self.zero.get()))
                elif value == "OE":
                    return self.eng.identify_oe_model(self.file_path, float(self.pole.get()), float(self.zero.get()))
                elif value == "BJ":
                    return self.eng.identify_bj_model(self.file_path, float(self.pole.get()), float(self.zero.get()))
            except Exception as e:
                print(f"An error occurred while identifying parameters: {e}")