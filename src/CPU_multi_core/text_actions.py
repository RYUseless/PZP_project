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

    @staticmethod
    def _filter_word(word):  # oproti single core přesunut filtr do vlastní funkce
        # Odfiltrování znaků co nejsou písmenka, odstranění teček před a za, pokus o odfiltraci i --
        cleaned_word = re.sub(r"^[^\w'-]+|[^\w'-]+$", "", word)

        # Filtrace slov, které jsou menší než 4 charaktery a delší než 8 charakterů
        if 4 <= len(cleaned_word) <= 8:
            return cleaned_word
        return None

    def _count_words(self, words):  # sčítání výskytu slov
        # paradoxně bez tohoto jsem měl výsledky poměrně random
        filtered_words_by_stopWords = {}
        filtered_words_sum = {}

        for word in words:
            if word in self.stopwords:
                filtered_words_by_stopWords[word] = filtered_words_by_stopWords.get(word, 0) + 1
            filtered_words_sum[word] = filtered_words_sum.get(word, 0) + 1

        return filtered_words_by_stopWords, filtered_words_sum

    def split_and_filter(self):  # split and filter metoda → basically ta hlavní
        num_processes = cpu_count()  # zjistí jádra cpučka

        # vytvoření chunků pro jednotlivé vlákna
        chunk_size = len(self.datatxt_input) // num_processes
        chunks = [self.datatxt_input[i:i + chunk_size] for i in range(0, len(self.datatxt_input), chunk_size)]

        # multithread power pro vyfiltrování slov:
        with Pool(processes=num_processes) as pool:
            filtered_results = pool.map(self._filter_word, self.datatxt_input)

        # vyfiltrovaná slova:
        filtered_words = [word for word in filtered_results if word is not None]

        # multithread power pro spočítání počtu slov:
        with Pool(processes=num_processes) as pool:
            count_results = pool.map(self._count_words, chunks)

        # Spojení výsledků do jedné kolekce
        filtered_words_by_stopWords = {}
        filtered_words_sum = {}

        for res in count_results:
            stopwords, word_count = res
            for word, count in stopwords.items():
                filtered_words_by_stopWords[word] = filtered_words_by_stopWords.get(word, 0) + count
            for word, count in word_count.items():
                filtered_words_sum[word] = filtered_words_sum.get(word, 0) + count

        return filtered_words_by_stopWords, filtered_words_sum, filtered_words

    def prints(self, filtered_words_by_stopWords, filtered_words_sum, filtered_words):  # výpis výsledku do konzole
        print("\tStopWords words:")
        for word, count in filtered_words_by_stopWords.items():
            print(f"\t{word}: {count}")

        # sort mechanismus podle formátu {slovo:počet} vyfiltruje nejčastější slova
        # oproti single core mám zde ale jinak předávané hodnoty, takže co jsem já pochopil, musím i zde reverse order
        sorted_items = sorted(filtered_words_sum.items(), key=itemgetter(1), reverse=True)

        # Výpis nejčastějších slov
        print("\nPět nejčastěji se opakujících slov:")
        counter = 1
        for word, count in sorted_items[:5]:
            percentil = round((count / len(self.datatxt_input)) * 100, 1)
            print(f"\t{counter}. nejčastější slovo \"{word}\" odpovídá {percentil}% z celkových(nevyfiltrovaných) slov.")
            counter += 1

        print("Input arr velikost:", len(self.datatxt_input))
        print("filtered arr velikost:", len(filtered_words))

    def check_removed_stopwords(self):  # Export výsledků do souboru
        print("\nKontrola odstranění:")
        judgement_bool = False
        for word in self.filtered_words:
            if word in self.stopwords:
                print("AJAJAJAJAJ SLOVO NEBYLO ODSTRANENO")
                judgement_bool = True
        if not judgement_bool:
            print("\tDAYUUUUM Vskutku sukcesfulní práce!")

    def export_data(self, filtered_words_sum):
        """ Export výsledků do souboru """
        filename = "sorted_words_multiThread.txt"
        # reverse postup oproti sortu v prints, protože chci jako poslední zapsat největší číslo
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
