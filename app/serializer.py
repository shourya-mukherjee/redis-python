class Serializer:
    def __init__(self):
        pass
    
    def decode(self, s): # bytecode string to array
        d_arr = []
        while s:
            newline = s.index(b'\r\n')
            decoded = s[:newline].decode()
            s = s[newline+2:]
            if decoded[0] == '*' or decoded[0] == '$':
                continue
            d_arr.append(decoded)
        return d_arr
    
    def encode(self, arr): # array to bytecode string
        if len(arr) == 1:
            return b'+' + arr[0].encode('utf-8') + b'\r\n'
        else:
            n = str(len(arr)).encode('utf-8')
            ret = b'*' + n + b'\r\n'
            for s in arr:
                ret += b'$' + str(len(s)).encode('utf-8') + b'\r\n'
                ret += s.encode('utf-8') + b'\r\n'
            return ret