from os import read
import logging_config
from siemens_comm import Plc
from system_simu import Contactor
import time

# Configure logging
setup_logging()

def main() -> None:
    plc: Plc = Plc()  # Assuming you need to initialize the Plc object

    try:
        while True:
            # Perform some operations with plc
            # Example: plc.read_data() or plc.write_data()
            km1_coil: bool = plc.read_output(0, 0)
            km2_coil: bool = plc.read_output(0, 1)
            print(km1_coil, km2_coil)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        plc.disconnect()  # Assuming you need to disconnect the Plc object

if __name__ == '__main__':
    main()
  
