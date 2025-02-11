import os
import re
import unicodedata
from natsort import natsorted
import numpy as np

def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")

def extract_temperature(file_path, lnum):
    with open(file_path, 'rb') as file0:
        # Read the second line
        file_con = file0.read()
        file = file_con.decode('latin-1')
        all_lines = file.splitlines()
        # Extract temperature value using regular expression]
        #print(all_lines[1])
        # match = re.search(r"Temp\. \[.\]=([0-9.e+-]+)[\s]+[AC]", all_lines[1])
        match0 = all_lines[int(lnum-1)]
        tmpr0 = re.split(r'\t|\ ', match0)
        match = re.split("=", tmpr0[5])[1]
        if match:
            # temperature = match.group(1)
            temperature = match
            return temperature
    return None

def extract_isothermal(file_name):
    # Extract isothermal value from filename
    # Replace "plate" with the correct keyword according to your filenames 
    match = re.search(r'plate(\d+)', file_name)
    if match:
        isothermal = match.group(1)
        return isothermal
    return None

# def extract_eps_column(file_path):
    # eps_column = []
    # print(f"Processing file: {file_path}")
    # with open(file_path, 'r') as file:
        # # Skip the first three lines
        # for _ in range(3):
            # next(file)
        # # Read the rest of the lines
        # for line in file:
            # # Use regular expression to find the Eps' value
            # match = re.search(r'\s+([0-9.]+e[+-][0-9]+)\s+([0-9.]+e[+-][0-9]+)\s+([0-9.]+e[+-][0-9]+)\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+', line)
            # if match:
                # # Extract the Eps' value (which is the second capture group)
                # eps_value = match.group(2)
                # eps_column.append(eps_value)
                # print(f"Extracted Eps' value: {eps_value}")
            # else:
                # print(f"Skipping line: {line.strip()} - No match found")
    # if not eps_column:
        # print(f"No Eps' values extracted from {file_path}")
    # return eps_column

def find_word_line_number(filename, target_word):
    line_number = 0

    with open(filename, 'rb') as file0:
        file_con = file0.read()
        file1 = file_con.decode('latin-1')
        lines = file1.splitlines()
        for line in lines:
            line_number += 1
            if target_word in line:
                return line_number

    # If the word is not found in the file, return None
    return None

def main():
    directory = os.path.dirname(os.path.realpath(__file__))
    #output_file = '[Eps\']output.dat'
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # print(dir_path)

    # Initialize header rows
    header1 = []
    header2 = []

    # Initialize Eps' data
    eps_data = []
    full_data = []
    freq = []
    
    
    ind=0
    # Iterate over files in the directory
    for file_name in natsorted(os.listdir(directory)):
        if file_name.endswith('.txt'):
            file_path = os.path.join(directory, file_name)
            print(file_name)
            print(file_path)

            lin_num = find_word_line_number(file_path, "Temp")
            if lin_num is None:
                print("something wrong for counting line number")
            # Extract temperature and isothermal values
            temperature = extract_temperature(file_path,lin_num)
            isothermal = extract_isothermal(file_name)
            # print(temperature, isothermal)
            if ind<1:
                with open(file_path, 'rb') as file0:
                    file_con = file0.read()
                    file = file_con.decode('latin-1')
                    all_lines = file.splitlines()
                    fheaders = all_lines[lin_num]
                    h2 = " ".join(fheaders.split())
                    h1 = h2.split()
                    
                    data0 = np.loadtxt(file_path, skiprows=lin_num+1, encoding='latin1')
                    freq = data0[:,0]
                    freq = freq.reshape(-1,1)
            #print(file_path)
            #print(temperature,isothermal)

            # Check if temperature and isothermal values are extracted successfully
            if temperature is not None and isothermal is not None:
                # Append temperature and isothermal to headers
                header1.append(temperature)
                header2.append(isothermal)

                # # Extract Eps' column
                # eps_column = extract_eps_column(file_path)
                # eps_data.append(eps_column)

                # # Print Eps' column for debugging
                # print(f"Eps' column extracted from {file_path}: {eps_column}")
                
            ind+=1

    # Check if both headers are not empty before writing to output file
    if header1 and header2 and h1:
        for i in range(len(h1)):
            h1[i] = h1[i].replace("''","-2")
            h1[i] = h1[i].replace("'","-1")
            output_file = '0' + str(i) + '[' + slugify(h1[i]) + ']-output' + '.dat'
            #print(output_file)
            # Write header rows to output file
            with open(output_file, 'w') as output:
                header1_line = ','.join([''] + header1) + '\n'
                header2_line = ','.join([''] + header2) + '\n'
                blank1_line = ','.join([''] + [''] * len(header1)) + '\n'
                blank2_line = ','.join([''] + [''] * len(header2)) + '\n'
                output.write(header1_line)
                output.write(blank1_line)
                output.write(header2_line)
                output.write(blank2_line)
                
                j = 0
                for file_name in natsorted(os.listdir(directory)):
                    if file_name.endswith('.txt'):
                        file_path = os.path.join(directory, file_name)
                        data0 = np.loadtxt(file_path, skiprows=lin_num+1, encoding='latin1')
                        data1 = data0[:,i]
                        data1 = data1.reshape(-1,1)
                        if j<1:
                            full_data = np.hstack((freq, data1))
                        else:
                            full_data = np.hstack((full_data, data1))
                        j+=1
                        
            with open(output_file, 'a') as output:
                np.savetxt(output, full_data, delimiter=',')

                # # Write Eps' data to output file
                # for i in range(len(eps_data[0])):
                    # eps_values = [eps_column[i] for eps_column in eps_data]
                    # output.write(','.join(eps_values) + '\n')

            print(f"Extraction completed. Output file: {output_file}")

if __name__ == "__main__":
    main()
