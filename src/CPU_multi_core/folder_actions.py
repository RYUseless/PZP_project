import os
import threading


class Actions:
    def __init__(self):
        self.dummy = "Dummy"
        self.data_file: str = ""
        self.stopword_file: str = ""

    @staticmethod
    def __find_resources_folder():
        working_dir = os.getcwd()
        project_name = "PZP_project"
        assets_dir_name = "resources"

        while os.path.basename(working_dir) != project_name:
            new_working_dir = os.path.abspath(os.path.join(working_dir, ".."))
            if new_working_dir == working_dir:
                print(f"Nepodařilo se najít kořenový adresář projektu '{project_name}'.")
                return None
            working_dir = new_working_dir

        location_assets = os.path.join(working_dir, assets_dir_name)
        if os.path.exists(location_assets) and os.path.isdir(location_assets):
            return location_assets
        else:
            print("Složka neexistuje")
            return None

    @staticmethod
    def _read_file(file_path):
        """ Pomocná metoda pro čtení souborů """
        try:
            with open(file_path, "r+", encoding="utf-8") as file:
                content = file.read().split()  # Split na jednotlivá slova
            return content
        except Exception as e:
            print(f"Chyba při čtení souboru {file_path}: {e}")
            return []

    def open_text_file(self):
        path_file = self.__find_resources_folder()
        files_in_folder = os.listdir(path_file)

        file_to_var_map = {
            "data.txt": "data_file",
            "stop_words.txt": "stopword_file"
        }

        # Použijeme dvě vlákna pro čtení souborů
        def load_file(file__name, var__name):
            if file__name in files_in_folder:
                data_file_path = os.path.join(path_file, file_name)
                content = self._read_file(data_file_path)
                setattr(self, var__name, content)

        threads = []
        # Vytvoření dvou vláken pro čtení dvou různých souborů
        for file_name, var_name in file_to_var_map.items():
            thread = threading.Thread(target=load_file, args=(file_name, var_name))
            threads.append(thread)
            thread.start()

        # Počkání na dokončení obou vláken
        for thread in threads:
            thread.join()

    def get_text(self):
        print(">> THREADING FOLDER ACTIONS")
        self.open_text_file()
        return self.data_file, self.stopword_file

