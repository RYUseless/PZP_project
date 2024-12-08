import src.CPU_multi_core.folder_actions as Ryu_FA
from multiprocessing import Pool, cpu_count
import re
from operator import itemgetter
import time


class Processing:
    def __init__(self):
        self.dummy = "Dummy"
        self.datatxt_input, self.stopwords = Ryu_FA.Actions().get_text()
        self.filtered_words = []

    def _filter_chunk(self, chunk):
        filtered_words = []  # Lokální seznam pro každou část
        for word in chunk:
            # Odfiltrování znaků, co nejsou písmenka, odstranění teček před a za
            cleaned_word = re.sub(r"^[^\w'-]+|[^\w'-]+$", "", word)

            # Filtrace slov, které jsou menší než 4 charaktery a delší než 8 charakterů
            if 4 <= len(cleaned_word) <= 8:
                # Pokud je slovo v seznamu stopwords, nebudeme ho přidávat
                if cleaned_word.lower() not in self.stopwords:
                    filtered_words.append(cleaned_word.lower())  # Přidáme slovo do výsledného seznamu ve formátu lower
        return filtered_words  # Vracíme pouze lokální seznam

    def split_and_filter(self):
        num_processes = cpu_count()  # Počet procesorů

        # Rozdělení dat do menších bloků pro paralelizaci
        chunk_size = len(self.datatxt_input) // num_processes
        chunks = [self.datatxt_input[i:i + chunk_size] for i in range(0, len(self.datatxt_input), chunk_size)]

        # Použití více procesů pro filtrování slov
        with Pool(processes=num_processes) as pool:
            filtered_results = pool.map(self._filter_chunk, chunks)

        # Spojení všech výsledků z jednotlivých chunků do jednoho seznamu
        filtered_words = [word for chunk in filtered_results for word in chunk]

        # Na konci přidáme všechny vyfiltrované slova do self.filtered_words
        self.filtered_words = filtered_words

        # Použití více vláken pro spočítání výskytů slov
        filtered_words_by_stopWords = {}
        filtered_words_sum = {}

        for word in filtered_words:
            filtered_words_sum[word] = filtered_words_sum.get(word, 0) + 1

        return filtered_words_by_stopWords, filtered_words_sum, filtered_words

    def prints(self, filtered_words_by_stopWords, filtered_words_sum, filtered_words):
        print("\tStopWords words:")
        for word, count in filtered_words_by_stopWords.items():
            print(f"\t{word}: {count}")

        # Seřazení slov podle počtu výskytů
        sorted_items = sorted(filtered_words_sum.items(), key=itemgetter(1))

        result_list = []
        for _ in range(5):
            if not sorted_items:
                break
            most_frequent_word, highest_count = sorted_items[-1]  # poslední = nejčastější
            result_list.append((most_frequent_word, highest_count))
            sorted_items.pop()

        # Výpis nejčastějších slov
        print("\nPět nejčastěji se opakujících slov:")
        counter = 1
        for word, count in result_list:
            percentil = round((count / len(self.datatxt_input)) * 100, 1)
            print(f"\t{counter}. nejčastější slovo \"{word}\" odpovídá {percentil}% z celkového počtu slov.")
            counter += 1

        print("Input arr velikost:", len(self.datatxt_input))
        print("filtered arr velikost:", len(filtered_words))

    def check_removed_stopwords(self):
        print("\nKontrola odstranění:")
        judgement_bool = False
        for word in self.filtered_words:
            if word in self.stopwords:
                print("AJAJAJAJAJ SLOVO NEBYLO ODSTRANENO")
                judgement_bool = True
        if not judgement_bool:
            print("\tDAYUUUUM Vskutku sukcesfulní práce!")

    def export_data(self, filtered_words_sum):
        filename = "sorted_words_multiThread.txt"
        sorted_items = sorted(filtered_words_sum.items(), key=itemgetter(1), reverse=True)

        with open(filename, 'w') as file:
            file.write(f"Slovo : Počet : Procentuální zastoupení\n")
            for word, count in sorted_items:
                percentil = round((count / len(self.datatxt_input)) * 100, 1)
                file.write(f"{word} : {count} : {percentil}%\n")

        print(f"Výsledky byly zapsány do souboru: {filename}")

    def run(self):
        start_time = time.time()

        stop_words, filtered_words_sum, filtered_words = self.split_and_filter()
        self.prints(stop_words, filtered_words_sum, filtered_words)
        self.check_removed_stopwords()
        self.export_data(filtered_words_sum)

        end_time = time.time()
        return end_time - start_time
