import src.CPU_single_core.text_actions as Ryu_SCP
# import src.CPU_multi_core as Ryu_MCP
import time


def run():
    print("--- MPC-PZP Project 2024 ---")

    # SINGLE CORE
    singleCore_instance = Ryu_SCP.Processing()
    start_time = time.time()
    singleCore_instance.run()

    end_time = time.time()  # Konec měření času

    # Výpočet a výpis doby běhu
    elapsed_time = end_time - start_time
    print(f"\nDélka běhu programu: {elapsed_time:.2f} sekund")


if __name__ == '__main__':
    run()
