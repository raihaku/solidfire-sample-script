SolidFire Sample Scripts
===

SolidFire��Provisioned IOPS��Account�������Ă���Volume���Ȃǂ̏W�v���ʂ�API���s���ʂɒǉ�����X�N���v�g�ł��B

GetClusterCapacitySumMetaWarn.py : Metadata��Warning�l��Ԃ�
ListAccountsCountVolume.py : Account������Volume����Ԃ�
ListActiveNodesCountNode.py : Active Node����Ԃ�
ListVolumesSumQoS.py : Provisioned Burst/Max/Min IOPS��Ԃ�

Demo
--------------
���s����

Requirement
--------------
apt-get install python python-requests

Usage
--------------
# Change your SolidFire URL, Username and Password in scripts
>endpoint['login'] = "admin"
>endpoint['passwd'] = "P@ssw0rd"
>url = 'https://solidfire.mvip/json-rpc/10.1'

# Execute scripts
python .ListAccountsCountVolume.py
