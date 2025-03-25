import time

from servers_configurator.config import 
from servers_configurator.kafka_utils import Writer

def main():
    writer = Writer()
    while True:
        time.sleep(1)
        writer.write()

if __name__ == "__main__":
    main()
