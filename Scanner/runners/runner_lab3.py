from Scanner.Scanner import Scanner

if __name__ == '__main__':
    scanner = Scanner()

    try:
        st, pif, message = scanner.scan_by_line("/Users/ioana/OneDrive/Desktop/FLCD-Laboratory-Work/Scanner"
                                                "/inputFiles/p2.txt")
        print("st: ", st)
        print("pif: ", pif)
        print(message)
    except ValueError as ve:
        print(ve)