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
import sys
import subprocess
from pcap_check import *

class HtmlReport():
	def __init__(self):
		self.job_name = ''
		self.job_id = ''
		self.job_url = ''
		self.job_start_time = 'TEMPLATE_TIME'

	def generate(self):
		cwd = os.getcwd()
		self.file = open(cwd + '/test_results_oai_epc_rhel8.html', 'w')
		self.generateHeader()

		self.deploymentSummaryHeader()

		finalStatus = True
		finalStatus = self.testSummaryHeader()
		self.testSummaryDetails()
		self.testSummaryFooter()

		self.generateFooter()
		self.file.close()

		if finalStatus:
			sys.exit(0)
		else:
			sys.exit(-1)

	def generateHeader(self):
		# HTML Header
		self.file.write('<!DOCTYPE html>\n')
		self.file.write('<html class="no-js" lang="en-US">\n')
		self.file.write('<head>\n')
		self.file.write('  <meta name="viewport" content="width=device-width, initial-scale=1">\n')
		self.file.write('  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">\n')
		self.file.write('  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n')
		self.file.write('  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>\n')
		self.file.write('  <title>OAI Core Network Test Results for ' + self.job_name + ' job build #' + self.job_id + '</title>\n')
		self.file.write('</head>\n')
		self.file.write('<body><div class="container">\n')
		self.file.write('  <br>\n')
		self.file.write('  <table width = "100%" style="border-collapse: collapse; border: none;">\n')
		self.file.write('   <tr style="border-collapse: collapse; border: none;">\n')
		# SVG has a invisible background color -- adding it.
		self.file.write('     <td bgcolor="#5602a4" style="border-collapse: collapse; border: none;">\n')
		self.file.write('       <a href="https://www.magmacore.org/">\n')
		self.file.write('          <img src="https://www.magmacore.org/img/magma-logo.svg" alt="" border="none" height=50 width=150>\n')
		self.file.write('          </img>\n')
		self.file.write('       </a>\n')
		self.file.write('     </td>\n')
		self.file.write('     </td>\n')
		self.file.write('     <td style="border-collapse: collapse; border: none; vertical-align: center;">\n')
		self.file.write('       <b><font size = "6">Job Summary -- Job: ' + self.job_name + ' -- Build-ID: <a href="' + self.job_url + '">' + self.job_id + '</a></font></b>\n')
		self.file.write('     </td>\n')
		self.file.write('     <td style="border-collapse: collapse; border: none;">\n')
		self.file.write('       <a href="http://www.openairinterface.org/">\n')
		self.file.write('         <img src="http://www.openairinterface.org/wp-content/uploads/2016/03/cropped-oai_final_logo2.png" alt="" border="none" height=50 width=150>\n')
		self.file.write('         </img>\n')
		self.file.write('       </a>\n')
		self.file.write('    </tr>\n')
		self.file.write('  </table>\n')
		self.file.write('  <br>\n')

	def generateFooter(self):
		self.file.write('  <div class="well well-lg">End of Test Report -- Copyright <span class="glyphicon glyphicon-copyright-mark"></span> 2020 <a href="http://www.openairinterface.org/">OpenAirInterface</a>. All Rights Reserved.</div>\n')
		self.file.write('</div></body>\n')
		self.file.write('</html>\n')

	def deploymentSummaryHeader(self):
		self.file.write('  <h2>Deployment Summary</h2>\n')
		cwd = os.getcwd()
		if os.path.isfile(cwd + '/archives/deployment_status.log'):
			cmd = 'egrep -c "DEPLOYMENT: OK" archives/deployment_status.log || true'
			status = False
			ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
			if ret.stdout is not None:
				if ret.stdout.strip() == '1':
					status = True
			if status:
				self.file.write('  <div class="alert alert-success">\n')
				self.file.write('    <strong>Successful Deployment! <span class="glyphicon glyphicon-warning-sign"></span></strong>\n')
				self.file.write('  </div>\n')
			else:
				self.file.write('  <div class="alert alert-danger">\n')
				self.file.write('    <strong>Failed Deployment! <span class="glyphicon glyphicon-warning-sign"></span></strong>\n')
				self.file.write('  </div>\n')
		else:
			self.file.write('  <div class="alert alert-warning">\n')
			self.file.write('    <strong>LogFile not available! <span class="glyphicon glyphicon-warning-sign"></span></strong>\n')
			self.file.write('  </div>\n')
		self.file.write('  <br>\n')
		self.file.write('  <button data-toggle="collapse" data-target="#deployment-details">More details on Deployment</button>\n')
		self.file.write('  <br>\n')
		self.file.write('  <div id="deployment-details" class="collapse">\n')
		self.file.write('  <br>\n')
		self.file.write('  <table class="table-bordered" width = "80%" align = "center" border = 1>\n')
		self.file.write('     <tr bgcolor = "#33CCFF" >\n')
		self.file.write('       <th>Container Name</th>\n')
		self.file.write('       <th>Used Image Tag</th>\n')
		self.file.write('       <th>Image Creation Date</th>\n')
		self.file.write('       <th>Used Image Size</th>\n')
		self.file.write('       <th>Configuration Status</th>\n')
		self.file.write('     </tr>\n')
		self.addImageRow('cassandra')
		self.addImageRow('redis')
		self.addImageRow('magma_mme')
		self.addImageRow('oai_hss')
		self.addImageRow('oai_spgwc')
		self.addImageRow('oai_spgwu')
		self.file.write('  </table>\n')
		self.file.write('  </div>\n')

	def addImageRow(self, imageInfoPrefix):
		cwd = os.getcwd()
		if imageInfoPrefix == 'magma_mme':
			containerName = 'magma-mme'
			tagPattern = 'MAGMA_MME_TAG'
			statusPrefix = 'mme'
		if imageInfoPrefix == 'oai_hss':
			containerName = 'oai-hss'
			tagPattern = 'OAI_HSS_TAG'
			statusPrefix = 'hss'
		if imageInfoPrefix == 'oai_spgwc':
			containerName = 'oai-spgwc'
			tagPattern = 'OAI_SPGWC_TAG'
			statusPrefix = 'spgwc'
		if imageInfoPrefix == 'oai_spgwu':
			containerName = 'oai-spgwu-tiny'
			tagPattern = 'OAI_SPGWU_TAG'
			statusPrefix = 'spgwu'
		if imageInfoPrefix == 'cassandra':
			containerName = imageInfoPrefix
			tagPattern = 'N/A'
		if imageInfoPrefix == 'redis':
			containerName = imageInfoPrefix
			tagPattern = 'N/A'
		if os.path.isfile(cwd + '/archives/' + imageInfoPrefix + '_image_info.log'):
			usedTag = ''
			createDate = ''
			size = ''
			with open(cwd + '/archives/' + imageInfoPrefix + '_image_info.log') as imageLog:
				for line in imageLog:
					line = line.strip()
					result = re.search(tagPattern + ': (?P<tag>[a-zA-Z0-9\-\_:]+)', line)
					if result is not None:
						usedTag = result.group('tag')
					result = re.search('Date = (?P<date>[a-zA-Z0-9 \-\_:]+)', line)
					if result is not None:
						createDate = result.group('date')
					result = re.search('Size = (?P<size>[0-9]+) bytes', line)
					if result is not None:
						sizeInt = int(result.group('size'))
						if sizeInt < 1000000:
							sizeInt = int(sizeInt / 1000)
							size = str(sizeInt) + ' kB'
						else:
							sizeInt = int(sizeInt / 1000000)
							size = str(sizeInt) + ' MB'
			imageLog.close()
			configState = 'KO'
			cmd = 'egrep -c "STATUS: healthy" archives/' + statusPrefix + '_config.log || true'
			ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
			if ret.stdout is not None:
				if ret.stdout.strip() == '1':
					configState = 'OK'
			self.file.write('     <tr>\n')
			self.file.write('       <td>' + containerName + '</td>\n')
			self.file.write('       <td>' + usedTag + '</td>\n')
			self.file.write('       <td>' + createDate + '</td>\n')
			self.file.write('       <td>' + size + '</td>\n')
			if configState == 'OK':
				self.file.write('       <td bgcolor = "DarkGreen"><b><font color="white">' + configState + '</font></b></td>\n')
			else:
				self.file.write('       <td bgcolor = "Red"><b><font color="white">' + configState + '</font></b></td>\n')
			self.file.write('     </tr>\n')
		else:
			if imageInfoPrefix == 'cassandra':
				self.file.write('     <tr>\n')
				self.file.write('       <td>' + containerName + '</td>\n')
				self.file.write('       <td>cassandra:2.1</td>\n')
				self.file.write('       <td>N/A</td>\n')
				self.file.write('       <td>367 MB</td>\n')
				configState = 'KO'
				cmd = 'egrep -c "STATUS: healthy" archives/cassandra_status.log || true'
				ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
				if ret.stdout is not None:
					if ret.stdout.strip() == '1':
						configState = 'OK'
				if configState == 'OK':
					self.file.write('       <td bgcolor = "DarkGreen"><b><font color="white">OK</font></b></td>\n')
				else:
					self.file.write('       <td bgcolor = "Red"><b><font color="white">KO</font></b></td>\n')
				self.file.write('     </tr>\n')
			elif imageInfoPrefix == 'redis':
				self.file.write('     <tr>\n')
				self.file.write('       <td>' + containerName + '</td>\n')
				self.file.write('       <td>redis:6.0.5</td>\n')
				self.file.write('       <td>N/A</td>\n')
				self.file.write('       <td>108 MB</td>\n')
				configState = 'KO'
				cmd = 'egrep -c "STATUS: healthy" archives/redis_status.log || true'
				ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
				if ret.stdout is not None:
					if ret.stdout.strip() == '1':
						configState = 'OK'
				if configState == 'OK':
					self.file.write('       <td bgcolor = "DarkGreen"><b><font color="white">OK</font></b></td>\n')
				else:
					self.file.write('       <td bgcolor = "Red"><b><font color="white">KO</font></b></td>\n')
				self.file.write('     </tr>\n')
			else:
				self.file.write('     <tr>\n')
				self.file.write('       <td>' + containerName + '</td>\n')
				self.file.write('       <td>UNKNOWN</td>\n')
				self.file.write('       <td>N/A</td>\n')
				self.file.write('       <td>N/A</td>\n')
				self.file.write('       <td bgcolor = "DarkOrange"><b><font color="white">UNKNOW</font></b></td>\n')
				self.file.write('     </tr>\n')

	def testSummaryHeader(self):
		self.file.write('  <h2>Test with full OAI RAN Stack Summary</h2>\n')
		finalStatusOK = False

		finalOaiRanTestFile = 'archives/oai_ran_stack_test.log'
		cwd = os.getcwd()
		if os.path.isfile(cwd + '/' + finalOaiRanTestFile):
			with open(cwd + '/' + finalOaiRanTestFile, 'r') as finalLog:
				for line in finalLog:
					line = line.strip()
					result = re.search('OAI RAN STACK TEST', line)
					if result is not None:
						result = re.search('OK', line)
						if result is not None:
							finalStatusOK = True
			finalLog.close()

			if finalStatusOK:
				self.file.write('  <div class="alert alert-success">\n')
				self.file.write('    <strong>Successful Test with OAI RAN stack! <span class="glyphicon glyphicon-warning-sign"></span></strong>\n')
				self.file.write('  </div>\n')
			else:
				self.file.write('  <div class="alert alert-danger">\n')
				self.file.write('    <strong>Failed Test with OAI RAN stack! <span class="glyphicon glyphicon-warning-sign"></span></strong>\n')
				self.file.write('  </div>\n')
		else:
			finalStatusOK = False
			self.file.write('  <div class="alert alert-warning">\n')
			self.file.write('    <strong>LogFile not available! <span class="glyphicon glyphicon-warning-sign"></span></strong>\n')
			self.file.write('  </div>\n')
		return finalStatusOK

	def testSummaryDetails(self):
		self.file.write('  <br>\n')
		self.file.write('  <button data-toggle="collapse" data-target="#oai-stack-details">More details on OAI RAN test results</button>\n')
		self.file.write('  <br>\n')
		self.file.write('  <div id="oai-stack-details" class="collapse">\n')
		self.file.write('  <br>\n')
		self.file.write('  <table class="table-bordered" width = "90%" align = "center" border = 1>\n')
		self.file.write('     <tr bgcolor = "#33CCFF" >\n')
		self.file.write('       <th>Test Name</th>\n')
		self.file.write('       <th>Test Status</th>\n')
		self.file.write('       <th>Test Details</th>\n')
		self.file.write('     </tr>\n')
		pcap_list = [f for f in os.listdir('archives') if os.path.isfile(os.path.join('archives', f)) and f.endswith('.pcap')]
		for pcap_fil in pcap_list:
			# MME to HSS Connection
			res = check_if_mme_connects_to_hss('archives/' + pcap_fil)
			self.addSectionRow('MME HSS S6A Connection')
			self.addDetailsRow('MME S6A Request', res['mme_request'], 'Realm = ' + res['origin_realm'])
			self.addDetailsRow('HSS S6A Response', res['mme_request'], 'Host = ' + res['origin_host'])
			# eNB to MME S1 Connection
			res = check_if_enb_connects_to_mme('archives/' + pcap_fil)
			self.addSectionRow('eNB S1 Setup to MME')
			self.addDetailsRow('eNB SCTP INIT', res['enb_init_req'], 'n/a')
			self.addDetailsRow('MME SCTP INIT_ACK', res['mme_init_answer'], 'n/a')
			details = 'MCC = ' + res['enb_mcc'] + '\n'
			details += 'MNC = ' + res['enb_mnc'] + '\n'
			details += 'eNB Name = ' + res['enb_name']
			self.addDetailsRow('eNB S1 Setup Request', res['enb_s1_setup_req'], details)
			self.addDetailsRow('MME S1 Setup Response', res['mme_s1_setup_res'], 'n/a')
			# UE attachment
			res = check_if_ue_attachs('archives/' + pcap_fil)
			self.addSectionRow('UE Attachment')
			self.addDetailsRow('UE Attach Request', res['ue_init_msg'], 'IMSI = ' + res['ue_imsi'])
			self.addDetailsRow('MME NAS Auth Request', res['nas_auth_req'], 'n/a')
			self.addDetailsRow('UE NAS Auth Res', res['nas_auth_res'], 'n/a')
			self.addDetailsRow('MME NAS Security Mode Command', res['nas_security_cmd'], 'n/a')
			self.addDetailsRow('UE NSA Security Mode Complete', res['nas_security_cmplt'], 'n/a')
			details = 'IMSI = ' + res['s11_cr_sess_imsi'] + '\n'
			details += 'MCC = ' + res['s11_cr_sess_mcc'] + '\n' 
			details += 'MNC = ' + res['s11_cr_sess_mnc'] + '\n' 
			details += 'APN = ' + res['s11_cr_sess_apn']
			self.addDetailsRow('S11 Create Session Request', res['s11_create_session_req'], details)
			details = 'PDN IP ADDR = ' + res['s11_cr_sess_pdn_addr']
			self.addDetailsRow('S11 Create Session Response', res['s11_create_session_res'], details)
			details = 'APN = ' + res['apn'] + '\n'
			details += 'Transport Layer IP (ie SPGW-U) = ' + res['transportlayeraddress']
			self.addDetailsRow('MME NAS UE Initial Context', res['initial_ue_context_req'], details)
			details = 'Transport Layer IP (ie eNB) = ' + res['enb_transportlayeraddress']
			self.addDetailsRow('UE NAS UE Initial Context Response', res['initial_ue_context_res'], details)
			details = 'eNB F-TEID = ' + res['s11_mod_bear_fteid']
			self.addDetailsRow('S11 Modify Bearer Request', res['s11_modify_bearer_req'], details)
			details = 'SPGW-U F-TEID = ' + res['s11_mod_bear_ufteid']
			self.addDetailsRow('S11 Modify Bearer Response', res['s11_modify_bearer_res'], details)
		self.file.write('  </table>\n')
		self.file.write('  </div>\n')

	def addSectionRow(self, sectionName):
		self.file.write('     <tr bgcolor = "LightGray">\n')
		self.file.write('       <td align = "center" colspan = "3">' + sectionName + '</td>\n')
		self.file.write('     </tr>\n')

	def addDetailsRow(self, testName, status, details):
		self.file.write('     <tr>\n')
		self.file.write('       <td>' + testName + '</td>\n')
		if status:
			self.file.write('       <td bgcolor = "Green"><font color="white"><b>OK</b></font></td>\n')
		else:
			self.file.write('       <td bgcolor = "Red"><font color="white"><b>KO</b></font></td>\n')
		self.file.write('       <td><pre>'+ details + '</td>\n')
		self.file.write('     </tr>\n')

	def testSummaryFooter(self):
		self.file.write('  <br>\n')

def Usage():
	print('----------------------------------------------------------------------------------------------------------------------')
	print('dsTestGenerateHTMLReport.py')
	print('   Generate an HTML report for the Jenkins pipeline on openair-epc-fed.')
	print('----------------------------------------------------------------------------------------------------------------------')
	print('Usage: python3 generateHtmlReport.py [options]')
	print('  --help  Show this help.')
	print('---------------------------------------------------------------------------------------------- Mandatory Options -----')
	print('  --job_name=[Jenkins Job name]')
	print('  --job_id=[Jenkins Job Build ID]')
	print('  --job_url=[Jenkins Job Build URL]')

#--------------------------------------------------------------------------------------------------------
#
# Start of main
#
#--------------------------------------------------------------------------------------------------------

argvs = sys.argv
argc = len(argvs)

HTML = HtmlReport()

while len(argvs) > 1:
	myArgv = argvs.pop(1)
	if re.match('^\-\-help$', myArgv, re.IGNORECASE):
		Usage()
		sys.exit(0)
	elif re.match('^\-\-job_name=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-job_name=(.+)$', myArgv, re.IGNORECASE)
		HTML.job_name = matchReg.group(1)
	elif re.match('^\-\-job_id=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-job_id=(.+)$', myArgv, re.IGNORECASE)
		HTML.job_id = matchReg.group(1)
	elif re.match('^\-\-job_url=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-job_url=(.+)$', myArgv, re.IGNORECASE)
		job_url = matchReg.group(1)
		result = re.search('oai-public.apps.5glab.nsa.eurecom.fr', job_url)
		if result is not None:
			job_url = job_url.replace('oai-public.apps.5glab.nsa.eurecom.fr','oai.eurecom.fr')
		HTML.job_url = job_url
	else:
		sys.exit('Invalid Parameter: ' + myArgv)

if HTML.job_name == '' or HTML.job_id == '' or HTML.job_url == '':
	sys.exit('Missing Parameter in job description')

HTML.generate()

