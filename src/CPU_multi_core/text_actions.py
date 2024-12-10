import src.CPU_multi_core.folder_actions as Ryu_FA
from multiprocessing import Pool, cpu_count
from collections import defaultdict, Counter
import re
from operator import itemgetter
import time


class Processing:
    def __init__(self):
        self.dummy = "Dummy"
        self.datatxt_input, self.stopwords = Ryu_FA.Actions().get_text()
        self.filtered_words = []

    def _filter_chunk(self, chunk):
        word_pattern = re.compile(r"^[^\w'-]+|[^\w'-]+$")
        dash_pattern = re.compile(r"^--+|--+$")

        stopwords_set = set(word.lower() for word in self.stopwords)

        filtered_words = []  # Lokální seznam pro každou část
        for word in chunk:
            cleaned_word = word_pattern.sub("", word)
            cleaned_word = dash_pattern.sub("", cleaned_word)

            word_length = len(cleaned_word)
            if 4 <= word_length <= 8 and cleaned_word.lower() not in stopwords_set:
                filtered_words.append(cleaned_word.lower())

        return filtered_words

    def split_and_filter(self):
        num_processes = cpu_count()  # Počet procesorů

        chunk_size = len(self.datatxt_input) // num_processes
        chunks = [self.datatxt_input[i:i + chunk_size] for i in range(0, len(self.datatxt_input), chunk_size)]

        with Pool(processes=num_processes) as pool:
            filtered_results = pool.map(self._filter_chunk, chunks)

        filtered_words = [word for chunk in filtered_results for word in chunk]

        filtered_words_sum = Counter(filtered_words)

        filtered_words_by_stopWords = Counter(word for word in filtered_words if word in self.stopwords)

        self.filtered_words = filtered_words

        return filtered_words_by_stopWords, filtered_words_sum, self.filtered_words

    def prints(self, filtered_words_by_stopWords, filtered_words_sum, filtered_words):
        print("\tStopWords words:")
        for word, count in filtered_words_by_stopWords.items():
            print(f"\t{word}: {count}")

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

        print("\n Staty k filtraci slov na jeden run:")
        print("\t Vstupní počet slov:", len(self.datatxt_input))
        print("\t Výstupní (vyfiltrovaný) počet slov:", len(filtered_words))

    def check_removed_stopwords(self):
        print("\nKontrola, zda-li se ve vyfiltrovaném seznamu slov nachází slova z stop_words.txr:")
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
        print("\n>> STARTING MULTI CORE ------------------------------------------------------------------------------")
        start_time = time.time()
        stop_words, filtered_words_sum, filtered_words = self.split_and_filter()
        self.export_data(filtered_words_sum)
        end_time = time.time()

        self.prints(stop_words, filtered_words_sum, filtered_words)
        self.check_removed_stopwords()
        print("\n>> ENDING MULTI CORE --------------------------------------------------------------------------------")

        return end_time - start_time
