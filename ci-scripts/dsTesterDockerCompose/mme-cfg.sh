#!/bin/bash

set -x
cd /magma-mme/scripts

INSTANCE=1
PREFIX='/magma-mme/etc'
MY_REALM='openairinterface.org'

declare -A MME_CONF

pushd $PREFIX
cp mme_fd.conf.tmplt mme_fd.conf

MME_CONF[@MME_S6A_IP_ADDR@]="192.168.61.196"
MME_CONF[@INSTANCE@]=$INSTANCE
MME_CONF[@PREFIX@]=$PREFIX
MME_CONF[@REALM@]=$MY_REALM
MME_CONF[@MME_FQDN@]="mme.${MME_CONF[@REALM@]}"
MME_CONF[@HSS_HOSTNAME@]='hss'
MME_CONF[@HSS_FQDN@]="${MME_CONF[@HSS_HOSTNAME@]}.${MME_CONF[@REALM@]}"
MME_CONF[@HSS_REALM@]=$MY_REALM
MME_CONF[@HSS_IP_ADDR@]="192.168.61.194"

for K in "${!MME_CONF[@]}"; do 
  egrep -lRZ "$K" $PREFIX/mme_fd.conf | xargs -0 -l sed -i -e "s|$K|${MME_CONF[$K]}|g"
  ret=$?;[[ ret -ne 0 ]] && echo "Tried to replace $K with ${MME_CONF[$K]}"
done

sed -i -e "s@etc/freeDiameter@etc@" /magma-mme/etc/mme_fd.conf
sed -i -e "s@bind: 127.0.0.1@bind: 192.168.61.195@" /etc/magma/redis.yml
# Generate freeDiameter certificate
popd
./check_mme_s6a_certificate $PREFIX mme.${MME_CONF[@REALM@]}
set +x

sleep infinity
