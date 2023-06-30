"""
Functionality for converting perovskite data to a .Json file

Written by:
T. Jesper Jacobsson 2023 06
The background is described in the paper ...
"""

import os
from itertools import zip_longest

import pandas as pd
import numpy as np
import json


# Filepaths
path_data_ion_folder = os.path.join(os.getcwd(), "Data_ions")
path_json_files = os.path.join(os.getcwd(), "Data") 
path_a_ions = os.path.join(path_data_ion_folder, "A-ion_data.xlsx")
path_b_ions = os.path.join(path_data_ion_folder, "B-ion_data.xlsx")
path_c_ions = os.path.join(path_data_ion_folder, "C-ion_data.xlsx")

path_json_file = os.path.join(path_json_files, "test.json")

class PerovskiteToJson:
    def __init__(self, A_ions=[], A_coef=[], B_ions=[], B_coef=[], C_ions=[], C_coef=[], Eg=np.nan, Dimensionality="", Additives=[], filepath=path_json_file):
        self.A_ions = A_ions
        self.A_coef = A_coef
        self.B_ions = B_ions
        self.B_coef = B_coef
        self.C_ions = C_ions
        self.C_coef = C_coef
        self.Eg = Eg
        self.Dimensionality = Dimensionality
        self.Additives = Additives
        self.path = filepath
                
        # Sort A_ions in alphabetic order
        self.A_ions, self.A_coef = self.sort_ions(self.A_ions, self.A_coef)
        
        # Sort B_ions in alphabetic order
        self.B_ions, self.B_coef = self.sort_ions(self.B_ions, self.B_coef)
        
        # Sort C_ions in alphabetic order
        self.C_ions, self.C_coef = self.sort_ions(self.C_ions, self.C_coef)
        
        # Get perovskite short composition
        self.short_formula = self.get_short_formula()
        
        # Get perovskite long composition
        self.long_formula = self.get_long_formula()
        
        # Get A-ion complementary data
        data_dict = self.get_ion_complementary_data(self.A_ions, path_a_ions)
        self.A_common_names = data_dict["common_names"]
        self.A_iupac_names = data_dict["iupac_names"]
        self.A_SMILES = data_dict["SMILES"]
        self.A_molecular_formula = data_dict["molecular_formulas"]
        self.A_cas_numbers = data_dict["cas_numbers"]
        self.A_parent_smiles = data_dict["Parent_SMILEs"] 
        self.A_parent_iupac = data_dict["Parent_IUPACs"]
        self.A_parent_cas = data_dict["Parent_CAS"]
                    
        # Get B-ion complementary data
        data_dict = self.get_ion_complementary_data(self.B_ions, path_b_ions)
        self.B_common_names = data_dict["common_names"]
        self.B_iupac_names = data_dict["iupac_names"]
        self.B_SMILES = data_dict["SMILES"]
        self.B_molecular_formula = data_dict["molecular_formulas"]
        self.B_cas_numbers = data_dict["cas_numbers"]
        self.B_parent_smiles = data_dict["Parent_SMILEs"] 
        self.B_parent_iupac = data_dict["Parent_IUPACs"]
        self.B_parent_cas = data_dict["Parent_CAS"]
    
        # Get C-ion complementary data
        data_dict = self.get_ion_complementary_data(self.C_ions, path_c_ions)
        self.C_common_names = data_dict["common_names"]
        self.C_iupac_names = data_dict["iupac_names"]
        self.C_SMILES = data_dict["SMILES"]
        self.C_molecular_formula = data_dict["molecular_formulas"]
        self.C_cas_numbers = data_dict["cas_numbers"]
        self.C_parent_smiles = data_dict["Parent_SMILEs"] 
        self.C_parent_iupac = data_dict["Parent_IUPACs"]
        self.C_parent_cas = data_dict["Parent_CAS"]
           
        # Format the dimensionality
        
        # Format the Additives
        
        # Convert data to a Json-file
        self.json = self.convert_to_json()
        
        # Save Json file
        self.save_data(file_path = self.path)
        
        

    def add_paranteses(self, ions, n=2):
        # Enclose every ion with three letters or more with a parenthesis
        new_list = []
        for i, ion in enumerate(ions):
            if len(ion) > n:
                new_list.append("".join(["(", ion, ")"]))
            else:
                new_list.append(ion)
        return new_list

    def convert_to_json(self):
        "Convert to Json"
        
        # Combine data into a dictionary
        perovskite_data ={
            "Perovskite family": self.short_formula, 
            "Perovskite composition": self.long_formula,
            "Band gap": self.Eg,
            "Dimensionality": self.Dimensionality,
            "A_ions": self.A_ions,
            "A_coef": self.A_coef,
            "A_SMILES": self.A_SMILES,
            "A_molecular_formula": self.A_molecular_formula,
            "A_IUPAC_names": self.A_common_names,
            "A_common_names": self.A_common_names,
            "A_cas_numbers": self.A_cas_numbers,
            "A_parent_SMILES": self.A_parent_smiles,
            "A_parent_IUPAC_names": self.A_parent_iupac,
            "A_parent_cas_numbers": self.A_parent_cas, 
            "B_ions": self.B_ions,
            "B_coef": self.B_coef,
            "B_SMILES": self.B_SMILES,
            "B_molecular_formula": self.B_molecular_formula,
            "B_IUPAC_names": self.B_common_names,
            "B_common_names": self.B_common_names,
            "B_cas_numbers": self.B_cas_numbers,
            "B_parent_SMILES": self.B_parent_smiles,
            "B_parent_IUPAC_names": self.B_parent_iupac,
            "B_parent_cas_numbers": self.B_parent_cas,
            "C_ions": self.C_ions,
            "C_coef": self.C_coef,
            "C_SMILES": self.C_SMILES,
            "C_molecular_formula": self.C_molecular_formula,
            "C_IUPAC_names": self.C_common_names,
            "C_common_names": self.C_common_names,
            "C_cas_numbers": self.C_cas_numbers,
            "C_parent_SMILES": self.C_parent_smiles,
            "C_parent_IUPAC_names": self.C_parent_iupac,
            "C_parent_cas_numbers": self.C_parent_cas,
            "Additives": self.Additives,    
        }
        
        # Convert to json
        return json.dumps(perovskite_data, indent=4)
       
    def get_data_from_ion_datatables(self, ion_data, ions, column):
        names = []
        for ion in ions:
            name = ion_data.loc[ion_data["Abbreviation"] == ion, column].values
            # If not in database
            if len(name) == 0:
                names.append("NaN") 
            # If not unique, chose the first one
            elif len(name) > 1:
                names.append(str(name[0]))          
            else:
                names.append(str(name[0]))
                            
        names = [name.strip() for name in names]
        return names
        
    def get_ion_complementary_data(self, ions, file_path):
        "Get complementary data about ions from file"
        ion_data = pd.read_excel(file_path)
        
        data_dict = {}
        
        # Get data
        data_dict["common_names"] = self.get_data_from_ion_datatables(ion_data, ions, "Common_name")
        data_dict["iupac_names"] = self.get_data_from_ion_datatables(ion_data, ions, "IUPAC_name")
        data_dict["SMILES"] = self.get_data_from_ion_datatables(ion_data, ions, "SMILE")
        data_dict["molecular_formulas"] = self.get_data_from_ion_datatables(ion_data, ions, "Molecular_formula")
        data_dict["cas_numbers"]  = self.get_data_from_ion_datatables(ion_data, ions, "CAS")   
        data_dict["Parent_SMILEs"]  = self.get_data_from_ion_datatables(ion_data, ions, "Parent_SMILE")
        data_dict["Parent_IUPACs"]  = self.get_data_from_ion_datatables(ion_data, ions, "Parent_IUPAC")
        data_dict["Parent_CAS"]  = self.get_data_from_ion_datatables(ion_data, ions, "Parent_CAS")
        
        return data_dict
 
    def get_long_formula(self):
        
        "The compleat perovskite formula"
        
        # The ions
        a_list = self.A_ions
        b_list = self.B_ions
        c_list = self.C_ions
        
        # Enclose every ion with three letters or more with a parenthesis
        a_list = self.add_paranteses(a_list, n=2)
        b_list = self.add_paranteses(b_list, n=2)
        c_list = self.add_paranteses(c_list, n=2)
            
        # The coefficients
        a_coef_list = self.A_coef
        b_coef_list = self.B_coef
        c_coef_list = self.C_coef
        
        # Convert coefficients to strings
        a_coef_list = [str(x) for x in a_coef_list]
        b_coef_list = [str(x) for x in b_coef_list]
        c_coef_list = [str(x) for x in c_coef_list]
        
        # Replace ones with empty strings
        a_coef_list = ['' if x in [' 1', '1', '1 '] else x for x in a_coef_list]
        b_coef_list = ['' if x in [' 1', '1', '1 '] else x for x in b_coef_list]
        c_coef_list = ['' if x in [' 1', '1', '1 '] else x for x in c_coef_list]
        
        # Zip together the lists
        a_compleat = list(zip_longest(a_list, a_coef_list, fillvalue = ''))
        b_compleat = list(zip_longest(b_list, b_coef_list, fillvalue = ''))
        c_compleat = list(zip_longest(c_list, c_coef_list, fillvalue = ''))
        
        # Flatten the list of tuples generated by the zip function
        a_compleat = [item for sublist in a_compleat for item in sublist]
        b_compleat = [item for sublist in b_compleat for item in sublist]
        c_compleat = [item for sublist in c_compleat for item in sublist]
        
        # Merge the lists
        LongCompList = a_compleat + b_compleat + c_compleat

        # Concatenate the ions
        LongComp = ''.join(LongCompList)

        return LongComp
           
    def get_short_formula(self):
        "The perovskite family"
        # The ions
        a_list = self.A_ions
        b_list = self.B_ions
        c_list = self.C_ions
        
        # Enclose every ion with three letters or more with a parenthesis
        a_list = self.add_paranteses(a_list, n=2)
        b_list = self.add_paranteses(b_list, n=2)
        c_list = self.add_paranteses(c_list, n=2)
        
        # Merge the lists
        shortCompList = a_list + b_list + c_list

        # Concatenate the ions
        shortComp = ''.join(shortCompList)

        return shortComp

    def sort_ions(self, ions, coef):
        "Sort ions in alphabetic order"   
        # Remove trailing blank spaces
        ions = [ion.strip() for ion in ions]
        
        # Remove any enclosing parenthesizes 
        for i, ion in enumerate(ions):
            if (ion[0] == "(" and ion[-1] == ")"):
                ions[i] = ion[1:-1]   
        
        # Check if coefficients are given for all ions   
        if len(coef) < len(ions):
            coef.extend(list(np.ones(len(ions)-len(coef))*np.nan))
           
        # Update the order of the ions
        order = np.argsort(ions) 
        ion_list = [ions[i] for i in order]
        
        # Update the order of the coefficients
        coef_list = [coef[i] for i in order]
        
        return ion_list, coef_list
      
    def save_data(self, file_path):
        "Save data"
        # with open("test.json", "w") as outfile:
        #     outfile.write(self.json)       
        with open(file_path, "w") as outfile:
            outfile.write(self.json)



# Basic check        
if __name__ == "__main__":     
    
    # Test data
    A_ions = ["Cs", "MA", "FA "]
    A_coef = [0.05, 0.79, 0.18]
    B_ions = ["Pb"]
    B_coef = [1]
    C_ions = ["Br", "I"]
    C_coef = [0.5, 2.5]
    Eg = 1.63
    Dimensionality = "3D"
    Additives = ["RbI", "PbI2"]
    filepath=os.getcwd()
    
    perovskite = PerovskiteToJson(A_ions=A_ions, 
                                  A_coef=A_coef, 
                                  B_ions=B_ions, 
                                  B_coef=B_coef, 
                                  C_ions=C_ions, 
                                  C_coef=C_coef, 
                                  Eg=Eg, 
                                  Dimensionality=Dimensionality, 
                                  Additives=Additives, 
                                  filepath=filepath)
    
    print(perovskite.A_ions)
    print(perovskite.A_coef)
    print(perovskite.short_formula)
    print(perovskite.long_formula)
    
    # Save data
    perovskite.save_data(path_json_file)