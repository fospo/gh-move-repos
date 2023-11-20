import os
import time
import sys
import requests
from typing import Dict

# Constants
GH_API_ENDPOINT = "https://api.github.com"
GH_URL = "https://github.com"
SLEEP_TIME = 0.5


def transfer_repository(source_org: str, dest_org: str, repo_name: str, access_token: str) -> bool:
    """Transfer repo via API, return status"""
    """See https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#transfer-a-repository"""
    url = f"{GH_API_ENDPOINT}/repos/{source_org}/{repo_name}/transfer"
    headers = {"Authorization": f"token {access_token}"}
    data = {"new_owner": dest_org}

    return requests.post(
        url,
        headers=headers,
        json=data,
    ).status_code == 202


def transfer_check(dest_org: str, repo_name: str) -> bool:
    """Check status of transfer, if it's done it should return 200"""
    url = f"{GH_URL}/{dest_org}/{repo_name}"
    for _ in range(5):  # let's try 5 times
        if requests.get(url).ok:
            return True
        time.sleep(SLEEP_TIME)

    return False


def print_results(transfer_results: Dict[str, bool]) -> None:
    """Print results of transfer"""
    success = 0
    fail = 0
    print("\n=== Transfer Results: ===")
    for repo_name, result in transfer_results.items():
        if result:
            print(f"{repo_name}: Success")
            success += 1
        else:
            print(f"{repo_name}: Fail")
            fail += 1

    if success + fail == 0:
        print("No repos were transferred")
        sys.exit()

    print("\n=== Transfer Summary: ===")
    print(f"Success: {success}, percentage: {success / (success + fail) * 100:.2f}%")
    print(f"Fail: {fail}, percentage: {fail / (success + fail) * 100:.2f}%")


if __name__ == "__main__":
    """Read repos from file, transfer each of them, double check, print results"""
    if len(sys.argv) != 4:
        sys.exit("Usage: python3 move_repos.py source_org dest_org file_name")

    source_org, dest_org, file_name = sys.argv[1:]

    access_token = os.getenv("GH_TOKEN")
    assert (
        access_token
    ), "GH_TOKEN is not set. Check your GH_TOKEN env variable."

    with open(file_name, "r") as fIn:
        repo_names_list = [line.strip().split(',')[0] for line in fIn.readlines()]

    transfer_results = {}
    for repo_name in repo_names_list:
        transfer_results[repo_name] = transfer_repository(
            source_org, dest_org, repo_name, access_token
        )
        if transfer_results[repo_name]:
            transfer_results[repo_name] = transfer_check(dest_org, repo_name)

    print_results(transfer_results)
    sys.exit()
