# config_auditing

##### Example:
```python
from config_auditing import config_search, config_audit


lookup = 'access_list'
config_search(
    'test_site_code'                        # Site code
    lookup)                                 # Name of template in nil_lib

config_audit(
    'remark --Ansible',                     # Keyword lookup in the search output file
    f'configs/search/{lookup}.yml',         # 'config_search' output file to audit
    contains=False)                         # If the keyword needs to be in the entry
```

##### Outputs:
Will generate the following folders and files.

*configs/search/access_list_lookup.yml* -> Captures all data based on textFSM file
```yaml
- name: test-sw-c3850-01
  data:
  - - ACL-SNMP-RO
    - standard
    - - permit 10.10.20.1
      - permit 10.10.20.2
      - permit 10.10.20.3
  - - Device-Mgmt-Access
    - extended
    - - remark --Managment Subnet
      - permit tcp 172.28.0.0 0.0.255.255 any eq 22
      - remark --Ansible
      - permit tcp host 10.10.10.100 any eq 22
      - remark --Admin Subnet
      - permit tcp 192.168.1.0 0.0.0.255 any eq 22
- name: test-sw-c3850-02
  data:
  - - ACL-SNMP-RO
    - standard
    - - permit 10.10.20.1
      - permit 10.10.20.2
      - permit 10.10.20.3
  - - Device-Mgmt-Access
    - extended
    - - remark --Managment Subnet
      - permit tcp 172.28.0.0 0.0.255.255 any eq 22
      - remark --Ansible
      - permit tcp host 10.10.10.100 any eq 22
      - remark --Admin Subnet
      - permit tcp 192.168.1.0 0.0.0.255 any eq 22
- name: test-sw-c3850-03
  data:
  - - ACL-SNMP-RO
    - standard
    - - permit 10.10.20.1
      - permit 10.10.20.2
      - permit 10.10.20.3
  - - Device-Mgmt-Access
    - extended
    - - remark --Managment Subnet
      - permit tcp 172.28.0.0 0.0.255.255 any eq 22
      - remark --Admin Subnet
      - permit tcp 192.168.1.0 0.0.0.255 any eq 22
```


*configs/search/audit/access_list_audit.yml* -> Filter search list with keyword
```yaml
- name: test-sw-c3850-03
  data:
  - - ACL-SNMP-RO
    - standard
    - - permit 10.10.20.1
      - permit 10.10.20.2
      - permit 10.10.20.3
  - - Device-Mgmt-Access
    - extended
    - - remark --Managment Subnet
      - permit tcp 172.28.0.0 0.0.255.255 any eq 22
      - remark --Admin Subnet
      - permit tcp 192.168.1.0 0.0.0.255 any eq 22
```