#!/usr/bin/env python3

import re
import subprocess

lowest_port = 9001
highest_port = 65535


def main():
    raw_output = _get_raw_output()
    _print_first_few(raw_output)
    print()

    first_pass = _filter_tcp_ports(raw_output)
    _print_first_few(first_pass)
    print()

    del raw_output

    second_pass = _split_up_sequences(first_pass)
    _print_first_few(second_pass)
    print()

    del first_pass

    reserved_ports = _expand_ranges(second_pass)
    _print_first_few(reserved_ports)
    print()

    del second_pass

    # for x in range(0, len(reserved_ports)):
    #     y = x + 1
    #     if y == len(reserved_ports) - 1:
    #         break
    #     current_port = reserved_ports[x]
    #     next_port = reserved_ports[y]
    #     if next_port == current_port + 1:
    #         continue
    #     else:
    #         print("low: " + str(current_port))
    #         print("high: " + str(next_port))
    #         print()


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
        port_number = str(parsed_line[2])
        if protocol == 'tcp':
            retval.append(port_number)
    return retval


def _split_up_sequences(my_array):
    """Split up lines with more than one port."""
    retval = []
    for entry in my_array:
        for port_field in entry.split('|'):
            if str(port_field) not in retval:
                retval.append(str(port_field))
    return retval


def _expand_ranges(my_array):
    # TODO: This doesn't seem to include non-ranged port numbers.
    """
    Expand the ranges denoted with a '-' and trim off any that are outside the
    range set above.
    """
    # The third and final stage: port ranges.
    retval = []
    for entry in my_array:
        port_range = entry.split('-')
        if len(port_range) == 1:
            port_number = int(port_range[0])
            if _is_within_range(port_number) and port_number not in retval:
                retval.append(port_number)
        else:
            low = int(port_range[0])
            high = int(port_range[1]) + 1
            for port_number in range(low, high):
                if _is_within_range(port_number) and port_number not in retval:
                    retval.append(port_number)
    return retval


def _is_within_range(port_number):
    if port_number >= lowest_port and port_number <= highest_port:
        return True
    else:
        return False


def _print_first_few(my_array):
    for i in range(0, 15):
        print(str(my_array[i]))


if __name__ == '__main__':
    main()
