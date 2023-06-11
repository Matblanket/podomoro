import os, misc, curses, random 
logo = [
    '''                                                                 
  _____  _____  _____   _____  ____    __  _____  _____   _____  
 |     |/     \|     \ /     \|    \  /  |/     \|     | /     \ 
 |    _||     ||      \|     ||     \/   ||     ||     \ |     | 
 |___|  \_____/|______/\_____/|__/\__/|__|\_____/|__|\__\\_____/ 
                                                                 
                                                                 ''',
    '''                    .___                                        
______    ____    __| _/ ____    _____    ____ _______   ____   
\____ \  /  _ \  / __ | /  _ \  /     \  /  _ \\_  __ \ /  _ \  
|  |_> >(  <_> )/ /_/ |(  <_> )|  Y Y  \(  <_> )|  | \/(  <_> ) 
|   __/  \____/ \____ | \____/ |__|_|  / \____/ |__|    \____/  
|__|                 \/              \/                         
                                                                ''',
    '''                                        
                                        
              .                         
              |                         
.,-.  .-.  .-.| .-. .--.--. .-. .--..-. 
|   )(   )(   |(   )|  |  |(   )|  (   )
|`-'  `-'  `-'`-`-' '  '  `-`-' '   `-' 
|                                       
'                                       ''',
           '''   _ __              _                                           
  | '_ \   ___    __| |    ___    _ __     ___      _ _    ___   
  | .__/  / _ \  / _` |   / _ \  | '  \   / _ \    | '_|  / _ \  
  |_|__   \___/  \__,_|   \___/  |_|_|_|  \___/   _|_|_   \___/  
_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' ''',

 '''                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  ''',
        ]


def decimalToBinary(n):
    return bin(n).replace("0b", "")


def ttywidth():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(columns)


def ttyheight():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows)


def getjob(y=0, x=0, t="%", ref=True,rand=False):
        return {
            "x": x,
            "y": y,
            "t": t,
            "ref": ref,
            "color": "rand" if rand else "norm"
        }

def block(y, x, joblist, rand=False, clear=False ):
    if clear:
        joblist.put(misc.getjob(y + 0, x, " " * 3))
        joblist.put(misc.getjob(y + 1, x, " " * 3))
    else:
        if rand:
            joblist.put(misc.getjob(y + 0, x, chr(9608) * 3,rand=True))
            joblist.put(misc.getjob(y + 1, x, chr(9608) * 3,rand=True))
        else:
            joblist.put(misc.getjob(y + 0, x, chr(9608) * 3))
            joblist.put(misc.getjob(y + 1, x, chr(9608) * 3))

