#!/bin/bash

#size=(1000 2500 5000 7500 10000 15000 20000)
size=(7500)
colours=(10 50 100)
degree=(2 5 8)
pre_cols=(25 50)
seeds=(1 2 3 4 5 6 7 8 9 10)

tot=0
for n in "${size[@]}"
do
    for s in "${seeds[@]}"
    do
	for c in "${colours[@]}"
	do
	    for d in "${degree[@]}"
	    do
		for p in "${pre_cols[@]}"
		do
		    exe_scpt="--input ../Data/DReg/HCD_${n}_${p}_${c}_${s}_${d}.txt --rtime 600 --stime 60"
		    # > Results/out_HCD_${n}_${p}_${c}_${s}_${d}.txt"
		    echo "${exe_scpt}"
		    fpath="Results/out_HCD_${n}_${p}_${c}_${s}_${d}.txt"
		    echo "${fpath}"
		    python solverCP.py ${exe_scpt} > ${fpath}
		    sleep 10
		    echo "************************************************"
		    ((tot++))
		done
	    done
	done
    done
done

echo "We have a total of: $tot"
