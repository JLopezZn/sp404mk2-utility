import struct
import xml.etree.ElementTree as ET

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
        print(f"Concatenating pattern {ptn_number+1}/{len(pattern_numbers)}: {bin_filename}")  # Aviso del patrón actual
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

def main():
    chn_filename = 'PATTERNCHAIN_00.CHN' #CHANGE THIS FOR YOUR PATTERN CHAIN FILE
    new_bin_filename = "PTN00016.BIN" #CHANGE THIS FOR YOUR NEW PATTERN FILE NAME
    
    pattern_numbers = read_chn_file(chn_filename)
    concatenated_data = concatenate_patterns(pattern_numbers)
    if concatenated_data is not None:
        write_bin_file(new_bin_filename, concatenated_data)
        print(f'New .BIN file "{new_bin_filename}" has been created.')

if __name__ == "__main__":
    main()
