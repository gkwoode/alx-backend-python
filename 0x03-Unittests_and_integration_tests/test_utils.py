#!/usr/bin/env python3
"""Parameterize a unit test"""

import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch
from utils import get_json
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """TestAccessNestedMap"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(
            self, nested_map, path, expected_exception
            ):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        self.assertEqual(str(context.exception), expected_exception)


class TestGetJson(unittest.TestCase):
    """Mock HTTP calls"""

    @patch('requests.get')
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload, mock_get):
        # Mock the response from requests.get
        mock_response = mock_get.return_value
        mock_response.json.return_value = test_payload

        # Call the get_json function with the test_url
        result = get_json(test_url)

        # Check that requests.get was called exactly once with the test_url
        mock_get.assert_called_once_with(test_url)

        # Check that the output of get_json is equal to test_payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Parameterize and patch"""

    def test_memoize(self):
        class TestClass:
            """TestClass"""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Create an instance of TestClass
        test_instance = TestClass()

        # Patch a_method
        with patch.object(TestClass, 'a_method') as mock_a_method:
            # Set the return value for a_method
            mock_a_method.return_value = 42

            # Call a_property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Check that a_method was called only once
            mock_a_method.assert_called_once()

            # Check that the results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)


if __name__ == "__main__":
    unittest.main()
