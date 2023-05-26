import os
import nil_lib as ks


def config_search(
    site_code,
    fsm_template,
    file_name=None,
    config_dir=None,
    debug=False) -> None:
    '''
    Uses textFSM file to search through config.
    Creates file of the searched config findings.
    '''
    if not file_name:
        file_name = fsm_template
    if not config_dir:
        config_dir = f'site_info/{site_code}/configs/dump/'
        file_dir = f'site_info/{site_code}/configs/search/'
    else:
        if not config_dir.endswith('/'):
            config_dir = config_dir + '/'
        file_dir = 'configs/search/'
    if not fsm_template.endswith('.fsm'):
        fsm_template = f'nil_lib/templates/{fsm_template}.fsm'

    data_results = []
    fsm = ks.file_loader(fsm_template)
    for subdir, dirs, files in os.walk(config_dir):
        for switch_name in files:
            fsm._result = []
            switch_config = ks.file_loader(
                f'{config_dir}{switch_name}')
            if switch_name.endswith('.txt'):
                switch_name = switch_name.split('.txt')[0]

            switch_data = fsm.ParseText(switch_config[0])
            data_results.append(
                {'name': switch_name, 'data': switch_data})

    if debug:
        print(data_results)
        exit()

    ks.file_create(
        file_name,
        file_dir,
        data_results,
        file_extension='yml',
        override=True
    )


def config_audit(
    site_code,
    search_keywords,
    search_file,
    contains=False,
    file_name=None,
    search_item_key=None,
    debug=False) -> None:
    '''
    Find switch entries that do not contain search_item in the last yaml entry
    '''
    if not isinstance(search_keywords, list):
        search_keywords = [search_keywords]
    if not search_file.endswith('.yml'):
        search_file += '.yml'
    if not file_name:
        file_name = search_file

    default_dir = f'site_info/{site_code}/configs'

    search_results = []
    switch_list = ks.file_loader(f'{default_dir}/search/{search_file}')
    for switch in switch_list:
        found = False
        for data in switch['data']:
            if len(data) > 1:
                if search_item_key:
                    if search_item_key not in data[0]:
                        continue
                data_entry = len(data) - 1
                for config in data[data_entry]:
                    for keyword in search_keywords:
                        if keyword in config:
                            found = True
            else:
                for keyword in search_keywords:
                    if keyword in data[0]:
                        found = True
        if found == contains:
            search_results.append(switch)

    if debug:
        for search in search_results:
            print(search)
        exit()

    ks.file_create(
        file_name,
        f'{default_dir}/audit/',
        search_results,
        file_extension='yml',
        override=True
    )


def config_audit_interfaces(
    search_keywords,
    search_file,
    file_name,
    site_code=None,
    contains=False,
    filter_interface_name=None,
    filter_description=None,
    filter_trunk_port=False,
    filter_port_channel=False,
    debug=False) -> None:
    '''
    Find switch entries that do not contain search_item within interfaces
    '''
    if not isinstance(search_keywords, list):
        search_keywords = [search_keywords]
    if not search_file.endswith('.yml'):
        search_file += '.yml'

    file_dir = 'configs/audit/'
    if site_code:
        file_dir = f'site_info/{site_code}/{file_dir}'
        search_file = f'site_info/{site_code}/configs/search/{search_file}'

    search_results = []
    switch_list = ks.file_loader(search_file)
    for switch in switch_list:
        found = False
        interface_list = []
        for data in switch['data']:
            if filter_interface_name:
                if filter_interface_name not in data[0]:
                    continue
            interface = data[1]
            if filter_trunk_port:
                if 'switchport mode trunk' in interface:
                    continue
            if filter_port_channel:
                if 'channel-group' in interface:
                    continue
            if filter_description:
                if filter_description not in interface:
                    continue
            for keyword in search_keywords:
                if contains:
                    if keyword in interface:
                        found = True
                        interface_list.append(data)
                if not contains:
                    if keyword not in interface:
                        found = True
                        interface_list.append(data)
        if found:
            search_results.append({'name': switch['name'], 'data': interface_list})

    if debug:
        for search in search_results:
            print(search)
        exit()

    ks.file_create(
        file_name,
        file_dir,
        search_results,
        file_extension='yml',
        override=True
    )


def switch_list_lookup(
    switch_list_file,
    lookup_file,
    file_name):
    '''
    Filters a lookup file based on a list of switch names.
    Creates a file of the filtered switches and their data.
    '''
    switch_list = ks.file_loader(switch_list_file)['Switchlist']
    lookup_list = ks.file_loader(lookup_file)

    switch_list_lookup, switch_list_missing = [], []
    for switch in switch_list:
        lookup = ks.search_within_list(
            switch, lookup_list, 'name')
        if not lookup:
            switch_list_missing.append(switch)
            continue
        switch_list_lookup.append(lookup)

    if switch_list_missing:
        for switch in switch_list_missing:
            switch_list_lookup.append({'name': switch})

    ks.file_create(
        file_name,
        'configs/audit',
        switch_list_lookup,
        file_extension='yml'
    )


def audit_filter(audit_file, filter_file) -> None:

    switch_list = ks.file_loader(audit_file)
    nxos_list = ks.file_loader(filter_file)['Switchlist']

    for switch in switch_list[:]:
        if switch['name'] not in nxos_list:
            switch_list.remove(switch)

    ks.file_create(
        audit_file.split('/')[-1],
        'configs/search/audit',
        switch_list,
        file_extension='yml',
        override=True
    )


def audit_switch_list(audit_list):
    '''
    Loads audit file and pulls switches in the file.
    Returns a list of switches.
    '''
    switch_list = []
    audit_switch_list = ks.file_loader(audit_list)
    for switch in audit_switch_list:
        switch_list.append(switch['name'].split('.', 1)[0])
    return switch_list


def format_audit_switch_list(audit_list, user, pwd=None):
    '''
    Formats a list of switches based on an audit file.
    Returns a list of switches ready for connection functions.
    '''
    switch_list = audit_switch_list(audit_list)
    return ks.format_switch_list(switch_list, user, pwd=pwd)


if __name__ == "__main__":
    pass
