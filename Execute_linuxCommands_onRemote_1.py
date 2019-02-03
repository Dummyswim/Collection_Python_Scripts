from sys import argv

from paramiko.client import AutoAddPolicy
from paramiko.client import SSHClient
from paramiko.ssh_exception import SSHException


def apply_commands(host, commands):
    with SSHClient() as client:
        client.set_missing_host_key_policy(AutoAddPolicy)
        client.load_system_host_keys()

        print("[%s]> Connecting as root on port 22..." % host)
        client.connect(host, 22, 'root')


        for command in commands:
            print("[%s]> Executing %s..." % (host, command.strip()))

            stdin, stdout, stderr = client.exec_command(command)

            print(stdout.read().decode('utf-8'))
            print(stderr.read().decode('utf-8'))

    print("[%s]> Done" % host)


if __name__ == '__main__':
    if len(argv) < 2:
        print("Invalid args!")
        print("Usage: python3 run.py <private ssh key filepath>")
        exit()

    with open('cmds.txt') as f:
        commands = f.readlines()

    with open('hosts.txt') as f:
        hosts = f.readlines()

    for host in hosts:
        for customer_index in range(1, 3):
            host = host.strip()
            #host = "disc%s.%s" % (customer_index, host)

            if host.startswith('--'):
                print("Host %s began with --, skipping" % host)
                continue

            try:
                apply_commands(host, commands)
            except KeyboardInterrupt:
                break
            except SSHException as err:
                print("[%s]> SSH Error: %s" % (host, err))
                continue