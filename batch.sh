#!/bin/bash

#########################################################################
# File Name: batch.sh
# Author: Wan Ji
# mail: wanji@live.com
# Created Time: 2015年07月28日 星期二 22时51分06秒
#########################################################################

# rm -fr build && python setup.py build

for i in 0 1 2 3 4; do
  ./eval_annoy.py   --ntrees 1 2 4 8 16 32 --topk 100   --exp_dir exp/annoy_eval_sift      exp/data/sift.mat      2>&1 | tee exp/annoy_eval_sift.log.$i
  ./eval_indexer.py --nbits 8 16 32 64 128 --topk 100   --exp_dir exp/hdidx_eval_siftsmall exp/data/siftsmall.mat 2>&1 | tee exp/hdidx_eval_siftsmall.log.$i
  ./eval_indexer.py --nbits 8 16 32 64 128 --topk 100   --exp_dir exp/hdidx_eval_sift      exp/data/sift.mat      2>&1 | tee exp/hdidx_eval_sift.log.$i
done

for i in 10 11 12 13 14; do
  ./eval_annoy.py   --ntrees 1 2 4 8 16 32 --topk 10000 --exp_dir exp/annoy_eval_sift      exp/data/sift.mat      2>&1 | tee exp/annoy_eval_sift.log.$i
  ./eval_indexer.py --nbits 8 16 32 64 128 --topk 10000 --exp_dir exp/hdidx_eval_siftsmall exp/data/siftsmall.mat 2>&1 | tee exp/hdidx_eval_siftsmall.log.$i
  ./eval_indexer.py --nbits 8 16 32 64 128 --topk 10000 --exp_dir exp/hdidx_eval_sift      exp/data/sift.mat      2>&1 | tee exp/hdidx_eval_sift.log.$i
done
