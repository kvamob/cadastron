address = 'global_addr'


def get_info():
    global address
    address = 'local_addr'


print(address)
get_info()
print(address)
