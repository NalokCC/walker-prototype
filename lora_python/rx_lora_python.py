import serial 
import time
import matplotlib.pyplot as plt

# Unique parameters
port="COM27"
tx_or_rx = "rx"
my_address = 0

# Code
time_sleep=0.2
RSSIs = []
times = []
stime = time.time()
RSSIRange = 100

fig = plt.figure()

print(f"Performing the initial {tx_or_rx} Lora setup at 115200")
with serial.Serial(port,baudrate=115200,timeout=0.5) as s:
	print("Health Check")
	time.sleep(time_sleep)
	s.write("AT\r\n".encode())
	try:
		health_message = s.read(128).decode('UTF-8')
	except:
		# When in doubt, try again
		health_message = s.read(128).decode('UTF-8')
	print(health_message)
	time.sleep(time_sleep)
	# needs to be unique
	s.write(f"AT+ADDRESS={my_address}\r\n".encode())
	time.sleep(time_sleep)
	# needs to be same for receiver and transmitter
	s.write("AT+NETWORKID=6\r\n".encode())
	time.sleep(time_sleep)
	# needs to be same for receiver and transmitter
	s.write("AT+PARAMETER=7,7,1,7\r\n".encode())
	time.sleep(time_sleep)
	# set to lower baudrate
	s.write("AT+IPR=9600\r\n".encode())
	time.sleep(time_sleep)
	s.close()

time.sleep(time_sleep)

print(f"Performing the initial {tx_or_rx} Lora setup at 9600")
with serial.Serial(port,baudrate=9600,timeout=0.5) as s:
	time.sleep(time_sleep)
	print("Health Check")
	s.write("AT\r\n".encode())
	try:
		health_message = s.read(128).decode('UTF-8')
	except:
		# When in doubt, try again
		health_message = s.read(128).decode('UTF-8')
	print(health_message)
	time.sleep(time_sleep)

	if tx_or_rx == "rx":
		print(f"Receiving data")
		while True:
			rx_message = s.read(128).decode('UTF-8')
			if len(rx_message) > 0:
				rx_packet = rx_message.split(",")
				if ("+RCV" in rx_packet[0]) and len(rx_packet) > 4:
					rx_packet_address = rx_message.split(",")[0].split("+RCV=")[1]
					rx_packet_message_length = rx_message.split(",")[1]
					rx_packet_message = rx_message.split(",")[2]
					rx_packet_rssi = rx_message.split(",")[3]
					rx_packet_snr =  rx_message.split(",")[4].split("\n")[0]

					print(f"rx_packet_address: {rx_packet_address}")
					print(f"rx_packet_message_length: {rx_packet_message_length}")
					print(f"rx_packet_message: {rx_packet_message}")
					print(f"rx_packet_rssi: {rx_packet_rssi}")
					print(f"rx_packet_snr: {rx_packet_snr}")
					time.sleep(time_sleep / 2)

					RSSIs.append(rx_packet_rssi)
					times.append(time.time()-stime)
					ax1 = plt.subplot2grid((2,1), (0,0))
					ax1.plot(RSSIs[-RSSIRange:],times[-RSSIRange:], label='RSSIs')
					plt.show()
				else:
					print(f"{rx_message} is too small or malformed")
			else:
				print(f"{rx_message} is not a valid rx_packet")
			

	if tx_or_rx == "tx":
		print(f"Transmitting data")
		while True:
			message_value = "Hello!"
			rx_address = "0"
			tx_message = f"AT+SEND={rx_address},{len(message_value)},{message_value}\r\n"
			s.write(f"{tx_message}".encode())
			time.sleep(time_sleep)