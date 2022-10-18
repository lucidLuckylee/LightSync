# LightSync
LightSync is the light client version of [ZeroSync](https://github.com/zerosync/zerosync/) that validates batches of Bitoin block headers and attests to their correct validation using a STARK proof. This allows anyone to simply verify the proof and use the resulting header chain as if they validated the blocks themselves.

The Proof confirms the correct execution of:
	- a header chain structure (every encoded previous block is the actual previous block)
	- Proof of Work validation (every block hash is below target)
	- correct retargeting (the target is correctly calculated from the epoch timestamps)
	- WHEN APPLICABLE the validation of each block's minimum timestamp ([median of previous eleven blocks](https://en.bitcoin.it/wiki/Block_timestamp))

Additionally the program output contains a Merkle root (from a Merkle tree over all block headers in the batch) that can be used to proof inclusion of block headers in the batch at a later point (e.g. for SPV).

To verify a proof you can use the respective verifier of SHARP or giza. There currently is a solidity contract in this repository to give you an idea of what has to be verified to create a correct header chain consisting of multiple batches. TODO: List/document verification constraints here. 
**All of this is experimental research code and CONTAINS CRITICAL SECURITY BUGS!**

## Requirements

- Python3.7
- [Cairo](https://github.com/starkware-libs/cairo-lang) - [installation guide](https://www.cairo-lang.org/docs/quickstart.html)
- Bitcoin client, e.g. [bitcoincore](https://bitcoincore.org/en/download/)
- If you want to create STARK-proofs without SHARP you need [giza](https://github.com/maxgillett/giza) (Keep the Cairo [license](https://github.com/starkware-libs/cairo-lang/blob/master/LICENSE.txt) in mind)

## Installation

- clone this repository and cd into it
- ` pip3 install -r python-requirements`
- starkRelay will prompt you for setup info when you first run it

## Usage

- Valdiate a batch:

```
starkRelay validate-batch [START]-[END] -s
```

- Proof inclusion of an intermediary header at position `X` in a batch:

```
starkRelay [X] [START]-[END] -s
```

If you want to create proofs locally with giza use `-g` flag and you will receive a proof binary.

## Tests

### Cairo

We provide tests using [protostar](https://github.com/software-mansion/protostar).

Initial setup from withing the cairo directory (the suggested standard lib directory is perfectly fine):
```
protostar init --existing
```

Run all Cairo tests from within the cairo dir (starkRelay/cairo):

```
protostar test ./tests --cairo-path=./src
```

**Note: Remove the output builtin from the first line of validate.cairo and/or merkle_proof.cairo to run the tests**

We might provide a script to run all tests that removes the output builtin automatically and adds it again after the tests were run.

## Credits
The approach is based on [zkRelay](https://github.com/informartin/zkRelay/) by Martin Westerkamp and the corresponding [paper](https://eprint.iacr.org/2020/433).
