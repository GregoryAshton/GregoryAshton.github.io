# Tips for SSH

SSH (Secure Shell) is a tool for accessing remote clusters and servers. This help page covers some general configuration and LIGO-specific tips

## Keys

SSH keys come in pairs: a **private key** (which you keep secret) and a **public key** (which you share with servers).

- **Private key** — Stored on your machine (typically `~/.ssh/id_ed25519`). This proves your identity and should never be shared. Anyone with your private key can impersonate you.
- **Public key** — Shared with servers you want to access. The server stores this in `~/.ssh/authorized_keys`. When you connect, the server uses this to verify you're the legitimate owner of the private key.

### Where Keys Live

By default, SSH keys are stored in the `~/.ssh/` directory:

```
~/.ssh/
├── id_ed25519           # Your private key (keep secret!)
├── id_ed25519.pub       # Your public key (safe to share)
├── config               # SSH configuration file
└── authorized_keys      # Keys allowed to log in on remote servers (file automatically created/edited)
```

**Never commit your private keys to version control or share them**. The `.pub` file is safe to share — you'll add this to servers you want to access.

### Generating a New SSH Key

If you don't have an SSH key yet, you can create one with a command like this:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

When prompted, press Enter to save it in the default location (`~/.ssh/id_ed25519`). You will then be asked to add a passphrase for extra security. Technically, you can hit Enter to have an empty passphrase, but this is not recommended and there are better ways to avoid entering your password multiple times.


## Configuration

SSH configuration is stored in `~/.ssh/config`. This file allows you to define shortcuts for frequently used hosts, avoiding the need to remember long hostnames and usernames.

A basic config looks like:

```
Host myserver
    HostName server.example.com
    User myusername
    IdentityFile ~/.ssh/id_ed25519
```

Then you can simply type `ssh myserver` instead of `ssh myusername@server.example.com -i ~/.ssh/id_ed25519`.
An additional benefit is that `vscode` will also recognise this configuration so you can ssh from there.

### Common SSH Config Options

- **HostName** — The actual hostname or IP address to connect to
- **User** — Default username for this host (if not specified, uses your current username)
- **IdentityFile** — Path to your private SSH key (can specify multiple for fallback)
- **Port** — Non-standard SSH port (default is 22)

**Note**: if you use a standard location for your identity file, e.g. `~/.ssh/id_ed25519`, then you can omit the `IdentityFile` argument as by default `SSH` tries a series of defaults. However, this may be useful if you have multiple keys with custom names.

### Using Wildcards

You can use wildcards to apply settings to multiple hosts:

```
Host *
    IdentityFile ~/.ssh/id_ed25519
```

### Configuring for accessing the LIGO Data Grid

There is help available on [the LIGO computing docs](https://computing.docs.ligo.org/guide/computing-centres/ldg/) for understanding how to access the different clusters. To add to that, here is an SSH config setup to simplify the process of accessing the CIT cluster (you will need to replace `<albert.einstein>` with your username).

```
Host caltechsshproxy
  Hostname sshproxy.ligo.caltech.edu
  User <albert.einstein>
  ControlMaster auto
  ControlPersist 10m
  ControlPath ~/.ssh/sockets/%r@%h:%p
  GSSAPIAuthentication yes
  GSSAPIDelegateCredentials yes

Host *.ligo.caltech.edu caltech
  User <albert.einstein>
  GSSAPIAuthentication yes
  GSSAPIDelegateCredentials yes
  ProxyJump caltechsshproxy

Host ldas-*.ligo.caltech.edu citlogin*.ligo.caltech.edu
  ForwardAgent yes

Host caltech
  Hostname citlogin2.ligo.caltech.edu
```

The first element sets up a **proxy** (or jump host): an intermediate server that relays your connection to a final destination that isn't directly accessible. This is common in cluster environments where login nodes are isolated from the internet for security reasons. Your SSH connection goes: your machine → proxy server → destination cluster. This is required for CIT due to the use of 2FA.

The second element sets default settings for all connections to CIT. Then, the third and fourth elements set up handy tools to simplify picking the node to log in to. Specifically, there is a preferred login node (in this case, `citlogin2`) which can be accessed with
```
ssh caltech
```
But, access to any node is also set up, e.g. you can do
```
ssh citlogin1.ligo.caltech.edu
```
Moreover, if you use <TAB> completion after typing `cit` it will fill in the rest of the address for you and leave you to type the number of the log in node.


## SSH key management

If your ssh key has a password and you login many times a day, you may wish to explore some kind of key management so that your computer can automate this process (effectively your log in to the computer becomes the security element).

### Using a keychain on macOS

macOS provides native SSH key management through the system keychain, which is more secure than storing passphrases in plaintext. Add these lines to the `Host *` section of your SSH config:

```
Host *
    UseKeychain yes
    AddKeysToAgent yes
```

Then, when you first use an SSH key with a passphrase, macOS will:
1. Prompt you to unlock the key
2. Automatically add it to the keychain
3. Remember it for future sessions

This means you'll only need to enter your passphrase once, and subsequent SSH connections will use the key from the keychain without prompting.

### Using SSH Agent on Windows

Windows 10/11 includes OpenSSH with an SSH Agent service, which provides similar functionality to macOS keychain. The SSH Agent securely stores your keys and passphrases in memory.

On Windows, the SSH Agent must be running as a service. To enable it:

```powershell
# Start the SSH Agent (run in PowerShell as Administrator)
Start-Service ssh-agent

# Optional: Set it to start automatically on boot
Set-Service -Name ssh-agent -StartupType Automatic
```

Once the agent is running, add your keys:

```powershell
ssh-add C:\Users\<your-username>\.ssh\id_ed25519
```

You'll be prompted to enter your passphrase (if your key has one). The key will be held in memory by the agent.

Add these lines to your SSH config to use the agent:

```
Host *
    AddKeysToAgent yes
```

With this setting, SSH automatically adds keys to the agent on first use. You only need to enter your passphrase once per session.

To see which keys are currently loaded in the agent:

```powershell
ssh-add -l
```

## Performance tips

### Connection Multiplexing

For cluster work where you make many rapid connections, it may be helpful to use connection multiplexing.

```
Host *
    ControlMaster auto
    ControlPath ~/.ssh/control-%C
    ControlPersist 10m
```

This reuses the same SSH connection for multiple sessions. After the first connection, subsequent ones are nearly instant. The connection stays open for 10 minutes of inactivity.

### Keep Connections Alive

```
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 10
```

This keeps connections alive by sending keepalive packets every 60 seconds, preventing timeouts on idle connections.

### Other Performance Options

- **ConnectTimeout** — Set timeout for initial connection attempts (in seconds). This may be useful for flaky networks:
  ```
  ConnectTimeout 10
  ```

- **CompressionLevel** — Compresses data to save bandwidth at the cost of CPU. This trades CPU usage for reduced data transfer. On fast local networks, the compression overhead often slows things down. On slow networks (internet, WAN), it usually helps by reducing latency.
  ```
  Compression yes
  ```
  Most useful for interactive sessions over slow connections where reduced latency matters.


## Troubleshooting

If you encounter connection issues:
- Check permissions: `chmod 600 ~/.ssh/id_ed25519` and `chmod 700 ~/.ssh/`
- Test verbosely: `ssh -vvv hostname` to see detailed connection attempts
- Verify the server accepts your key: Check `authorized_keys` on the remote server
