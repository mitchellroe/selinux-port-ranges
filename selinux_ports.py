#!/usr/bin/env python3

# TODO: Instead of checking whether the numbers are already in the intermediate
# arrays, use sets instead.  These will only add if the number is not already
# present.


import re
import subprocess

lowest_port = 9001
highest_port = 65535


def main():
    raw_output = _get_raw_output()
    first_pass = _filter_tcp_ports(raw_output)
    del raw_output
    second_pass = _split_up_sequences(first_pass)
    del first_pass
    reserved_ports = _expand_ranges(second_pass)
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
    """
    Return the output of `semanage port -l` (without the header row)
    as an array.
    """
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
    """
    Expand the ranges denoted with a '-' and trim off any that are outside the
    range set above.
    """
    # TODO: This doesn't seem to include non-ranged port numbers.
    # TODO: This function tries to accomplish too much.  Split it up.
    retval = []
    for entry in my_array:
        # You can use str.find to search for '-'.  If it returns -1, then it's
        # not in the string and you can just compare it against your acceptable
        # port ranges.
        port_range = entry.split('-')
        if len(port_range) == 1:
            port_number = str(port_range[0])
            if port_number not in retval:
                retval.append(port_number)
        else:
            low = int(port_range[0])
            high = int(port_range[1]) + 1
            for port_number in range(low, high):
                if port_number not in retval:
                    retval.append(str(port_number))
    return retval


def _is_within_range(port_number):
    if port_number >= lowest_port and port_number <= highest_port:
        return True
    else:
        return False


if __name__ == '__main__':
    main()
