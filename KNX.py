# -*- coding: utf-8 -*-
import socket
import sys

from knxnet import *


class connectionKNX:
    def __init__(self, gateway_ip, gateway_port):
        # -> in this example, for sake of simplicity, the two ports are the same.
        self.gateway_ip = gateway_ip
        self.gateway_port = gateway_port
        self.data_endpoint = ('0.0.0.0', 0)
        self.control_endpoint = ('0.0.0.0', 0)

        # -> Socket creation
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', 3672))

    def send_data(self, data, data_size, dest_group_addr):
        #   -----------------------------------
        #   -> (1) Sending Connection request
        #   -----------------------------------

        conn_resp_object = self.connectionRequest()

        # <- Retrieving channel_id & status from Connection response
        conn_channel_id = conn_resp_object.channel_id
        conn_status = conn_resp_object.status

        print('Channel ID: ', conn_channel_id)
        print('Channel status: ', conn_status)
        print('-----------------------------------')

        #   -----------------------------------
        #   -> (2) Sending Connection State request
        #   -----------------------------------

        state_resp_object = self.connectionStateRequest(conn_channel_id)

        # <- Retrieving channel_id & status from Connection State response
        state_channel_id = state_resp_object.channel_id
        state_status = state_resp_object.status

        print('Channel ID: ', state_channel_id)
        print('Channel status: ', state_status)
        print('-----------------------------------')

        #   -----------------------------------
        #   -> (3) Tunneling request
        #   -----------------------------------

        tunnel_resp_object = self.tunnelingRequest(conn_channel_id, data, data_size, dest_group_addr)

        # <- Retrieving data from Tunneling response
        tunnel_channel_id = tunnel_resp_object.channel_id
        tunnel_status = tunnel_resp_object.status
        sequ_counter = tunnel_resp_object.sequence_counter
        print('Channel ID: ', tunnel_channel_id)
        print('Channel status: ', tunnel_status)
        print('Sequence counter: ', sequ_counter)

        print('-----------------------------------')

        #   -----------------------------------
        #   -> (4) Tunneling reqAck request
        #   -----------------------------------

        self.tunneling_ack_request(tunnel_channel_id)


        print('-----------------------------------')

        #   -----------------------------------
        #   -> (5) Disconnect request
        #   -----------------------------------

        disconnect_resp_object = self.disconnect_request(conn_channel_id)
        disconnect_resp_object = self.disconnect_request(conn_channel_id)

        # <- Retrieving data from disconnect request
        disconnect_channel_id = disconnect_resp_object.channel_id
        disconnect_status = disconnect_resp_object.status
        print('Channel ID: ', disconnect_channel_id)
        print('Channel status: ', disconnect_status)

        print('-----------------------------------')


        # TODO

    def disconnect_request(self, conn_channel_id):
        print('#5 Disconnect request')
        disconnect_req = \
            knxnet.create_frame(knxnet.ServiceTypeDescriptor.DISCONNECT_REQUEST, conn_channel_id, self.control_endpoint)
        conn_req_dtgrm = disconnect_req.frame  # -> Serializing
        self.sock.sendto(conn_req_dtgrm, (self.gateway_ip, self.gateway_port))
        data_recv, addr = self.sock.recvfrom(1024)
        disconnect_resp_object = knxnet.decode_frame(data_recv)
        return disconnect_resp_object


    def tunneling_ack_request(self, tunnel_channel_id):
        print('#4 Tunneling ACK')
        tunneling_ack = \
            knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_ACK, tunnel_channel_id, 0)
        conn_req_dtgrm = tunneling_ack.frame  # -> Serializing
        self.sock.sendto(conn_req_dtgrm, (self.gateway_ip, self.gateway_port))


    def tunnelingRequest(self, conn_channel_id, data, data_size, dest_group_addr):
        print('#3 Tunneling request')
        tunneling_req = \
            knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_REQUEST,
                                dest_group_addr,
                                conn_channel_id,
                                data,
                                data_size)
        conn_req_dtgrm = tunneling_req.frame  # -> Serializing
        self.sock.sendto(conn_req_dtgrm, (self.gateway_ip, self.gateway_port))

        # <- Receiving Connection State response
        data_recv, addr = self.sock.recvfrom(1024)
        tunnel_resp_object = knxnet.decode_frame(data_recv)
        return tunnel_resp_object

    def connectionStateRequest(self, conn_channel_id):
        print('#2 Connection State request')
        conn_state_req = \
            knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_STATE_REQUEST,
                                conn_channel_id, self.control_endpoint)
        conn_req_dtgrm = conn_state_req.frame  # -> Serializing
        self.sock.sendto(conn_req_dtgrm, (self.gateway_ip, self.gateway_port))

        # <- Receiving Connection State response
        data_recv, addr = self.sock.recvfrom(1024)
        state_resp_object = knxnet.decode_frame(data_recv)
        return state_resp_object

    def connectionRequest(self):
        print('#1 Connection request')
        conn_req_object = \
            knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_REQUEST,
                                self.control_endpoint, self.data_endpoint)
        conn_req_dtgrm = conn_req_object.frame  # -> Serializing
        self.sock.sendto(conn_req_dtgrm, (self.gateway_ip, self.gateway_port))

        # <- Receiving Connection response
        data_recv, addr = self.sock.recvfrom(1024)
        conn_resp_object = knxnet.decode_frame(data_recv)
        return conn_resp_object

    def read_data(self, dest_group_addr):
        data_endpoint = ('0.0.0.0', 0)
        control_endpoint = ('0.0.0.0', 0)

        #   -----------------------------------
        #   -> (1) Sending Connection request
        #   -----------------------------------

        conn_resp_object = self.connectionRequest()

        # <- Retrieving channel_id & status from Connection response
        conn_channel_id = conn_resp_object.channel_id
        conn_status = conn_resp_object.status

        print('Channel ID: ', conn_channel_id)
        print('Channel status: ', conn_status)
        print('-----------------------------------')

        #   -----------------------------------
        #   -> (2) Sending Connection State request
        #   -----------------------------------

        state_resp_object = self.connectionStateRequest(conn_channel_id)

        # <- Retrieving channel_id & status from Connection State response
        state_channel_id = state_resp_object.channel_id
        state_status = state_resp_object.status

        print('Channel ID: ', state_channel_id)
        print('Channel status: ', state_status)
        print('-----------------------------------')

        #   -----------------------------------
        #   -> (3) Tunneling request (read)
        #   -----------------------------------
        tunneling_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_REQUEST,
                                         dest_group_addr,
                                         conn_channel_id,
                                         0,
                                         1,
                                         0)
        self.sock.sendto(tunneling_req.frame, (self.gateway_ip, self.gateway_port))

        print('OK1')

        # <- Tunneling ack
        data_recv, addr = self.sock.recvfrom(1024)
        tunnel_resp_object = knxnet.decode_frame(data_recv)

        print('OK2')
        # <- Read tunnelling request
        data_recv, addr = self.sock.recvfrom(1024)
        tunnel_resp_object = knxnet.decode_frame(data_recv)

        print('OK3')
        # <- Send Tunneling ack
        tunnel_ack = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_ACK,
                                         conn_channel_id,
                                         0,
                                         tunnel_resp_object.sequence_counter)
        self.sock.sendto(tunnel_ack.frame, (self.gateway_ip, self.gateway_port))

        # <- Read Status
        data_recv, addr = self.sock.recvfrom(1024)
        tunnel_resp_object = knxnet.decode_frame(data_recv)


        #   -----------------------------------
        #   -> (5) Disconnect request
        #   -----------------------------------

        disconnect_resp_object = self.disconnect_request(conn_channel_id)
        disconnect_resp_object = self.disconnect_request(conn_channel_id)

        # <- Retrieving data from disconnect request
        disconnect_channel_id = disconnect_resp_object.channel_id
        disconnect_status = disconnect_resp_object.status
        print('Channel ID: ', disconnect_channel_id)
        print('Channel status: ', disconnect_status)

        print('-----------------------------------')

        return tunnel_resp_object.data


def main(argv):
    data = int(argv[0])
    size = int(argv[1])
    apci = argv[2]
    grp_add = argv[3]

    print(grp_add[0])

    print('First arg is "', argv[0])
    print('Second arg is "', argv[1])
    print('Third arg is "', argv[2])
    print('Fourth arg is "', argv[3])

    dest_addr_group = knxnet.GroupAddress.from_str(grp_add)


    c1 = connectionKNX("127.0.0.1", 3671)

    if grp_add[0] < '4' :
        c1.send_data(data, size, dest_addr_group)

    else:
        data=c1.read_data(dest_addr_group)
        print('The value is : "',data)


if __name__ == "__main__":
    # run in terminal with 'python3 KNX.py arg1 arg2 arg3'
    main(sys.argv[1:])
