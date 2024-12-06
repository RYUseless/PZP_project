import src.CPU_single_core.folder_actions as Ryu_FA
import re
from operator import itemgetter


class Processing:
    def __init__(self):
        self.dummy = "Dummy"
        R_FA = Ryu_FA.Actions()
        self.data_text, self.stopwords = R_FA.get_text()

    def split_and_filter(self):
        filtered_words = []
        filtered_words_by_stopWords = {}
        filtered_words_sum = {}
        print("\ndayum bro, ram goes away")
        # TODO: perhaps vyřešit issue s SLOVO--SLOVO aka nechává to existovat
        for word in self.data_text:
            # odfiltrování znaků co nejsou písmenka, odstranění teček před a za, pokus o odfiltraci i --
            cleaned_word = re.sub(r"^[^\w'-]+|[^\w'-]+$", "", word)

            # Filtrace slov, které jsou menší než 4 charaktery a delší než 8 charakterů
            if 4 <= len(cleaned_word) <= 8:
                filtered_words.append(cleaned_word)

            # Filtr slov, které jsou identické jako slova z stop_words.txá → akce s něma zatím žádný
            if cleaned_word in self.stopwords:
                filtered_words_by_stopWords[cleaned_word] = filtered_words_by_stopWords.get(cleaned_word, 0) + 1

            # Přidat slova do hlavního počítadla
            filtered_words_sum[cleaned_word] = filtered_words_sum.get(cleaned_word, 0) + 1

        print("\tStopWords words:")
        for word, count in filtered_words_by_stopWords.items():
            print(f"\t{word}: {count}")

        # print("Slova a kolikrát se vyskytla:")
        # Seřadí slova podle počtu opakování
        # sorted_items = sorted(filtered_words_sum.items(), key=itemgetter(1))
        # for word, count in sorted_items:
        #    print(f"{word}: {count}")

        # Seřadí slova podle počtu (od nejmenšího po největší)
        sorted_items = sorted(filtered_words_sum.items(), key=itemgetter(1))

        # Získáme slovo s nejvyšší četností (první položka v seřazeném seznamu)
        most_frequent_word, highest_count = sorted_items[-1]  # poslední prvek = nejvyšší četnost

        # Celkový počet znaků v textu
        total_characters = len(self.data_text)

        # Spočítání procenta
        percentage = (highest_count / total_characters) * 100

        print(f"\n\tSlovo s nejvyšší četností: {most_frequent_word}")
        print(f"\tPočet výskytů: {highest_count}")
        print(f"\tProcentuální podíl na celkovém počtu znaků: {percentage:.2f}%")

        print("\tcelkovy pocet slov:", len(self.data_text))
        print("\tvyfiltrovany pocet slov:", len(filtered_words))

    def run(self):
        self.split_and_filter()
