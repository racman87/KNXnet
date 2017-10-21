# -*- coding: utf-8 -*-
import socket
import sys

from knxnet import *

# -> in this example, for sake of simplicity, the two ports are the same.
def init():
    gateway_ip = "127.0.0.1"
    gateway_port = 3671
    # -> Socket creation
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 3672))



def send_data(dest_group_addr, data, data_size):

    data_endpoint = ('0.0.0.0', 0)
    control_endpoint = ('0.0.0.0', 0)


    #   -----------------------------------
    #   -> (1) Sending Connection request
    #   -----------------------------------
    print('#1 Connection request')
    conn_req_object = \
		knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_REQUEST,
							control_endpoint, data_endpoint)

	conn_req_dtgrm = conn_req_object.frame  # -> Serializing
	sock.sendto(conn_req_dtgrm, (gateway_ip, gateway_port))

	# <- Receiving Connection response
	data_recv, addr = sock.recvfrom(1024)
	conn_resp_object = knxnet.decode_frame(data_recv)

	# <- Retrieving channel_id & status from Connection response
	conn_channel_id = conn_resp_object.channel_id
	conn_status = conn_resp_object.status
	print('Channel ID: ', conn_channel_id)
	print('Channel status: ', conn_status)

	print('-----------------------------------')

	#   -----------------------------------
	#   -> (2) Sending Connection State request
	#   -----------------------------------

	print('#2 Connection State request')
	conn_req_object = \
		knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_STATE_REQUEST,
							conn_channel_id, control_endpoint)

	conn_req_dtgrm = conn_req_object.frame  # -> Serializing
	sock.sendto(conn_req_dtgrm, (gateway_ip, gateway_port))

	# <- Receiving Connection State response
	data_recv, addr = sock.recvfrom(1024)
	conn_resp_object = knxnet.decode_frame(data_recv)

	# <- Retrieving channel_id & status from Connection State response
	conn_channel_id = conn_resp_object.channel_id
	conn_status = conn_resp_object.status
	print('Channel ID: ', conn_channel_id)
	print('Channel status: ', conn_status)

	print('-----------------------------------')

	#   -----------------------------------
	#   -> (3) Tunneling request
	#   -----------------------------------

	print('#3 Tunneling request')

	dest_addr_group = knxnet.GroupAddress.from_str("1/4/1")

	conn_req_object = \
		knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_REQUEST,
							dest_addr_group,
							conn_channel_id,
							255,
							2)

	conn_req_dtgrm = conn_req_object.frame  # -> Serializing
	sock.sendto(conn_req_dtgrm, (gateway_ip, gateway_port))

	# <- Receiving Connection State response
	data_recv, addr = sock.recvfrom(1024)
	conn_resp_object = knxnet.decode_frame(data_recv)

	# <- Retrieving data from Tunneling response
	conn_channel_id = conn_resp_object.channel_id
	conn_status = conn_resp_object.status
	sequ_counter = conn_resp_object.sequence_counter
	print('Channel ID: ', conn_channel_id)
	print('Channel status: ', conn_status)
	print('Sequence counter: ', sequ_counter)

	print('-----------------------------------')


	#   -----------------------------------
	#   -> (3) Tunneling reqACKuest
	#   -----------------------------------

	print('#4 Tunneling ACK')
	# TODO

def read_data(dest_group_addr):
	data_endpoint = ('0.0.0.0', 0)
	control_endpoint = ('0.0.0.0', 0)


    # TODO

def main(argv):
    size = ''
    data = ''
    apci = ''

    print('First arg is "', argv[0])
    print('Second arg is "', argv[1])


if __name__ == "__main__":
    main(sys.argv[1:])
