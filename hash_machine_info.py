#!/usr/bin/env python3

from hashlib import blake2b
import json

# NOTE: cpu_rate: 单位Mhz; sys_disk/data_disk单位: G， mem_num: G
# NOTE: is_support: 支持传1，不支持传0
# NOTE: 请先修改自己的随机字符串: rand_str

raw_info = json.loads(
    """
{
  "machine_id": "28df925728b1cb0bd843d646c40b9ac7c6f695d92156e7fea907fb0998ab0138",
  "gpu_type": "GeForceRTX3080",
  "gpu_num": 4,
  "cuda_core": 8704,
  "gpu_mem": 10,
  "calc_point": 67975,
  "sys_disk": 350,
  "data_disk": 5500,
  "cpu_type": "Intel(R) Xeon(R) CPU E5-2697 v3 @ 2.60GHz",
  "cpu_core_num": 56,
  "cpu_rate": 2600,
  "mem_num": 723,
  "rand_str": "yanfeihong1",
  "is_support": 1
}
    """
)



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

print("MachineId:\t", raw_info["machine_id"])
h = blake2b(digest_size=16)
h.update(raw_input0.encode())
print("Hash:" + "\t0x" + h.hexdigest())