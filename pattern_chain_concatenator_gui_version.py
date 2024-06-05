import struct
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

MAX_BARS = 64

def read_bin_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return list(struct.unpack(f'{len(data)}B', data))

def write_bin_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(bytearray(data))

def read_chn_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    pattern_numbers = [int(ptn.attrib['NUMBER']) for ptn in root.findall('PTN')]
    return pattern_numbers

def concatenate_patterns(pattern_numbers):
    concatenated_data = []
    bars_sum = 0
    for i, ptn_number in enumerate(pattern_numbers):
        bin_filename = f'PTN{ptn_number+1:05d}.BIN'
        bin_data = read_bin_file(bin_filename)

        if i < len(pattern_numbers) - 1:
            concatenated_data.extend(bin_data[:-16])
            bars_sum += bin_data[-2]
        else:
            bars_sum += bin_data[-2]
            if bars_sum > MAX_BARS:
                print(f"Pattern chain exceeds 64 bars, actual bars: ({bars_sum}), adjusting....")
                excess_bars = bars_sum - MAX_BARS
                bin_data[-2] -= excess_bars
                bin_data[-8] -= excess_bars
                bars_sum = MAX_BARS
            concatenated_data.extend(bin_data[:-16])
            concatenated_data.extend(bin_data[-16:])
            concatenated_data[-8] = bars_sum
            concatenated_data[-2] = bars_sum

    return concatenated_data

def process_files(chn_filename, new_bin_filename):
    try:
        pattern_numbers = read_chn_file(chn_filename)
        concatenated_data = concatenate_patterns(pattern_numbers)
        if concatenated_data is not None:
            write_bin_file(new_bin_filename, concatenated_data)
            messagebox.showinfo("Success", f'New .BIN file "{new_bin_filename}" has been created.')
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def select_chn_file():
    filename = filedialog.askopenfilename(title="Select .CHN file", filetypes=[("CHN files", "*.CHN")])
    chn_file_entry.delete(0, tk.END)
    chn_file_entry.insert(0, filename)

def run_processing():
    chn_filename = chn_file_entry.get()
    selected_pad = pad_var.get()
    if selected_pad:
        new_bin_filename = f'PTN{selected_pad:05d}.BIN'
        if chn_filename and new_bin_filename:
            process_files(chn_filename, new_bin_filename)
        else:
            messagebox.showwarning("Input Error", "Please select a .CHN file and specify an output filename.")
    else:
        messagebox.showwarning("Input Error", "Please select a pad number.")

# Opciones para los pads del Banco A
pad_options = [i + 1 for i in range(16)]  # 1 to 16

# Setup GUI
root = tk.Tk()
root.title("Pattern Concatenation Tool")

# File selection
tk.Label(root, text="Select .CHN File:").grid(row=0, column=0, padx=10, pady=10)
chn_file_entry = tk.Entry(root, width=50)
chn_file_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_chn_file).grid(row=0, column=2, padx=10, pady=10)

# Pad selection
tk.Label(root, text="Select Pattern Pad (Bank A):").grid(row=1, column=0, padx=10, pady=10)
pad_var = tk.IntVar()
pad_menu = ttk.Combobox(root, textvariable=pad_var, values=pad_options, width=47)
pad_menu.grid(row=1, column=1, padx=10, pady=10)

# Process button
tk.Button(root, text="Process", command=run_processing).grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
