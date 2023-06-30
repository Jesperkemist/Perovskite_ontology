"""
A simple GUI for generating a .json file describing a perovskite
Written by T. Jesper Jacobsson 2023 06
The background is described in the paper ...
"""

import os

import customtkinter as ctk
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Label, Style

from perovskite_to_json_v2 import PerovskiteToJson

# Number of possible alternatives for ions
number_of_alternatives = 6

new_font = ('TkDefaultFont', 15)

# Filepaths to reference data
path_data_ion_folder = os.path.join(os.getcwd(), "Data_ions")
path_a_ions = os.path.join(path_data_ion_folder, "A-ion_data.xlsx")
path_b_ions = os.path.join(path_data_ion_folder, "B-ion_data.xlsx")
path_c_ions = os.path.join(path_data_ion_folder, "C-ion_data.xlsx")

def getIonAbbreviationsFromDatabase(file_path):
    """Get the abbreviations for all ions we have data on"""
    ion_data = pd.read_excel(file_path)
    ions = ion_data["Abbreviation"].values
    ions = ions.astype(str)
    ions.sort()
    return list(ions) 

# a_ions_from_database = ["Cs", "MA", "FA"]
# b_ions_from_database = ["Pb", "Sn"]
# c_ions_from_database = ["I", "Br", "Cl"]
a_ions_from_database = ["Cs", "FA", "MA"] + getIonAbbreviationsFromDatabase(path_a_ions)
b_ions_from_database = ["Pb", "Sn"] + getIonAbbreviationsFromDatabase(path_b_ions)
c_ions_from_database = ["Br", "I"] + getIonAbbreviationsFromDatabase(path_c_ions)
dimensionality_from_database = ["0D", "1D", "2D", "3D", "2D/3D", "Unknown"]

class Dimensionality(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master) 
        self.title = title
        self.values=values

        self.title = ctk.CTkLabel(self, width=140, text=self.title, fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        
        self.entrybox = ctk.CTkComboBox(self, values=self.values, variable="", font=new_font)
        self.entrybox.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w") 
       
    def clear(self):
        self.entrybox.set("")     
        
    def get(self):
        return self.entrybox.get().strip()    

class EntryboxFrame(ctk.CTkFrame):
    def __init__(self, master, number_of_boxes, title):
        super().__init__(master) 
        self.title = title     
        self.boxes = []

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="ew")

        for i in range(number_of_boxes):
            entrybox = ctk.CTkEntry(self, placeholder_text="", font=new_font)
            entrybox.grid(row=1, column=i, padx=10, pady=(10, 0), sticky="w")
            self.boxes.append(entrybox)

    def get(self):
        coef = []
        for box in self.boxes:
            x = box.get()
            x = x.replace(",", ".")
            x = x.strip()
            coef.append(x)
        return coef

    def clear(self):
        for box in self.boxes:
            box.delete(0, tk.END)
            # box.delete(0, len(box.get()))

class GetBandgap(ctk.CTkFrame):
    def __init__(self, master, title, text):
        super().__init__(master) 
        self.title = title
        self.text = text

        self.title = ctk.CTkLabel(self, width=140, text=self.title, fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        
        self.entrybox = ctk.CTkEntry(self, width=140, placeholder_text=self.text, font=new_font)
        self.entrybox.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

    def clear(self):
        self.entrybox.delete(0, tk.END)
        
    def get(self):
        x = self.entrybox.get()
        x = x.replace(",", ".")
        x = x.strip()
        return x
    
class GetFileName(ctk.CTkFrame):
    def __init__(self, master, title, text):
        super().__init__(master) 
        self.title = title
        self.text = text

        self.title = ctk.CTkLabel(self, width=140, text=self.title, fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        
        self.entrybox = ctk.CTkEntry(self, width=800, placeholder_text=self.text, font=new_font)
        self.entrybox.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

    def clear(self):
        self.entrybox.delete(0, tk.END)
        
    def get(self):
        return self.entrybox.get().strip()     

class MyButton(ctk.CTkFrame):
    def __init__(self, master, text, command):
        super().__init__(master) 
        
        self.button = ctk.CTkButton(self, text=text, command=command, font=new_font)
        self.button.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

class MyComboboxFrame(ctk.CTkFrame):
    def __init__(self, master, number_of_boxes, values, title):
        super().__init__(master) 
        self.title = title     
        self.values = values
        self.boxes = []

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6, font=new_font)
        self.title.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="ew")

        for i in range(number_of_boxes):
            combobox = ctk.CTkComboBox(self, values=self.values, variable="", font=new_font)
            combobox.grid(row=1, column=i, padx=10, pady=(10, 0), sticky="w")
            self.boxes.append(combobox)

    def get(self):
        ions = []
        for box in self.boxes:
            ions.append(box.get().strip())
        return ions
    
    def clear(self):
        for box in self.boxes:
            box.set("")

class SaveFolder(ctk.CTkFrame):
        def __init__(self, master, button_text, text, command):
            super().__init__(master) 
            self.text = text

            self.button = ctk.CTkButton(self, text=button_text, command=command, font=new_font)
            self.button.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

            self.entrybox = ctk.CTkEntry(self, width=800, placeholder_text=self.text, font=new_font)
            self.entrybox.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        
        def get(self):
            return self.entrybox.get().strip() 
            
        def update_textbox(self, text):
            self.entrybox.delete(0, tk.END)
            self.entrybox.insert(0, text)
            

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Perovskite description to JSON")
        self.geometry("1000x950")
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure((0, 1), weight=1)

        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("dark")

        # Instantiating Style class
        self.style = Style(self.master)
  
        # Configuring Custom Style
        # Name of the Style is "My.TLabel"
        self.style.configure("My.TLabel", font=('TkDefaultFont', 25))

        # Generate JSON button
        self.json_button_frame = MyButton(self, text="Generate JSON file", command=self.generate_json)
        self.json_button_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw") 

        # Clear user input button
        self.clear_button_frame = MyButton(self, text="Clear user input", command=self.clear_user_input)
        self.clear_button_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsw")        
        
        # Get file folder
        self.save_folder_frame = SaveFolder(self, button_text="Save folder", 
                                            text="Give save folder (or browse by pressing the button)", 
                                            command=self.get_filepath)
        self.save_folder_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsw") 
        
        # Get file name to save to
        self.file_name_frame = GetFileName(self, title="File name", text="Provide file name")
        self.file_name_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsw")
        
        # A ions   
        self.combobox_frame_a = MyComboboxFrame(self, number_of_boxes=number_of_alternatives, 
                                                values=a_ions_from_database, 
                                                title="A-ions. In alphabetic order. One ion per box")
        self.combobox_frame_a.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="nsw") 
        
        # A ions coefficients
        self.entrybox_frame_a = EntryboxFrame(self, number_of_boxes=number_of_alternatives, 
                                              title="A-ions coefficients")
        self.entrybox_frame_a.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="nsw") 
        
        # B ions   
        self.combobox_frame_b = MyComboboxFrame(self, number_of_boxes=number_of_alternatives, 
                                                values=b_ions_from_database, title="B-ions")
        self.combobox_frame_b.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="nsw") 
        
        # B ions coefficients
        self.entrybox_frame_b = EntryboxFrame(self, number_of_boxes=number_of_alternatives, 
                                              title="B-ions coefficients")
        self.entrybox_frame_b.grid(row=7, column=0, padx=10, pady=(10, 0), sticky="nsw") 

        # C ions   
        self.combobox_frame_c = MyComboboxFrame(self, number_of_boxes=number_of_alternatives, 
                                                values=c_ions_from_database, title="C-ions")
        self.combobox_frame_c.grid(row=8, column=0, padx=10, pady=(10, 0), sticky="nsw") 
        
        # C ions coefficients
        self.entrybox_frame_c = EntryboxFrame(self, number_of_boxes=number_of_alternatives, 
                                              title="C-ions coefficients")
        self.entrybox_frame_c.grid(row=9, column=0, padx=10, pady=(10, 0), sticky="nsw") 

        # Dimensionality
        self.combobox_frame_dim = Dimensionality(self, values=dimensionality_from_database, title="Dimensionality")
        self.combobox_frame_dim.grid(row=10, column=0, padx=10, pady=(10, 0), sticky="nsw") 
               
        # Band gap
        self.entrybox_frame_Eg = GetBandgap(self, title="Band gap [eV]", text="")
        self.entrybox_frame_Eg.grid(row=11, column=0, padx=10, pady=(10, 0), sticky="nsw") 
        
        # Additives
        self.entrybox_frame_add = EntryboxFrame(self, number_of_boxes=number_of_alternatives, title="Additives. One additive per box")
        self.entrybox_frame_add.grid(row=12, column=0, padx=10, pady=(10, 0), sticky="nsw") 

    def clear_user_input(self):
        "Clear user input"
        self.combobox_frame_a.clear()
        self.entrybox_frame_a.clear() 
        self.combobox_frame_b.clear()
        self.entrybox_frame_b.clear() 
        self.combobox_frame_c.clear()
        self.entrybox_frame_c.clear() 
        self.combobox_frame_dim.clear() 
        self.file_name_frame.clear()
        self.entrybox_frame_Eg.clear()
        self.entrybox_frame_add.clear()

    def clean_ion_input(self, ions, coef):
        ions_formated = []
        coef_formated = []
        for i, ion in enumerate(ions):
            if ion != "":
                ions_formated.append(ion)
                if coef[i] != "":
                    coef_formated.append(coef[i])
                else:
                    coef_formated.append(np.nan)
        return ions_formated, coef_formated 
                      
    def generate_json(self):
        "Put user data together in a json file"
        # Clean user input for A-ions
        A_ions, A_coef = self.clean_ion_input(ions=self.combobox_frame_a.get(), 
                                              coef=self.entrybox_frame_a.get())
        # Clean user input for A-ions
        B_ions, B_coef = self.clean_ion_input(ions=self.combobox_frame_b.get(), 
                                              coef=self.entrybox_frame_b.get())
        # Clean user input for A-ions
        C_ions, C_coef = self.clean_ion_input(ions=self.combobox_frame_c.get(), 
                                              coef=self.entrybox_frame_c.get())
        # Clean additives
        Additives = self.entrybox_frame_add.get()
        Additives = [x for x in Additives if x !=""]
        Additives.sort()
        
        # Generate a perovskite Json object
        perovskite = PerovskiteToJson(A_ions=A_ions, 
                                A_coef=A_coef, 
                                B_ions=B_ions, 
                                B_coef=B_coef, 
                                C_ions=C_ions, 
                                C_coef=C_coef, 
                                Eg=self.entrybox_frame_Eg.get(), 
                                Dimensionality=self.combobox_frame_dim.get(), 
                                Additives=Additives)

        # Save the generated JSON object
        self.save_json(perovskite)
        
    def get_filepath(self):
        "Ask user for a path to the catalog to store the files"
        self.folder_selected = tk.filedialog.askdirectory()
        self.save_folder_frame.update_textbox(text=self.folder_selected)

    def save_json(self, perovskite):
        """Save the generated Json file"""
        folder_path = self.save_folder_frame.get()
        file_name = self.file_name_frame.get()
        
        # Check file ending
        if file_name[-4:] == ".txt":
            file_name = file_name[:-4]
        if file_name[-5:] != ".json":
            file_name = file_name + ".json"
            
        file_path = os.path.join(folder_path, file_name)
        # Save data  
        perovskite.save_data(file_path)

app = App()
app.mainloop()


