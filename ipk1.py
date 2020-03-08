#!/usr/bin/env python3

############################################
# @author:  Pavol Gumancik                 #
#           xguman01                       #
#           <xguman01@stud.fit.vutbr.cz>   #
############################################

import sys #na kontrolu argumentov
import socket

##########################################
#poslanie validnych dat klientovi - opGet
def Dsend (data, type, s, conn, err):
    if err < 400:
        #kontrola existencie url
        try:
            ip = socket.gethostbyname(data)
        except socket.error:
            conn.sendall(b'HTTP/1.0 404 Not Found\r\n\r\n')
            return
        if type == 'A':
            Sdata = ('HTTP/1.0 200 OK\r\n\r\n%s:%s=%s\n'% (data, type, socket.gethostbyname(data)))
        elif type == 'PTR':
            Sdata = ('HTTP/1.0 200 OK\r\n\r\n%s:%s=%s\n'% (data, type, socket.gethostbyaddr(data)))
        Bdata = Sdata.encode() #string -> bytes
        conn.send((Bdata))

##########################################
#spracovanie operacie GET
def opGet(Sdata,s,conn):
    Sdata = Sdata.split("HTTP/1.1")[0] + "HTTP/1.1"     #odstranenie koncoveho stringu
    if Sdata.startswith( 'GET' ):                       #kontrola prefixu a nasledne odstranenie
        Sdata = Sdata.replace("GET/resolve?name=","", 1)
    else:
        conn.sendall(b'HTTP/1.0 400 Bad Request\r\n\r\n')
        return

    if Sdata.endswith('HTTP/1.1'):                      #kontrola postfixu a nasledne odstranenie
        Sdata = Sdata.replace("HTTP/1.1","", 1)
    else:
        conn.sendall(b'HTTP/1.0 400 Bad Request\r\n\r\n')
        return

    if Sdata.endswith('&type=A'):                       #kontrola postfixu a vyhodnotenie validity
        Sdata = Sdata.replace("&type=A","", 1)
        Dsend (Sdata, 'A', s, conn, 0)                  #posielanie dat clientovi
    elif Sdata.endswith('&type=PTR'):
        Sdata = Sdata.replace("&type=PTR","", 1)
        Dsend (Sdata, 'PTR', s, conn, 0)                #posielanie dat clientovi
    else:
        conn.sendall(b'HTTP/1.0 400 Bad Request\r\n\r\n')
        return

##########################################
#spracovanie operacie POST
def opPost(Sdata, s, conn):
    Sdata = Sdata.replace("\n", " ")
    Sdata = Sdata.replace("\r", " ")

    if Sdata.startswith('POST/dns-queryHTTP/1.1'):
        pass
    else:
        conn.sendall(b'HTTP/1.0 400 Bad Request\r\n\r\n')
        return

    arr = Sdata.split(' ')                  # ulozenie vstupu do pola
    arrLen = len(arr)

    counter = 0
    header = False                          #ukazatel na error~False (ziaden validny vysledok)

    while counter < arrLen:                 #prechadzanie polom a jeho vyhodnocovanie
        line = arr[counter].replace(" ", "")
        if line.endswith(':A'):             #A type
            counter = counter + 1
            line = line.replace(":A", "")
            try:                            #kontrola existencie ip
                ip = socket.gethostbyname(line)
            except socket.error:
                continue
            if header == False:             #kontrola hlavicky
                conn.sendall(b'')
                conn.sendall(b'HTTP/1.0 200 OK\r\n\r\n')
            Sdata = ('%s:A=%s\r\n'%(line,ip))
            Sdata = Sdata.encode()          #string  -> byte
            conn.sendall((Sdata))
            header = True

        elif line.endswith(':PTR'):         #PTR type
            counter = counter + 1
            line = line.replace(":PTR", "")
            try:                            #kontrola existencie ip
                ip = socket.gethostbyaddr(line)
            except socket.error:
                continue
            if header == False:             # kontrola hlavicky
                conn.sendall(b'')
                conn.sendall(b'HTTP/1.0 200 OK\r\n\r\n')
            Sdata = ('%s:PTR=%s\r\n'%(line,ip[0]))
            Sdata = Sdata.encode()          #string  -> byte
            conn.sendall((Sdata))
            header = True

        else:
            counter = counter + 1

    if header == False:                     #nevalidny vstup, error
        conn.sendall(b'HTTP/1.0 400 Bad Request\r\n\r\n')
        return

##########################################
#nacitavanie dat od klienta a vyhodnotenie prikazov
def DTload(s):
    s.listen()
    conn, addr = s.accept()
    with conn:
        while True:                     #pokial beriem data od clienta
            Bdata = conn.recv(1024)

            if not Bdata:
                break

            Sdata = Bdata.decode("utf-8") #prevedenie bitoveho vstupu na string
            Sdata = Sdata.replace(" ", "")

            if Sdata.startswith( 'GET' ):
                opGet(Sdata,s,conn)
                break

            elif Sdata.startswith( 'POST/' ):
                opPost(Sdata,s,conn)
                break
            else: #neznamy prikaz
                conn.sendall(b'HTTP/1.0 405 Method Not Allowed\r\n\r\n')
                break

##########################################
def main():
    if len(sys.argv) != 2:              #validny pocet argumentov
        print("Wrong number of arguments\r\n\r\n.", file=sys.stderr)
        exit(1)

    if sys.argv[1].isnumeric():         #validny port - short int
        range = int(sys.argv[1])        #funguje iba na prirodzene cisla
        if range > 65535 or range == 0:
            print("Incorect format of PORT - out of range.\r\n\r\n", file=sys.stderr)
            exit(1)

    else:
        print("Incorect format of PORT - invalid characters.\r\n\r\n", file=sys.stderr)
        exit(1)

    HOST = '127.0.0.1'
    PORT = range

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        while True:
            DTload(s)

##########################################
main()
