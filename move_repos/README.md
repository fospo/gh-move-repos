# Move GitHub Repositories via API

This script automates the process of transferring repositories from one GitHub organization to another via the GitHub API.

## Prerequisites

* Python 3.6 or higher
* A personal access token with repo scope

## Usage

1. Clone or download this repository.
2. Install the required packages via pip: `pip install -r requirements.txt`
3. Set your GitHub token as an environment variable `GH_TOKEN`.
4. Prepare a file with a list of repository names, one per line.
5. Run the script with the following command:

```
python3 move_repos.py source_org dest_org file_name
```

Where `source_org` is the name of the source organization, `dest_org` is the name of the destination organization, and `file_name` is the name of the file with the repository names.

## Functionality

The script performs the following steps for each repository:

1. Transfer the repository from the source organization to the destination organization via the GitHub API.
2. Double check the transfer status by querying the new repository URL.
3. Record the transfer result (success or fail).

After transferring all repositories, the script prints a summary of the transfer results.
