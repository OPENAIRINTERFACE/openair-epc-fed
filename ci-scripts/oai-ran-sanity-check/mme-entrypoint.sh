#!/bin/bash

function generateConfFile()
{
  set +x
  rm -f mme.conf
  echo 'MME :' >> mme.conf
  echo '{' >> mme.conf
  echo '    REALM                                     = "'$REALM'"' >> mme.conf
  echo '    PID_DIRECTORY                             = "/var/run";' >> mme.conf
  echo '    MAXENB                                    = 8;                              # power of 2' >> mme.conf
  echo '    MAXUE                                     = 16;                             # power of 2' >> mme.conf
  echo '    RELATIVE_CAPACITY                         = 10;' >> mme.conf
  echo '' >> mme.conf
  echo '    EMERGENCY_ATTACH_SUPPORTED                     = "no";' >> mme.conf
  echo '    UNAUTHENTICATED_IMSI_SUPPORTED                 = "no";' >> mme.conf
  echo '' >> mme.conf
  echo '    # EPS network feature support' >> mme.conf
  echo '    EPS_NETWORK_FEATURE_SUPPORT_IMS_VOICE_OVER_PS_SESSION_IN_S1      = "no";    # DO NOT CHANGE' >> mme.conf
  echo '    EPS_NETWORK_FEATURE_SUPPORT_EMERGENCY_BEARER_SERVICES_IN_S1_MODE = "no";    # DO NOT CHANGE' >> mme.conf
  echo '    EPS_NETWORK_FEATURE_SUPPORT_LOCATION_SERVICES_VIA_EPC            = "no";    # DO NOT CHANGE' >> mme.conf
  echo '    EPS_NETWORK_FEATURE_SUPPORT_EXTENDED_SERVICE_REQUEST             = "no";    # DO NOT CHANGE' >> mme.conf
  echo '' >> mme.conf
  echo '    # Display statistics about whole system (expressed in seconds)' >> mme.conf
  echo '    MME_STATISTIC_TIMER                       = 10;' >> mme.conf
  echo '    IP_CAPABILITY = "IPV4";                                                   # UE PDN_TYPE' >> mme.conf
  echo '    USE_STATELESS = "";' >> mme.conf
  echo '' >> mme.conf
  echo '    INTERTASK_INTERFACE :' >> mme.conf
  echo '    {' >> mme.conf
  echo '        # max queue size per task' >> mme.conf
  echo '        ITTI_QUEUE_SIZE            = 2000000;' >> mme.conf
  echo '    };' >> mme.conf
  echo '' >> mme.conf
  echo '    S6A :' >> mme.conf
  echo '    {' >> mme.conf
  echo '        S6A_CONF                   = "'$PREFIX'/mme_fd.conf"; # YOUR MME freeDiameter config file path' >> mme.conf
  echo '        HSS_HOSTNAME               = "'$HSS_FQDN'";' >> mme.conf
  echo '        HSS_REALM                  = "'$HSS_REALM'";' >> mme.conf
  echo '    };' >> mme.conf
  echo '' >> mme.conf
  echo '    # ------- SCTP definitions' >> mme.conf
  echo '    SCTP :' >> mme.conf
  echo '    {' >> mme.conf
  echo '        # Number of streams to use in input/output' >> mme.conf
  echo '        SCTP_INSTREAMS  = 8;' >> mme.conf
  echo '        SCTP_OUTSTREAMS = 8;' >> mme.conf
  echo '    };' >> mme.conf
  echo '' >> mme.conf
  echo '    # ------- S1AP definitions' >> mme.conf
  echo '    S1AP :' >> mme.conf
  echo '    {' >> mme.conf
  echo '        # outcome drop timer value (seconds)' >> mme.conf
  echo '        S1AP_OUTCOME_TIMER = 10;' >> mme.conf
  echo '    };' >> mme.conf
  echo '    # ------- MME served GUMMEIs' >> mme.conf
  echo '    GUMMEI_LIST = (' >> mme.conf
  echo '         { MCC="'$MCC'" ; MNC="'$MNC'"; MME_GID="455" ; MME_CODE="5"; }' >> mme.conf
  echo '    );' >> mme.conf
  echo '' >> mme.conf
  echo '    # ------- MME served TAIs' >> mme.conf
  echo '    TAI_LIST = (' >> mme.conf
  echo '         {MCC="'$MCC'" ; MNC="'$MNC'";  TAC = "'$TAC0'"; },' >> mme.conf
  echo '         {MCC="'$MCC'" ; MNC="'$MNC'";  TAC = "2"; },' >> mme.conf
  echo '         {MCC="'$MCC'" ; MNC="'$MNC'";  TAC = "3"; }' >> mme.conf
  echo '    );' >> mme.conf
  echo '' >> mme.conf
  echo '    TAC_LIST = (' >> mme.conf
  echo '         {MCC="'$MCC'" ; MNC="'$MNC'";  TAC = "'$TAC0'"; }' >> mme.conf
  echo '    );' >> mme.conf
  echo '' >> mme.conf
  echo '    CSFB :' >> mme.conf
  echo '    {' >> mme.conf
  echo '        NON_EPS_SERVICE_CONTROL = "OFF";' >> mme.conf
  echo '        CSFB_MCC = "'$MCC'";' >> mme.conf
  echo '        CSFB_MNC = "'$MNC'";' >> mme.conf
  echo '        LAC = "1";' >> mme.conf
  echo '    };' >> mme.conf
  echo '    NAS :' >> mme.conf
  echo '    {' >> mme.conf
  echo '        ORDERED_SUPPORTED_INTEGRITY_ALGORITHM_LIST = [ "EIA2" , "EIA1" , "EIA0" ];' >> mme.conf
  echo '        ORDERED_SUPPORTED_CIPHERING_ALGORITHM_LIST = [ "EEA0" , "EEA1" , "EEA2" ];' >> mme.conf
  echo '        T3402                                 =  1                              # in minutes (default is 12 minutes)' >> mme.conf
  echo '        T3412                                 =  54                             # in minutes (default is 54 minutes, network dependent)' >> mme.conf
  echo '        T3422                                 =  6                              # in seconds (default is 6s)' >> mme.conf
  echo '        T3450                                 =  6                              # in seconds (default is 6s)' >> mme.conf
  echo '        T3460                                 =  6                              # in seconds (default is 6s)' >> mme.conf
  echo '        T3470                                 =  6                              # in seconds (default is 6s)' >> mme.conf
  echo '        T3485                                 =  8                              # UNUSED in seconds (default is 8s)' >> mme.conf
  echo '        T3486                                 =  8                              # UNUSED in seconds (default is 8s)' >> mme.conf
  echo '        T3489                                 =  4                              # UNUSED in seconds (default is 4s)' >> mme.conf
  echo '        T3495                                 =  8                              # UNUSED in seconds (default is 8s)' >> mme.conf
  echo '    };' >> mme.conf
  echo '' >> mme.conf
  echo '    SGS :' >> mme.conf
  echo '    {' >> mme.conf
  echo '        TS6_1                                 =  10                             # in seconds (default is 10s)' >> mme.conf
  echo '        TS8                                   =  4                              # in seconds (default is 4s)' >> mme.conf
  echo '        TS9                                   =  2                              # in seconds (default is 4s)' >> mme.conf
  echo '        TS10                                   =  4                              # in seconds (default is 4s)' >> mme.conf
  echo '        TS13                                   =  4                              # in seconds (default is 4s)' >> mme.conf
  echo '    };' >> mme.conf
  echo '' >> mme.conf
  echo '    NETWORK_INTERFACES :' >> mme.conf
  echo '    {' >> mme.conf
  echo '        MME_INTERFACE_NAME_FOR_S1_MME         = "eth0";' >> mme.conf
  echo '        MME_IPV4_ADDRESS_FOR_S1_MME           = "'$MME_S1_IP_ADDR'/24";' >> mme.conf
  echo '        MME_INTERFACE_NAME_FOR_S11_MME        = "eth0";' >> mme.conf
  echo '        MME_IPV4_ADDRESS_FOR_S11_MME          = "'$MME_S1_IP_ADDR'/24";' >> mme.conf
  echo '        MME_PORT_FOR_S11_MME                  = 2123;' >> mme.conf
  echo '    };' >> mme.conf
  echo '' >> mme.conf
  echo '    LOGGING :' >> mme.conf
  echo '    {' >> mme.conf
  echo '        OUTPUT            = "CONSOLE";' >> mme.conf
  echo '        THREAD_SAFE       = "no";' >> mme.conf
  echo '        COLOR             = "no";' >> mme.conf
  echo '' >> mme.conf
  echo '        SCTP_LOG_LEVEL     = "ERROR";' >> mme.conf
  echo '        GTPV1U_LOG_LEVEL   = "INFO";' >> mme.conf
  echo '        SPGW_APP_LOG_LEVEL = "INFO";' >> mme.conf
  echo '        UDP_LOG_LEVEL      = "INFO";' >> mme.conf
  echo '        S1AP_LOG_LEVEL     = "DEBUG";' >> mme.conf
  echo '        NAS_LOG_LEVEL      = "DEBUG";' >> mme.conf
  echo '        MME_APP_LOG_LEVEL  = "DEBUG";' >> mme.conf
  echo '        GTPV2C_LOG_LEVEL   = "DEBUG";' >> mme.conf
  echo '        S11_LOG_LEVEL      = "DEBUG";' >> mme.conf
  echo '        S6A_LOG_LEVEL      = "DEBUG";' >> mme.conf
  echo '        UTIL_LOG_LEVEL     = "INFO";' >> mme.conf
  echo '        MSC_LOG_LEVEL      = "ERROR";' >> mme.conf
  echo '        ITTI_LOG_LEVEL     = "ERROR";' >> mme.conf
  echo '        MME_SCENARIO_PLAYER_LOG_LEVEL = "ERROR";' >> mme.conf
  echo '        ASN1_VERBOSITY    = "INFO";' >> mme.conf
  echo '    };' >> mme.conf
  echo '' >> mme.conf
  echo '    S-GW :' >> mme.conf
  echo '   {' >> mme.conf
  echo '       SGW_IPV4_ADDRESS_FOR_S11              = "'$SPGWC0_IP_ADDR'";' >> mme.conf
  echo '   };' >> mme.conf
  echo '};' >> mme.conf
  set -x
}

function generateFdConfFile()
{
  set +x
  rm -f mme_fd.conf
  echo 'Identity = "'$MME_FQDN'";' >> mme_fd.conf
  echo 'Realm = "'$REALM'";' >> mme_fd.conf
  echo 'TLS_Cred = "'$PREFIX'/mme.cert.pem",' >> mme_fd.conf
  echo '           "'$PREFIX'/mme.key.pem";' >> mme_fd.conf
  echo 'TLS_CA   = "'$PREFIX'/mme.cacert.pem";' >> mme_fd.conf
  echo 'No_SCTP;' >> mme_fd.conf
  echo 'Prefer_TCP;' >> mme_fd.conf
  echo 'No_IPv6;' >> mme_fd.conf
  echo 'SCTP_streams = 3;' >> mme_fd.conf
  echo 'NoRelay;' >> mme_fd.conf
  echo 'AppServThreads = 4;' >> mme_fd.conf
  echo 'ListenOn = "'$MME_S1_IP_ADDR'";' >> mme_fd.conf
  echo 'Port = 3870;' >> mme_fd.conf
  echo 'SecPort = 5870;' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_3gpp2_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_draftload_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_etsi283034_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_rfc4004_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_rfc4006bis_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_rfc4072_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_rfc4590_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_rfc5447_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_rfc5580_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_rfc5777_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_rfc5778_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_rfc6734_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_rfc6942_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_rfc7155_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_rfc7683_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_rfc7944_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29061_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29128_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29154_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29173_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29212_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29214_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29215_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29217_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29229_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29272_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29273_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29329_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29336_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29337_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29338_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29343_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29344_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29345_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29368_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts29468_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_ts32299_avps.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_S6as6d.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_S6t.fdx";' >> mme_fd.conf
  echo 'LoadExtension = "/usr/local/lib/freeDiameter/dict_S6c.fdx";' >> mme_fd.conf
  echo '# -------- Peers ---------' >> mme_fd.conf
  echo 'ConnectPeer= "'$HSS_FQDN'" { ConnectTo = "'$HSS_IP_ADDR'"; No_SCTP ; No_IPv6; Prefer_TCP; No_TLS; port = 3868;};' >> mme_fd.conf
  set -x
}

set -x
cd /magma-mme/scripts
mkdir -p $PREFIX

pushd $PREFIX

generateConfFile
generateFdConfFile

# Configure REDIS container
sed -i -e "s@bind: 127.0.0.1@bind: $REDIS_IP_ADDR@" /etc/magma/redis.yml

# Generate freeDiameter certificate
popd
./check_mme_s6a_certificate $PREFIX mme.$REALM
set +x

echo "Starting tcpdump capture"
nohup tcpdump -i any -w /magma-mme/mme-`date -u +"%Y-%m-%dT%H-%M-%S"`.pcap > /dev/null 2>&1 &
sleep 5

echo "Starting sctpd"
nohup /magma-mme/bin/sctpd > /magma-mme/sctpd.log 2>&1 &
sleep 2
echo "Starting mme executable"
nohup /magma-mme/bin/oai_mme -c $PREFIX/mme.conf > /magma-mme/mme-stdout.log 2>&1 &
sleep 2
tail -f /var/log/mme.log

