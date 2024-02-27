import os
import pandas as pd

class BaseStructure:

    title = "Base Structure(s):"
    header = "name, total energy, elements"

    def __init__(self, name: str, total_energy: float):
        self.name = name
        self.total_energy = total_energy
        self.elements = BaseStructure.extract_elements(self.name)

    def save_structure(self): # function that saves an into the corresponding file

        try:

            structure = {key: str(value) for key, value in self.__dict__.items()}
        
            structure_df = pd.DataFrame([structure])
        
            structure_df.to_csv(self.__class__.get_output_path(), mode='a', sep=';', index=False, header=False)
    
        except Exception as e:

            print(f"error while saving: {e}")

    @staticmethod
    def extract_elements(name): # function that derives elements in structure based on name
        
        possible_elements = ("Al", "H", "Cu", "Mn", "Mg", "Ar", "Kr", "Ne", "He") # possible elements in structure name
        element_dictionary = {} # initialize disctionary of elements
        
        try:

            for i in range(len(possible_elements)): # loop through each of the possible elements

                found_element_index = name.find(possible_elements[i]) # check if each element is in name

                if found_element_index != -1: # if element is found

                    number_of_atoms = '' # initialize numebr of atoms

                    for j in range(found_element_index + len(possible_elements[i]), len(name)): # read possible number after element symbol

                        if name[j].isdigit(): # only add if following characters are numbers

                            number_of_atoms += name[j]

                        else:

                            break

                    if number_of_atoms == '': # if no digits were found, only 1 atom exists in structure

                        number_of_atoms = 1

                    element_dictionary[possible_elements[i]] = int(number_of_atoms) # add element and number of atoms to dictionary
        
        except AttributeError:

            return {}

        return element_dictionary
    
    @classmethod
    def get_output_path(cls): # function that creates the file path based on the working file location
        try:
            directory = os.path.dirname(os.path.abspath(__file__))
        except NameError: # if directory is not declared, this means __file__ does not exist
            directory = cls.getcwd()
        
        file_name = f"{cls.__name__.lower()}.txt"

        return os.path.join(directory, file_name)
    
    @classmethod
    def display_structures(cls): # function that prints the contents of the file for a given class
        
        try:

            file_path = cls.get_output_path()

            if not os.path.exists(file_path):

                print("file not found")

                return

            with open(file_path, "r") as file:

                print(cls.title)
                print(cls.header)

                for line in file:
                    print(line)

        except Exception as e:

            print(f"error: {e}")

class HydrogenSimStructure(BaseStructure):

    hydrogen_energy = -6.77173

    title = "Hydrogen Sim Structure(s):"
    header = "name, total energy, elements, hydrogen site, grain boundary position, hydrogen position, distance, binding energy"

    def __init__(self, name: str, total_energy: float, grain_boundary_position: float, hydrogen_position: float, hydrogen_site: str):
        super().__init__(name, total_energy)
        self.hydrogen_site = hydrogen_site
        self.grain_boundary_position = grain_boundary_position
        self.hydrogen_position = hydrogen_position
        self.hydrogen_distance = self.calculate_hydrogen_distance()
        self.hydrogen_binding_energy = self.calculate_hydrogen_binding_energy()

    def calculate_hydrogen_binding_energy(self): # function to calculate how much energy the hydrogen requires to bind to location

        hydrogen_binding_energy = "unable to calculate binding energy"

        sim_elements = BaseStructure.extract_elements(self.name)

        base_file = pd.read_csv(BaseStructure.get_output_path(), sep = ';', header = None, names = ["name", "energy", "elements"])

        for index, row in base_file.iterrows():

            base_elements = BaseStructure.extract_elements(row['name']) # cannot use row['elements'] because it will be a string, not a dictionary

            for key, value in base_elements.items():

                if key in sim_elements and sim_elements[key] == value:
                    
                    base_total_energy = row['energy']

                    for key, value in sim_elements.items():

                        if key == 'H':

                            number_of_hydrogen = value
                            hydrogen_binding_energy = (self.total_energy - float(base_total_energy) - ( float(number_of_hydrogen) / 2.0 ) * self.hydrogen_energy) / float(number_of_hydrogen)

        return hydrogen_binding_energy
    
    def calculate_hydrogen_distance(self): # function to calculate distance between grain boundary and hydrogen

        if isinstance(self.grain_boundary_position, str) or isinstance(self.hydrogen_position, str):

            return "N/A"

        else:

            return self.grain_boundary_position - self.hydrogen_position
