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


from unittest.mock import patch, Mock, call

from owca.storage import LogStorage
from owca.metrics import Metric


@patch('owca.storage.get_current_time', return_value=1)
def test_log_storage(*mocks):
    open_mock = Mock()
    with patch('builtins.open', open_mock):
        metric = Metric(name='foo', value=8)
        log_storage = LogStorage(output_filename='mocked_file_name.log')
        log_storage.store([metric])
    assert open_mock.return_value.write.call_count == 2
    assert open_mock.return_value.method_calls[0] == call.write('foo 8 1\n\n')
