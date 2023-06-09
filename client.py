import socket
import time

s = socket.socket()
host = "54.224.145.170"#ip public
port = 2929


matrix=[[" " for i in range(3)] for j in range(3)]

def print_matrix(cord):
    i,j=cord[0],cord[1]
    
    if(cord[2]==1):
        matrix[i][j]="X"
    else:
        matrix[i][j]="O"



    print(f""" --- --- --- 
| {matrix[0][0]} | {matrix[0][1]} | {matrix[0][2]} |
 --- --- --- 
| {matrix[1][0]} | {matrix[1][1]} | {matrix[1][2]} |
 --- --- --- 
| {matrix[2][0]} | {matrix[2][1]} | {matrix[2][2]} |
 --- --- --- """)

def start_player():
    try:
        s.connect((host, port))
        print("Connected to :", host, ":", port)
        start_game()
        s.close()
    except socket.error as e:
        print("Socket connection error:", e) 

def start_game():
    welcome = s.recv(2048 * 10)
    print(welcome.decode())

    name = input("Enter Player name:")
    s.send(name.encode())

    while True:
        try: 
            recvData = s.recv(2048 * 10)
            recvDataDecode = recvData.decode()

            if recvDataDecode == "Input" or recvDataDecode=="already entered Error" or recvDataDecode=="out of bound input Error":
                failed = 1
                while failed:
                    try:
                        x = int(input("Enter the x coordinate:"))
                        y = int(input("Enter the y coordinate:"))
                        coordinates = str(x)+"," + str(y)
                        s.send(coordinates.encode())
                        failed = 0
                    except:
                        print("Error occured....Try again")
                

            elif recvDataDecode == "Error":
                print("Error occured! Try again..")
            
            elif  recvDataDecode == "Board":
                print(recvDataDecode)
                cordRecv = s.recv(2048 * 100)
                cordRecvDecoded = cordRecv.decode("utf-8")
                print_matrix(eval(cordRecvDecoded))

            elif recvDataDecode == "":
                time.sleep(10)
                break

            else:
                print(recvDataDecode)
        except KeyboardInterrupt:
            print("\nKeyboard Interrupt")
            time.sleep(1)
            break

start_player()