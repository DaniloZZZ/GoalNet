from Types import *
from Actors import *

def main():
    N = Notif()
    R = Record({'hello':12})
    Lg = Link({'ref':919},Goal)
    Lh = Link({'ref':191},Goal_Notif)
    notif = N.apply([R,Lg,Lh])
    print(notif)
    if isinstance(notif,Notification):
        print("OK well done")
        print(notif.data)

if __name__=="__main__":
    main()
