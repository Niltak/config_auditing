from paramiko import SSHClient, AutoAddPolicy
from getpass import getpass


def rancid_config_download(user, config_dir, pwd=None) -> None:
    '''
    Connects to the rancid server and downloads config files.
    '''
    if not pwd:
        pwd = getpass()
    rancid_server = '172.28.248.18'
    rancid_config_dir = '/var/lib/rancid/PURDUE/configs/'
    with SSHClient() as conn:
        conn.set_missing_host_key_policy(AutoAddPolicy())
        conn.connect(rancid_server, 22, user, pwd)
        with conn.open_sftp() as sftp:
            sftp.chdir(rancid_config_dir)
            switch_list = sftp.listdir()
            # Download each file appearing in the directory
            for switch in switch_list:
                try:
                    sftp.get(switch, f'{config_dir}{switch}')
                except OSError:
                    print(f'File name {switch} is a directory and will not download')


if __name__ == "__main__":
    pass
