import src.CPU_single_core.text_actions as Ryu_SCP
import src.CPU_multi_core.text_actions as Ryu_MCP
import src.utils.cream as ryu_cream


def run():
    print("--- MPC-PZP Project 2024 ---")
    singleCore_times = []
    multiCore_times = []

    for _ in range(5):
        # single thread
        singleCore_instance = Ryu_SCP.Processing()
        time_single = singleCore_instance.run()
        singleCore_times.append(time_single)
        # multi thread
        multiCore_instance = Ryu_MCP.Processing()
        time_multi = multiCore_instance.run()
        multiCore_times.append(time_multi)

    # Výpočet průměrů
    average_single = sum(singleCore_times) / len(singleCore_times)
    average_multi = sum(multiCore_times) / len(multiCore_times)

    # Výpis výsledků
    print("\n --------------------------------------------------------------------------------------------------------")
    print("Dosažené časy pro CPU run:")
    print(f"\tPrůměrná délka programu z pěti instancí single-thread programu: {average_single:.2f} sekund")
    print(f"\tPrůměrná délka programu z pěti instancí multi-thread programu: {average_multi:.2f} sekund")

    # Vykreslení grafů
    ryu_cream_inst = ryu_cream.Pie()
    ryu_cream_inst.run(singleCore_times, multiCore_times, average_single, average_multi)


if __name__ == '__main__':
    run()
