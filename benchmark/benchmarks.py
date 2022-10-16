# This contains the benchmark cases for the cairo-runner
# Cairo vm runtime is measured from within the python wrapper and apart
# from that only includes the time it takes for the subprocess to start

# Note that I assume the bitcoin chain will not change and collect the
# blocks from a running bitcoin client.
# WARNING: THIS CAN LEAD TO DIFFERENT INPUTS WHEN THE CLIENT SWITCHED
# BETWEEN TESTNET AND MAINNET OR THE CHAIN TIP IS USED.

import sys
import atexit
import csv
from prettytable import PrettyTable
from lib.benchmark_lib import benchmarkInit, benchmarkBatches, benchmarkMerkleProofs


# Imitating the ctx object from click allows to share code base
class Ctx:
    obj = {}


# CAN CHANGE/ADD THE BATCHES TO TEST HERE
smallBatches = [(1, 3), (2015, 2017)]
mediumBatches = [(1, 21), (2015, 2035)]
largeBatches = [(1, 252), (2015, 2266)]
hugeBatches = [(1, 1008), (2015, 3022), (1, 2016), (2015, 4030), (1, 4032)]
# list of lists of batches - the bigger the batch the farther at the end of the list
# one can decide to only run the first x batches
batches = [smallBatches, mediumBatches, largeBatches, hugeBatches]

results = []
resTable = PrettyTable()
merkleResTable = PrettyTable()
resTable.field_names = [
    "size",
    "start",
    "end",
    "time (s)",
    "memory (KB)",
    "steps",
    "cells"]
merkleResTable.field_names = resTable.field_names


def printResults():
    print("\n--- Batch Validation Results ---")
    print(resTable)
    print("\n--- Inclusion Merkle Proof Results ---")
    print(merkleResTable)


# If the program is stopped still output the results up to this point
atexit.register(printResults)

ctx = Ctx()
ctx.obj = benchmarkInit()


# no command-line option given -> run all batches and do not output csv
batchesToRun = len(batches)
if len(sys.argv) >= 2:
    if int(sys.argv[1]) <= batchesToRun:
        batchesToRun = int(sys.argv[1])
    else:
        print("WARNING: There are not as many batch sets as you specified to run. Running all batch sets now.")

for i in range(0, batchesToRun):
    print(
        f"Running batch set {i + 1}/{batchesToRun}... (batch size increases with every batch set)\r",
        end="")
    results = benchmarkBatches(ctx, batches[i])
    merkleResults = benchmarkMerkleProofs(ctx, batches[i])
    resTable.add_rows(results)
    merkleResTable.add_rows(merkleResults)

if len(sys.argv) == 3:
    with open(sys.argv[2], 'w') as resFile:
        wr = csv.writer(resFile)
        wr.writerow(
            ("batchsize",
             "start",
             "end",
             "time",
             "memory",
             "steps",
             "cells"))
        wr.writerows(results)
