import os
import yaml
import nil_lib as ks


def config_search(
    new_file_name,
    fsm_template,
    config_dir,
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
            file_url = f"{config_dir}/{file_name}"
            text_data = ks.file_loader(file_url)
            
            output = fsm.ParseText(text_data[0])
            output_format = {
                'name': file_name,
                'data': output
            }
            new_file_data.append(output_format)

    if debug:
        print(new_file_data)
        exit()
    
    ks.file_create(
        new_file_name,
        'configs/search/',
        new_file_data,
        file_extension='yml',
        override=True
    )


def config_search_audit(
    search_keywords,
    yaml_config_file,
    new_file_name,
    contains=False,
    search_item_key=False,
    # switch_names_filter=None,
    debug=False
    ) -> None:
    # Find switch entries that do not contain search_item in the last yaml entry

    if not isinstance(search_keywords, list):
        search_keywords = [search_keywords]

    # if switch_names_filter:
    #     if not isinstance(switch_names_filter, list):
    #         switch_names_filter = [switch_names_filter]
    
    with open(yaml_config_file) as yaml_file:
        switch_list = yaml.load(yaml_file, Loader=yaml.FullLoader)

    search_list = []
    for switch in switch_list:
        # if switch_names_filter:
        #     found = False
        #     for switch_name_filter in switch_names_filter:
        #         if switch_name_filter not in switch['name']:
        #             continue
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
            search_list.append(switch) 

    if debug:
        for search in search_list:
            print(search)
        exit()

    ks.file_create(
        new_file_name,
        'configs/search/audit/',
        search_list,
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
        'configs/search/audit',
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
