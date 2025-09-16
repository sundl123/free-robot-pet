import platform
import struct

# Using platform module
architecture = platform.machine()
print("CPU Architecture (platform module):", architecture)

print(f'system: {platform.system()}, processor: {platform.processor()}, uname: {platform.uname()}')

# Using os and struct modules
bit_architecture = "64-bit" if struct.calcsize("P") * 8 == 64 else "32-bit"
print("CPU Architecture (os and struct modules):", bit_architecture)
