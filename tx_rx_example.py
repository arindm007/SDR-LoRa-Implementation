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


sf_rx = [7]
sleep_time = 1

rx_listeners = list()

#NUMBER OF SAMPLES IN THE BASE RECEIVING WINDOW. THE LONGER IT IS, THE LESSER WILL BE THE DECODING FREQUENCY. A LONGER
#RECEIVING WINDOWS IS NECESSARY TO CORRECTLY DECODE PACKETS AT HIGHER SFs
#NOTE HOW, AT TIMES, GIVEN THE OVERLAP OVER RECEIVING WINDOWS, SOME PACKETS MAY BE DUPLICATED.
# IT IS THEREFORE NECESSARY TO FILTER THOSE PACKETS, E.G. THROUGH THE SEQUENCE NUMBER
samplesBlockRec = 12000000



serial = "34A2548" # Serial address of the USRP
rx_gain = 70
tx_gain = 80
# bandwidth = 125000
bandwidth = 200000  # Hz
center_freq = 1e9  # Hz
sample_rate = 1e6




tx_freq = 990e6  # Hz
rx_freq = 1010e6  # Hz

# tx_freq = 4.7e8  # Hz
# rx_freq = 4.7e8  # Hz

ID = int(input("Insert Node ID (0 or 1):\n"))

if(ID == 0):
    srcID = 0
    dstID = 1

else:
    srcID = 1
    dstID = 0
    temp = tx_freq
    tx_freq = rx_freq
    rx_freq = temp


tx_ch_ID = 1
rx_ch_ID = 0


SF = 7



sleep_time = 1
loradio = lora_transceiver.lora_transceiver(serial, rx_gain, tx_gain, bandwidth, rx_freq, tx_freq, sample_rate,
                                            rx_ch_ID, tx_ch_ID)


# data_array = np.random.randint(255,size=(500),dtype=np.uint8)

# give a text and convert it to bytes

# For example, if you want to send "Hello, this is a test message for LoRa transmission."
# you can do it like this:

data_array = np.frombuffer(b"Hello, this is a test message for Arindam transmission.", dtype=np.uint8)
            




packet_size = 250

CR = 1

tx_queue = loradio.tx_start(sleep_time = sleep_time, verbose=False)
rx_queues = loradio.rx_start(sf_rx, samplesBlockRec)




data = lora_utils.pack_lora_data(data_array, SF, bandwidth, packet_size, srcID, dstID, extended_sqn=False, CR = CR)
print("Number of packets to be sent: ", len(data))
print("data", data)
print("len-sf_rx", len(sf_rx))

for i in range(len(sf_rx)):
    rx_listeners.append(mp.Process(target=pkt_reader, args=(rx_queues[i],)))
    rx_listeners[i].start()


for _ in range(1):
    for pack in data:
        tx_queue.put(pack)
    time.sleep(3)



for i in range(len(sf_rx)):
    rx_listeners[i].join()

loradio.tx_stop()
loradio.rx_stop()
