# Print the real LAN IPv4 address.
# ASCII only on purpose: PowerShell 5.1 reads .ps1 as ANSI when there is no BOM,
# so any non-ASCII character here would silently break this script.
#
# Skips loopback, APIPA, and virtual adapters (singbox/clash TUN, VM bridges).
# Taking the first line of `ipconfig` would pick the proxy's virtual NIC
# (e.g. 172.18.0.1), which a phone on the same Wi-Fi cannot reach.
$bad = 'tun|tap|singbox|clash|v2ray|VPN|Loopback|vEthernet|VMware|VirtualBox|Hyper-V|Bluetooth'
$all = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object {
    $_.IPAddress -notlike '127.*' -and
    $_.IPAddress -notlike '169.254.*' -and
    $_.InterfaceAlias -notmatch $bad
}
$wifi = $all | Where-Object { $_.InterfaceAlias -match 'WLAN|Wi-Fi|Wireless' } | Select-Object -First 1
if ($wifi) { $wifi.IPAddress }
elseif ($all) { ($all | Select-Object -First 1).IPAddress }
