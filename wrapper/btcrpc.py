# adopted from
# https://github.com/informartin/zkRelay/blob/master/preprocessing/create_input.py

from blockstream import blockexplorer


def getBitcoinClientURL(ctx):
    return f"http://{ctx.obj['btc-client']['user']}:{ctx.obj['btc-client']['psw']}@{ctx.obj['btc-client']['host']}:{ctx.obj['btc-client']['port']}"


def checkClientRunning(ctx):
    return True


def getBlockHeadersInRange(ctx, i, j):
    blocks = []
    for x in range(i, j):
        blocks.append(blockexplorer.get_block_by_height(x))
    block_dicts = [
        {
            "versionHex": f"{x.version:08x}",
            "previousblockhash": x.previous_block_hash,
            "height": x.height,
            "merkleroot": x.merkle_root,
            "time": x.timestamp,
            "nonce": x.nonce,
            "bits": f"{x.bits:x}",
        } for x in blocks]
    return block_dicts
