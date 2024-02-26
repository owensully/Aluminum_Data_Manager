from aluminum_data_manager import BaseStructure, HydrogenSimStructure
import os

def terminal_menu():
    
    while True:

        print("(b): add base structure")
        print("(s): add sim structure")
        print("(v): view existing structures")
        print("(e): exit")
        option = input("-> ")

        print()

        if option == 'e':

            break

        elif option == 'b':

            name = input("name: ")
            total_energy = float(input("total energy (eV): "))

            new_structure = BaseStructure(name, total_energy)
            new_structure.save_structure()

            print(f"data saved for {new_structure.name}\n")

        elif option == 's':

            name = input("name: ")
            total_energy = float(input("total energy (eV): "))
            hydrogen_site = input("hydrogen site: ")

            print("\ndoes this structure have a grain boundary?")
            print("(y): yes")
            print("(n): no")
            has_gb = input("-> ")
            print()

            if has_gb == 'y':

                grain_boundary_position = float(input("grain boundary position: "))
                
                print("\nhow many hydrogen does this structure have?")
                hnum = int(input("-> "))
                print()

                hydrogen_position = "N/A"

                if hnum > 0:

                    hydrogen_position = 0

                    for _ in range(hnum):

                        hydrogen_position += float(input("hydrogen position: "))
                        
                    hydrogen_position /= hnum

            else: 

                grain_boundary_position = "N/A"
                hydrogen_position = "N/A"

            new_structure = HydrogenSimStructure(name, total_energy, grain_boundary_position, hydrogen_position, hydrogen_site)
            new_structure.save_structure()
            print(f"\ndata saved for {new_structure.name}.\n")
        
        elif option == 'v':

            print("existing structures:\n")
            if os.path.exists(BaseStructure.get_output_path()):
                print()
                BaseStructure.display_structures()
            if os.path.exists(HydrogenSimStructure.get_output_path()):
                print()
                HydrogenSimStructure.display_structures()