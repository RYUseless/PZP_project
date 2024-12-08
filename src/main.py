import src.CPU_single_core.text_actions as Ryu_SCP
import src.CPU_multi_core.text_actions as Ryu_MCP


def run():
    print("--- MPC-PZP Project 2024 ---")

    # SINGLE THREAD
    print("\n>> STARTING SINGLE THREAD RUN...")
    singleCore_instance = Ryu_SCP.Processing()
    time_single = singleCore_instance.run()
    print(">> ENDING SINGLE THREAD RUN...")

    # MULTI THREAD
    print("\n>> STARTING MULTI THREAD RUN...")
    multiCore_instance = Ryu_MCP.Processing()
    time_multi = multiCore_instance.run()
    print(">> ENDING MULTI THREAD RUN...")

    print("časy:")
    print(f"\nDélka běhu single-thread programu: {time_single:.2f} sekund")  # dummy print for now
    print(f"\nDélka běhu multi-thread programu: {time_multi:.2f} sekund")  # dummy print for now


if __name__ == '__main__':
    run()
