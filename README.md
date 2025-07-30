# SDR-LoRa: Implementing LoRa on software-defined radios

SDR-LoRa is a Python project for sending and receiving data wirelessly using LoRa, a long-range, low-power wireless technology. It is designed to work with software-defined radios (SDR), which are flexible radio devices controlled by software.

## What is LoRa and SDR?
- **LoRa**: A wireless protocol for long-range, low-power communication, often used in IoT and sensor networks.
- **SDR (Software-Defined Radio)**: Radio hardware that is controlled and configured by software, allowing flexible and programmable wireless communication.

## Project Overview
This project provides:
- LoRa packet encoding and decoding (modulation/demodulation)
- Utilities for packing/unpacking data into LoRa packets
- Transceiver management for sending/receiving packets using SDR hardware
- Example scripts for transmission and reception

## Main Files
- `lora.py`: Implements the LoRa protocol, including encoding/decoding and the `LoRaPacket` class.
- `lora_utils.py`: Helper functions for creating, packing, and unpacking LoRa packets.
- `lora_transceiver.py`: Manages SDR hardware, transmission, and reception using multithreading and multiprocessing.
- `tx_example.py`, `rx_example.py`, `tx_rx_example.py`: Example scripts for sending and receiving data.

## How It Works
1. **Setup**: Configure the transceiver with radio settings (frequency, bandwidth, etc.).
2. **Transmit**:
   - Data is packed into LoRa packets using utility functions.
   - Packets are encoded into radio signals.
   - SDR hardware sends the signals over the air.
3. **Receive**:
   - SDR hardware listens for signals.
   - Received signals are decoded to extract LoRa packets.
   - Packets are unpacked to recover the original data.
4. **Multithreading/Multiprocessing**: The code uses multiple processes/threads to handle large amounts of data efficiently.

## Features
- Support for multiple LoRa spreading factors and bandwidths
- Multiprocessing and multithreading for efficient data handling
- Modular design for easy extension and integration
- Example scripts for quick testing and demonstration
- Utilities for packet management and data packing/unpacking

## Installation
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd sdr-lora
   ```
2. Install Python dependencies:
   ```bash
   pip install numpy scipy
   ```
3. Install UHD (for SDR hardware):
   - On Ubuntu:
     ```bash
     sudo apt-get install libuhd-dev uhd-host
     ```
   - Or see [UHD installation guide](https://github.com/EttusResearch/uhd#installation) for other platforms.

## Usage
- To transmit data:
  ```bash
  python tx_example.py
  ```
- To receive data:
  ```bash
  python rx_example.py
  ```
- To run both transmitter and receiver:
  ```bash
  python tx_rx_example.py
  ```
- For custom usage, import and use the `lora_transceiver` class in your own Python scripts.

## Code Documentation
### lora.py
- **LoRaPacket**: Class representing a LoRa packet (payload, source, destination, sequence number, etc.).
- **encode()**: Converts data and transmission parameters into LoRa radio signals.
- **decode()**: Extracts LoRa packets from received radio signals.

### lora_utils.py
- **pack_lora_data()**: Splits data into multiple LoRa packets for transmission.
- **unpack_lora_data()**: Reassembles data from received LoRa packets.
- **gen_pack_polling()**: Creates polling packets for network management.
- **pack_lora_nack()**: Creates acknowledgment (ACK/NACK) packets.

### lora_transceiver.py
- **lora_transceiver**: Main class for managing SDR hardware and LoRa communication.
  - `rx_start()`: Starts receiving packets.
  - `rx_stop()`, `rx_pause()`, `rx_resume()`: Controls reception.
  - `tx_send_burst()`, `tx_send_burst_multi_sf()`: Sends packets in bursts (single or multiple spreading factors).
  - `tx_start()`, `tx_stop()`: Starts/stops continuous transmission.

## Function and Class Documentation

### lora.py
- **lora_packet**: Generates the signal samples for a LoRa packet, including preamble, header, and payload, using modulation techniques.
- **lora_header_init**: Calculates the number of header symbols and bits based on spreading factor and header mode.
- **lora_header**: Encodes the header bits into LoRa symbols, applying parity and interleaving.
- **lora_payload_init**: Prepares the payload bits, applies whitening and CRC if needed, and calculates the number of payload symbols.
- **CRC16**: Computes a CRC-16 checksum for error detection in the payload.
- **gray_lut**: Generates lookup tables for Gray code encoding and decoding.
- **lora_payload**: Encodes the payload bits into LoRa symbols, applying Hamming codes and interleaving.
- **chirp**: Generates a chirp signal (frequency sweep) used in LoRa modulation.
- **lora_packet_rx**: Decodes a received LoRa packet, extracting header and payload information.
- **lora_header_decode**: Decodes the header symbols from a received packet, checks parity, and extracts metadata.
- **num2binary**: Converts a number to its binary representation as a numpy array.
- **lora_payload_n_sym**: Calculates the number of payload symbols needed for a given packet.
- **lora_payload_decode**: Decodes the payload symbols, applies whitening and CRC check, and extracts the message.
- **bit2uint8**: Converts a binary array to a uint8 number.
- **lora_preamble**: Generates the preamble (start sequence) for a LoRa packet.
- **lora_chirp**: Generates a LoRa upchirp or downchirp for modulation.
- **samples_decoding**: Scans a stream of samples for LoRa packets and decodes them.
- **rf_decode**: Detects and decodes a LoRa packet from a stream of samples.
- **complex_lora_packet**: Generates a complete LoRa packet as complex samples, including preamble and tail.
- **encode**: High-level function to encode data and transmission parameters into LoRa samples for transmission.
- **decode**: High-level function to extract LoRa packets from received samples.
- **LoRaPacket (class)**: Represents a LoRa packet, storing payload, source, destination, sequence number, and other metadata.

### lora_utils.py
- **rate_calculator**: Estimates the data rate for given LoRa parameters (spreading factor, bandwidth, coding rate).
- **gen_pack_polling**: Creates a polling packet (used for network management or broadcast).
- **pack_lora_data**: Splits large data into multiple LoRa packets, optionally with extended sequence numbers.
- **pack_lora_nack**: Creates packets for negative acknowledgments (NACK) or acknowledgments (ACK).
- **pack16bit**: Combines two bytes into a single 16-bit integer.
- **unpack_lora_data**: Reassembles the original data from an array of received LoRa packets.
- **unpack_lora_ack**: Extracts missing sequence numbers from an array of acknowledgment packets.

### lora_transceiver.py
- **bcolors (class)**: Utility for colored terminal output (for debugging).
- **threshold_trigger_process**: Monitors sample counts and triggers decoding when enough samples are collected.
- **decoder_process**: Decodes received samples for a specific spreading factor, using shared memory and multiprocessing.
- **thread_decode**: Runs the actual decoding of samples in a separate thread.
- **tx_burst**: Sends a burst of packets over the air, encoding each and transmitting via SDR.
- **tx_burst_multi_sf**: Sends bursts of packets using multiple spreading factors, combining them for transmission.
- **tx**: Continuously sends packets from a queue, encoding and transmitting each.
- **rx**: Main receiver function; reads samples from SDR, buffers them, and triggers decoding processes.
- **lora_transceiver (class)**: Main class for managing SDR hardware and LoRa communication.
  - **__init__**: Initializes SDR hardware and sets up transmission/reception parameters.
  - **rx_start**: Starts the receiver thread and sets up packet queues.
  - **rx_stop**: Stops the receiver thread.
  - **rx_pause**: Pauses reception.
  - **rx_resume**: Resumes reception.
  - **tx_send_burst**: Starts a thread to send a burst of packets.
  - **tx_send_burst_multi_sf**: Starts a thread to send bursts with multiple spreading factors.
  - **tx_start**: Starts continuous transmission using a queue.
  - **tx_stop**: Stops transmission.

## Example Usage
See `tx_example.py`, `rx_example.py`, and `tx_rx_example.py` for sample scripts demonstrating how to send and receive data.

## Requirements
- Python 3.x
- numpy, scipy
- UHD (for SDR hardware)

## Credits
This work is the modification of the original Code Developed by Authors: Fabio Busacca<sup>1</sup>, Stefano Mangione<sup>1</sup>, Ilenia Tinnirello<sup>1</sup>, Sergio Palazzo<sup>2</sup>, Francesco Restuccia<sup>3</sup>

## References
- [Implementation Paper](https://dl.acm.org/doi/pdf/10.1145/3556564.3558239)
- [LoRa Technology Overview](https://lora-alliance.org/about-lora/)
- [Software Defined Radio (SDR) Introduction](https://en.wikipedia.org/wiki/Software-defined_radio)
- [UHD Documentation](https://files.ettus.com/manual/)
- [LoRa Modulation Basics](https://www.semtech.com/uploads/documents/an1200.22.pdf)
- [Original Research Paper](https://ieeexplore.ieee.org/document/7890492)

