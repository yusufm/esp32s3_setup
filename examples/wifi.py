"""
WiFi Connection Example
Connect to WiFi and display network information
"""

import network
import time
import machine

# WiFi configuration
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

def connect_wifi(ssid, password, timeout=10):
    """Connect to WiFi network"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"Connecting to {ssid}...")
        wlan.connect(ssid, password)
        
        # Wait for connection or timeout
        for i in range(timeout * 2):
            if wlan.isconnected():
                break
            time.sleep(0.5)
            print(".", end="")
        print()
    
    if wlan.isconnected():
        print("WiFi connected!")
        print(f"IP address: {wlan.ifconfig()[0]}")
        print(f"Netmask: {wlan.ifconfig()[1]}")
        print(f"Gateway: {wlan.ifconfig()[2]}")
        print(f"DNS: {wlan.ifconfig()[3]}")
        return True
    else:
        print("Failed to connect to WiFi")
        return False

def scan_networks():
    """Scan for available WiFi networks"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    print("Scanning for WiFi networks...")
    networks = wlan.scan()
    
    if networks:
        print(f"Found {len(networks)} networks:")
        for net in networks:
            ssid = net[0].decode('utf-8')
            rssi = net[3]
            print(f"  {ssid}: {rssi} dBm")
    else:
        print("No networks found")

def main():
    """Main WiFi example"""
    print("ESP32-S3 WiFi Example")
    print("=" * 30)
    
    # Scan networks first
    scan_networks()
    print()
    
    # Update these with your WiFi credentials
    ssid = WIFI_SSID
    password = WIFI_PASSWORD
    
    if ssid == "YOUR_WIFI_SSID":
        print("Please update WIFI_SSID and WIFI_PASSWORD in the script")
        return
    
    # Connect to WiFi
    if connect_wifi(ssid, password):
        print("Connection successful!")
        
        # Test network connectivity
        try:
            import urequests
            response = urequests.get("http://httpbin.org/ip")
            print(f"External IP: {response.json()['origin']}")
            response.close()
        except:
            print("Could not test external connectivity")
    else:
        print("Connection failed")

if __name__ == "__main__":
    main()
