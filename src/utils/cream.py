import matplotlib.pyplot as plt


class Pie:
    def __init__(self):
        self.dummy = "dummy"

    @staticmethod
    def plot_pie_chart(average_single, average_multi):
        """
        Připraví koláčový graf na základě průměrných hodnot.
        """
        labels = ['Single Thread', 'Multi Thread']
        sizes = [average_single, average_multi]

        # Vytvoření koláčového grafu
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightgreen'])
        plt.title('Porovnání průměrů výkonu: Single Thread vs Multi Thread')
        plt.axis('equal')  # Zajištění kruhového tvaru

    def show_each_run(self, single, multi):
        """
        Připraví jednotlivé grafy časů běhů pro single a multi thread.

        :param single: Pole časů pro Single Thread běhy
        :param multi: Pole časů pro Multi Thread běhy
        """
        # Graf pro Single Thread
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, len(single) + 1), single, marker='o', label='Single Thread', color='blue')
        plt.title('Časy jednotlivých epizod: Single Thread')
        plt.xlabel('Epizoda')
        plt.ylabel('Čas (s)')
        plt.grid(True)
        plt.legend()

        # Graf pro Multi Thread
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, len(multi) + 1), multi, marker='o', label='Multi Thread', color='green')
        plt.title('Časy jednotlivých epizod: Multi Thread')
        plt.xlabel('Epizoda')
        plt.ylabel('Čas (s)')
        plt.grid(True)
        plt.legend()

    def run(self, single, multi, average_single, average_multi):
        """
        Zavolá všechny metody pro vykreslení grafů a na závěr vykreslí vše najednou.

        :param single: Pole časů pro Single Thread běhy
        :param multi: Pole časů pro Multi Thread běhy
        :param average_single: Průměrný čas pro Single Thread
        :param average_multi: Průměrný čas pro Multi Thread
        """
        self.plot_pie_chart(average_single, average_multi)  # Koláčový graf
        self.show_each_run(single, multi)  # Grafy pro jednotlivé běhy
        plt.show()  # Zobrazí všechny grafy najednou



