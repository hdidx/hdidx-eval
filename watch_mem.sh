#!/bin/bash

#########################################################################
# File Name: watch_mem.sh
# Author: Wan Ji
# mail: wanji@live.com
# Created Time: 2015年10月05日 星期一 14时38分33秒
#########################################################################

rm -f $2
while true; do
  date >> $2
  python tests/ps_mem.py -p $1 >> $2
  sleep 1
done
