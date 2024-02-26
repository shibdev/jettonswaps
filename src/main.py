import asyncio
from pytoniq import BlockIdExt, Address, LiteBalancer, Transaction
from block_scanner import BlockScanner
from aiogram import Bot
from logger import logger
from swap_functions import init_raw_result, raw_to_userfriendly
from functions import get_json, put_json, get_jetton_content_by_jetton_wallet
from config import TOKEN, CHAT_ID, addresses, flipped_token

bot = Bot(
    token = TOKEN,
    parse_mode = "HTML"
)


async def handle_block(block: BlockIdExt):
    if block.workchain == -1:  # skip masterchain blocks
        return

    try:
        transactions: list[Transaction] = await client.raw_get_block_transactions_ext(block)

        transactions_hashes: dict[bytes, Transaction] = {}
        msg_hashes: dict[bytes, bytes] = {}
        traces: dict[bytes, bytes] = {}

        transactions = sorted(
            transactions,
            key = lambda transaction: transaction.lt
        )

        for transaction in transactions:
            tr_hash: bytes = transaction.cell.hash
            in_msg_hash: bytes = transaction.in_msg.serialize().hash

            transactions_hashes[tr_hash] = transaction

            if in_msg_hash in msg_hashes:
                traces[tr_hash] = msg_hashes[in_msg_hash]

            if transaction.out_msgs:
                for msg in transaction.out_msgs:
                    msg_hashes[msg.serialize().hash] = tr_hash

            else:
                results: list[Transaction] = []
                pretty_result: list[dict] = []

                build_trace(tr_hash, transactions_hashes, traces, results)
 
                results = results[::-1]
 
                for transaction in results:
                    if not transaction.in_msg.is_internal:
                        continue
 
                    if len(transaction.in_msg.body.bits) < 32:
                        pretty_result.append(dict(
                            type_ = "TonTransfer",
                            amount = transaction.in_msg.info.value_coins,
                            destination = transaction.in_msg.info.dest.to_str(
                                is_user_friendly = False
                            ),
                            from_ = transaction.in_msg.info.src.to_str(
                                is_user_friendly = False
                            ),
                            lt = transaction.lt
                        ))

                        continue

                    body_slice = transaction.in_msg.body.begin_parse()
                    op_code = hex(body_slice.load_uint(32))

                    if op_code == "0xf8a7ea5":
                        body_slice.load_uint(64) # skip query_id

                        jetton = await get_jetton_content_by_jetton_wallet(
                            client,
                            "0:" + transaction.account_addr_hex
                        )

                        pretty_result.append({
                            "type": "JettonTransfer",
                            "amount": transaction.in_msg.info.value_coins,
                            "jetton_amount": body_slice.load_coins(),
                            "destination": body_slice.load_address().to_str(1, 1, 1),
                            "from": transaction.in_msg.info.src.to_str(1, 1, 1),
                            "op-code": op_code,
                            "lt": transaction.lt,
                            "jetton": jetton
                        })

                    elif op_code == "0x72aca8aa":
                        body_slice.load_uint(64) # skip query_id
                        body_slice.load_ref() # skip proof

                        asset = {}

                        if body_slice.load_uint(4) == 1: # is jetton
                            asset = {"address": Address((
                                body_slice.load_uint(8),
                                body_slice.load_bytes(32)
                            ))}

                        else:
                            asset = {"address": Address((
                                0,
                                bytes(32)
                            ))}

                        pretty_result.append({
                            "type": "Routing",
                            "asset": asset,
                            "amount": transaction.in_msg.info.value_coins,
                            "destination": transaction.in_msg.info.dest.to_str(1, 1, 1),
                            "from": transaction.in_msg.info.src.to_str(1, 1, 1),
                            "op-code": op_code,
                            "lt": transaction.lt
                        })

                    elif op_code == "0x61ee542d":
                        body_slice.load_uint(64) # skip query_id
                        body_slice.load_ref() # skip proof

                        pretty_result.append({
                            "type": "PayIn",
                            "amount": transaction.in_msg.info.value_coins,
                            "pay_amount": body_slice.load_coins(),
                            "pay_sender": body_slice.load_address().to_str(1, 1, 1),
                            "destination": transaction.in_msg.info.dest.to_str(1, 1, 1),
                            "from": transaction.in_msg.info.src.to_str(1, 1, 1),
                            "op-code": op_code,
                            "lt": transaction.lt
                        })

                    elif op_code == "0xad4eb6f5":
                        body_slice.load_uint(64) # skip query_id
                        body_slice.load_ref() # skip proof

                        pretty_result.append({
                            "type": "PayOut",
                            "amount": transaction.in_msg.info.value_coins,
                            "pay_amount": body_slice.load_coins(),
                            "pay_sender": body_slice.load_address().to_str(1, 1, 1),
                            "destination": transaction.in_msg.info.dest.to_str(1, 1, 1),
                            "from": transaction.in_msg.info.src.to_str(1, 1, 1),
                            "op-code": op_code,
                            "lt": transaction.lt
                        })

                    elif op_code not in ["0x178d4519", "0x7362d09c"]:
                        pretty_result.append({
                            "type": "SmartContractExec",
                            "amount": transaction.in_msg.info.value_coins,
                            "destination": transaction.in_msg.info.dest.to_str(1, 1, 1),
                            "from": transaction.in_msg.info.src.to_str(1, 1, 1),
                            "op-code": op_code,
                            "lt": transaction.lt
                        })

                for pretty_data in pretty_result:
                    jetton_address = None

                    if pretty_data["type"] == "JettonTransfer":
                        jetton_address = pretty_data["jetton"]["jetton_address"]

                    if pretty_data["destination"] in flipped_token or pretty_data["from"] in flipped_token or jetton_address in addresses:
                        raw_results = init_raw_result(pretty_result)
                        old_results = get_json("old_results")

                        for raw_result in raw_results:
                            if raw_result in old_results:
                                continue

                            old_results.append(raw_result)

                            while len(old_results) > 10:
                                old_results.pop(0)

                            put_json(old_results, "old_results")

                            uf_result = await raw_to_userfriendly(client, raw_result, transaction.cell.hash.hex())

                            await bot.send_message(CHAT_ID, uf_result, disable_web_page_preview=True)

                        break

    except Exception as e:
        logger.error(f"Handle_block error: {e}")


client = LiteBalancer.from_mainnet_config(1)


def build_trace(tr_hash: str, transactions_hashes: dict, traces: dict, result: list):
    result.append(transactions_hashes.get(tr_hash))

    if tr_hash in traces:  # we have this trace
        build_trace(traces[tr_hash], transactions_hashes, traces, result)

    return


async def main():
    logger.info("Start")

    while True:
        try:
            await client.start_up()
            await BlockScanner(client=client, block_handler=handle_block).run()

        except asyncio.TimeoutError:
            await client.close_all()
            await asyncio.sleep(3)
            continue


if __name__ == "__main__":
    asyncio.run(main())
