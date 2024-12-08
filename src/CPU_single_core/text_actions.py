import src.CPU_single_core.folder_actions as Ryu_FA
import re
from operator import itemgetter
import time


class Processing:
    def __init__(self):
        self.dummy = "Dummy"
        self.datatxt_input, self.stopwords = Ryu_FA.Actions().get_text()
        self.filtered_words = []

    def split_and_filter(self):
        filtered_words_by_stopWords = {}
        filtered_words_sum = {}
        print("\ndayum bro, ram goes away")

        for word in self.datatxt_input[:]:  # [:] → kopie
            # odfiltrování znaků co nejsou písmenka, odstranění teček před a za, pokus o odfiltraci i --
            cleaned_word = re.sub(r"^[^\w'-]+|[^\w'-]+$", "", word)

            # Filtrace slov, které jsou menší než 4 charaktery a delší než 8 charakterů
            if not (4 <= len(cleaned_word) <= 8):
                continue
            self.filtered_words.append(cleaned_word)  # uloží jen slova, která jsou mezi 4 a 8 char length

            # stop words bullshit
            if cleaned_word in self.stopwords:
                filtered_words_by_stopWords[cleaned_word] = filtered_words_by_stopWords.get(cleaned_word, 0) + 1
                if cleaned_word in self.filtered_words:
                    self.filtered_words.remove(cleaned_word)
                    continue

            # sum big epic storage
            filtered_words_sum[cleaned_word] = filtered_words_sum.get(cleaned_word, 0) + 1
        return filtered_words_by_stopWords, filtered_words_sum

    def prints(self, filtered_words_by_stopWords, filtered_words_sum):
        print("\tStopWords words:")
        for word, count in filtered_words_by_stopWords.items():
            print(f"\t{word}: {count}")

        # převod z {value:počet} do seřazení, že poslední print je nejčastější, první nejméně časté
        sorted_items = sorted(filtered_words_sum.items(), key=itemgetter(1))

        result_list = []
        for _ in range(5):
            if not sorted_items:
                break  # Zastaví smyčku, pokud už nejsou žádné položky
            most_frequent_word, highest_count = sorted_items[-1]  # poslední prvek = nejvyšší četnost
            result_list.append((most_frequent_word, highest_count))
            sorted_items.pop()

        # Výpis výsledků
        print("\nPět nejčastěji se opakujících slov:")
        counter = 1
        for word, count in result_list:
            percentil = round((count / len(self.datatxt_input)) * 100, 1)
            print(
                f"\t{counter}. nejčastější slovo \"{word}\" odpovídá {percentil}% z celkového počtu slov.")
            counter += 1

        print("Input arr veliksot:", len(self.datatxt_input))
        print("filtered arr velikost:", len(self.filtered_words))

    def check_removed_stopwords(self):
        print("\nkontrola odstraneni:")
        judgement_bool = False
        for word in self.filtered_words:
            if word in self.stopwords:
                print("AJAJAJAJAJ SLOVO NEBYLO ODSTRANENO")
                judgement_bool = True
        # dayum, judgement time!
        if not judgement_bool:
            print("\tDAYUUUUM Vskutku suksesfulní práce!")

    def export_data(self, filtered_words_sum):  # Export výsledků do souboru
        filename = "sorted_words_singleThread.txt"
        # reversed order, aby poslední bylo nejčastější v .txt
        sorted_items = sorted(filtered_words_sum.items(), key=itemgetter(1), reverse=True)

        # Otevře soubor pro zápis
        with open(filename, 'w') as file:
            # Pro každé slovo v seřazené sadě
            file.write(f"Slovo : Počet : Procentuální zastoupení\n")
            for word, count in sorted_items:
                percentil = round((count / len(self.datatxt_input)) * 100, 1)
                # Zápis do souboru ve formátu: slovo : počet : procentuální zastoupení
                file.write(f"{word} : {count} : {percentil}%\n")

        print(f"Výsledky byly zapsány do souboru: {filename}")

    def run(self):
        start_time = time.time()

        stop_words, filtered_words = self.split_and_filter()
        self.prints(stop_words, filtered_words)
        self.check_removed_stopwords()
        self.export_data(filtered_words)
        print("Finished single thread file filtering etc.")

        end_time = time.time()  # Konec měření času
        return end_time - start_time
