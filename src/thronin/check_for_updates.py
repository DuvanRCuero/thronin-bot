# check_for_updates.py

import requests
import toml
import sys
from packaging.version import parse as parse_version
import os

# --- Configuration ---
GITHUB_REPO_OWNER = "StevensUneven"
GITHUB_REPO_NAME = "thronin-bot"
# -------------------


def get_local_version():
    """Reads the version from pyproject.toml."""
    try:
        with open("pyproject.toml", "r") as f:
            pyproject_data = toml.load(f)
        return pyproject_data["project"]["version"]
    except FileNotFoundError:
        print("Error: pyproject.toml not found.", file=sys.stderr)
        return None
    except KeyError:
        print(
            "Error: 'version' not found in pyproject.toml [project] section.",
            file=sys.stderr,
        )
        return None
    except Exception as e:
        print(f"Error reading pyproject.toml: {e}", file=sys.stderr)
        return None


def get_github_latest_release_version(owner, repo):
    """Fetches the latest release version from GitHub API."""
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        release_info = response.json()
        # Release tags often start with 'v' (e.g., v1.0.0), so we strip it for comparison
        version_tag = release_info.get("tag_name", "").lstrip("v")
        return version_tag
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub release: {e}", file=sys.stderr)
        return None
    except KeyError:
        print(
            "Error: 'tag_name' not found in GitHub release info. Is there a release?",
            file=sys.stderr,
        )
        return None
    except Exception as e:
        print(
            f"An unexpected error occurred while fetching GitHub release: {e}",
            file=sys.stderr,
        )
        return None


def main():
    local_version_str = get_local_version()
    if not local_version_str:
        sys.exit(1)  # Indicate error

    github_version_str = get_github_latest_release_version(
        GITHUB_REPO_OWNER, GITHUB_REPO_NAME
    )
    if not github_version_str:
        print(
            "Could not retrieve latest GitHub version. Skipping update check.",
            file=sys.stderr,
        )
        sys.exit(0)  # Not an error, just couldn't check

    try:
        local_version = parse_version(local_version_str)
        github_version = parse_version(github_version_str)
    except Exception as e:
        print(
            f"Error parsing version strings: {e}. Local: '{local_version_str}', GitHub: '{github_version_str}'",
            file=sys.stderr,
        )
        sys.exit(1)  # Indicate error

    print(f"Local version: {local_version}")
    print(f"Latest GitHub version: {github_version}")

    if github_version > local_version:
        print("UPDATE_AVAILABLE")  # This string will be parsed by the batch script
        sys.exit(100)  # Custom exit code for update available
    else:
        print("NO_UPDATE_NEEDED")  # This string will be parsed by the batch script
        sys.exit(0)  # Indicate no update needed


if __name__ == "__main__":
    main()
