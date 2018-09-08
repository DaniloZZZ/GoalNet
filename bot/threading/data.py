
global List
def init():
    global List
    List = [1,3]
def add_num(num):
    print("adding ",num)
    global List
    List.append(num)

def out():
    global List
    print(List)

