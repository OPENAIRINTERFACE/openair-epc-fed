#!/bin/bash

STATUS=0
NB_UNREPLACED_AT=`cat /magma-mme/etc/*.conf | grep -c @ || true`
if [ $NB_UNREPLACED_AT -ne 0 ]
then
  STATUS=-1
fi

NB_GENERATED_CERTIFICATES=`ls /magma-mme/etc/mme.cacert.pem /magma-mme/etc/mme.cakey.pem /magma-mme/etc/mme.cert.pem /magma-mme/etc/mme.key.pem | grep -c pem || true`
if [ $NB_GENERATED_CERTIFICATES -ne 4 ]
then
  STATUS=-1
fi

exit $STATUS
