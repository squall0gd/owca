# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import unittest

from unittest import mock

from owca.cbm_bits import check_cbm_bits, get_min_cbm_bits, get_max_mask


class CbmTest(unittest.TestCase):
    def setUp(self):
        self.info_path = '/sys/fs/resctrl/info/L3'

    @mock.patch('owca.cbm_bits.open')
    def test_get_min_cbm_bits(self, open_mock):
        open_mock.return_value = mock.mock_open(read_data='1').return_value
        self.assertEqual(get_min_cbm_bits(self.info_path), 1)

    @mock.patch('owca.cbm_bits.open')
    def test_get_max_mask(self, open_mock):
        open_mock.return_value = mock.mock_open(read_data='ffff').return_value
        self.assertEqual(get_max_mask(self.info_path), 65535)

    @mock.patch('owca.cbm_bits.get_max_mask')
    @mock.patch('owca.cbm_bits.get_min_cbm_bits')
    def test_check_cbm_bits_success(self, min_cbm_bits, max_mask):
        min_cbm_bits.return_value = 1
        max_mask.return_value = 65535
        check_cbm_bits(0xff00)

    @mock.patch('owca.cbm_bits.get_max_mask')
    @mock.patch('owca.cbm_bits.get_min_cbm_bits')
    def test_check_cbm_bits_gap(self, min_cbm_bits, max_mask):
        min_cbm_bits.return_value = 1
        max_mask.return_value = 65535
        self.assertRaises(ValueError, check_cbm_bits, 0xf0f)

    @mock.patch('owca.cbm_bits.get_max_mask')
    @mock.patch('owca.cbm_bits.get_min_cbm_bits')
    def test_check_not_enough_cbm_bits(self, min_cbm_bits, max_mask):
        min_cbm_bits.return_value = 1
        max_mask.return_value = 65535
        self.assertRaises(ValueError, check_cbm_bits, 0x00)

    @mock.patch('owca.cbm_bits.get_max_mask')
    @mock.patch('owca.cbm_bits.get_min_cbm_bits')
    def test_check_too_big_mask(self, min_cbm_bits, max_mask):
        min_cbm_bits.return_value = 1
        max_mask.return_value = 65535
        self.assertRaises(ValueError, check_cbm_bits, 0xffffff)
