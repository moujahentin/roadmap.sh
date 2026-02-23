SSH Remote Server Setup (Personal Example)

Project URL: https://roadmap.sh/projects/ssh-remote-server-setup

This project demonstrates how I set up a remote Linux server and configured SSH access using multiple SSH keys. The goal is to be able to connect to the server using different SSH key pairs and convenient SSH aliases.

Server: Armbian (Debian-based) running on RK322x TV box
Access: SSH over LAN and via Tailscale (for remote access)
User: moujahentin

Server Setup

I provisioned a Linux server running Armbian on an RK322x TV box.
The server is reachable over the local network and remotely via Tailscale.

SSH Key Generation

On my local machine (Windows), I generated two SSH key pairs:

ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_key1
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_key2

This created:

~/.ssh/id_ed25519_key1 and ~/.ssh/id_ed25519_key1.pub

~/.ssh/id_ed25519_key2 and ~/.ssh/id_ed25519_key2.pub

Adding SSH Keys to the Server

I added both public keys to the server user’s authorized_keys:

cat ~/.ssh/id_ed25519_key1.pub | ssh moujahentin@rk322x-box "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
cat ~/.ssh/id_ed25519_key2.pub | ssh moujahentin@rk322x-box "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

On the server, the keys exist in:

~/.ssh/authorized_keys

Connecting Using Both SSH Keys

I verified that I can connect using both keys:

ssh -i ~/.ssh/id_ed25519_key1 moujahentin@rk322x-box
ssh -i ~/.ssh/id_ed25519_key2 moujahentin@rk322x-box

Both connections authenticate successfully.

SSH Config Aliases

To simplify access, I configured SSH aliases in ~/.ssh/config:

Host armbianbox-key1
HostName rk322x-box
User moujahentin
IdentityFile ~/.ssh/id_ed25519_key1

Host armbianbox-key2
HostName rk322x-box
User moujahentin
IdentityFile ~/.ssh/id_ed25519_key2

Host armbianbox
HostName rk322x-box
User moujahentin
IdentityFile ~/.ssh/id_ed25519_key1

Now I can connect with:

ssh armbianbox-key1
ssh armbianbox-key2
ssh armbianbox

SSH Hardening

I hardened SSH by disabling root login and password authentication in /etc/ssh/sshd_config:

PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes

Then restarted SSH:

sudo systemctl restart ssh

Firewall (UFW)

I enabled UFW and allowed only SSH:

sudo apt update
sudo apt install -y ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status verbose

Stretch Goal: Fail2Ban

I installed and enabled Fail2Ban to protect against brute-force SSH attempts:

sudo apt install -y fail2ban
sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd

Verification

whoami
sudo whoami
sudo ufw status
ss -tulpn | grep ssh
sudo fail2ban-client status sshd

All checks confirm that:

I am using a non-root user with sudo

SSH is running and secured

Firewall allows only SSH

Fail2Ban is active for SSH

Security Notes

Private SSH keys were never committed to any public repository.

Only public keys were added to the server.

SSH password authentication is disabled.

Outcome

At the end of this project, the server is accessible via SSH using two different SSH key pairs, and convenient SSH aliases are configured for easy access. Basic hardening (UFW and Fail2Ban) is in place to reduce the attack surface.
