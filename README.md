# DBC平台收集机器信息

## Usage
1. 下载最新的在线文档到程序根目录中。
2. 在main_xls.py中填写随机字符串rand_str,签名sign_str等信息。
3. 执行main_xls.py。

```python
python main_xls.py
```

4. 产生的结果保存在了"result.xlsx"中。

## 友情提示

1. 机器数量较多的时候，一定要随机挑选几台手动获取机器信息，并计算hash。防止程序有bug导致全都弄错了。
2. 当增加新机器的时候，可以再次将在线表格下载到本地，或者将新添加的行保存到本地已下载的待验证机器表中。再次执行程序，程序会以附加的方式来添加新机器的信息。

## 感谢
感谢 [Weipeilang](https://github.com/Weipeilang)  将本项目利用pandas重写以及增添了附加新机器的功能。
