#!/usr/bin/python
import json, sys, hashlib, gmpy2

def usage():
    print """Usage:
    python recover.py student_id (i.e., qchenxiong3)"""
    sys.exit(1)

#TODO
def recover_msg(N1, N2, N3, C1, C2, C3):

    m = 42
    # your code starts here: to calculate the original message - m
    # Note 'm' should be an integer
    N = N1 * N2 * N3
    #y1 = N / N1
    #y2 = N / N2
    #y3 = N / N3

    s=[1, 0]
    r=[(N / N1), N1]
    i = 2
    temp = (N / N1) % N1
    while (temp > 0):
        temp = r[i-2] % r[i-1]
        r.append(temp)
        s.append(s[i - 2] - (r[i - 2] / r[i - 1]) * s[i - 1])
        i += 1
    z1 = s[i - 2]

    s=[1, 0]
    r=[(N / N2), N2]
    i = 2
    temp = (N / N2) % N2
    while (temp > 0):
        temp = r[i-2] % r[i-1]
        r.append(temp)
        s.append(s[i - 2] - (r[i - 2] / r[i - 1]) * s[i - 1])
        i += 1
    z2=s[i - 2]

    s=[1, 0]
    r=[(N / N3), N3]
    i = 2
    temp = (N / N3) % N3
    while (temp > 0):
        temp = r[i - 2] % r[i - 1]
        r.append(r[i - 2] % r[i - 1])
        s.append(s[i - 2] - (r[i - 2] / r[i - 1]) * s[i - 1])
        i += 1
    z3 = s[i - 2]
    if z1 < 0: z1 += N1
    if z2 < 0: z2 += N2
    if z3 < 0: z3 += N3
    x=(z1 * C1 * (N / N1) + z2 * C2 * (N / N2) + z3 * C3 * (N / N3)) % N 
    gmpy2.set_context(gmpy2.context())
    gmpy2.get_context().precision=1000000
    m = int(gmpy2.cbrt(x))
    # your code ends here
    
    # convert the int to message string
    msg = hex(m).rstrip('L')[2:].decode('hex')
    return msg

def main():
    if len(sys.argv) != 2:
        usage()

    all_keys = None
    with open('keys4student.json', 'r') as f:
        all_keys = json.load(f)

    name = hashlib.sha224(sys.argv[1].strip()).hexdigest()
    if name not in all_keys:
        print sys.argv[1], "not in keylist"
        usage()

    data = all_keys[name]
    N1 = int(data['N0'], 16)
    N2 = int(data['N1'], 16)
    N3 = int(data['N2'], 16)
    C1 = int(data['C0'], 16)
    C2 = int(data['C1'], 16)
    C3 = int(data['C2'], 16)
    
    msg = recover_msg(N1, N2, N3, C1, C2, C3)
    print msg
    
if __name__ == "__main__":
    main()
