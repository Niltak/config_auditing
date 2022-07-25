import os
import yaml
import nil_lib as ks


def config_search(
    config_dir,
    fsm_template,
    new_file_name,
    site_folder=True,
    debug=False) -> None:
    '''
    Uses textFSM file to search through config.
    Creates file of the searched config findings.
    '''
    fsm = ks.file_loader(fsm_template)

    new_file_data = []
    for subdir, dirs, files in os.walk(config_dir):
        for file_name in files:
            fsm._result = []
            if not config_dir.endswith('/'):
                config_dir = config_dir + '/'
            file_url = f"{config_dir}{file_name}"
            text_data = ks.file_loader(file_url)
            if file_name.endswith('.txt'):
                file_name = file_name.split('.txt')[0]

            output = fsm.ParseText(text_data[0])
            output_format = {
                'name': file_name,
                'data': output
            }
            new_file_data.append(output_format)

    if debug:
        print(new_file_data)
        exit()

    file_dir = 'configs/search/'
    if site_folder:
        site_code = config_dir.split('/')[1]
        file_dir = f'site_info/{site_code}/configs/search/'

    ks.file_create(
        new_file_name,
        file_dir,
        new_file_data,
        file_extension='yml',
        override=True
    )


def config_search_audit(
    search_keywords,
    yaml_config_file,
    new_file_name,
    site_code=None,
    contains=False,
    search_item_key=False,
    debug=False) -> None:
    '''
    Find switch entries that do not contain search_item in the last yaml entry
    '''
    if not isinstance(search_keywords, list):
        search_keywords = [search_keywords]

    if not yaml_config_file.endswith('.yml'):
        yaml_config_file += '.yml'

    if site_code:
        yaml_config_file = f'site_info/{site_code}/configs/search/{yaml_config_file}'

    with open(yaml_config_file) as yaml_file:
        switch_list = yaml.load(yaml_file, Loader=yaml.FullLoader)

    search_results = []
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

    file_dir = 'configs/audit/'
    if site_code:
        file_dir = f'site_info/{site_code}/{file_dir}'

    ks.file_create(
        new_file_name,
        file_dir,
        search_results,
        file_extension='yml',
        override=True
    )


def config_search_audit_interfaces(
    search_keywords,
    yaml_config_file,
    new_file_name,
    site_code=None,
    contains=False,
    interface_name_filter=None,
    debug=False) -> None:
    '''
    Find switch entries that do not contain search_item within interfaces
    '''
    if not isinstance(search_keywords, list):
        search_keywords = [search_keywords]
    if not yaml_config_file.endswith('.yml'):
        yaml_config_file += '.yml'
    if site_code:
        yaml_config_file = f'site_info/{site_code}/configs/search/{yaml_config_file}'

    switch_list = ks.file_loader(yaml_config_file)
    search_results = []
    for switch in switch_list:
        found = False
        interface_list = []
        for data in switch['data']:
            if interface_name_filter:
                if interface_name_filter not in data[0]:
                    continue
            interface = data[1]
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

    file_dir = 'configs/audit/'
    if site_code:
        file_dir = f'site_info/{site_code}/{file_dir}'

    ks.file_create(
        new_file_name,
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
    switch_list_lookup = []
    switch_list_missing = []

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


def audit_filter(audit_file, filter_file, ) -> None:

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
