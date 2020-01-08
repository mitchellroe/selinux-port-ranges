#!/usr/bin/env python3

import re
import subprocess


def main():
    raw_output = _get_raw_output()
    first_pass = _filter_tcp_ports(raw_output)
    second_pass = _split_up_sequences(first_pass)

    # The third and final stage: port ranges.
    third_pass = []
    for entry in second_pass:
        # This seems to be problematic.
        for my_range in entry.split("-"):
            if len(my_range) == 1:
                port_number = my_range[0]
                if port_number not in third_pass:
                    third_pass.append(port_number)
            else:
                low = int(my_range[0])
                high = int(my_range[0]) + 1
                for port_number in range(low, high):
                    if port_number not in third_pass:
                        third_pass.append(port_number)


def _get_raw_output():
    """Get the raw output."""
    raw_output = subprocess.check_output(['semanage', 'port', '-l'],
                                         universal_newlines=True)
    # Replace all consecutive spaces with a single space.
    raw_output = re.sub(' +', ' ', raw_output.strip())
    # Replace all comma-spaces with pipes.
    raw_output = re.sub(', ', '|', raw_output.strip())
    # Convert the string to an array.
    raw_output = raw_output.splitlines()
    # Remove the first two entries, as they are just the header row and a blank
    # line.
    del raw_output[0]
    del raw_output[0]
    return raw_output


def _filter_tcp_ports(my_array):
    """Only keep the tcp ports."""
    retval = []
    for entry in my_array:
        parsed_line = entry.split(' ')
        protocol = parsed_line[1]
        port_number = parsed_line[2]
        if protocol == 'tcp':
            retval.append(port_number)
    return retval


def _split_up_sequences(my_array):
    """Split up lines with more than one port."""
    retval = []
    for entry in my_array:
        for port_field in entry.split('|'):
            if port_field not in retval:
                retval.append(port_field)
    return retval


if __name__ == '__main__':
    main()
