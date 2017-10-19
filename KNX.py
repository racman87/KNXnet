# -*- coding: utf-8 -*-
import socket,sys
from knxnet import *

gateway_ip = "adresse IP da la passerelle KNXnet/IP"
gateway_port = Port sur lequel la passerelle KNXnet/IP écoute"

# -> in this example, for sake of simplicity, the two ports are the same.

data_endpoint = ('0.0.0.0', 3672)
control_enpoint = ('0.0.0.0', 3672)

# -> Socket creation
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('',3672))

# -> Sending Connection request
conn_req_object = \
    knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_REQUEST,
                        control_enpoint,data_endpoint)

conn_req_dtgrm = conn_req_object.frame # -> Serializing
sock.sendto (conn_req_dtgrm, (gateway_ip, gateway_port))

# <- Receiving Connection response
data_recv, addr = sock.recvfrom(1024)
conn_resp_object = knxnet.decode_frame(data_recv)

# <- Retrieving channel_id from Connection response
conn_channel_id = conn_resp_object.channel_id

#TODO