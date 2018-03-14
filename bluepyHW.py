#!/usr/bin/python3

from bluepy.btle import Scanner, DefaultDelegate, Peripheral, UUID
import time
import binascii

out_data = bytearray()
end_packet= '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'.encode()
stoptime = time.time()
starttime = time.time()
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

    def handleNotification(self, cHandle, data):
        dataAscii = binascii.hexlify(data)
        print('Notification! from handle: ' + str(cHandle) + " data :" + dataAscii.decode('UTF-8'))
#        print(dataAscii.decode('UTF-8')[:8])
#        print(data)
#        print(data[:4])

        if data != end_packet:
            out_data.extend(data)

        if end_packet in data:
            raw_data = binascii.hexlify(out_data)
            stoptime = time.time()
            print('elapsed time: ' + str(stoptime-starttime))
            print('end_packet detected!')
            print(raw_data)

            # Write raw data to file. Includes the header
            fo_raw = open("RawData.dat", "wb")
            fo_raw.write(out_data)
            fo_raw.close()

            # Header file: Device UUID, Date Time, and Payload Length
            fo_uuid = open("devUUID_DateTime.txt", "w")
            fo_uuid.write("Device UUID: %s \nDate Time: %s \nPayload Length: %s \n" % (raw_data.decode('UTF-8')[:8], raw_data.decode('UTF-8')[8:16], raw_data.decode('UTF-8')[16:24]))
            fo_uuid.close()

            # Actual payload file
            fo_payload = open("Report.txt", "w")
            fo_payload.write("%s\n" % raw_data.decode('UTF-8')[40:])
            fo_payload.close()

            exit(0)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(3.0)


addr = ""

for dev in devices:
    # Print out all the detected BLE
    #print("Device %s (%s), RSSI=%d dB" %(dev.addr, dev.addrType, dev.rssi))
    for (adtype, desc, value) in dev.getScanData():
        if value == 'SensorSys Tx':
            print('SensorSys located with Addr ' + dev.addr)
            addr = dev.addr
        print("  %s = %s" %(desc, value))

print(addr)

#temp_UUID = UUID("2902")

p = Peripheral(addr)
p.setDelegate(ScanDelegate())

print("connected")
sub_ch = 0
try:
    chars = p.getCharacteristics(startHnd=0x01, endHnd=0x24)
    for ch in chars:
        if(ch.supportsRead()):
            # Subscribe to notifications if ch.properties contains NOTIFY
            if 'NOTIFY' in ch.propertiesToString():
                # Subscribe here
                data = ch.read()
                sub_ch = ch
                p.writeCharacteristic(ch.valHandle + 1, bytes('\x02\x00'.encode('UTF-8')))
                print('now subscribed')
    p.writeCharacteristic(0x0024, bytes('\x01'.encode('UTF-8')))
    if sub_ch != 0:
        starttime = time.time()
        while 1:
            if(p.waitForNotifications(2.0)):
                continue
            print('nothing heard')
            time.sleep(1)
finally:
    p.disconnect()




