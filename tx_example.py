import lora_transceiver
import lora
import lora_utils
import numpy as np
import multiprocessing as mp
import multiprocessing.queues as mp_queues
import queue as q
import time

def main():
    """
    Main function to run the transmitter example.
    No arguments.
    """

    serial = "3439ADE" # Serial address of the USRP
    rx_gain = 70
    tx_gain = 80
    # bandwidth = 125000
    bandwidth = 250000
    center_freq = 1e9
    sample_rate = 1e6

    tx_freq = 990e6  # Hz
    rx_freq = 1010e6  # Hz
    tx_ch_ID = 1
    rx_ch_ID = 0


    SF = 7



    sleep_time = 1      
    loradio = lora_transceiver.lora_transceiver(serial, rx_gain, tx_gain, bandwidth, rx_freq, tx_freq, sample_rate,
                                                rx_ch_ID, tx_ch_ID)


    # data_array = np.ones(500,dtype=np.uint8)
    data_array = np.frombuffer(b"This is a test paragraph generated to exactly match the maximum MAVLink 2 message size. Each byte in this sentence is counted precisely, ensuring the total length is exactly two hundred and fifty bytes. This helps in testing the LoRa transmitter cod.", dtype=np.uint8)



    packet_size = 250
    srcID = 0
    dstID = 1
    CR = 1

    tx_queue = loradio.tx_start(sleep_time = sleep_time, verbose=True)

    data = lora_utils.pack_lora_data(data_array, SF, bandwidth, packet_size, srcID, dstID, extended_sqn=False, CR = CR)

    for pack in data:
        tx_queue.put(pack)


    # for _ in range(1):
    #     for pack in data:
    #         tx_queue.put(pack)
    #     time.sleep(1)

if __name__ == "__main__":
    main()
