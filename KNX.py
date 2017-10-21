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

    def send_data(self, dest_group_addr, data, data_size):
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
        #   -> (4) Tunneling reqACKuest
        #   -----------------------------------

        #   -----------------------------------
        #   -> (5) Disconnect request
        #   -----------------------------------
        disconn_resp_object = self.disconnectRequest(conn_channel_id)

        # <- Retrieving channel_id & status from Connection State response
        state_channel_id = disconn_resp_object.channel_id
        state_status = disconn_resp_object.status
        print('Channel ID: ', state_channel_id)
        print('Channel status: ', state_status)

        print('#4 Tunneling ACK')
        # TODO

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

    def disconnectRequest(self, conn_channel_id):
        # <- Send desconnect request
        disconnect_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.DISCONNECT_REQUEST,
                                             conn_channel_id,
                                             self.control_endpoint)
        self.sock.sendto(disconnect_req.frame, (self.gateway_ip, self.gateway_port))

        # <- Receiving Connection State response
        data_recv, addr = self.sock.recvfrom(1024)
        disconn_resp_object = knxnet.decode_frame(data_recv)
        return disconn_resp_object

    def read_data(self, dest_group_addr):
        data_endpoint = ('0.0.0.0', 0)
        control_endpoint = ('0.0.0.0', 0)


        # TODO


def main(argv):
    size = ''
    data = ''
    apci = ''

    print('First arg is "', argv[0])
    print('Second arg is "', argv[1])

    dest_addr_group = knxnet.GroupAddress.from_str("1/4/1")

    c1 = connectionKNX("127.0.0.1", 3671)
    c1.send_data(dest_addr_group, 255, 2)


if __name__ == "__main__":
    main(sys.argv[1:])
