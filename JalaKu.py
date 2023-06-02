import PySimpleGUI as sg
import heapq
import datetime
from collections import deque


#Class yang digunakan untuk inisiasi struktur data
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def appendleft(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def popleft(self):
        if self.head is None:
            return None
        data = self.head.data
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        return data

    def len(self):
        current = self.head
        length = 0

        while current is not None:
            length += 1
            current = current.next

        return length

    def __getitem__(self, index):
        if index < 0:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(index):
            if current is None:
                raise IndexError("Index out of range")
            current = current.next
        if current is None:
            raise IndexError("Index out of range")
        return current.data

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

data_transaksi = DoublyLinkedList()
waiting_list = deque()

#data-data yang dibutuhkan untuk program
initial_route = {
    'WPPNRI_711': {'WPPNRI_712': 4, 'WPPNRI_713': 7, 'WPPNRI_714': 10},
    'WPPNRI_712': {'WPPNRI_713': 9},
    'WPPNRI_713': {'WPPNRI_715': 7, 'WPPNRI_714': 7},
    'WPPNRI_714': {'WPPNRI_712': 6, 'WPPNRI_715': 10},
    'WPPNRI_715': {'WPPNRI_712': 6, 'WPPNRI_711': 2}
}
data_user = {
    "verlino": "linolino",
    "annisa": "nisanisa",
    "andro": "drodro",
    "angelita": "litalita",
    "harits": "ritsrits",
    "arel": "relrel"
}
jenis_ikan_options = {
    'Ikan Tongkol': 10000,
    'Ikan Sardin': 12000,
    'Ikan Gurame': 12500,
    'Ikan Bandeng': 18000,
    'Ikan Bawal': 15000,
    'Ikan Kakap': 16000,
    'Ikan Tengiri': 12000
}
jenis_ikan_options_gudang = {
    'Ikan Tongkol': 11000,
    'Ikan Sardin': 13000,
    'Ikan Gurame': 13500,
    'Ikan Bandeng': 19000,
    'Ikan Bawal': 16000,
    'Ikan Kakap': 17000,
    'Ikan Tengiri': 13000
}


initial_route = {
    'WPPNRI_711': {'WPPNRI_712': 4, 'WPPNRI_713': 7, 'WPPNRI_714': 10},
    'WPPNRI_712': {'WPPNRI_713': 9},
    'WPPNRI_713': {'WPPNRI_715': 7, 'WPPNRI_714': 7},
    'WPPNRI_714': {'WPPNRI_712': 6, 'WPPNRI_715': 10},
    'WPPNRI_715': {'WPPNRI_712': 6, 'WPPNRI_711': 2}
}

#beberapa function yang digunakan untuk membantu program
def shortest_path(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [(0, start)]
    visited = set()
    previous = {}

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_node == end:
            path = []
            while current_node != start:
                path.insert(0, current_node)
                current_node = previous[current_node]
            path.insert(0, start)
            return distances[end], path
        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return float('inf'), []  # No path found


def stock_counter(jenis_ikan):
    counter = 0
    if data_transaksi.len() != 0:
        for i in range(data_transaksi.len()):
            if data_transaksi[i]['Jenis Ikan'] == jenis_ikan:
                if data_transaksi[i]['Tipe'] == 'Penjualan':
                    counter += int(data_transaksi[i]['Berat Ikan'])
                else:
                    counter -= int(data_transaksi[i]['Berat Ikan'])
            else:
                continue
        return counter
    return counter

#Kode untuk tampilan GUI program
def login():
    sg.theme('Dark Blue 3')
    layout = [
        [sg.Text("\n\n\n\n\n")],
        [sg.Text("Halaman Login", font=('Arial', 16))],
        [sg.Text("Nama Pengguna    "), sg.Input(key='-username-', size=25)],
        [sg.Text("Password\t"), sg.Input(
            key='-ps-', password_char='*', size=25)],
        [sg.Button("Login", size=20), sg.Cancel(size=20)],
    ]
    window = sg.Window('Fishing App', layout, size=(
        400, 400), element_justification='center')
    while True:
        event, values = window.read()
        username = values['-username-']
        password = values['-ps-']
        if event == "Login":
            if username in data_user and password == data_user[username]:
                window.close()
                main()
                break
            else:
                sg.popup_ok("Username Tidak Ditemukan",
                            title="Login Error")
        else:
            break
    window.close()


def main():
    layout = [
        [sg.Text('JalaKu', font=('Helvetica', 16, 'bold'))],
        [sg.Text('Pilih Menu', font=('Helvetica', 10))],
        [sg.Button('Penjualan Ikan oleh Nelayan', size=(24, 2)),
         sg.Button('Pembelian Ikan oleh Konsumen', size=(24, 2))],
        [sg.Button('Daftar Antrian Pembelian', size=(24, 2)),
         sg.Button('Data Transaksi', size=(24, 2))],
        [sg.Button('Data Stok Ikan', size=(24, 2)),
         sg.Button('Jalur Pelayaran', size=(24, 2))],
        [sg.Button('Harga Ikan', size=(24, 2)),
         sg.Button('Keluar', size=(24, 2))]
    ]

    window = sg.Window('JalaKu', layout, size=(
        500, 300), element_justification='center')
    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED:
            window.close()
            break
        elif event == 'Daftar Antrian Pembelian':
            window.close()
            waiting_list_window()
            break
        elif event == 'Penjualan Ikan oleh Nelayan':
            window.close()
            show_sales_window()
            break
        elif event == 'Harga Ikan':
            window.close()
            harga_ikan_window()
            break
        elif event == 'Pembelian Ikan oleh Konsumen':
            window.close()
            show_purchase_window()
            break
        elif event == 'Data Stok Ikan':
            window.close()
            show_stock_data_window()
            break
        elif event == 'Data Transaksi':
            window.close()
            show_transaction_data_window()
            break
        elif event == 'Jalur Pelayaran':
            window.close()
            show_route()
            break
        elif event == 'Keluar':
            window.close()
            login()
            break
        window.close()


def show_sales_window():
    layout = [
        [sg.Text('Menu Penjualan Ikan oleh Nelayan', font=('Arial', 16))],
        [sg.Text('Nama Penjual '), sg.InputText(key='-NAMA_PENJUAL-')],
        [sg.Text('Jenis Ikan       '), sg.Combo(
            list(jenis_ikan_options.keys()), key='-JENIS_IKAN-', enable_events=True)],
        [sg.Text('Berat Ikan (kg)'), sg.InputText(key='-BERAT_IKAN-')],
        [sg.Button('Submit', size=(10, 1)),
         sg.Button('Kembali', size=(10, 1))]
    ]
    window = sg.Window('Penjualan ikan', layout, size=(500, 300))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            window.close()
            break
        elif event == 'Kembali':
            window.close()
            main()
            break
        elif event == 'Submit':
            try:
                nama_penjual = values['-NAMA_PENJUAL-']
                jenis_ikan = values['-JENIS_IKAN-']
                berat_ikan = int(values['-BERAT_IKAN-'])
                harga_ikan = jenis_ikan_options[jenis_ikan]
                data_transaksi.appendleft({
                    'Nama': nama_penjual,
                    'Jenis Ikan': jenis_ikan,
                    'Berat Ikan': berat_ikan,
                    'Total Harga': berat_ikan * jenis_ikan_options[jenis_ikan],
                    'Tipe': "Penjualan"
                })
                now = datetime.datetime.now()
                dt = now.strftime('%d/%m/%Y %H:%M:%S')
                receipt_text = f"---------------------------------------------------\n"
                receipt_text += f"\t KUITANSI PENJUALAN\n"
                receipt_text += f"---------------------------------------------------\n"
                receipt_text += f"Waktu              : {dt}\n"
                receipt_text += f"Nama Penjual   : {nama_penjual}\n"
                receipt_text += f"Jenis Ikan         : {jenis_ikan}\n"
                receipt_text += f"Berat Ikan         : {berat_ikan} kg\n"
                receipt_text += f"Harga Penjualan: {berat_ikan * jenis_ikan_options[jenis_ikan]}\n"
                sg.popup('\t     Penjualan berhasil!', receipt_text)
            except:
                sg.popup("Input tidak valid!", title='Invalid Input')
    window.close()




def show_purchase_window():
    layout = [
        [sg.Text('Menu Pembelian Ikan oleh Konsumen', font=('Arial', 16))],
        [sg.Text('Nama Pembeli:'), sg.InputText(key='-NAMA_PEMBELI-')],
        [sg.Text('Jenis Ikan:       '), sg.Combo(
            list(jenis_ikan_options.keys()), key='-JENIS_IKAN-', enable_events=True)],
        [sg.Text('Berat Ikan (kg):'), sg.InputText(key='-BERAT_IKAN-')],
        [sg.Button('Submit', size=(10, 1)), sg.Button('Kembali', size=(10, 1))]
    ]

    window = sg.Window('Pembelian ikan', layout, size=(500, 300))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            window.close()
            break
        elif event == 'Submit':
            try:
                nama_pembeli = values['-NAMA_PEMBELI-']
                jenis_ikan = values['-JENIS_IKAN-']
                berat_ikan = int(values['-BERAT_IKAN-'])
                harga_ikan = jenis_ikan_options_gudang[jenis_ikan] * berat_ikan
                if int(values['-BERAT_IKAN-']) <= stock_counter(values['-JENIS_IKAN-']):
                    data_transaksi.appendleft({
                        'Nama': nama_pembeli,
                        'Jenis Ikan': jenis_ikan,
                        'Berat Ikan': berat_ikan,
                        'Total Harga': harga_ikan,
                        'Tipe': "Pembelian"
                    })
                    now = datetime.datetime.now()
                    dt = now.strftime('%d/%m/%Y %H:%M:%S')
                    receipt_text = f"---------------------------------------------------\n"
                    receipt_text += f"\t KUITANSI PEMBELIAN\n"
                    receipt_text += f"---------------------------------------------------\n"
                    receipt_text += f"Waktu              : {dt}\n"
                    receipt_text += f"Nama Pembelian   : {nama_pembeli}\n"
                    receipt_text += f"Jenis Ikan         : {jenis_ikan}\n"
                    receipt_text += f"Berat Ikan         : {berat_ikan} kg\n"
                    receipt_text += f"Harga Pembelian: {berat_ikan * jenis_ikan_options[jenis_ikan]}\n"
                    sg.popup('\t     Pembelian berhasil!', receipt_text, title="Success")
                else:
                    waiting_list.append({
                        'Nama Pembeli': nama_pembeli,
                        'Jenis Ikan': jenis_ikan,
                        'Berat Ikan': berat_ikan,
                        'Total Harga': harga_ikan,
                        'Tipe': "Pembelian"
                    })
                    sg.popup(
                        "Stok tidak mencukupi, Anda masuk ke Daftar Antrian Pembelian", title='information')
            except:
                sg.popup("Input tidak valid!", title='Invalid')
        elif event == 'Kembali':
            window.close()
            main()
            break

    window.close()

def waiting_list_window():
    heading = ['Nama Pembeli', 'Jenis Ikan',
               'Berat Ikan', 'Total Harga']
    data = [[waiting.get(key, '') for key in heading]
            for waiting in waiting_list]

    layout = [
        [sg.Text('Daftar Antrian Pembelian', font=('Arial', 16))],
        [sg.Table(values=data, headings=heading, enable_events=True,
                  justification='center', auto_size_columns=True, key=('-TABLE-'))],
        [sg.Button('Selesai', size=(10, 1)),
         sg.Button('Kembali', size=(10, 1))]
    ]
    window = sg.Window('Daftar Antrian Pembelian', layout, size=(650, 300))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            window.close()
            break
        elif event == 'Selesai':
            try:
                # Get the selected row index
                selected_row = values['-TABLE-'][0]

                # Get the data of the selected row
                selected_data = data[selected_row]
                if stock_counter(selected_data[1]) >= selected_data[2]:
                    data_transaksi.appendleft({
                        'Nama': selected_data[0],
                        'Jenis Ikan': selected_data[1],
                        'Berat Ikan': selected_data[2],
                        'Total Harga': selected_data[3],
                        'Tipe': "Pembelian"
                    })

                    dictToRemove = {
                        'Nama Pembeli': selected_data[0],
                        'Jenis Ikan': selected_data[1],
                        'Berat Ikan': selected_data[2],
                        'Total Harga': selected_data[3],
                        'Tipe': "Pembelian"
                    }
                    for item in waiting_list:
                        if item == dictToRemove:
                            waiting_list.remove(item)
                            break
                    sg.popup("Pembelian berhasil", title='Success')
                else:
                    sg.popup(
                        "Maaf, stok belum tersedia. Data pembelian masih dalam waiting list.", title='Information')
            except:
                sg.popup(
                    "Tidak ada data yang dipilih. Silakan pilih baris data.", title="Error message")
        elif event == 'Kembali':
            window.close()
            main()
            break

    window.close()

def show_stock_data_window():
    heading = ['Jenis Ikan', 'Stock']
    data = [[key, stock_counter(key)]for key in jenis_ikan_options]
    layout = [
        [sg.Table(headings=heading, values=data,
                  justification='left', auto_size_columns=True)],
        [sg.Button('Kembali')]
    ]

    window = sg.Window('Data stok ikan', layout, size=(
        500, 300), element_padding=(20))

    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED:
            window.close()
            break
        elif event == 'Kembali':
            window.close()
            main()
            break

    window.close()


def show_transaction_data_window():
    heading = ['Nama', 'Jenis Ikan',
               'Berat Ikan', 'Total Harga', 'Tipe']
    data = [[transaction.get(key, '') for key in heading]
            for transaction in data_transaksi]

    layout = [
        [sg.Text('Data transaksi', font=('Arial', 16))],
        [sg.Table(values=data, headings=heading,
                  justification='center', auto_size_columns=True)],
        [sg.Button('Kembali', size=(10, 1))]
    ]

    window = sg.Window('Data transaksi', layout, size=(650, 300))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            window.close()
            break
        elif event == 'Kembali':
            window.close()
            main()
            break

    window.close()


def show_route():
    layout = [
        [sg.Text('Jalur Pelayaran Terpendek', font=('Arial', 16))],
        [sg.Text('Titik Awal: '), sg.Combo(
            list(initial_route.keys()), size=40, key='-INITIAL_NODE-')],
        [sg.Text('Titik Akhir:'), sg.Combo(
            list(initial_route.keys()), size=40, key='-END_NODE-')],
        [sg.Button('Cari', size=(10, 1)),
         sg.Button('Kembali', size=(10, 1))]
    ]
    window = sg.Window('Jalur Pelayaran Terbaik', layout, size=(650, 300))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            window.close()
            break
        elif event == 'Kembali':
            window.close()
            main()
            break
        elif event == 'Cari':
            try:
                shortest_distance, jalur = shortest_path(
                    initial_route, values['-INITIAL_NODE-'], values['-END_NODE-'])
                sg.popup(
                    f"Jarak yang harus ditempuh dari {values['-INITIAL_NODE-']} Ke {values['-END_NODE-']} adalah: {shortest_distance} km \nJalur yang harus dilewati: \n{' -> '.join(jalur)}", title="Shortest path")
            except:
                sg.popup("Input tidak valid!", title='Invalid')


def harga_ikan_window():
    heading = ['Jenis Ikan', 'Harga']
    dataNelayan = [[key, jenis_ikan_options.get(key, '')]
                   for key in jenis_ikan_options]
    dataKonsumen = [[key, jenis_ikan_options_gudang.get(key, '')]
                    for key in jenis_ikan_options_gudang]

    layout = [
        [sg.Text('Harga Jual Ikan\t', font=('Arial', 10), justification='center'),
         sg.Text('\tHarga Beli Ikan', font=('Arial', 10), justification='center')],
        [sg.Table(values=dataNelayan, headings=heading,
                  justification='left', auto_size_columns=True),
            sg.Table(values=dataKonsumen, headings=heading,
                     justification='left', auto_size_columns=True)],
        [sg.Button('Kembali', size=(10, 1))]
    ]

    window = sg.Window('Data transaksi', layout, size=(
        500, 300), element_justification='center')

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            window.close()
            break
        elif event == 'Kembali':
            window.close()
            main()
            break

    window.close()


# Driver Code
if __name__ == '__main__':
    login()
