import paramiko

def ssh_command(hostname, username, password, command):
    print("ssh_command called")
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

        return output, error

    except paramiko.AuthenticationException:
        return None, "Authentication failed. Please check your credentials."
    finally:
        # Close the SSH session
        ssh.close()

def main(prompt):

    # Server details
    hostname = "gpu-stats-2021.iac.gatech.edu"
    username = "lzhang793"
    password = "Vanessa0729"

    # Commands to execute
    commands = [
        "conda bash",
        "cd ~/stable-diffusion",
        "conda activate ldm",
        f"python scripts/txt2img.py --prompt '{prompt}'"
    ]

    # Execute commands one by one
    output = ""
    error = ""
    for cmd in commands:
        command_output, command_error = ssh_command(hostname, username, password, cmd)
        output += command_output
        error += command_error

    return output, error

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
