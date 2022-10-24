# LightSync
LightSync is the light client version of [ZeroSync](https://github.com/zerosync/zerosync/) that validates batches of Bitoin block headers and attests to their correct validation using a STARK proof. This allows anyone to simply verify the proof and use the resulting header chain as if they validated the blocks themselves.

The Proof confirms the correct execution of:
- A header chain structure (every encoded previous block is the actual previous block)
- Proof of Work validation (every block hash is below the encoded target)
- Correct retargeting (the target is correctly calculated from the epoch timestamps)
- The validation of each block's minimum timestamp ([median of previous eleven blocks](https://en.bitcoin.it/wiki/Block_timestamp))

Additionally the program output contains a Merkle root (from a Merkle tree over all block headers in the batch) that can be used to proof inclusion of block headers in the batch at a later point (e.g. for SPV).


**All of this is experimental research code and CONTAINS CRITICAL SECURITY BUGS!**

## Current Status
See `src/chain_proof/main.py` for an example on how to call the program and receive a computation trace that can then be proven using e.g. [giza](https://github.com/maxgillett/giza).

Essentially creating a chain of batches only requires checking the input and output state of each batch validation run to be equal. Further, the batch size should be verified against the current block height.

There is no recursive verifier added yet, however, if you have access to StarkWare's proving systems you can add their recursive verifier and create a cairo program that verifies the LightSync `main.cairo` execution as stated above.

## Requirements

- Python3.9
- [Cairo](https://github.com/starkware-libs/cairo-lang) - [installation guide](https://www.cairo-lang.org/docs/quickstart.html)
- If you want to create STARK-proofs without SHARP you need [giza](https://github.com/maxgillett/giza) (Keep the Cairo [license](https://github.com/starkware-libs/cairo-lang/blob/master/LICENSE.txt) in mind)

## Tests

### Cairo

We provide tests using [protostar](https://github.com/software-mansion/protostar).

```
protostar test --cairo-path=./src
```

## Some documentation TODOS
TODO: List/document verification constraints.

TODO: document how chain\_proof/main.py works and what it does.
