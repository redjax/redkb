# Setup

## Server setup

`...`

## Client setup

- Download & install Wireguard
  - Debian/Ubuntu: `sudo apt install -y wireguard wireguard-tools`
  - Fedora: `sudo dnf install -y wireguard wireguard-tools`
- Create `/etc/wireguard/wg0.conf`
  - You can use any filename i.e. `my-connection-name.conf`, wg0.conf` is just the default.
  - Example `wg0.conf`:

    ```conf
    [Interface]
    PrivateKey = YOUR_PRIVATE_KEY
    Address = 10.0.0.2/24
    DNS = 1.1.1.1

    [Peer]
    PublicKey = SERVER_PUBLIC_KEY
    Endpoint = your.server.ip:51820
    ## 0.0.0.0/0 for all IPs, or limit with
    #  AllowedIPs = 10.xxx.xxx.xxx/32 192.168.1.0/24
    AllowedIPs = 0.0.0.0/0
    PersistentKeepalive = 25
    ```

  - Secure the config with `sudo chmod 600 /etc/wireguard/wg0.conf`
- Bring up the interface with `sudo wg-quick up wg0`
  - If you named the file something other than `wg0.conf`, use the name of the file without `.conf`
    - i.e. `/etc/wireguard/my-connection-name.conf` -> `sudo wg-quick up my-connection-name`
  - Bring the connection down with `sudo wg-quick down wg0`
- You can also control the connection with `sudo systemctl [start|stop|enable|disable] wg-quick@wg0`
  - If you used a different filename, use `wg-quick@my-connnection-name`
- Ensure port forwarding is enabled:
  - `echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf`

