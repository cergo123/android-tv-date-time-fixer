# Import the necessary packages and modules
from adb_shell.auth.keygen import keygen
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
import os
import urllib.request
import ctypes


def gen_keys():
    """
    This function generates the ADB key pair (public and private keys) that will be used to connect to the Android TV device
    """
    print('Generating ADB keys...')
    current_path = os.getcwd()
    keys_folder = os.path.join(current_path, 'keys')

    # Check if the keys folder already exists, if not, create it
    if not os.path.exists(keys_folder):
        os.makedirs(keys_folder)
        priv = os.path.join(keys_folder, 'adbkey')
        keygen(priv)
        print('ADB keys have been generated successfully')
    else:
        print('ADB keys already exist')


def connect(ip):
    """
    This function connects to the Android TV device via ADB using the generated key pair
    """
    print(f'Connecting to {ip}:5555...')
    current_path = os.getcwd()
    keys_folder = os.path.join(current_path, 'keys')

    # Load the public and private keys from the keys folder
    with open(os.path.join(keys_folder, 'adbkey.pub'), 'rb') as f:
        pub = f.read()
    with open(os.path.join(keys_folder, 'adbkey'), 'rb') as f:
        priv = f.read()

    # Create a PythonRSASigner object using the loaded keys
    signer = PythonRSASigner(pub, priv)

    try:
        # Create an AdbDeviceTcp object and connect to the Android TV device using the signer object
        device = AdbDeviceTcp(ip.strip(), 5555, default_transport_timeout_s=9.)
        device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
        print(f'Connected to {ip}:5555 successfully')
        return device
    except Exception as e:
        print(e)
        print('Make sure to grant ADB permission to your device (check always allow from X device and click allow),'
              ' then try again')
        print('If the above not worked, check the IP and try again')
        print('Click any key to exit & re-run it again...')
        input()
        exit(1)


def fix(device, code):
    """
    This function fixes the date and time settings on the Android TV device by setting the NTP server to a specified country code
    """
    current_ntp = device.shell('settings get global ntp_server')
    print(f'Current NTP server is {current_ntp}')
    print(f'Setting the NTP server to {code.strip().lower()}.pool.ntp.org...')
    device.shell(f'settings put global ntp_server {code.strip().lower()}.pool.ntp.org')
    print(f'The NTP server has been set to {code.strip().lower()}.pool.ntp.org successfully')
    print('Set Time & Date to automatic on your TV, then it should work :)')
    print('This script was made by Jagar Yousef (Rojava Programmers Forum)')
    print('Click any key to exit...')
    input()
    # open https://www.facebook.com/groups/rpforums
    urllib.request.urlopen('https://www.facebook.com/groups/rpforums')


def set_title(title):
    # get os name
    os_name = os.name
    # if windows
    if os_name == 'nt':
        # Set the new window title
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    # if linux
    elif os_name == 'posix':
        # Set the new window title
        print(f'\33]0;{title}\a', end='', flush=True)
    elif os_name == 'darwin':
        # Set the new window title
        os.system(f'echo -n -e "\033]0;{title}\a"')


if __name__ == '__main__':
    # set window title
    set_title('Android Time & Date Fixer')
    # start working
    print(
        'Make sure to enable ADB debugging on your TV (Settings > Device Preferences > About > Build > Click 7 times on Build Number > Back > Developer Options > ADB Debugging)')
    print('If already done, click any key to continue...')
    input()
    print(
        'Make sure to set your Time & Date to automatic on your TV (Settings > Device Preferences > Date & Time > Use Network Provided Time)')
    print('If already done, click any key to continue...')
    input()
    print('Make sure that your PC and TV are connected to the same network')
    print('If already done, click any key to continue...')
    input()
    gen_keys()
    ip = input('Enter your TV IP (You can find it in Settings > Network & Internet > Your network name): ')
    device = connect(ip)
    code = input('Enter your country code (eg: eg for Egypt, us for USA, etc...): ')
    fix(device, code)
