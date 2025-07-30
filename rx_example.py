import lora_transceiver
import lora
import lora_utils
import numpy as np
import multiprocessing as mp
import multiprocessing.queues as mp_queues
import queue as q
import time



# def pkt_reader(pkt_queue):
#     while True:
#         pkt = pkt_queue.get()
#         if(isinstance(pkt,lora.LoRaPacket)):
#             print(pkt)
def pkt_reader(pkt_queue):
    """
    Args:
        pkt_queue: multiprocessing.Queue, queue from which packets are read and printed.
    """
    while True:
        pkt = pkt_queue.get()
        if isinstance(pkt, lora.LoRaPacket):
            print("\n=== Received LoRa Packet ===")
            print(f"Source ID: {pkt.src}")
            print(f"Destination ID: {pkt.dst}")
            # print(f"Sequence Number: {pkt.sqn}")
            print(f"Payload (raw): {pkt.payload}")
            try:
                print(f"Payload (decoded): {pkt.payload.tobytes().decode(errors='ignore')}")
            except Exception as e:
                print(f"Could not decode payload: {e}")
            # print(f"Metadata: {pkt.metadata}")
            print("============================\n")
        else:
            print(f"Received non-LoRaPacket: {pkt} (type: {type(pkt)})")





serial = "34A2548"  # Serial address of the USRP
rx_gain = 70
tx_gain = 80
bandwidth = 125000
center_freq = 1e9
sample_rate = 1e6

rx_freq = 990e6  # Hz
tx_freq = 1010e6  # Hz
tx_ch_ID = 1
rx_ch_ID = 0




sf = [7,8,9,10,11,12]
sleep_time = 1

rx_listeners = list()
samplesBlockRec = 3000000
loradio = lora_transceiver.lora_transceiver(serial, rx_gain, tx_gain, bandwidth, rx_freq, tx_freq, sample_rate,
                                            rx_ch_ID, tx_ch_ID)

rx_queues = loradio.rx_start(sf, samplesBlockRec)

for i in range(len(sf)):
    rx_listeners.append(mp.Process(target=pkt_reader, args=(rx_queues[i],)))
    rx_listeners[i].start()

for i in range(len(sf)):
    rx_listeners[i].join()

