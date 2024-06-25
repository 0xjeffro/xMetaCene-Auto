import json
import time
import random
import requests
from web3 import Web3

from config import USER_INFO, RPC

SUM_TMNK, WAIT_TMNK = 0, 0
ALL_SPEED = 0

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'Content-Length': '23',
    'Content-Type': 'application/json',
    'Cookie': 'PHPSESSID=',
    'Origin': 'chrome-extension://igimfdmnnijclcfdgimooedbealfpndj',
    'Priority': 'u=1, i',
    'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'none',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

URL = 'https://x.metacene.io/cmd.php'

data_wakePet = {"user": {"wakePet": {}}}  # 唤醒宠物
data_levelUp = {"user": {"petLvUp": {}}}  # 宠物升级
data_levelUp1 = {"user": {"roleLvUp": {"role_id": 1}}}  # 角色1升级
data_levelUp2 = {"user": {"roleLvUp": {"role_id": 2}}}  # 角色2升级
data_login = {"guide": {"login": {}}}  # 登录
data_recharge = {"user": {"recharge": {"spar": "10000000"}}}  # 充值
data_useEnergy1 = {"user": {"useEnergy": {"role_id": 1, "count": 1}}}  # 角色1使用1个电池
data_useEnergy2 = {"user": {"useEnergy": {"role_id": 2, "count": 1}}}  # 角色2使用1个电池
data_MineBoxInfo = {"user": {"getMineBoxInfo": {}}}  # 宝箱信息
data_OpenMineBox = {"user": {"openMineBox": {}}}  # 开宝箱
data_checkIn = {"user": {"getCheckInSign": {}}}  # 每日签到
data_lockRole1 = {"user": {"lockRole": {"role_id": 1}}}  # 解锁角色1
data_getConfig = {"guide": {"getConfig": {}}}  # 获取配置信息
data_getExchangeRate = {"user": {"getExchangeRate": {}}}  # 获取积分数和兑换比例
data_exchange = {"user": {"exchange": {"integral": 164}}}  # 兑换积分
data_getNumTMAK = {"user": {"getHdAllGet": {}}}  # 获取TMNK数量
data_getDailyTask = {"user": {"getTaskList": {"type": 0}}}  # 获取每日任务


def get_time_to_7am():
    import datetime

    current_time = datetime.datetime.now()
    next_7am = current_time.replace(hour=7, minute=0, second=0, microsecond=0)

    if current_time >= next_7am:
        next_7am = next_7am + datetime.timedelta(days=1)

    time_difference = next_7am - current_time
    seconds_left = time_difference.total_seconds()

    return seconds_left


def get_headers(user):
    time.sleep(random.randint(5, 15))
    headers = HEADERS
    headers['Cookie'] = 'PHPSESSID=' + user[1]
    return headers


def login(user):
    headers = get_headers(user)
    response = requests.post(URL, json=data_login, headers=headers)
    print('> Login@' + user[0] + ' ' + response.text)
    return response.text


def wakePet(user):
    headers = get_headers(user)
    response = requests.post(URL, json=data_wakePet, headers=headers)
    print('> wakePet@' + user[0] + ' ' + response.text)
    return response.text


def levelUp(user):
    headers = get_headers(user)
    response = requests.post(URL, json=data_levelUp, headers=headers)
    print('> levelUp@' + user[0] + ' ' + response.text)
    return response.text


def levelUp1(user):
    headers = get_headers(user)
    response = requests.post(URL, json=data_levelUp1, headers=headers)
    print('> levelUp1@' + user[0] + ' ' + response.text)
    return response.text


def levelUp2(user):
    headers = get_headers(user)
    response = requests.post(URL, json=data_levelUp2, headers=headers)
    print('> levelUp2@' + user[0] + ' ' + response.text)
    return response.text


def lockRole1(user):
    headers = get_headers(user)
    response = requests.post(URL, json=data_lockRole1, headers=headers)
    print('> lockRole1@' + user[0] + ' ' + response.text)
    return response.text


def recharge(user, spar):
    headers = get_headers(user)
    data_recharge['user']['recharge']['spar'] = str(int(spar))
    response = requests.post(URL, json=data_recharge, headers=headers)
    print('> recharge@' + user[0] + ' ' + response.text)
    return response.text


def getMineBoxInfo(user):
    headers = get_headers(user)
    response = requests.post(URL, json=data_MineBoxInfo, headers=headers)
    print('> getMineBoxInfo@' + user[0] + ' ' + response.text)
    return response.text


def getDailyTask(user):
    headers = get_headers(user)
    response = requests.post(URL, json=data_getDailyTask, headers=headers)
    print('> getDailyTask@' + user[0] + ' ' + response.text)
    return response.text


def openMineBox(user):
    headers = get_headers(user)
    response = requests.post(URL, json=data_OpenMineBox, headers=headers)
    print('> openMineBox@' + user[0] + ' ' + response.text)
    mine_box_info = json.loads(response.text)
    to_ = mine_box_info['check']['to']
    expired = mine_box_info['check']['expired']
    mnt = mine_box_info['check']['mnt']
    tmak = mine_box_info['check']['tmak']
    nonce = mine_box_info['check']['nonce']
    signature = mine_box_info['check']['signature']
    uid = mine_box_info['check']['uid']
    type_ = mine_box_info['check']['type']

    web3 = Web3(Web3.HTTPProvider(RPC))
    if not web3.is_connected():
        print("RPC Connection Error")
        return

    caller, private_key = user[2], user[3]
    abi = json.loads(open("abi.json", "r").read())
    contract_address = "0x9B63C5B7a68573Bbc47336Ec0247798411f561b9"
    contract = web3.eth.contract(address=contract_address, abi=abi)

    tx_obj = contract.functions.openLuckyChest(nonce, expired, signature)
    transaction = tx_obj.build_transaction({
        'from': caller,
        'gas': int(_getEstimateGas(caller, contract_address) * 2.5),
        'gasPrice': _getGasPrice(),
        'nonce': web3.eth.get_transaction_count(caller),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_status = web3.eth.wait_for_transaction_receipt(tx_hash)['status']
    tx_status_msg = 'Success' if tx_status == 1 else 'Failed'
    print('> openMineBox@' + user[0] + ' Status: ' + tx_status_msg + ' TxHash: ', tx_hash.hex())


def dailyCheckIn(user):
    daily_check = json.loads(getDailyTask(user))
    has_daily_check = False
    for task in daily_check['data']:
        if task['type'] == 5 and task['name'] == 'Daily check-in':
            has_daily_check = True
            break
    if has_daily_check:
        headers = get_headers(user)
        response = requests.post(URL, json=data_checkIn, headers=headers)
        print('> dailyCheckIn@' + user[0] + ' ' + response.text)
        daily_box_info = json.loads(response.text)
        to_ = daily_box_info['check']['to']
        expired = daily_box_info['check']['expired']
        mnt = daily_box_info['check']['mnt']
        tmak = daily_box_info['check']['tmak']
        nonce = daily_box_info['check']['nonce']
        signature = daily_box_info['check']['signature']
        uid = daily_box_info['check']['uid']
        type_ = daily_box_info['check']['type']
        task_id = daily_box_info['check']['task_id']

        web3 = Web3(Web3.HTTPProvider(RPC))
        if not web3.is_connected():
            print("RPC Connection Error")
            return

        caller, private_key = user[2], user[3]
        abi = json.loads(open("abi.json", "r").read())
        contract_address = "0x9B63C5B7a68573Bbc47336Ec0247798411f561b9"
        contract = web3.eth.contract(address=contract_address, abi=abi)

        tx_obj = contract.functions.signIn(int(nonce), int(expired), int(tmak), int(mnt), signature)
        transaction = tx_obj.build_transaction({
            'from': caller,
            'gas': int(_getEstimateGas(caller, contract_address) * 3.5),
            'gasPrice': _getGasPrice(),
            'nonce': web3.eth.get_transaction_count(caller),
        })

        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_status = web3.eth.wait_for_transaction_receipt(tx_hash)['status']
        tx_status_msg = 'Success' if tx_status == 1 else 'Failed'
        print('> dailyCheckIn@' + user[0] + ' Status: ' + tx_status_msg + ' TxHash: ', tx_hash.hex())



def getNumTMAK(user):
    try:
        headers = get_headers(user)
        response = requests.post(URL, json=data_getNumTMAK, headers=headers)
        print('> getNumTMAK@' + user[0] + ' ' + response.text)
        sum_gat = json.loads(response.text)['data']['sum_gat']
        wait_get = json.loads(response.text)['data']['wait_get']

        sum_tmak, wait_tmak = 0, 0
        for it in sum_gat:
            if it['item_name'] == 'TMAK':
                sum_tmak = it['count']

        for it in wait_get:
            if it['item_name'] == 'TMAK':
                wait_tmak = it['count']

        return sum_tmak, wait_tmak
    except Exception as e:
        print('Error > getNumTMAK: ', e)
        return 0, 0


def _getGasPrice():
    payload = json.dumps({
        "method": "eth_gasPrice",
        "params": [],
        "id": 1,
        "jsonrpc": "2.0"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", RPC, headers=headers, data=payload)
    res = json.loads(response.text)['result']
    return int(res, 16)


def _getEstimateGas(caller, contract_addr):
    payload = json.dumps({
        "method": "eth_estimateGas",
        "params": [
            {
                "from": caller,
                "to": contract_addr
            }
        ],
        "id": 1,
        "jsonrpc": "2.0"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", RPC, headers=headers, data=payload)
    res = json.loads(response.text)['result']
    return int(res, 16)


def getExchangeRate(user):
    try:
        headers = get_headers(user)
        response = requests.post(URL, json=data_getExchangeRate, headers=headers)
        print('> getExchangeRate@' + user[0] + ' ' + response.text)
        data_json = json.loads(response.text)
        return data_json['data']['integral'], data_json['data']['rate']
    except Exception as e:
        print('Error > getExchangeRate: ', e)
        return 0, 0


def exchange(user, integral):
    headers = get_headers(user)
    data_exchange['user']['exchange']['integral'] = integral
    response = requests.post(URL, json=data_exchange, headers=headers)
    print('> exchange@' + user[0] + ' ' + response.text)
    return response.text


def useEnergy1(user):
    headers = get_headers(user)
    response = requests.post(URL, json=data_useEnergy1, headers=headers)
    print('> useEnergy1@' + user[0] + ' ' + response.text)
    return response.text


def useEnergy2(user):
    headers = get_headers(user)
    response = requests.post(URL, json=data_useEnergy2, headers=headers)
    print('> useEnergy2@' + user[0] + ' ' + response.text)
    return response.text


def op(user):
    info = login(user)
    info = json.loads(info)
    # 计算总速度
    global ALL_SPEED
    all_speed = info['data']['pet']['all_speed']
    ALL_SPEED += all_speed
    # 宠物唤醒逻辑
    end_time = info['data']['pet']['end_time']
    now = time.time()

    if end_time - now < 3600 * 4:  # 如果now距离end_time小于4h，则唤醒宠物
        wakePet(user)

    spar = info['data']['header']['spar']
    energy = info['data']['header']['energy']
    integral = info['data']['header']['integral']

    # 充值逻辑
    if get_time_to_7am() < 3600 * 7 and spar > 100000:  # 如果距离7点不足7小时
        recharge(user, spar)
        spar = 0

    lv0 = info['data']['pet']['lv']
    # 宠物升级逻辑，优先升级pet
    pet_level_up = False
    up_need_spar = info['data']['pet']['upNeedSpar']
    if lv0 < 500:
        while spar >= up_need_spar:
            pet_level_up = True
            rsp = json.loads(levelUp(user))
            spar -= up_need_spar
            up_need_spar = rsp['data']['pet']['upNeedSpar']
    else:
        pet_level_up = True

    # 角色1解锁逻辑
    if info['data']['roleMan']['lv'] == 0:  # 未解锁
        if spar >= info['data']['roleMan']['unlock_cost']['count']:
            spar -= info['data']['roleMan']['unlock_cost']['count']
            lockRole1(user)

    # 角色1升级逻辑
    if 0 < info['data']['roleMan']['lv'] < 500 and pet_level_up:
        up_need_spar = info['data']['roleMan']['upNeedSpar']
        while spar >= up_need_spar:
            rsp = json.loads(levelUp1(user))
            spar -= up_need_spar
            up_need_spar = rsp['data']['roleMan']['upNeedSpar']
    # 角色1使用电池
    energy1 = info['data']['roleMan']['energy']
    while energy1 < 4 and energy > 0:
        useEnergy1(user)
        energy1 += 1
        energy -= 1

    # 角色2升级逻辑

    if 0 < info['data']['roleWoman']['lv'] < 500 and pet_level_up:
        up_need_spar = info['data']['roleWoman']['upNeedSpar']
        while spar >= up_need_spar:
            rsp = json.loads(levelUp2(user))
            spar -= up_need_spar
            up_need_spar = rsp['data']['roleWoman']['upNeedSpar']

    # 角色2使用电池
    if info['data']['roleWoman']['lv'] > 0:
        energy2 = info['data']['roleWoman']['energy']
        while energy2 < 4 and energy > 0:
            useEnergy2(user)
            energy2 += 1
            energy -= 1

    # 开宝箱
    if len(user) == 4:
        mine_box_info = json.loads(getMineBoxInfo(user))
        if mine_box_info['data']['cd'] == 0:
            openMineBox(user)

    # 每日签到
    if len(user) == 4:
        dailyCheckIn(user)

    # 兑换tmak
    # integral, rate = getExchangeRate(user)
    if integral > 0:
        exchange(user, integral)

    # 获取tmak数量
    sum_tmak, wait_tmak = getNumTMAK(user)
    global SUM_TMNK, WAIT_TMNK
    SUM_TMNK += sum_tmak
    WAIT_TMNK += wait_tmak
    print('> NumTMNK@' + user[0] + ' sum_tmak: ', sum_tmak, ' wait_tmak: ', wait_tmak)


if __name__ == '__main__':
    loop_cnt = 0
    while True:
        SUM_TMNK, WAIT_TMNK = 0, 0
        ALL_SPEED = 0
        loop_cnt += 1
        print('Loop Start: ', loop_cnt, '-------------------------',
              time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        time.sleep(random.randint(5, 15))
        for user in USER_INFO:
            try:
                op(user)
            except Exception as e:
                print('Error @' + user[0] + ': ', e)
        print('Loop End: ', loop_cnt, '-------------------------', 'SUM_TMNK: ', SUM_TMNK, 'WAIT_TMNK: ', WAIT_TMNK, 'ALL_SPEED: ', ALL_SPEED)