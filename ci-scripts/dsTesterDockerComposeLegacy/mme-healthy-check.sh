#!/bin/bash

STATUS=0
NB_UNREPLACED_AT=`cat /openair-mme/etc/*.conf | grep -v 'IPv4@' | grep -c @ || true`
if [ $NB_UNREPLACED_AT -ne 0 ]
then
  STATUS=-1
fi

NB_GENERATED_CERTIFICATES=`ls /openair-mme/etc/mme.cacert.pem /openair-mme/etc/mme.cakey.pem /openair-mme/etc/mme.cert.pem /openair-mme/etc/mme.key.pem | grep -c pem || true`
if [ $NB_GENERATED_CERTIFICATES -ne 4 ]
then
  STATUS=-1
fi

exit $STATUS
