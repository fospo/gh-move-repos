# Move GitHub Repositories via API

This script automates the process of transferring repositories from one GitHub
organization to another via the GitHub API.

## Prerequisites

* Python 3.6 or higher
* A personal access token.
Github recommends the following:

```
If you have owner permissions in an organization or admin permissions to one of
its repositories, you can transfer a repository owned by your organization to
your personal account or to another organization.
```

## Usage

1. Clone or download this repository.
2. (optional) Install a virtualenv `python3 -m virtualenv .venv` and then
   `source .venv/bin/activate`
3. Install the required packages via pip: `pip install -r requirements.txt`
4. Set your GitHub token as an environment variable `GH_TOKEN`.
5. Prepare a file with a list of repository names, one per line.
6. Run the script with the following command:

```
python3 move_repos.py source_org dest_org file_name
```

Where `source_org` is the name of the source organization, `dest_org` is the
name of the destination organization, and `file_name` is the name of the file
with the repository names.

## Functionality

The script performs the following steps for each repository:

1. Transfer the repository from the source organization to the destination
   organization via the GitHub API.
2. Double check the transfer status by querying the new repository URL.
3. Record the transfer result (success or fail).

After transferring all repositories, the script prints a summary of the
transfer results.

:warning: The API call is aynchronous, meaning that it will return as soon as
possible and then the transfer continues in the background. As of today, Github
does not have a predetermined time for this task to complete so the check at
point 2 _may_ fail, especially if the repository is quite large. Increasing the
`SLEEP_TIME` constant might do the trick. 

