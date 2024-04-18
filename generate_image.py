import warnings
from cryptography.utils import CryptographyDeprecationWarning
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=CryptographyDeprecationWarning)
    import paramiko
import os
import stat
def ssh_command(hostname, username, password, command):
    # Create an SSH client instance
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the server
        ssh.connect(hostname, username=username, password=password)

        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)

        # Read and return the output
        output = stdout.read().decode()
        error = stderr.read().decode()

        return output, error, ssh

    except paramiko.AuthenticationException:
        return None, "Authentication failed. Please check your credentials.", None
    except Exception as e:
        return None, str(e), None


def sftp_transfer(ssh, remote_path, local_path):
    try:
        # Create a transport object based on the existing SSH connection
        transport = ssh.get_transport()

        # Create an SFTP client instance
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Recursive function to transfer directories and files
        def _transfer_files(remote_dir, local_dir):
            items = sftp.listdir_attr(remote_dir)
            # Sort the items by their modification time (mtime)
            items.sort(key=lambda item: item.st_mtime)
            # Only keep the last 4 items
            items = items[-5:]
            for item in items:
                remote_item = os.path.join(remote_dir, item.filename)
                local_item = os.path.join(local_dir, item.filename)

                if stat.S_ISDIR(item.st_mode):
                    os.makedirs(local_item, exist_ok=True)
                    _transfer_files(remote_item, local_item)
                else:
                    sftp.get(remote_item, local_item)
        # Call the recursive function to transfer files
        _transfer_files(remote_path, local_path)

        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        # Close the SFTP connection
        if 'sftp' in locals():
            sftp.close()
        if 'transport' in locals():
            transport.close()

def main(prompt):
    # Server details
    hostname = os.getenv('GT_DOMAIN')  # Get the hostname from environment variable
    username = os.getenv('GT_USERNAME')  # Get the username from environment variable
    password = os.getenv('GT_PASSWORD')  # Get the password from environment variable

    # Concatenate commands into a single string
    command = (
        f"source ~/anaconda3/etc/profile.dc/conda.sh;"
        f"conda init bash;  "
        f"cd ~/stable-diffusion; "
        f"conda activate ldm; "
        f"python scripts/txt2img.py --prompt '{prompt}';"
    )

    # f"python scripts/txt2img.py --W 256 --H 256 --prompt '{prompt}';"
    # Execute the concatenated command
    output, error, ssh = ssh_command(hostname, username, password, command)

    if error:
        print("Error:", error)
        # TODO: global seed is 42, change to random seed
        # TODO: 'Error: Global seed set to 42', not an error, it's a warning
        #return output, error

    # Now, perform SFTP transfer
    remote_path = "/home/lzhang793/stable-diffusion/outputs/txt2img-samples/"
    local_path = os.path.expanduser("~/ChatGPT-Installation/app/static/generated/")

    success, sftp_error = sftp_transfer(ssh, remote_path, local_path)

    # Close the SSH connection
    ssh.close()

    if success:
        return output, None
    else:
        return output, sftp_error


if __name__ == "__main__":
    print("generate_image.py called")
    import sys

    if len(sys.argv) != 2:
        print("Usage: python generate_image.py <prompt>")
        sys.exit(1)

    prompt = sys.argv[1]
    output, error = main(prompt)

    if output:
        print("Output:", output)
    if error:
        print("Error:", error)
