import os
import tkinter as tk
from tkinter import filedialog, messagebox
import heapq
import collections

class Node:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo no encontrado.")
        return None

def build_frequency_table(data):
    freq_table = collections.Counter(data)
    return freq_table

def build_huffman_tree(freq_table):
    heap = [Node(symbol, freq) for symbol, freq in freq_table.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = Node(frequency=left.frequency + right.frequency)
        parent.left = left
        parent.right = right
        heapq.heappush(heap, parent)
    return heap[0]

def get_file_size(file_path):
    return os.path.getsize(file_path)

def on_select_file():
    file_path = filedialog.askopenfilename(title="Seleccionar archivo")
    if file_path:
        content = read_file(file_path)
        if content:
            initial_size = get_file_size(file_path)
            freq_table = build_frequency_table(content)
            huffman_tree = build_huffman_tree(freq_table)
            encoded_data = huffman_encode(content, build_codewords_table(huffman_tree))
            encoded_size = len(encoded_data) // 8
            initial_size_label.config(text=f"Tamaño inicial del archivo: {initial_size} bytes")
            encoded_size_label.config(text=f"Tamaño del archivo codificado: {encoded_size} bytes")
            
            output_file_path = "./Gullivers_Travel_compressed.txt"
            with open(output_file_path, 'wb') as output_file:
                output_file.write(int(encoded_data, 2).to_bytes((len(encoded_data) + 7) // 8, byteorder='big'))

            decoded_output_file_path = "./Gullivers_Travel_decompressed.txt"
            decode_and_save(output_file_path, decoded_output_file_path, huffman_tree)

def huffman_encode(data, codewords):
    encoded_data = ""
    for symbol in data:
        encoded_data += codewords[symbol]
    return encoded_data

def build_codewords_table(root, prefix="", codewords={}):
    if root.symbol is not None:
        codewords[root.symbol] = prefix
    if root.left is not None:
        build_codewords_table(root.left, prefix + "0", codewords)
    if root.right is not None:
        build_codewords_table(root.right, prefix + "1", codewords)
    return codewords

def huffman_decode(encoded_data, root):
    decoded_data = ""
    current_node = root
    for bit in encoded_data:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.symbol is not None:
            decoded_data += current_node.symbol
            current_node = root
    return decoded_data

def decode_and_save(encoded_file_path, output_file_path, huffman_tree):
    with open(encoded_file_path, 'rb') as encoded_file:
        encoded_data = ""
        byte = encoded_file.read(1)
        while byte:
            byte_as_int = int.from_bytes(byte, byteorder='big')
            encoded_data += format(byte_as_int, '08b')
            byte = encoded_file.read(1)
        
        decoded_data = huffman_decode(encoded_data, huffman_tree)
        
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(decoded_data)


root = tk.Tk()
root.geometry("400x400")
root.title("Codificación de Huffman")

select_button = tk.Button(root, text="Seleccionar archivo", command=on_select_file)
select_button.pack(pady=20)

initial_size_label = tk.Label(root, text="")
initial_size_label.pack()
encoded_size_label = tk.Label(root, text="")
encoded_size_label.pack()

root.mainloop()

