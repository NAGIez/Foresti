import time
from colorama import Fore

def trm_star(call, callans):
    print(Fore.YELLOW)
    print("\n---------Foresti_TRM---------")
    print(time.ctime(int(time.time())), "\nUSER: @{0}\
                                         \nИмя: {1}\
                                         \nФамилия: {2}\
                                         \nID: {3}\n\
                                         \nПоставил звезд:".format(call.from_user.username, call.from_user.first_name,
                                                                   call.from_user.last_name,
                                                                   str(call.from_user.id)))
    print(callans)
    print("-----------------------------")
    print(Fore.WHITE)

def trm_txt_call(call, ansfunc):
    print(Fore.CYAN)
    print("\n---------Foresti_TRM---------")
    print(time.ctime(int(time.time())), "\nUSER: @{0}\
                                         \nИмя: {1}\
                                         \nФамилия: {2}\
                                         \nID: {3}\n".format(call.from_user.username, call.from_user.first_name,
                                                                   call.from_user.last_name,
                                                                   str(call.from_user.id)))
    print("->", ansfunc)
    print("-----------------------------")
    print(Fore.WHITE)

def trm_txt(message, answer):
    print("\n---------Foresti_TRM---------")
    print(time.ctime(int(time.time())), "\nUSER: @{0}\
                                         \nИмя: {1}\
                                         \nФамилия: {2}\
                                         \nID: {3}\n\
                                         \nMSG: {4}".format(message.from_user.username,
                                                                   message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id),
                                                                   message.text))
    print("->", answer, "<-")
    print("-----------------------------")

def trm_launch():
    print("""
███████╗████████╗     ██████╗███╗   ███╗██████╗     ██╗      █████╗ ██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗
██╔════╝╚══██╔══╝    ██╔════╝████╗ ████║██╔══██╗    ██║     ██╔══██╗██║   ██║████╗  ██║██╔════╝██║  ██║
█████╗     ██║       ██║     ██╔████╔██║██║  ██║    ██║     ███████║██║   ██║██╔██╗ ██║██║     ███████║
██╔══╝     ██║       ██║     ██║╚██╔╝██║██║  ██║    ██║     ██╔══██║██║   ██║██║╚██╗██║██║     ██╔══██║
██║        ██║       ╚██████╗██║ ╚═╝ ██║██████╔╝    ███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╗██║  ██║
╚═╝        ╚═╝        ╚═════╝╚═╝     ╚═╝╚═════╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝
    """)
