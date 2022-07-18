import nil_lib as ks


def port_description_update(
    switch_list,
    old_build_code,
    new_build_code,
    debug=None) -> None:
    '''
    Updates port description on a list of switches.
    '''
    old_build_code += '-'
    new_build_code += '-'
    change_list = []

    command = 'sh interface description'
    switch_list_port = ks.switch_list_send_command(switch_list, command, fsm=True)

    for switch_port in switch_list_port:
        change_format = {
            'name': switch_port['name'],
            'port_change': []
        }
        for port in switch_port['output']:
            if 'description' in port.keys():
                if port['description'].startswith(old_build_code):
                    change_format['port_change'].append({
                        'port': port['port'],
                        'old': port['description'],
                        'description': port['description'].replace(old_build_code, new_build_code)
                    })
            elif 'descrip' in port.keys():
                if port['descrip'].startswith(old_build_code):
                    change_format['port_change'].append({
                        'port': port['port'],
                        'old': port['descrip'],
                        'description': port['descrip'].replace(old_build_code, new_build_code)
                    })
        change_list.append(change_format)

    for switch_change in change_list[:]:
        if not switch_change['port_change']:
            change_list.remove(switch_change)
            continue

        change_log = []
        for port in switch_change['port_change']:
            change_log.append(f"int {port['port']}\n")
            change_log.append(f"  description {port['description']}\n")

        ks.make_file(
            f"port_change_{switch_change['name']}",
            'configs/command_list/',
            change_log,
            override=True
        )

    if debug:
        ks.make_file(
            f'port change for building {new_build_code[:-1]}',
            'logs/',
            change_list,
            file_extension='yml'
        )


if __name__ == '__main__':
    pass
