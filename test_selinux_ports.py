#!/usr/bin/env python3

import unittest
import selinux_ports


class SelinuxPortsCase(unittest.TestCase):

    def test__get_raw_output(self):
        raw_output = selinux_ports._get_raw_output()
        # I don't really know of a way to test the output of this
        # function, so we'll just test that we got a list back and
        # that it's got more than one element.
        self.assertIsInstance(raw_output, list)
        self.assertTrue(len(raw_output) >= 3)

    def test__filter_tcp_ports(self):
        """
        Test the _filter_tcp_ports function, which should return entries
        which are TCP protocol only.
        """
        test_val = [
            "foo tcp 80",
            "bar udp 90",
            "baz foobar 120",
            "topaz tcp 42",
        ]
        expected_val = [
            "80",
            "42",
        ]
        retval = selinux_ports._filter_tcp_ports(test_val)
        self.assertEqual(retval, expected_val)

    def test__split_up_sequences(self):
        """Test the _split_up_sequences function in selinux_ports."""
        test_val = ["80", "70|40", "60", "9|19|42", "3"]
        expected_val = ["80", "70", "40", "60", "9", "19", "42", "3"]
        retval = selinux_ports._split_up_sequences(test_val)
        self.assertEqual(retval, expected_val)

    def test__expand_ranges(self):
        """Test the _expand_ranges function in selinux_ports."""
        test_val = ["62", "12-14", "74", "6001-6007"]
        expected_val = [
            "62", "12", "13", "14", "74",
            "6001", "6002", "6003", "6004", "6005", "6006", "6007"
        ]
        retval = selinux_ports._expand_ranges(test_val)
        self.assertEqual(retval, expected_val)

    def test__is_within_range(self):
        low = 9001
        high = 65535
        self.assertFalse(selinux_ports._is_within_range(9000))
        self.assertTrue(selinux_ports._is_within_range(9001))
        self.assertTrue(selinux_ports._is_within_range(9002))

        self.assertTrue(selinux_ports._is_within_range(65534))
        self.assertTrue(selinux_ports._is_within_range(65535))
        self.assertFalse(selinux_ports._is_within_range(65536))

def main():
    unittest.main()


if __name__ == '__main__':
    main()
