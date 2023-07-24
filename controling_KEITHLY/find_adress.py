import Gpib
# X is your interface number (usually 0)
# Y is your instrument address (should be configured on the device)
for i in range(30):
    inst = Gpib.Gpib(0,i) 
    try:
        inst.write("*IDN?")
        print("address",i,"is",inst.read(100))
    except:
        pass
