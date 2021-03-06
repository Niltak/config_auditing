import nil_lib as ks


def capture_wireless_ports(
    site_code,
    user,
    site_yaml=None,
    pwd=None):
    '''
    Connect to site switch list and check cdp neighbors for APs.
    Create and send a command list of ports for APs.
    Outputs switch port list of interface configs for APs.
    '''
    if not pwd:
        pwd = ks.verify_pwd(user)
    if not site_yaml:
        site_yaml = f'site_info/{site_code}/{site_code}.yml'

    # Checking cdp neighbors for APs
    switch_list = ks.format_site_yaml(
        site_yaml, user, pwd=pwd)
    switch_cdp_list = ks.switch_list_send_command(
        switch_list, 'show cdp neighbors detail', fsm=True)

    # Creating switch_command_list to send to a corresponding switch
    switch_list, switch_command_list = [], []
    for switch in switch_cdp_list:
        if switch['name']:
            wireless_list = []
            if not isinstance(switch['output'], list):
                print(f"FSM did not convert {switch['name']}")
                continue
            for cdp_list in switch['output']:
                if not isinstance(cdp_list, list):
                    cdp_list = [cdp_list]
                for cdp in cdp_list:
                    if 'AIR-' in cdp['platform']:
                        wireless_port = f"show run int {cdp['local_port']}"
                        wireless_list.append(wireless_port)
            if len(wireless_list) > 0:
                switch_list.append(switch['name'])
                switch_command_list.append(wireless_list)

    switch_list = ks.format_switch_list(switch_list, user, pwd=pwd)
    switch_list_data = ks.switch_list_send_command(
        switch_list,
        switch_command_list,
        fsm=True,
        fsm_template='nil_lib/templates/interfaces.fsm')

    # Formatting data
    for switch_data in switch_list_data:
        if switch_data['name']:
            del switch_data['host']
            del switch_data['device_type']
            output_list = []
            for output in switch_data['output']:
                for data in output:
                    output_list.append(data)
            switch_data['output'] = output_list

    ks.file_create(
        f'{site_code}_wireless',
        f'site_info/{site_code}/',
        switch_list_data,
        file_extension='yml',
        override=True
    )


def auditing_wireless_ports(site_code) -> None:
    '''
    Search site wireless list for the speed command.
    Outputs switch list of speed commands.
    '''
    wireless_file = f'site_info/{site_code}/{site_code}_wireless.yml'
    switch_port_list = ks.file_loader(wireless_file)

    port_list = []
    for switch in switch_port_list:
        found = False
        port_details = []
        if not switch['name'] or not switch['output']:
            continue
        for port in switch['output']:
            for details in port['interface_details']:
                if 'speed' in details:
                    port_details.append({'interface_name': port['interface_name'], 'interface_details': details})
                    found = True
        if found:
            port_list.append({'name': switch['name'], 'data': port_details})

    ks.file_create(
        'wireless_ports',
        'configs/audit/',
        port_list,
        file_extension='yml',
        override=True
    )


if __name__ == "__main__":
    pass
