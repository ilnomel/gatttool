import pygatt

adapter = pygatt.GATTToolBackend()

def handle_data(handle,value):
    print("received data:", value)


try:
    adapter.start()
    device = adapter.connect('A0:E6:F8:BF:AF:00')
    #value = device.char_read_handle("0x001e")
    #print(value)
    
    device.subscribe("2902", callback=handle_data)
finally:
    adapter.stop()
