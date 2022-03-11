import nil_lib as ks


def capture_wireless_ports(
    site_code,
    user,
    site_yaml=None,
    pwd=None):
    '''
    '''
    if not pwd:
        pwd = ks.verify_pwd(user)
    if not site_yaml:
        site_yaml = f'site_info/{site_code}/{site_code}.yaml'

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
            for cdp in switch['output']:
                if 'AIR-' in cdp['platform']:
                    wireless_port = f"show run int {cdp['local_port']}"
                    wireless_list.append(wireless_port)
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
            for i, output in enumerate(switch_data['output']):
                for data in output:
                    switch_data['output'][i] = data

    ks.file_create(
        f'{site_code}_wireless',
        f'site_info/{site_code}/',
        switch_list_data,
        file_extension='yml',
        override=True
    )


if __name__ == "__main__":
    pass