import lora_transceiver
import lora
import lora_utils
import numpy as np
import time
import multiprocessing as mp

SYNC_CODE = 250  # Custom code for sync packets

class PTPSyncMaster:
    def __init__(self, loradio, SF, BW, srcID, dstID, CR=1, interval=5):
        self.loradio = loradio
        self.SF = SF
        self.BW = BW
        self.srcID = srcID
        self.dstID = dstID
        self.CR = CR
        self.interval = interval
        self.tx_queue = loradio.tx_start(sleep_time=1, verbose=True)

    def send_sync(self):
        while True:
            timestamp = int(time.time())
            payload = np.zeros((5,), dtype=np.uint8)
            payload[0] = SYNC_CODE
            payload[1:] = np.frombuffer(timestamp.to_bytes(4, 'big'), dtype=np.uint8)
            sync_packet = lora.LoRaPacket(payload, self.srcID, self.dstID, seqn=0, hdr_ok=1, has_crc=1, crc_ok=1,
                                          cr=self.CR, ih=0, SF=self.SF, BW=self.BW)
            self.tx_queue.put(sync_packet)
            print(f"[PTP Master] Sent SYNC packet with timestamp: {timestamp}")
            time.sleep(self.interval)

class PTPSyncSlave:
    def __init__(self):
        self.time_offset = 0
        self.last_sync = None

    def process_packet(self, packet):
        if packet.payload[0] == SYNC_CODE:
            master_time = int.from_bytes(packet.payload[1:], 'big')
            local_time = int(time.time())
            self.time_offset = master_time - local_time
            self.last_sync = master_time
            print(f"[PTP Slave] Received SYNC. Master time: {master_time}, Local time: {local_time}, Offset: {self.time_offset}")

    def get_synced_time(self):
        return int(time.time()) + self.time_offset

# Example usage:
# On master node:
# loradio = lora_transceiver.lora_transceiver(...)
# ptp_master = PTPSyncMaster(loradio, SF=7, BW=250000, srcID=0, dstID=1)
# ptp_master.send_sync()

# On slave node:
# ptp_slave = PTPSyncSlave()
# while True:
#     packet = rx_queue.get()  # Replace with your RX logic
#     ptp_slave.process_packet(packet)
#     print("Synced time:", ptp_slave.get_synced_time())
