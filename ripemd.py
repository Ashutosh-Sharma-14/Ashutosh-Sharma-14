def leftrotate(x, c):
    return (x << c) | (x >> (32-c))

def ripemd128(message):
    # Padding the message
    message = bytearray(message)
    message_len = len(message)
    message.append(0x80)
#     0x80 is the hexadecimal representation of 10000000 - this marks the start of the padding bit
    while (len(message) % 64) != 56:
#         if the length of the block is not a multiple of 64 append padding bits at the end
        message.append(0x00)
    message += message_len.to_bytes(8, byteorder='little')
    
    # Initial hash values - chaining variables
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    
    # Constants
    k = [0x00000000]*16 + [0x5A827999]*16 + [0x6ED9EBA1]*16 + [0x8F1BBCDC]*16 + [0xA953FD4E]*16
#     These constants are pre-defined as 32-bit integers and are unique to the RIPEMD-128 algorithm. 
# They are used in the message expansion step to generate the 80 words needed for each of the 4 rounds.
    r = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         [7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8],
         [3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12],
         [1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2],
         [4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13]]
#     shift specified in each round
    s = [[11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8],
         [7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12],
         [11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5],
         [11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12],
         [9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]]

    # Loop through each 512-bit block of the message
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        
        # Initialize variables for this block
        a = h0
        b = h1
        c = h2
        d = h3
        
        # Main loop
        for j in range(80):
            if j < 16:
                f = (b & c) | ((~b) & d)
                g = j
            elif j < 32:
                f = (d & b) | ((~d) & c)
                g = (5*j + 1) % 16
            elif j < 48:
                f = b ^ c ^ d
                g = (3*j + 5) % 16
            elif j < 64:
                f = c ^ (b | (~d))
                g = (7*j) % 16
            else:
                f = d ^ (b | (~c))
                g = (3*j + 1) % 16
                
            temp = leftrotate(a + f + k[j] + int.from_bytes(block[4*g:4*g+4], byteorder='little'), s[j//16][j%16]) + b
            a, b, c, d = d, temp & 0xFFFFFFFF, b, c
        
        # Update the hash values
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
    
    # Concatenate the hash values and return the final hash
    return (h0.to_bytes(4, byteorder='little') + 
            h1.to_bytes(4, byteorder='little') + 
            h2.to_bytes(4, byteorder='little') + 
            h3.to_bytes(4, byteorder='little'))

message = b'The quick brown fox jumps over the lazy dog'
hashed_message = ripemd128(message)
print(hashed_message.hex())
