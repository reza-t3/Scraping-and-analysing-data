#######################server############################
import socket
import json
import re


class Table:
    def __init__(self, table_name, col_lenth, row_length):
        self.table = [['None' for _ in range(col_lenth)] for _ in range(row_length)]
        table_dict[table_name] = self
    def set_in_table(self, column, row, value):
        try:
            self.table[row][column] = int(value)
        except:
            self.table[row][column] = value

def context(table_name):
    global current_table
    current_table = table_dict[table_name] 

def PrintEror():
    print('Error')
    quit()
#_________________________________________________________________________
def white_space(inp):
    while True:
        m0 = re.search(r'\s+[=*/+-]', inp)
        if not m0:
            break
        a = m0.span()[1]
        inp = re.sub(r'\s+[=*/+-]', inp[a-1], inp, 1)
    while True:
        m1 = re.search(r'[=*/+-]\s+', inp)
        if not m1:
            break
        b = m1.span()[0]
        inp = re.sub(r'[=*/+-]\s+', inp[b], inp, 1)
    return inp


def num_to_let(inp):
    inp = int(inp)
    remainder_list = []
    i = 0
    while True:
        i += 1
        q = inp // 26
        r = inp % 26
        inp = q - 1
        remainder_list.append(r) 
        if q == 0:
            break
    index_list = []
    for i in range(len(remainder_list)-1,-1,-1):
        index_list.append(remainder_list[i])
    mystring = ''
    for i in range(len(index_list)):
        mystring += chr(index_list[i]+65)
    return mystring    

def let_to_num(inp):
    inp_list = list(inp)
    if len(inp_list) == 1:
        return ord(inp_list[0])-65
    else:
        ans = 0
        for i in range(len(inp_list)):
            if i == len(inp_list) - 1:
                ans *= 26
                ans += ord(inp_list[i])-65
            else:
                ans *= 26
                ans += ord(inp_list[i])-64
        return ans


def find_index(inp):
    pattern1 = re.search(r'([A-Z]+)([0-9]+)', inp)
    letter = pattern1.group(1)
    number = pattern1.group(2)
    col_num = let_to_num(letter)
    row_num = int(number)
    return col_num, row_num
#_________________________________________________________________________
def create_func(inp):
    create_pattern = re.search(r'create\((\w+),(\d+),(\d+)\)', inp)
    table_name = create_pattern.group(1)
    col_length = create_pattern.group(2)
    row_length = create_pattern.group(3)
    Table(table_name, int(col_length), int(row_length))
    return
def context_func(inp):
    context_pattern = re.search(r'context\((\w+)+\)', inp)
    try:
        context(context_pattern.group(1))
        return
    except:
        PrintEror()
def table_func(inp):
    table_pattern = re.search(r'(^[A-Z]\w+)=(.+)', inp)
    left1 = table_pattern.group(1)
    right1 = table_pattern.group(2)
    col, row = find_index(left1)
    try:
        table_pattern2 = re.search(r'(^[A-Z]\w+)=\'(.*)\'', inp)
        if table_pattern2:
            right2 = table_pattern2.group(2)
            current_table.set_in_table(col, row-1, right2)
        else:
            current_table.set_in_table(col, row-1, right1)
    except:
        PrintEror()
    return


#_________________________________________________________________________

def read(inp):
    inp = white_space(inp)
    create_pattern = re.search(r'create\((\w+),(\d+),(\d+)\)', inp)
    if create_pattern:
        create_func(inp)
        return
    context_pattern = re.search(r'context\((\w+)+\)', inp)
    if context_pattern:
        context_func(inp)
        return
    table_pattern = re.search(r'(^[A-Z]\w+)=(.+)', inp)
    if table_pattern:
        table_func(inp)
        return

table_dict = dict()
current_table : Table = None





class Server:
    def __init__(self, port_num: int = 5050, max_req_size: int = 10):


        self.port = port_num
        self.max_req_size = max_req_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def runServer(self) -> None:
        self.sock.bind(('localhost', self.port))
        self.sock.listen()
        print(f"listening on port {self.port}")
        sock_obj, address_info = self.sock.accept()
        print(f"connected to a client: IP: {address_info}")
        self.talk(sock_obj)

    def talk(self, sock_obj: socket.socket):
        while True:
            new_req = self.__getReq(sock_obj)
            if new_req["req_type"] == "command":
                response = self.handleCommand(new_req["command_str"])
                self.__sendRes(sock_obj, response)
            elif new_req["req_type"] == "get_results":
                for listt in current_table.table:
                    self.__sendRes(sock_obj, listt)
                self.__sendRes(sock_obj, "end")
                break
        sock_obj.close()

    def handleCommand(self, command: str) -> dict:
        read(command)
        return {"command": command}

    def __getReq(self, sock_obj: socket.socket) -> dict:
        req_len = sock_obj.recv(self.max_req_size).decode('utf-8')
        if req_len:
            req_len = int(req_len)
            return json.loads(sock_obj.recv(req_len).decode('utf-8'))

    def __sendRes(self, sock_obj: socket.socket, res_matr: list) -> None:
        res_str = json.dumps(res_matr)
        res_str = f"{len(res_str):<{self.max_req_size}}" + res_str
        sock_obj.send(bytes(res_str, encoding='utf-8'))


# if __name__ == "__main__":
#     server = Server()
#     server.runServer()





#######################client############################
import socket
import json
from typing import Union

from requests import Session
from bs4 import BeautifulSoup

import csv

ses = Session()

def web_scrapping():
    rs = ses.post("http://utproject.ir/bp/login.php",data={"username":"610300032",
                "password":49704339167678442900})
    print(rs.status_code)

    car_dicts = list()

    j = 0
    for i in range(500):
        print(i)
        result = ses.get(f"http://utproject.ir/bp/Cars/page{i}.php")
        result.encoding = 'utf8'
        soup = BeautifulSoup(result.text, "html.parser")
        #print(soup.prettify())


        matches = soup.find_all('li', class_='car-list-item-li list-data-main')
        for match in matches:
            newdict = dict()

            data_list = match['data-url'].split('-')[2:]
            newdict['company'] = data_list[0]
            data_list.pop(0)
            newdict['car'] = data_list[0]
            data_list.pop(0)
            newdict['year'] = int(data_list[-1])
            data_list.pop(-1)
            newdict['tream'] = '-'.join(data_list)
            
            price = match.find('p', class_='cost')
            if price['class'][-1] == 'small':
                newdict['price'] = 0 # 0 means agreement
            elif price['class'][-1] == 'installment-cost':
                newdict['price'] = -1 # -1 means installment
            else:
                newdict['price'] = int(price.span['content'])

            kilometer_list = match.find('div', class_='car-func-details').span.text.split()
            if len(kilometer_list) == 1:
                newdict['kilometer'] = 0
            else:
                kilometer = kilometer_list[1]
                try:
                    kilometers = kilometer.split(',')
                    kilometer = int(kilometers[0] + kilometers[1])
                except:
                    kilometer = 0
                newdict['kilometer'] = kilometer

            car_dicts.append(newdict)

    #print(car_dicts)

def num_to_let(inp):
    inp = int(inp)
    remainder_list = []
    i = 0
    while True:
        i += 1
        q = inp // 26
        r = inp % 26
        inp = q - 1
        remainder_list.append(r) 
        if q == 0:
            break
    index_list = []
    for i in range(len(remainder_list)-1,-1,-1):
        index_list.append(remainder_list[i])
    mystring = ''
    for i in range(len(index_list)):
        mystring += chr(index_list[i]+65)
    return mystring


class Client:
    def __init__(self, port: int = 5050, max_req_len: int = 10):
        self.port = port
        self._max_req_len = max_req_len
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect(("localhost", port))
        

    def run(self):
        while True:
            self.__sendReq({"req_type": "command", "command_str": 'create(cars,6,15007)'})
            print(self.__getRes())
            self.__sendReq({"req_type": "command", "command_str": 'context(cars)'})
            print(self.__getRes())
            mylist = ['company', 'car', 'tream', 'kilometer', 'year', 'price']
            for i in range(len(mylist)):
                self.__sendReq({"req_type": "command", "command_str": f'{num_to_let(i)}1={mylist[i]}'})
                print(self.__getRes())
            for i in range(len(car_dicts)):
                for j in range(6):
                    self.__sendReq({"req_type": "command", "command_str": f'{num_to_let(j)}{i+2}={car_dicts[i][mylist[j]]}'})
                    print(self.__getRes())
            self.__sendReq({"req_type": "get_results"})

            csv_file = open('car_tables.csv', 'w')
            csv_writer = csv.writer(csv_file)
            car_matris = list()
            while True:
                get_req = self.__getRes()
                if isinstance(get_req,list):
                    csv_writer.writerow(get_req)
                    car_matris.append(get_req)
                elif get_req == "end":
                    break
            csv_file.close()
            print(car_matris)
            break


    def __getRes(self) -> Union[list, dict]:
        req_len = self._sock.recv(self._max_req_len).decode('utf-8')
        if req_len:
            req_len = int(req_len)
            return json.loads(self._sock.recv(req_len).decode('utf-8'))

    def __sendReq(self, res_dic: dict) -> None:
        res_str = json.dumps(res_dic)
        res_str = f"{len(res_str):<{self._max_req_len}}" + res_str
        self._sock.send(bytes(res_str, encoding='utf-8'))


# if __name__ == "__main__":
#     client = Client()
#     client.run()
