#!/bin/bash

STATUS=0
NB_UNREPLACED_AT=`cat /openair-hss/etc/*.json /openair-hss/etc/*.conf | grep -v contact@openairinterface.org | grep -c @ || true`
if [ $NB_UNREPLACED_AT -ne 0 ]
then    
  STATUS=-1
fi

NB_GENERATED_CERTIFICATES=`ls /openair-hss/etc/cacert.pem /openair-hss/etc/hss.cert.pem /openair-hss/etc/hss.key.pem | grep -c pem || true`
if [ $NB_GENERATED_CERTIFICATES -ne 3 ]
then
  STATUS=-1
fi

exit $STATUS
