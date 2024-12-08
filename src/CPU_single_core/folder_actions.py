import os


class Actions:
    def __init__(self):
        self.dummy = "Dummy"
        self.data_file: str = ""
        self.stopword_file: str = ""

    @staticmethod
    def __find_resources_folder():
        working_dir = os.getcwd()
        project_name = "PZP_project"  # horní hradlo, kam až hledá funkce složku resources
        assets_dir_name = "resources"  # hledaná složka

        # Najdi kořenový adresář projektu
        while os.path.basename(working_dir) != project_name:
            new_working_dir = os.path.abspath(os.path.join(working_dir, ".."))
            if new_working_dir == working_dir:  # Narazili jsme na kořenový adresář disku
                print(f"Nepodařilo se najít kořenový adresář projektu '{project_name}'.")
                return None
            working_dir = new_working_dir

        # overeni, ze slozka opravdu existuje
        location_assets = os.path.join(working_dir, assets_dir_name)
        if os.path.exists(location_assets) and os.path.isdir(location_assets):  # slozka existuje
            # print(f"Složka '{assets_dir_name}' existuje na cestě: {location_assets}")
            return location_assets
        else:  # slozka neexistuje
            print("womp womp")

    def open_text_file(self):
        path_file = self.__find_resources_folder()

        files_in_folder = os.listdir(path_file)

        # odkaz na proměnnou bez self, lebo ta se předává při setattr!
        file_to_var_map = {
            "data.txt": "data_file",
            "stop_words.txt": "stopword_file"
        }
        for file_name in file_to_var_map:
            if file_name in files_in_folder:
                # print(f"Soubor {file_name} existuje.")
                data_file_path = os.path.join(path_file, file_name)  # Plná cesta k souboru

                try:
                    with open(data_file_path, "r+", encoding="utf-8") as file:
                        content = file.read()
                        content = content.lower().split()  # → rozdeli na slova, jinak by to parsovalo chary
                except Exception as e:
                    print(f"Došlo k chybě při čtení souboru: {e}")
                    continue  # Pokud nastane chyba, přeskočí se další krok

                # stop words are stored for each line = word
                # dynamic assignment file to its value
                setattr(self, file_to_var_map[file_name], content)
            else:
                print(f"Womp womp: soubor {file_name} neexistuje.")

    def get_text(self):
        self.open_text_file()
        return self.data_file, self.stopword_file
