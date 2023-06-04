import os
import nil_lib as ks


def rename_site(site_code, new_site_code):
    # def rename_site(site_code, new_site_code, user, pwd=None):
    '''
    '''
    # switch_list = ks.format_site_yaml(site_code, user, pwd=pwd)

    # hostnames = ks.switch_list_send_command(switch_list, '')

    hostnames = []
    for subdir, dirs, files in os.walk(f'site_info/{site_code}/configs/dump/'):
        for file_name in files:
            hostnames.append(file_name)

    for output in hostnames:
        current_name = output['name'].lower()
        if current_name.startswith('rtr'):
            number = current_name.split('-')[0].split('rtr')[1]
            new_name = f"{new_site_code}-RTR-{number}"
        elif current_name.startswith('sw'):
            split = current_name.split('-')
            number = split[0].split('sw')[1]
            tag = 'ASW'
            if number == '01':
                tag = 'CSW'
            new_name = f"{new_site_code}-{tag}-{number}"
            if len(current_name) > 2:
                suffix = ' '
                extra_details = current_name.split[2:]
                for detail in extra_details:
                    suffix += detail + ' '

                new_name += suffix[:-1]
