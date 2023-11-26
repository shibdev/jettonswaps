import json
import hashlib
from pytoniq import begin_cell, Cell, Slice
import httpx
from config import token
from logger import logger

def get_json(filename):
    with open(f"{filename}.json", "r") as file:
        return json.loads(file.read())

def put_json(content, filename):
    with open(f"{filename}.json", "w") as file:
        file.write(json.dumps(content))

async def get_lp_price(client, symbol):
    r = await client.run_get_method(address=token[symbol], method="estimate_swap_out",
                                    stack=[
                                        begin_cell().store_uint(1, 4).end_cell().begin_parse(),
                                        1000000000
                                    ])
    if symbol in ["jusdt", "jusdc"]:
        return r[1] / 1e12
    return r[1] / 1e9


def get_hash(string: str) -> int:
    return int.from_bytes(hashlib.sha256(string.encode()).digest(), 'big')

def get_str_attr_value(meta: dict, attr_name: str):
    hash_ = get_hash(attr_name)
    value: Slice = meta.get(hash_)
    if value is not None:
        return value.load_snake_string().replace('\x00', '')


def get_bytes_attr_value(meta: dict, attr_name: str) -> bytes:
    hash_ = get_hash(attr_name)
    value: Slice = meta.get(hash_)
    if value is not None:
        return value.load_snake_bytes()


def process_metadata(cell: Cell):
    cs = cell.begin_parse()
    if not len(cell.refs):  # some metadata cells do not have b'\x01' prefix
        url = cs.load_snake_string().replace('\x01', '')
        return url
    else:
        cs.load_uint(8)
        metadata = cs.load_dict(key_length=256)
        if metadata is None:
            return {}

        result = {
            'name': get_str_attr_value(metadata, 'name'),
            'description': get_str_attr_value(metadata, 'description'),
            'image': get_str_attr_value(metadata, 'image'),
            'image_data': get_bytes_attr_value(metadata, 'image_data'),
            'symbol': get_str_attr_value(metadata, 'symbol'),
            'decimals': get_str_attr_value(metadata, 'decimals'),
            'uri': get_str_attr_value(metadata, 'uri')
        }
        
        try:
            result['decimals'] = int(result['decimals'])
        except Exception as e:
            logger.error(f'Process_metadata error: {e}')

        return result

async def get_jetton_content_by_jetton_wallet(client, jetton_wallet):
    result = {}

    stack = await client.run_get_method(address=jetton_wallet, method="get_wallet_data", stack=[])
    result["jetton_address"] = stack[2].load_address().to_str(1, 1, 1)

    stack = await client.run_get_method(address=result["jetton_address"], method="get_jetton_data", stack=[])
    metadata = process_metadata(stack[3])
    if isinstance(metadata, str):
        async with httpx.AsyncClient() as async_client:
            if metadata[0:4] == "ipfs":
                r = await async_client.get(f"https://ipfs.io/ipfs/{metadata.replace('ipfs://', '')}")
            else:
                r = await async_client.get(metadata)
            r = r.json()
        result["decimals"] = r.get("decimals", 9)
        result["symbol"] = r.get("symbol", "None")
    elif not metadata["symbol"]:
        async with httpx.AsyncClient() as async_client:
            r = await async_client.get(metadata["uri"])
            r = r.json()
        result["decimals"] = r.get("decimals", 9)
        result["symbol"] = r.get("symbol", "None")

    else:
        result["decimals"] = metadata["decimals"]
        result["symbol"] = metadata["symbol"]

    if result["symbol"].upper() in ["JUSDT", "JUSDC"]:
        result["decimals"] = 6

    return result
