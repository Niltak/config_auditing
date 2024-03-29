from nil_lib import format_switch_list, switch_list_send_command, file_loader, file_create


def rogue_bpdu_switches(switch_list, user, pwd=None) -> None:
    '''
    '''
    if switch_list.endswith('.yml'):
        switch_list = file_loader(switch_list)

    switch_list = format_switch_list(
        switch_list, user, pwd=pwd)

    switch_list = switch_list_send_command(
        switch_list, ['sh spanning-tree detail', 'sh run'])

    fsm_bpdu = file_loader(
        'nil_lib/templates/spanning_tree_int_detail.fsm')
    fsm_interfaces = file_loader(
        'nil_lib/templates/interfaces.fsm')

    audit_list, debug_list = [], []
    for switch in switch_list:
        if not switch['name']:
            continue    # Could not connect to switch

        fsm_bpdu._result, fsm_interfaces._result = [], []
        switch['output'][0] = fsm_bpdu.ParseTextToDicts(
            switch['output'][0])
        switch['output'][1] = fsm_interfaces.ParseTextToDicts(
            switch['output'][1])

        portfast_list, non_portfast_list = [], []
        for spanning_entry in switch['output'][0]:
            if ('Port-channel' not in spanning_entry['INTERFACE']
                and spanning_entry['INTERFACE'] not in portfast_list):
                if spanning_entry['BPDU_RECIEVE'] != '0':
                    for int_entry in switch['output'][1]:
                        # Find interface configs
                        if spanning_entry['INTERFACE'] == int_entry['INTERFACE_NAME']:
                            found = False
                            for int_details in int_entry['INTERFACE_DETAILS']:
                                if 'portfast' in int_details:
                                    portfast_list.append(spanning_entry['INTERFACE'])
                                    found = True
                                    break
                            if not found:
                                # Entry does not have portfast
                                # int_entry['SWITCH_NAME'] = switch['name']
                                if int_entry not in non_portfast_list:
                                    non_portfast_list.append(int_entry)
                            else:
                                break
        if portfast_list:
            audit_list.append({
                'name': switch['name'], 'interface': portfast_list})
        if non_portfast_list:
            debug_list.append({
                'name': switch['name'], 'interface': non_portfast_list})

    file_create(
        'rogue_bpdu_switches',
        'logs/audit/',
        audit_list,
        file_extension='yml',
        override=True)

    file_create(
        'rogue_bpdu_non_portfast',
        'logs/audit/',
        debug_list,
        file_extension='yml',
        override=True)


def rogue_mac_ports(switch_list, user, pwd=None) -> None:
    '''
    '''
    if switch_list.endswith('yml'):
        switch_list = file_loader(switch_list)

    switch_list = format_switch_list(
        switch_list, user, pwd=pwd)

    switch_list = switch_list_send_command(
        switch_list, ['show mac address-table', 'sh run'])

    fsm_mac = file_loader(
        'nil_lib/templates/mac_address_table.fsm')
    fsm_interfaces = file_loader(
        'nil_lib/templates/interfaces.fsm')

    audit_list = []
    for switch in switch_list:
        if not switch['name']:
            break

        fsm_mac._result, fsm_interfaces._result = [], []
        switch['output'][0] = fsm_mac.ParseTextToDicts(
            switch['output'][0])
        switch['output'][1] = fsm_interfaces.ParseTextToDicts(
            switch['output'][1])

        mac_list, processed_list = [], []
        for check_entry in switch['output'][0][:]:
            if check_entry['PORTS'] in processed_list:
                continue
            if ('CPU' in check_entry['PORTS']
                or 'Po' in check_entry['PORTS']):
                switch['output'][0].remove(check_entry)
                continue
            found = []
            for entry in switch['output'][0]:
                if (check_entry == entry
                    or entry['PORTS'] in processed_list):
                    continue
                if check_entry['PORTS'] == entry['PORTS']:
                    found.append(entry)

            list_check = [
                {'key': 'VLAN', 'value': check_entry['VLAN']},
                {'key': 'MAC', 'value': check_entry['MAC']},
                {'key': 'TYPE', 'value': check_entry['TYPE']}]
            for check in list_check:
                if not isinstance(check['value'], list):
                    check_entry[check['key']] = [check['value']]

            if found:
                for entry in found:
                    list_check = [
                        {'key': 'VLAN', 'value': entry['VLAN']},
                        {'key': 'MAC', 'value': entry['MAC']},
                        {'key': 'TYPE', 'value': entry['TYPE']}]
                    for check in list_check:
                        if entry[check['key']] not in check_entry[check['key']]:
                            check_entry[check['key']].append(check['value'])

                    switch['output'][0].remove(entry)

            processed_list.append(check_entry['PORTS'])
            if len(check_entry['MAC']) > 2:
                mac_list.append(check_entry['PORTS'])

        if mac_list:
            mac_list = sorted(mac_list)
            for port in mac_list[:]:
                found = ''
                if 'Gi' in port:
                    for interface in switch['output'][1]:
                        if port[2:] in interface['INTERFACE_NAME']:
                            found = interface['INTERFACE_DETAILS']
                            for detail in interface['INTERFACE_DETAILS']:
                                if 'switchport mode trunk' in detail:
                                    found = ''
                                    mac_list.remove(port)
                                    break
                            break

                if found:
                    mac_list.remove(port)
                    mac_list.append({'port_name': port, 'port_details': found})

        if mac_list:
            audit_list.append({
                'name': switch['name'], 'ports': mac_list})

    file_create(
        'rogue_mac_ports',
        'logs/audit/',
        audit_list,
        file_extension='yml',
        override=True)


if __name__ == "__main__":
    pass
