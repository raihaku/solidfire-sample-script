SolidFire Sample Scripts
===

SolidFireのProvisioned IOPSやAccountが持っているVolume数などの集計結果をAPI実行結果に追加するスクリプトです。

* GetClusterCapacitySumMetaWarn.py : MetadataのWarning値を返す
* ListAccountsCountVolume.py : Accountが持つVolume数を返す
* ListActiveNodesCountNode.py : Active Node数を返す
* ListVolumesSumQoS.py : Provisioned Burst/Max/Min IOPSを返す
* SFVolMoveSimuration_v0.2.py : Upgrade時のVolume数 遷移をシミュレーションする

Demo
--------------
実行結果

Requirement
--------------
    apt-get install python python-requests

Usage
--------------
1. Change your SolidFire URL, Username and Password in scripts  
    >endpoint['login'] = "admin"  
    >endpoint['passwd'] = "P@ssw0rd"  
    >url = 'https://solidfire.mvip/json-rpc/10.1'  

2. Execute scripts  
    python .ListAccountsCountVolume.py


参考
--------------
https://www.slideshare.net/raihaku/solidfire-kibanaelk-stack
