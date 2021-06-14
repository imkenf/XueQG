from colorama import init, Fore, Back, Style
colorama.init(autoreset=True)
#colorama.init(wrap=True)

def red(mystr):
    return Fore.LIGHTRED_EX + mystr + Fore.RESET

def yellow(mystr):
    return Fore.YELLOW + mystr + Fore.RESET

def blue(mystr):
    return Fore.LIGHTBLUE_EX + mystr + Fore.RESET

def green(mystr):
    return Fore.GREEN + mystr + Fore.RESET

def magenta(mystr):
    return Fore.MAGENTA + mystr + Fore.RESET
    
def cyan(mystr):
    return Fore.CYAN + mystr + Fore.RESET
    
def white(mystr):
    return Fore.WHITE + mystr + Fore.RESET
