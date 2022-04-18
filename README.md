# config_auditing

##### Example:
```python
from config_auditing import config_search, config_search_audit


lookup = 'access_list'
config_search(
    f'{lookup}_lookup',                     # File name of the configuration search
    f'nil_lib/templates/{lookup}.fsm',      # Requires nil_lib to be in the same folder group
    'config_dump/'                          # Path for the switch configuration dump
)

config_search_audit(
    'remark --Ansible',                     # String lookup in the search output file
    f'configs/search/{lookup}_lookup.yml',  # Search output file to audit
    f'{lookup}_audit'                       # File name of the configuration search
    contains=False                          # String is not found
)
```

##### Outputs:
Will generate the following folders and files.

*configs/search/access_list_lookup.yml* -> 
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


*configs/search/audit/access_list_audit.yml* -> 
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