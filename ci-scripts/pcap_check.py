#/*
# * Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
# * contributor license agreements.  See the NOTICE file distributed with
# * this work for additional information regarding copyright ownership.
# * The OpenAirInterface Software Alliance licenses this file to You under
# * the OAI Public License, Version 1.1  (the "License"); you may not use this file
# * except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *   http://www.openairinterface.org/?page_id=698
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *-------------------------------------------------------------------------------
# * For more information about the OpenAirInterface (OAI) Software Alliance:
# *   contact@openairinterface.org
# */
#---------------------------------------------------------------------

import os
import re
import socket
import struct
import sys
import subprocess
import pyshark

# IP addresses
HSS_IP_ADDRESS = '192.168.61.67'
MME_IP_ADDRESS = '192.168.61.68'
SPGWC_IP_ADDRESS = '192.168.61.70'
SPGWU_IP_ADDRESS = '192.168.61.71'
ENB_IP_ADDRESS = '192.168.61.80'

# Diameter constants
FLAGS__REQUEST = '0x00000080'
FLAGS__ANSWER = '0x00000000'

CMD_CODE__ABORT_SESSION = '274'
CMD_CODE__ACCOUNTING = '271'
CMD_CODE__CAPABILITIES_EXCHANGE = '257'
CMD_CODE__DEVICE_WATCHDOG = '280'
CMD_CODE__DISCONNECT_PEER = '282'
CMD_CODE__RE_AUTH = '258'
CMD_CODE__SESSION_TERMINATE = '275'

RES_CODE__DIAMETER_SUCCESS = '2001'
RES_CODE__DIAMETER_LIMITED_SUCCESS = '2002'
RES_CODE__COMMAND_UNSUPPORTED = '3001'
RES_CODE__UNABLE_TO_DELIVER = '3002'
RES_CODE__REALM_NOT_SERVED = '3003'
RES_CODE__TOO_BUSY = '3003'

# SCTP Constants
CHUNK_TYPE__DATA = '0'
CHUNK_TYPE__INIT = '1'
CHUNK_TYPE__INIT_ACK = '2'
CHUNK_TYPE__SACK = '3'
CHUNK_TYPE__ABORT = '6'
CHUNK_TYPE__SHUTDOWN = '7'
CHUNK_TYPE__SHUTDOWN_ACK = '8'
CHUNK_TYPE__ERROR = '9'
CHUNK_TYPE__AUTH = '15'

# S1AP Constants
S1AP_PDU_INITIATINGMESSAGE = '0'
S1AP_PDU_SUCCESSFULOUTCOME = '1'

PROC_CODE__ID_S1SETUP = '17'
PROC_CODE__ID_INITIALUEMESSAGE = '12'
PROC_CODE__ID_DOWNLINKNASTRANSPORT = '11'
PROC_CODE__ID_UPLINKNASTRANSPORT = '13'
PROC_CODE__ID_INITIALCONTEXTSETUP = '9'

NAS__AUTHENTICATION_REQ = '82'
NAS__AUTHENTICATION_RES = '83'
NAS__SECURITY_MODE_CMD = '93'
NAS__SECURITY_MODE_COMPLETE = '94'
NAS__ATTACH_ACCEPT = '66'

# GTPV2 Constants
GTPV2_MSG_TYPE__CREATE_SESSION_REQUEST = '32'
GTPV2_MSG_TYPE__CREATE_SESSION_RESPONSE = '33'
GTPV2_MSG_TYPE__MODIFY_BEARER_REQUEST = '34'
GTPV2_MSG_TYPE__MODIFY_BEARER_RESPONSE = '35'
GTPV2_MSG_TYPE__DELETE_SESSION_REQUEST = '36'
GTPV2_MSG_TYPE__DELETE_SESSION_RESPONSE = '37'

# PGCP Constants
PFCP_MSG_TYPE__SX_HEARTBEAT_REQUEST = '1'
PFCP_MSG_TYPE__SX_HEARTBEAT_RESPONSE = '2'
PFCP_MSG_TYPE__SX_ASSOCIATION_SETUP_REQUEST = '5'
PFCP_MSG_TYPE__SX_ASSOCIATION_SETUP_RESPONSE = '6'
PFCP_NODE_ID_TYPE__FQDN = '2'

def check_if_mme_connects_to_hss(pcap_file):
	""" Normally the 2 first DIAMETER packets are the MME <-> HSS peerage """
	res = {}
	res['mme_request'] = False
	res['hss_answer'] = False
	res['origin_host'] = ''
	res['origin_realm'] = ''
	try:
		cap = {}
		cap = pyshark.FileCapture(pcap_file, keep_packets=True, display_filter="tcp.port == 3868")
		cnt = 0
		for pkt in cap:
			if pkt is not None:
				if 'DIAMETER' in pkt:
					if cnt == 0:
						if pkt.diameter.flags == FLAGS__REQUEST and pkt.diameter.cmd_code == CMD_CODE__CAPABILITIES_EXCHANGE: 
							res['mme_request'] = True
					if cnt == 1:
						if pkt.diameter.flags == FLAGS__ANSWER and pkt.diameter.cmd_code == CMD_CODE__CAPABILITIES_EXCHANGE:
							if pkt.diameter.result_code == RES_CODE__DIAMETER_SUCCESS:
								res['hss_answer'] = True
								res['origin_host']=pkt.diameter.origin_host
								res['origin_realm']=pkt.diameter.origin_realm
					cnt += 1
		cap.close()
	except Exception as e:
		print('Could not open MME PCAP file')
	return res

def check_if_enb_connects_to_mme(pcap_file):
	"""
	Sequence is:
    - INIT
    - INIT_ACK
    - S1SetupRequest
    - S1SetupResponse
	"""
	res = {}
	res['enb_init_req'] = False
	res['mme_init_answer'] = False
	res['enb_s1_setup_req'] = False
	res['mme_s1_setup_res'] = False
	res['enb_mcc'] = ''
	res['enb_mnc'] = ''
	res['enb_name'] = ''
	try:
		cap = {}
		cap = pyshark.FileCapture(pcap_file, keep_packets=True, display_filter="sctp.port == 36412")
		cnt = 0
		for pkt in cap:
			if pkt is not None:
				if 'SCTP' in pkt:
					if pkt.sctp.chunk_type == CHUNK_TYPE__INIT:
						if pkt.ip.src == ENB_IP_ADDRESS and pkt.ip.dst == MME_IP_ADDRESS:
							res['enb_init_req'] = True
					if pkt.sctp.chunk_type == CHUNK_TYPE__INIT_ACK:
						if pkt.ip.src == MME_IP_ADDRESS and pkt.ip.dst == ENB_IP_ADDRESS:
							res['mme_init_answer'] = True
					if pkt.sctp.chunk_type == CHUNK_TYPE__DATA:
						if pkt.ip.src == ENB_IP_ADDRESS and pkt.ip.dst == MME_IP_ADDRESS and 'S1AP' in pkt:
							if pkt.s1ap.procedurecode == PROC_CODE__ID_S1SETUP and pkt.s1ap.s1ap_pdu == S1AP_PDU_INITIATINGMESSAGE:
								res['enb_s1_setup_req'] = True
								res['enb_mcc'] = pkt.s1ap.e212_mcc
								res['enb_mnc'] = pkt.s1ap.e212_mnc
								res['enb_name'] = pkt.s1ap.enbname
						if pkt.ip.src == MME_IP_ADDRESS and pkt.ip.dst == ENB_IP_ADDRESS and 'S1AP' in pkt:
							if pkt.s1ap.procedurecode == PROC_CODE__ID_S1SETUP and pkt.s1ap.s1ap_pdu == S1AP_PDU_SUCCESSFULOUTCOME:
								res['mme_s1_setup_res'] = True
							elif pkt.s1ap.procedurecode == PROC_CODE__ID_S1SETUP:
								res['mme_s1_setup_res'] = False
					cnt += 1
		cap.close()
	except Exception as e:
		print('Could not open MME PCAP file')
	return res

def check_if_ue_attachs(pcap_file):
	res = {}
	res['ue_init_msg'] = False
	res['nas_auth_req'] = False
	res['nas_auth_res'] = False
	res['nas_security_cmd'] = False
	res['nas_security_cmplt'] = False
	res['initial_ue_context_req'] = False
	res['initial_ue_context_res'] = False
	res['s11_create_session_req'] = False
	res['s11_create_session_res'] = False
	res['s11_modify_bearer_req'] = False
	res['s11_modify_bearer_res'] = False
	res['ue_imsi'] = ''
	res['apn'] = ''
	res['transportlayeraddress'] = ''
	res['enb_transportlayeraddress'] = ''
	res['s11_cr_sess_imsi'] = ''
	res['s11_cr_sess_mcc'] = ''
	res['s11_cr_sess_mnc'] = ''
	res['s11_cr_sess_apn'] = ''
	res['s11_cr_sess_pdn_addr'] = ''
	res['s11_mod_bear_fteid'] = ''
	res['s11_mod_bear_ufteid'] = ''
	try:
		cap = {}
		cap = pyshark.FileCapture(pcap_file, keep_packets=True, display_filter="sctp.port == 36412 || udp.port == 2123")
		cnt = 0
		for pkt in cap:
			if pkt is not None:
				if 'SCTP' in pkt:
					if pkt.sctp.chunk_type == CHUNK_TYPE__DATA:
						if pkt.ip.src == ENB_IP_ADDRESS and pkt.ip.dst == MME_IP_ADDRESS and 'S1AP' in pkt:
							if pkt.s1ap.procedurecode == PROC_CODE__ID_INITIALUEMESSAGE and pkt.s1ap.s1ap_pdu == S1AP_PDU_INITIATINGMESSAGE:
								res['ue_init_msg'] = True
								res['ue_imsi'] = pkt.s1ap.e212_imsi
								print('UE --> send NAS INITIAL UE MESSAGE (pkt #' + str(cnt) + ')')
							# The UE Initial Context Response has 2 S1AP layers!
							myLayers = pkt.get_multiple_layers('S1AP')
							if len(myLayers) == 2:
								if myLayers[0].procedurecode == PROC_CODE__ID_INITIALCONTEXTSETUP and myLayers[0].s1ap_pdu == S1AP_PDU_SUCCESSFULOUTCOME and \
									 myLayers[1].procedurecode == PROC_CODE__ID_UPLINKNASTRANSPORT and myLayers[1].s1ap_pdu == S1AP_PDU_INITIATINGMESSAGE:
									res['initial_ue_context_res'] = True
									res['enb_transportlayeraddress'] = myLayers[0].transportlayeraddressipv4
									#print (myLayers[1].nas_eps_nas_msg_emm_type)
									print('UE --> send UE INITIAL UE CONTEXT RESPONSE (pkt #' + str(cnt) + ')')

					if pkt.sctp.chunk_type == CHUNK_TYPE__SACK:
						if pkt.ip.src == MME_IP_ADDRESS and pkt.ip.dst == ENB_IP_ADDRESS and 'S1AP' in pkt:
							if pkt.s1ap.procedurecode == PROC_CODE__ID_DOWNLINKNASTRANSPORT and pkt.s1ap.s1ap_pdu == S1AP_PDU_INITIATINGMESSAGE:
								if pkt.s1ap.nas_eps_nas_msg_emm_type == NAS__AUTHENTICATION_REQ:
									res['nas_auth_req'] = True
									print('MME --> send NAS AUTHENTICATION_REQ (pkt #' + str(cnt) + ')')
								if pkt.s1ap.nas_eps_nas_msg_emm_type == NAS__SECURITY_MODE_CMD:
									res['nas_security_cmd'] = True
									print('MME --> send NAS SECURITY_MODE_CMD (pkt #' + str(cnt) + ')')
							if pkt.s1ap.procedurecode == PROC_CODE__ID_INITIALCONTEXTSETUP and pkt.s1ap.s1ap_pdu == S1AP_PDU_INITIATINGMESSAGE:
								if pkt.s1ap.nas_eps_nas_msg_emm_type == NAS__ATTACH_ACCEPT:
									res['initial_ue_context_req'] = True
									res['apn'] = pkt.s1ap.gsm_a_gm_sm_apn
									res['transportlayeraddress'] = pkt.s1ap.transportlayeraddressipv4
									print('MME --> send NAS INITIAL UE CONTEXT (pkt #' + str(cnt) + ')')

						if pkt.ip.src == ENB_IP_ADDRESS and pkt.ip.dst == MME_IP_ADDRESS and 'S1AP' in pkt:
							if pkt.s1ap.procedurecode == PROC_CODE__ID_UPLINKNASTRANSPORT and pkt.s1ap.s1ap_pdu == S1AP_PDU_INITIATINGMESSAGE:
								if pkt.s1ap.nas_eps_nas_msg_emm_type == NAS__AUTHENTICATION_RES:
									res['nas_auth_res'] = True
									print('eNB --> send NAS AUTHENTICATION_RES (pkt #' + str(cnt) + ')')
								if pkt.s1ap.nas_eps_nas_msg_emm_type == NAS__SECURITY_MODE_COMPLETE:
									res['nas_security_cmplt'] = True
									print('eNB --> send NAS SECURITY_MODE_COMPLETE (pkt #' + str(cnt) + ')')
					cnt += 1
				if 'GTPV2' in pkt:
					if pkt.ip.src == MME_IP_ADDRESS and pkt.ip.dst == SPGWC_IP_ADDRESS:
						if pkt.gtpv2.message_type == GTPV2_MSG_TYPE__CREATE_SESSION_REQUEST:
							res['s11_create_session_req'] = True
							res['s11_cr_sess_imsi'] = pkt.gtpv2.e212_imsi
							res['s11_cr_sess_mcc'] = pkt.gtpv2.e212_tai_mcc
							res['s11_cr_sess_mnc'] = pkt.gtpv2.e212_tai_mnc
							res['s11_cr_sess_apn'] = pkt.gtpv2.apn
							print('S11 CREATE SESSION REQ (pkt #' + str(cnt) + ')')
						if pkt.gtpv2.message_type == GTPV2_MSG_TYPE__MODIFY_BEARER_REQUEST:
							res['s11_modify_bearer_req'] = True
							res['s11_mod_bear_fteid'] = pkt.gtpv2.f_teid_ipv4
							print('S11 MODIFY BEARER REQ (pkt #' + str(cnt) + ')')
					if pkt.ip.src == SPGWC_IP_ADDRESS and pkt.ip.dst == MME_IP_ADDRESS:
						if pkt.gtpv2.message_type == GTPV2_MSG_TYPE__CREATE_SESSION_RESPONSE:
							res['s11_create_session_res'] = True
							res['s11_cr_sess_pdn_addr'] = pkt.gtpv2.pdn_addr_and_prefix_ipv4
							print('S11 CREATE SESSION RES (pkt #' + str(cnt) + ')')
						if pkt.gtpv2.message_type == GTPV2_MSG_TYPE__MODIFY_BEARER_RESPONSE:
							res['s11_modify_bearer_res'] = True
							res['s11_mod_bear_ufteid'] = pkt.gtpv2.f_teid_ipv4
							print('S11 MODIFY BEARER RES (pkt #' + str(cnt) + ')')
					cnt += 1
		cap.close()
	except Exception as e:
		print('Could not open MME PCAP file')
	return res

def check_if_spgwu_connects_to_spgwc(pcap_file):
	""" Normally the 2 first PFCP packets are the SPGWC <-> SPGWU association """
	res = {}
	res['spgwu_request'] = False
	res['spgwc_answer'] = False
	res['spgwu_fdqn'] = ''
	res['spgwc_ipv4'] = ''
	try:
		cap = {}
		cap = pyshark.FileCapture(pcap_file, keep_packets=True, display_filter="udp.port == 8805")
		cnt = 0
		for pkt in cap:
			if pkt is not None:
				if 'PFCP' in pkt:
					if cnt == 0:
						if pkt.pfcp.msg_type == PFCP_MSG_TYPE__SX_ASSOCIATION_SETUP_REQUEST and pkt.pfcp.node_id_type == PFCP_NODE_ID_TYPE__FQDN: 
							res['spgwu_request'] = True
							res['spgwu_fdqn'] = pkt.pfcp.node_id_fqdn
					if cnt == 1:
						if pkt.pfcp.msg_type == PFCP_MSG_TYPE__SX_ASSOCIATION_SETUP_RESPONSE:
							if pkt.pfcp.cause == '1':
								res['spgwc_answer'] = True
								res['spgwc_ipv4']=pkt.pfcp.node_id_ipv4
					cnt += 1
		cap.close()
	except Exception as e:
		print('Could not open SPGWC PCAP file')
	return res

def check_cups_heartbeat(pcap_file):
	""" Normally the heartbeat request/response pace is one every second """
	res = {}
	res['spgwc_hrt_request'] = False
	res['spgwu_hrt_answer'] = False
	res['spgwc_hrt_nb_req'] = '0'
	res['spgwu_hrt_nb_res'] = '0'
	nb_requests = 0
	nb_responses = 0
	try:
		cap = {}
		cap = pyshark.FileCapture(pcap_file, keep_packets=True, display_filter="udp.port == 8805")
		cnt = 0
		for pkt in cap:
			if pkt is not None:
				if 'PFCP' in pkt:
					if pkt.pfcp.msg_type == PFCP_MSG_TYPE__SX_HEARTBEAT_REQUEST:
						nb_requests += 1
					if pkt.pfcp.msg_type == PFCP_MSG_TYPE__SX_HEARTBEAT_RESPONSE:
						nb_responses += 1
					cnt += 1
		cap.close()
	except Exception as e:
		print('Could not open SPGWC PCAP file')
	if nb_requests > 0:
		res['spgwc_hrt_request'] = True
		res['spgwc_hrt_nb_req'] = str(nb_requests)
	if nb_responses > 0:
		res['spgwu_hrt_answer'] = True
		res['spgwu_hrt_nb_res'] = str(nb_responses)
	return res
