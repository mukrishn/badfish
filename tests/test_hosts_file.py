import os
from asynctest import patch
from tests import config
from tests.test_base import TestBase


class TestHostsFile(TestBase):
    option_arg = "--host-list"

    tests_dir = os.path.dirname(__file__)
    mock_hosts_good_path = os.path.join(tests_dir, "fixtures/hosts_good.txt")
    mock_hosts_garbled_path = os.path.join(tests_dir, "fixtures/hosts_garbled.txt")
    mock_hosts_empty_path = os.path.join(tests_dir, "fixtures/hosts_empty.txt")

    def test_hosts_good(self):
        self.args = [self.option_arg, self.mock_hosts_good_path]

        with patch("badfish.badfish.execute_badfish") as badfish_mock:
            self.badfish_call(mock_host=None)

        badfish_mock.assert_awaited()
        assert (
            len(badfish_mock.await_args_list) == 3
        ), "Amount of calls does not match amount of hosts in file"
        for call in badfish_mock.await_args_list:
            _host, _args, _logger = call[0]
            assert _host == config.MOCK_HOST

            assert _args["host_list"] == self.mock_hosts_good_path
            assert _args["u"] == config.MOCK_USER
            assert _args["p"] == config.MOCK_PASS

    def test_hosts_non_existent(self):
        self.args = [self.option_arg, "non/existent/file"]

        with patch("badfish.badfish.execute_badfish") as badfish_mock:
            out, err = self.badfish_call(mock_host=None)
        badfish_mock.assert_not_awaited()

        assert (
            err
            == "[badfish.badfish] - ERROR    - There was something wrong reading from non/existent/file\n"
        )

    def test_hosts_empty(self):
        """
        Do nothing when there are no hosts.
        """
        self.args = [self.option_arg, self.mock_hosts_empty_path]

        with patch("badfish.badfish.execute_badfish") as badfish_mock:
            result = self.badfish_call(mock_host=None)

        badfish_mock.assert_not_awaited()
        assert result == ("", "")

    def test_hosts_bad(self):
        self.args = [self.option_arg, self.mock_hosts_garbled_path]

        with patch("badfish.badfish.execute_badfish") as badfish_mock:
            self.badfish_call(mock_host=None)

        badfish_mock.assert_awaited()
        assert (
            len(badfish_mock.await_args_list) == 3
        ), "Amount of calls does not match amount of hosts in file"
        for call in badfish_mock.await_args_list:
            _host, _args, _logger = call[0]
            assert _host == config.MOCK_HOST

            assert _args["host_list"] == self.mock_hosts_garbled_path
            assert _args["u"] == config.MOCK_USER
            assert _args["p"] == config.MOCK_PASS
