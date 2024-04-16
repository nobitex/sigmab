# to create the hex address from the output of eth_addr circuit
# https://github.com/0xPARC/circom-ecdsa/blob/master/circuits/eth_addr.circom
def get_address_hex(number):
    big_endian_bytes = number.to_bytes((number.bit_length() + 7) // 8, 'little')
    hex_string = big_endian_bytes.hex()
    standard1_address = '0x' + hex_string
    return standard1_address