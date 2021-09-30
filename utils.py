# http://jinbao.pinduoduo.com/index?page=1里面的分类，
import requests
import json
from hashlib import blake2b
import os
import pandas as pd


# peer_node="942bd171889df3c9b0e45425f8c82b8feeb075fe017bb98e53115a88ad6d6b7d"
# sign="0c4ee12b9e6649ce8f6250f30fd5d1a62245d3ebf352f53cbe05dfe50ba3d84c9aaa03c94c9aa6b4b2dc21ef6594682e2b6ec518aa2a36c38bfdedce9196c885"
# nonce="3bQrNa5nE93e3yk1MMFYc1bcnEcVHxWaMe29EAB7y9BZFSqFwm95whV"
# wallet="5FNiuSGMonSGYibxiSYRvQr1oXdRsBXBXE3Mnt8iQ1K4Tgav"

def create_dir_not_exist(path,sheet_name):
    if not os.path.exists(path):
        df_blank = pd.DataFrame()
        df_blank.to_excel(path,sheet_name=sheet_name,index=False)


def transUnit (part,machine_info):
    part=str(part)
    num = float(machine_info["result_message"][part]["size"][0:-1])
    unit = machine_info["result_message"][part]["size"][-1]
    if (unit) == "T":
        num *= 1000
    elif unit != "G":
        print("unit error:" + unit)
        return -1
    num = int(num)
    return num



def requestFromDBC(peer_node,sign,nonce,wallet):
    peer_node=str(peer_node)

    sign=str(sign)

    nonce=str(nonce)
    wallet=str(wallet)
    headers = {
        "Cache-Control": "no-cache",
        "Postman-Token": "<calculated when request is sent>",
        "Content-Type": "application/json",
        "Content-Length": "<calculated when request is sent>",
        "Host": "<calculated when request is sent>",
        "User-Agent": "PostmanRuntime/7.28.3",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        }
    url = "http://111.44.254.162:20001/api/v1/mining_nodes"
    pyload = {"peer_nodes_list":[peer_node],"additional":{},"sign":sign,"nonce":nonce,"wallet":wallet}
    response = requests.post(url, data=json.dumps(pyload), headers=headers).text

    # print(response)
    return response
# requestFromDBC(peer_node,sign,nonce,wallet)



def hashMachineInfo(MachineInfo):
    raw_info = json.loads(MachineInfo)
    raw_input0 = (
            raw_info["machine_id"]
            + raw_info["gpu_type"]
            + str(raw_info["gpu_num"])
            + str(raw_info["cuda_core"])
            + str(raw_info["gpu_mem"])
            + str(raw_info["calc_point"])
            + str(raw_info["sys_disk"])
            + str(raw_info["data_disk"])
            + str(raw_info["cpu_type"])
            + str(raw_info["cpu_core_num"])
            + str(raw_info["cpu_rate"])
            + str(raw_info["mem_num"])
            + str(raw_info["rand_str"])
            + str(raw_info["is_support"])
    )
    #print(raw_input0)
    print("MachineId:\t", raw_info["machine_id"])
    h = blake2b(digest_size=16)
    h.update(raw_input0.encode())
    hashcode=str("\t0x" + h.hexdigest())
    print("Hash:" +hashcode)
    return hashcode


