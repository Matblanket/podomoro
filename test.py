pi = "00:10"
if len(pi) != 5:
    if pi.find(':') < 2:
        while pi.find(':') != 2:
            pi = '0'+pi
    while len(pi) != 5:
        pi = pi+'0'
print(pi)
