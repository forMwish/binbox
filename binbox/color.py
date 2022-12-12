HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

if __name__ == "__main__":
    print(HEADER + "TEST:HEADER" + ENDC)
    print(OKBLUE + "TEST:OKBLUE" + ENDC)
    print(OKCYAN + "TEST:OKCYAN" + ENDC)
    print(OKGREEN + "TEST:OKGREEN" + ENDC)
    print(WARNING + "TEST:WARNING" + ENDC)
    print(FAIL + "TEST:FAIL" + ENDC)
    print(BOLD + "TEST:BOLD" + ENDC)
    print(UNDERLINE + "TEST:UNDERLINE" + ENDC)
    pass