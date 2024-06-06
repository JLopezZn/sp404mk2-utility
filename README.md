# sp404mk2-utility
Repository for utility scripts for the Roland SP404MK2 sampler.

# Pattern Concatenator GUI VERSION

pattern_chain_concatenator_gui_version.py reads a pattern chain file (.CHN) and concatenates the corresponding pattern binary data from .BIN files.

Consider this:  The script ensures that the total number of bars in the concatenated pattern does not exceed a specified maximum limit of 64 bars (default by Roland).

** Currently just working for BANK A **

![image](https://github.com/JLopezZn/sp404mk2-utility/assets/42882196/f0f5f412-6b95-421c-94c7-6cd10fca2877)

Steps:

1 - Go and download Python https://www.python.org/downloads/release/python-3111/ , Im using Python 3.11.1.

2 - Move the script into the pattern folder:

````
  /ROLAND
     /SP-404MKII
       /PROJECT_PROJECT_01
          /PTN  <- move the script here
````

3 - run on a cmd/terminal inside the pattern folder the next line:

````py pattern_chain_concatenator_gui_version.py````


4 - Import the modified project to your SP404MK2 and enjoy :)



# Pattern Concatenator NO GUI VERSION

** Currently just working for BANK A **

pattern_chain_concatenator.py reads a pattern chain file (.CHN) and concatenates the corresponding pattern binary data from .BIN files.

Consider this:  The script ensures that the total number of bars in the concatenated pattern does not exceed a specified maximum limit of 64 bars (default by Roland).

Steps:

1 - Go and download Python https://www.python.org/downloads/release/python-3111/ , Im using Python 3.11.1.

2 - Move the pattern_chain_concatenator.py script to the pattern folder, example:
````
  /ROLAND
     /SP-404MKII
       /PROJECT_PROJECT_01
          /PTN  <- move the script here
````

3 - Open the pattern_chain_concatenator.py file and make sure to change the variables **chn_filename** and **new_bin_filename** values of the main() fuction:
````
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

````
4 - run on a cmd/terminal inside the pattern folder the next line:

````py pattern_chain_concatenator.py````


5 - Import the modified project to your SP404MK2 and enjoy :)
