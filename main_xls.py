from utils import requestFromDBC
from utils import hashMachineInfo
from utils import transUnit
import json
import math
import pandas as pd
import re
import os


sign_str='''
        wallet: 5FL1FThg9D76yNRxWzoiWeY1rjCFWvAbHLBNeVxD7Wdohaux
     nonce: 3SkmNNEs5Hps7ACwJareQVMGyBeHJK9roHyHe256s4xzhttKUcekPiG
nonce_sign: b602678835b56abf6b61b1caa9618aa15d817d24dba378551a8b8de2923f402eeba4b665607334f01690c1eabec55bec4cea88bd785b53727bbae78798ca6481

'''
#rand_str
rand_str="yanfeihong1"
# 在线文档文档名
so_file="utf-8\'\'验证人预主网待审核机器列表.xlsx"
#在线文档表名
so_sheet="待上链机器统计表"
# 存放结果的文件
re_file="result.xlsx"
# 表名
re_sheet="待上链机器统计表"

cpu_type_rate={"Intel(R) Xeon(R) Silver 4214R CPU @ 2.40GHz":2400,
               "Intel(R) Xeon(R) Silver 4210R CPU @ 2.40GHz":2400,
               "Intel(R) Xeon(R) CPU E5-2697 v3 @ 2.60GHz":2600,
               "Intel(R) Xeon(R) Gold 6226R CPU @ 2.90GHz":2900,
               "Intel(R) Xeon(R) CPU E5-2678 v3 @ 2.50GHz":2500,
               "Intel(R) Xeon(R) Gold 5218R CPU @ 2.10GHz":2100,
               "AMD EPYC 7601 32-Core Processor":2200,
               "Intel(R) Core(TM) i9-10850K CPU @ 3.60GHz":3600,
               "Intel(R) Core(TM) i9-10980XE CPU @ 3.00GHz":3000,
               "Intel(R) Core(TM) i9-10920X CPU @ 3.50GHz":3500,
               "Intel(R) Xeon(R) Silver 4110 CPU @ 2.10GHz":2100,
               "Intel(R) Xeon(R) CPU E5-2680 v3 @ 2.50GHz":2500,
               "AMD EPYC 7302P 16-Core Processor":3000}


search_result = re.search( r'wallet:\s*(.*)\n\s*nonce:\s*(.*)\n\s*nonce_sign:\s*(.*)', sign_str)
wallet=search_result.group(1)
nonce=search_result.group(2)
nonce_sign=search_result.group(3)

# workbook = xlrd.open_workbook()  # 文件路径
workbook = pd.read_excel(so_file,sheet_name=so_sheet)

if os.path.exists(re_file):
    result = pd.read_excel(re_file,sheet_name=re_sheet)
    recorded_hash = [result.iloc[:, 0][i] for i in range(len(result.iloc[:, 0]))]
else:
    recorded_hash = []

# #
nrows, ncols = workbook.shape
# # '''对workbook对象进行操作'''
# # # 通过sheet名获得sheet对象
# worksheet = workbook.sheet_by_name("待上链机器统计表")
# #
# nrows = worksheet.nrows  # 获取该表总行数
#
# ncols = worksheet.ncols  # 获取该表总列数
# #
# #




title=["机器ID","hash","gpu类型","gpu数量"	,"cuda_core数量","显存大小(G)","算力值","系统盘大小(G)","数据盘大小(G)","CPU类型","CPU核数","CPU频率(M)","内存大小(G)"]
row_info = []

try:
    for i in range(nrows):  # 循环打印每一行
        # if i==0:
        #     title=["序号","机器ID","hash","gpu类型","gpu数量"	,"cuda_core数量","显存大小(G)","算力值","系统盘大小(G)","数据盘大小(G)","CPU类型","CPU核数","CPU频率(M)","内存大小(G)"]
        #     # for j in range(0, len(title)):
        #     #     sheet.write(i, j, title[j])
        #     continue
        # time.sleep(2)

        # machine_id=str(worksheet.row_values(i)[1])
        machine_id = str(workbook.loc[i].values[1])
        #print(machine_id)
        if machine_id == 'nan' or machine_id in recorded_hash:
            continue

        reText = requestFromDBC(machine_id, nonce_sign, nonce, wallet)
        machine_info = json.loads(reText)
        # print(i)
        # print(machine_info["result_code"])
        if ("result_code" not in machine_info.keys() or machine_info["result_code"] != 0):
            print("client error!:" + machine_id + " " + str(machine_info))
            continue

        cpu_type = str(machine_info["result_message"]["cpu"]["type"])
        cpu_core_nums = int(machine_info["result_message"]["cpu"]["cores"])

        mem_num=transUnit("mem",machine_info)
        if(mem_num==-1):
            continue

        sys_disk=transUnit("disk_system",machine_info)
        if(sys_disk==-1):
            continue

        data_disk=transUnit("disk_data",machine_info)
        if(data_disk==-1):
            continue
        gpu_type = str(workbook.iloc[i, 2])
        gpu_num = int(workbook.iloc[i, 3])
        cuda_core = int(workbook.iloc[i, 4])
        gpu_mem = int(workbook.iloc[i, 5])
        calc_point = round((math.sqrt(gpu_num) * 50 + mem_num / 3.5 + (
                    math.sqrt(cuda_core) * math.sqrt(gpu_mem / 10) * gpu_num)) * 100)
        if cpu_type in cpu_type_rate.keys():
            cpu_rate = cpu_type_rate[cpu_type]
        else:
            print("cpu type of " + machine_id + " is: " + cpu_type + ", please contain it")
            continue
        dict = {
            "machine_id": machine_id,
            "gpu_type": gpu_type,
            "gpu_num": gpu_num,
            "cuda_core": cuda_core,
            "gpu_mem": gpu_mem,
            "calc_point": calc_point,
            "sys_disk": sys_disk,
            "data_disk": data_disk,
            "cpu_type": cpu_type,
            "cpu_core_num": cpu_core_nums,
            "cpu_rate": cpu_rate,
            "mem_num": mem_num,
            "rand_str": rand_str,
            "is_support": 1
        }
        machine_hash = hashMachineInfo(json.dumps(dict))

        row_info.append(
            [machine_id, machine_hash, gpu_type, gpu_num, cuda_core, gpu_mem, calc_point, sys_disk, data_disk,
             cpu_type, cpu_core_nums, cpu_rate, mem_num])
        print(machine_id + " success!")

finally:
    data = {}
    for t in title:
        data[t] = []
    for r in row_info:
        for i, t in enumerate(data.keys()):
            data[t].append(r[i])
    df = pd.DataFrame(data)
    if recorded_hash != []:
        df = pd.concat([result, df], ignore_index=True)
    df.to_excel(re_file,sheet_name=re_sheet,index=False)