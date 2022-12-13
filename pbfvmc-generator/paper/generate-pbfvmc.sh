#!/bin/bash -e

PBFVMCGENERATOR=../pbfvmc-generator-mac64

if uname -a | grep -q Linux; then
  PBFVMCGENERATOR=../pbfvmc-generator-linux64
fi

for HW in 32 64 128 256 512; do
  echo "======= $HW hardware"
  for LOAD in 25 50 75 85 90 95 98 99 100 110; do
    echo "-- $LOAD load"
    cat hw$HW/hw$HW-vm${LOAD}p.desc | $PBFVMCGENERATOR > hw$HW/hw$HW-vm${LOAD}p.pbs
  done
done
