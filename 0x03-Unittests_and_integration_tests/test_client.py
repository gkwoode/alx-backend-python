#!/usr/bin/env python3
"""Parameterize and patch as decorators"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from parameterized import parameterized_class
from fixtures import org_payload
from fixtures import repos_payload
from fixtures import expected_repos
from fixtures import apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Parameterize and patch as decorators"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.GithubOrgClient.get_json')
    def test_org(self, org_name, mock_get_json):
        """summary"""

        # Set the expected return value of get_json
        expected_return_value = {"login": org_name}

        # Set the return value for mock_get_json
        mock_get_json.return_value = expected_return_value

        # Create a GithubOrgClient instance with the org_name
        github_org_client = GithubOrgClient(org_name)

        # Call the org method
        result = github_org_client.org

        # Check that get_json was called
        # exactly once with the expected argument
        mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}")

        # Check that the result is correct
        self.assertEqual(result, expected_return_value)

    @patch('client.GithubOrgClient.org', new_callable=property)
    def test_public_repos_url(self, mock_org):
        """summary"""

        # Set the expected org payload
        expected_payload = {
                "repos_url": "https://api.github.com/orgs/example/repos"}

        # Set the return value for mock_org (GithubOrgClient.org)
        mock_org.return_value = expected_payload

        # Create a GithubOrgClient instance with any org_name (example)
        github_org_client = GithubOrgClient("example")

        # Access the _public_repos_url property
        public_repos_url = github_org_client._public_repos_url

        # Check that the result is the expected one based on the mocked payload
        self.assertEqual(public_repos_url, expected_payload["repos_url"])

    @patch('client.GithubOrgClient.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=property)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """summary"""

        # Set the expected repos payload
        expected_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        # Set the return value for mock_public_repos_url
        # (GithubOrgClient._public_repos_url)
        mock_public_repos_url.return_value = (
                "https://api.github.com/orgs/example/repos")

        # Set the return value for mock_get_json (GithubOrgClient.get_json)
        mock_get_json.return_value = expected_payload

        # Create a GithubOrgClient instance with any org_name (example)
        github_org_client = GithubOrgClient("example")

        # Call the public_repos method
        repos = github_org_client.public_repos()

        # Check that GithubOrgClient._public_repos_url was called once
        mock_public_repos_url.assert_called_once()

        # Check that GithubOrgClient.get_json was called once
        mock_get_json.assert_called_once()

        # Check that the list of repos is
        # what we expect from the chosen payload
        self.assertEqual(repos, expected_payload)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """summary"""

        # Set the return value for GithubOrgClient.public_repos
        with patch('client.GithubOrgClient.public_repos') as mock_public_repos:
            mock_public_repos.return_value = [repo]

            # Create a GithubOrgClient instance with any org_name (example)
            github_org_client = GithubOrgClient("example")

            # Call the has_license method
            result = github_org_client.has_license(license_key)

            # Check that GithubOrgClient.public_repos was called once
            mock_public_repos.assert_called_once()

            # Check that the result is the expected one
            self.assertEqual(result, expected_result)


@parameterized_class(
        "org_payload", "repos_payload", "expected_repos", "apache2_repos")
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test: fixtures"""

    @classmethod
    def setUpClass(cls):
        """summary"""

        # Patch requests.get and mock the JSON responses
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Set the side effect for requests.get(url).json()
        cls.mock_get.side_effect = [
            cls.org_payload,  # Mock for GithubOrgClient.org
            cls.repos_payload  # Mock for GithubOrgClient.public_repos
        ]

    @classmethod
    def tearDownClass(cls):
        """summary"""

        # Stop the patcher
        cls.get_patcher.stop()

    def setUp(self):
        """summary"""

        # Create a GithubOrgClient instance with any org_name (example)
        self.github_org_client = GithubOrgClient("example")

    def test_public_repos(self):
        """summary"""

        # Set the return value for requests.get(url).json()
        self.mock_get.side_effect = [
            self.org_payload,  # Mock for GithubOrgClient.org
            self.repos_payload  # Mock for GithubOrgClient.public_repos
        ]

        # Call the public_repos method
        repos = self.github_org_client.public_repos()

        # Check that requests.get was called twice with the correct URLs
        self.mock_get.assert_called_with("https://api.github.com/orgs/example")
        self.mock_get.assert_called_with(
                "https://api.github.com/orgs/example/repos")

        # Check that the result is the expected_repos list
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """summary"""

        # Set the return value for requests.get(url).json()
        self.mock_get.side_effect = [
            self.org_payload,  # Mock for GithubOrgClient.org
            self.repos_payload  # Mock for GithubOrgClient.public_repos
        ]

        # Call the public_repos method with the license_key "apache-2.0"
        repos = self.github_org_client.public_repos("apache-2.0")

        # Check that requests.get was called twice with the correct URLs
        self.mock_get.assert_called_with("https://api.github.com/orgs/example")
        self.mock_get.assert_called_with(
                "https://api.github.com/orgs/example/repos")

        # Check that the result is the apache2_repos list
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
