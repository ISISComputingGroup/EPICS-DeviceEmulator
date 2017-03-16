import serial
import time
import socket
import threading
import argparse


def listen_to_tcp(tcp_conn, ser_conn):
    while 1:
        tcp_data = tcp_conn.recv(1024)
        if len(data) > 0:
            ser_conn.writelines(tcp_data)
            print "Data on tcp: " + str(tcp_data)
        time.sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transfers the data being sent to a COM port to be sent to a TCP port.")
    parser.add_argument("tcp_port", help="The port to send TCP messages to. (e.g. 57677)", type=int)
    parser.add_argument("com_port", help="The COM port to send serial messages to. (e.g. COM2)")
    parser.add_argument('-b', "--baud", help="The baud rate to communicate on the COM port.", default=9600)

    args = parser.parse_args()

    tcp = socket.create_connection(('localhost', args.tcp_port))
    ser = serial.Serial(args.com_port, args.baud)

    listen_thread = threading.Thread(target=listen_to_tcp, args=(tcp, ser))
    listen_thread.start()

    print "Listening on " + str(args.com_port) + " and localhost:" + str(args.tcp_port)
    print "Press Ctrl+C+Break to stop"

    while True:
        if ser.inWaiting():
            data = ser.readline()
            print "Data on serial: " + data
            tcp.sendall(data)

        time.sleep(0.1)

