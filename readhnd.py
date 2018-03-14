import pexpect
import math
import sys
import time

# Get address from command parameter
if len(sys.argv) != 2:
    print("Error! Must specify bluetooth address as parameter")
    sys.exit(1)
bt = sys.argv[1]

# Run gatttool interactively
print("Run gatttool...")
gatt = pexpect.spawn('gatttool -I')

# Connect to device
print("Connecting to...", bt)
gatt.sendline("connect {0}".format(bt))
gatt.expect("Connection successful", timeout =5)
print(" Connected!")

# Read characteristic
gatt.sendline("char-read-hnd 0x001e")
gatt.expect("Characteristic value/descriptor:", timeout = 10)
gatt.expect("\r\n", timeout=10)

# Write characteristic
#gatt.sendline("char-write-cmd 0024 00")
#gatt.expect("Characteristic value was written successfully")
#gatt.expect("\r\n", timeout = 10)
#gatt.expect("Notification handle = 0x001e value:", timeout =10)
print(gatt.before)
