import src.CPU_single_core.folder_actions as Ryu_FA
import re
from operator import itemgetter
from collections import defaultdict
import time


class Processing:
    def __init__(self):
        self.dummy = "Dummy"
        self.datatxt_input, self.stopwords = Ryu_FA.Actions().get_text()
        self.filtered_words = []

    def split_and_filter(self):
        # defaultdict → automatické počítání!
        filtered_words_by_stopWords = defaultdict(int)
        filtered_words_sum = defaultdict(int)

        # regex precompile: odstranění white znaků, teček čárek atd
        word_pattern = re.compile(r"^[^\w'-]+|[^\w'-]+$")
        dash_pattern = re.compile(r"^--+|--+$")

        for word in self.datatxt_input:
            cleaned_word = word_pattern.sub("", word)
            cleaned_word = dash_pattern.sub("", cleaned_word)

            if not (4 <= len(cleaned_word) <= 8):
                continue

            # Filtrace stop slov podle stop words, pokud shoda, skipne se for loop a jde se na další slovo (aka neuloží se toto slov do filtrovaných slov)
            if cleaned_word in self.stopwords:
                filtered_words_by_stopWords[cleaned_word] += 1
                continue  # skip in question

            self.filtered_words.append(cleaned_word)

            # Počítání výskytů všech slov
            filtered_words_sum[cleaned_word] += 1

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

        print("\n Staty k filtraci slov na jeden run:")
        print("\t Vstupní počet slov:", len(self.datatxt_input))
        print("\t Výstupní (vyfiltrovaný) počet slov:", len(self.filtered_words))

    def check_removed_stopwords(self):
        print("\nKontrola, zda-li se ve vyfiltrovaném seznamu slov nachází slova z stop_words.txr:")
        judgement_bool = False
        for word in self.filtered_words:
            if word in self.stopwords:
                print(f"CHYBA, SLOVO {word} JE STÁLE PŘÍTOMNO!!!")
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
        print("\n>> STARTING SINGLE CORE -----------------------------------------------------------------------------")
        start_time = time.time()
        stop_words, filtered_words = self.split_and_filter()
        self.export_data(filtered_words)
        end_time = time.time()

        self.prints(stop_words, filtered_words)
        self.check_removed_stopwords()
        print("\n>> ENDING SINGLE CORE -------------------------------------------------------------------------------")
        return end_time - start_time
