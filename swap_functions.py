import copy
from pytoniq import Address
from logger import logger
from functions import get_lp_price, get_json, put_json
from config import token, flipped_token, known_wallets

symbols = {"sold": "🔴", "bought": "🟢",
           "withdraw": "💀", "deposit": "👛"}

async def raw_to_userfriendly(client, raw_result, tx):
    result = None
    price = None
    sell_or_buy = None

    const_raw_result = copy.deepcopy(raw_result)

    if raw_result["symbols"][0] == "TON":
        raw_result["symbols"][1] = const_raw_result["symbols"][0]
        raw_result["amounts"][1] = const_raw_result["amounts"][0]

        raw_result["symbols"][0] = const_raw_result["symbols"][1]
        raw_result["amounts"][0] = const_raw_result["amounts"][1]

    if raw_result['symbols'][0].upper() != "JWBTC":
        amount = round(raw_result['amounts'][0], 3)
    else:
        amount = f"{raw_result['amounts'][0]:.10f}"

    if symbols[raw_result["station"]] == "🟢":
        sell_or_buy = "BUY"

        try:
            price = await get_lp_price(client, raw_result['symbols'][0].lower())
            data = get_json("data")
            if raw_result["symbols"][0].lower() not in data:
                data[raw_result['symbols'][0].lower()] = price
            old_price = float(data[raw_result['symbols'][0].lower()])

            if "UNKNOWN_JETTON" not in raw_result["multi-hop data"] and raw_result["is_multi-hop"]:
                multihop_data = raw_result["multi-hop data"].split(" -> ")
                if multihop_data[1] == "TON":
                    if multihop_data[0].lower() in token:
                        data[multihop_data[0].lower()] = await get_lp_price(client, multihop_data[0].lower())
                    if multihop_data[2].lower() in token:
                        data[multihop_data[2].lower()] = await get_lp_price(client, multihop_data[2].lower())

                if (multihop_data[0].upper() == "TON" ) and multihop_data[1].lower() in token:
                    data[multihop_data[1].lower()] = await get_lp_price(client, multihop_data[1].lower())
                if (multihop_data[2].upper() == "TON" ) and multihop_data[1].lower() in token:
                    data[multihop_data[1].lower()] = await get_lp_price(client, multihop_data[1].lower())

        except Exception as e:
            logger.error(f"Raw_to_userfriendly error: {e}")
            price = old_price

        procent = f"{'{:0.5f}'.format(((float(price) - old_price)/old_price)*100)}"

        additional_string = ""
        if raw_result["is_multi-hop"]:
            additional_string = f'({raw_result["multi-hop data"][:-3]})'

        result = (f"""<a href="https://tonviewer.com/transaction/{tx}">{symbols[raw_result['station']]}</a> <b>{sell_or_buy}: {amount} ${raw_result['symbols'][0].upper()} for {round(raw_result['amounts'][1], 3)} ${raw_result['symbols'][1].upper()} {additional_string}\n\n"""
                    f"{raw_result['symbols'][0].upper()} Price:</b> <code>{'{:0.9f}'.format(price)} TON</code> ({procent}%)\n"
                    f"#{raw_result['symbols'][0].upper()}{sell_or_buy} <a href='https://tonviewer.com/{raw_result['who']}'>[{raw_result['who'][0:4]}...{raw_result['who'][44:48]}]</a> #addr_{Address(raw_result['who']).to_str(False, False, False)[-8:]} {known_wallets[raw_result['who']] if raw_result['who'] in known_wallets else ''}"
                    )

        data[raw_result['symbols'][0].lower()] = float(price)
        put_json(data, "data")

    if symbols[raw_result["station"]] == "🔴":
        sell_or_buy = "SELL"

        try:
            price = await get_lp_price(client, raw_result['symbols'][0].lower())
            data = get_json("data")
            if raw_result["symbols"][0].lower() not in data:
                data[raw_result['symbols'][0].lower()] = price
            old_price = float(data[raw_result['symbols'][0].lower()])
            if "UNKNOWN_JETTON" not in raw_result["multi-hop data"] and raw_result["is_multi-hop"]:
                multihop_data = raw_result["multi-hop data"].split(" -> ")
                if multihop_data[1] == "TON":
                    if multihop_data[0].lower() in token:
                        data[multihop_data[0].lower()] = await get_lp_price(client, multihop_data[0].lower())
                    if multihop_data[2].lower() in token:
                        data[multihop_data[2].lower()] = await get_lp_price(client, multihop_data[2].lower())

                if (multihop_data[0].upper() == "TON" ) and multihop_data[1].lower() in token:
                    data[multihop_data[1].lower()] = await get_lp_price(client, multihop_data[1].lower())
                if (multihop_data[2].upper() == "TON" ) and multihop_data[1].lower() in token:
                    data[multihop_data[1].lower()] = await get_lp_price(client, multihop_data[1].lower())

        except:
            price = old_price

        procent = f"{'{:0.5f}'.format(((float(price) - old_price)/old_price)*100)}"

        additional_string = ""
        if raw_result["is_multi-hop"]:
            additional_string = f'({raw_result["multi-hop data"][:-3]})'

        result = (f"""<a href="https://tonviewer.com/transaction/{tx}">{symbols[raw_result['station']]}</a> <b>{sell_or_buy}: {amount} ${raw_result['symbols'][0].upper()} for {round(raw_result['amounts'][1], 3)} ${raw_result['symbols'][1].upper()} {additional_string}\n\n"""
                    f"{raw_result['symbols'][0].upper()} Price:</b> <code>{'{:0.9f}'.format(price)} TON</code> ({procent}%)\n"
                    f"#{raw_result['symbols'][0].upper()}{sell_or_buy} <a href='https://tonviewer.com/{raw_result['who']}'>[{raw_result['who'][0:4]}...{raw_result['who'][44:48]}]</a> #addr_{Address(raw_result['who']).to_str(False, False, False)[-8:]} {known_wallets[raw_result['who']] if raw_result['who'] in known_wallets else ''}"
                )


        data[raw_result['symbols'][0].lower()] = float(price)
        put_json(data, "data")

    if symbols[raw_result["station"]] == "💀":
        sell_or_buy = "WITHDRAW"

        data = get_json("data")
        if raw_result["symbols"][0].lower() not in data:
            data[raw_result['symbols'][0].lower()] = 0.1
        old_price = float(data[raw_result['symbols'][0].lower()])

        result = (f"""<a href="https://tonviewer.com/transaction/{tx}">{symbols[raw_result['station']]}</a> <b>{sell_or_buy}: {amount}({raw_result['symbols'][0].upper()}) + {round(raw_result['amounts'][1], 3)}(TON)\n\n"""
                    f"{raw_result['symbols'][0].upper()} Price:</b> <code>{old_price} TON</code>\n"
                    f"#{raw_result['symbols'][0].upper()}{sell_or_buy} <a href='https://tonviewer.com/{raw_result['who']}'>[{raw_result['who'][0:4]}...{raw_result['who'][44:48]}]</a> #addr_{Address(raw_result['who']).to_str(False, False, False)[-8:]} {known_wallets[raw_result['who']] if raw_result['who'] in known_wallets else ''}"
                )

    if symbols[raw_result["station"]] == "👛":
        sell_or_buy = "DEPOSIT"

        data = get_json("data")
        if raw_result["symbols"][0].lower() not in data:
            data[raw_result['symbols'][0].lower()] = 0.1
        old_price = float(data[raw_result['symbols'][0].lower()])

        result = (f"""<a href="https://tonviewer.com/transaction/{tx}">{symbols[raw_result['station']]}</a> <b>{sell_or_buy}: {amount}({raw_result['symbols'][0].upper()}) + {round(raw_result['amounts'][1], 3)}(TON)\n\n"""
                    f"{raw_result['symbols'][0].upper()} Price:</b> <code>{old_price} TON</code>\n"
                    f"#{raw_result['symbols'][0].upper()}{sell_or_buy} <a href='https://tonviewer.com/{raw_result['who']}'>[{raw_result['who'][0:4]}...{raw_result['who'][44:48]}]</a> #addr_{Address(raw_result['who']).to_str(False, False, False)[-8:]} {known_wallets[raw_result['who']] if raw_result['who'] in known_wallets else ''}"
                )

    return result

def init_raw_result(data):
    raw_results = [{"station": None,
                    "symbols": [None, None],
                    "amounts": [None, None],
                "who": None,
                "is_multi-hop": False,
                "multi-hop data": ""}]
    num = 0

    for i in data:
        if i["type"] == "SmartContractExec":
            if i["op-code"] == "0x7bdd97de":
                raw_results[num]["station"] = "withdraw"

            elif i["op-code"] == "0xd55e4686":
                raw_results[num]["station"] = "deposit"
                raw_results[num]["amounts"][0] = i["amount"] / 1e9
                raw_results[num]["symbols"][0] = "TON"

        elif i["type"] == "Routing":
            raw_results[num]["station"] = "bought"
            raw_results[num]["is_multi-hop"] = True

            if i["asset"]["address"].to_str(1, 1, 1) in flipped_token:
                raw_results[num]["multi-hop data"] += flipped_token[i["asset"]["address"].to_str(1, 1, 1)].upper() + " -> "
            elif i["asset"]["address"].to_str(0, 0, 0) == "0:0000000000000000000000000000000000000000000000000000000000000000":
                raw_results[num]["multi-hop data"] += "TON" + " -> "
            else:
                raw_results[num]["multi-hop data"] += "UNKNOWN_JETTON" + " -> "

        elif i["type"] == "PayIn":
            if any([raw_results[num]["amounts"][0], raw_results[num]["symbols"][0]]):
                num += 1
                raw_results.append({"station": None,
                                    "symbols": [None, None],
                                    "amounts": [None, None],
                                    "who": None,
                                    "is_multi-hop": False,
                                    "multi-hop data": ""})

            index = data.index(i)
            if data[index - 1]["type"] in ["TonTransfer", "SmartContractExec"]:
                raw_results[num]["multi-hop data"] +=  "TON" + " -> "
                raw_results[num]["symbols"][0] = "TON"
                raw_results[num]["amounts"][0] = i["pay_amount"] / 1e9

                if raw_results[num]["station"] not in ["withdraw", "deposit"]:
                    raw_results[num]["station"] = "bought"
            elif data[index - 1]["type"] == "JettonTransfer":
                raw_results[num]["symbols"][0] = data[index - 1]["jetton"]["symbol"].upper()
                raw_results[num]["amounts"][0] = i["pay_amount"] / 10**int(data[index - 1]["jetton"]["decimals"])

                if raw_results[num]["station"] not in ["withdraw", "deposit"]:
                    raw_results[num]["station"] = "sold"

                raw_results[num]["multi-hop data"] += raw_results[num]["symbols"][0] + " -> "

            raw_results[num]["who"] = Address(i["pay_sender"]).to_str(1, 1, 0)

        elif i["type"] == "PayOut":
            if any([raw_results[num]["amounts"][1], raw_results[num]["symbols"][1]]):
                num += 1
                raw_results.append({"station": None,
                                    "symbols": [None, None],
                                    "amounts": [None, None],
                                    "who": None,
                                    "is_multi-hop": False,
                                    "multi-hop data": ""})

            index = data.index(i)
            if data[index + 1]["type"] in ["TonTransfer", "SmartContractExec", "PayIn"]:
                raw_results[num]["multi-hop data"] +=  "TON" + " -> "

                if raw_results[num]["station"] == "withdraw":
                    raw_results[num]["symbols"][0] = "TON"
                    if not raw_results[num]["amounts"][0]:
                        raw_results[num]["amounts"][0] = i["pay_amount"] / 1e9
                    if not raw_results[num]["amounts"][1]:
                        raw_results[num]["symbols"][1] = "TON"
                        raw_results[num]["amounts"][1] = i["pay_amount"] / 1e9
                else:
                    raw_results[num]["symbols"][1] = "TON"
                    raw_results[num]["amounts"][1] = i["pay_amount"] / 1e9

                if raw_results[num]["station"] not in ["withdraw", "deposit"]:
                    raw_results[num]["station"] = "sold"

            elif data[index + 1]["type"] == "JettonTransfer":
                if raw_results[num]["station"] == "withdraw":
                    if not raw_results[num]["amounts"][0]:
                        raw_results[num]["symbols"][0] = data[index + 1]["jetton"]["symbol"].upper()
                        raw_results[num]["amounts"][0] = i["pay_amount"] / 10**int(data[index + 1]["jetton"]["decimals"])
                    if not raw_results[num]["amounts"][1]:
                        raw_results[num]["symbols"][1] = data[index + 1]["jetton"]["symbol"].upper()
                        raw_results[num]["amounts"][1] = i["pay_amount"] / 10**int(data[index + 1]["jetton"]["decimals"])

                else:
                    raw_results[num]["symbols"][1] = data[index + 1]["jetton"]["symbol"].upper()
                    raw_results[num]["multi-hop data"] += raw_results[num]["symbols"][1] + " -> "
                    raw_results[num]["amounts"][1] = i["pay_amount"] / 10**int(data[index + 1]["jetton"]["decimals"])

                if raw_results[num]["station"] not in ["withdraw", "deposit"]:
                    raw_results[num]["station"] = "bought"

            raw_results[num]["who"] = Address(i["pay_sender"]).to_str(1, 1, 0)

    result = []

    for i in raw_results:
        if all([bool(i["station"]), bool(i["amounts"][0]), bool(i["amounts"][1]), bool(i["who"]), bool(i["symbols"][0]), bool(i["symbols"][1])]):
            # if not i["is_multi-hop"]:
            #     if i["station"] == "bought":
            #         i["amounts"][1] -= 0.2
            #     if i["station"] == "sold":
            #         i["amounts"][1] -= 0.105
            #     if i["station"] == "deposit":
            #         i["amounts"][1] -= 0.15
            #     if i["station"] == "withdraw":
            #         i["amounts"][1] -= 0.225
            
            if i["symbols"][0] == i["symbols"][1]:
                continue

            if i["symbols"][0] != "TON" and i["symbols"][1] != "TON":
                i["station"] = "sold"

            if str(i["amounts"][0]) != str(i["amounts"][0]).rstrip('0').rstrip('.'):
                i["amounts"][0] = int(i["amounts"][0])

            if str(i["amounts"][1]) != str(i["amounts"][1]).rstrip('0').rstrip('.'):
                i["amounts"][1] = int(i["amounts"][1])

            result.append(i)
    return result
