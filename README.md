# Move GitHub Repositories

You have to migrate your GitHub repositories from one organization to another?
Or maybe you need to bulk move a bunch of archived repositories to a archive-only org without having to click through the web interface?
This script automates the process of transferring repositories from one GitHub
organization to another. It provides two possibilities: a simple BASH script or more versatile a Python implementation. Both check the results after the move. 

## Bash Script
The Bash script uses the gh CLI tool to transfer repositories. It assumes that you are already logged in to gh in your shell environment.

To use the Bash script:

Set your GitHub access token as an environment variable: `export GH_TOKEN=your_github_token`.

Run the script with a text file containing the names of the repositories to transfer: 
`cat repos.txt | ./move_repos.sh <source_org> <dest_org>`

The text file should contain one repository name per line.

Please note that both scripts transfer repositories from a source organization to a destination organization. You should replace source_org and dest_org in the scripts with the names of your source and destination organizations.

```
If you have owner permissions in an organization or admin permissions to one of
its repositories, you can transfer a repository owned by your organization to
your personal account or to another organization.
```

## Python Script
The Python script uses the GitHub API to transfer repositories. It requires a GitHub access token, which should be set as the GH_TOKEN environment variable.

To use the Python script:

Install the required Python packages with pip install -r requirements.txt.
Set your GitHub access token as an environment variable: export GH_TOKEN=your_github_token.
Run the script with a text file containing the names of the repositories to transfer: python move_repos.py repos.txt.

:warning: The API call is aynchronous, meaning that it will return as soon as
possible and then the transfer continues in the background. As of today, Github
does not have a predetermined time for this task to complete so the check at
point 2 _may_ fail, especially if the repository is quite large. Increasing the
`SLEEP_TIME` constant might do the trick. 

## Chaining
It is possible to launch this script from another script. For example, you can chain it in the following way:
    
```bash
python3 crawler.py -i org fospo -o print -f name archived > tmp.txt && \
python3 move_repos.py fospo dest_org tmp.txt && \
rm tmp.txt
```

In this way, for example, you will get all the repositories marked as archived in the organization `fospo` and move them to an organization of your choice.

## Moving archived repos
If you want to get a list of archived repos in a given org and then move them to another org, you can use the following command:

```bash
gh repo list <source_org> --archived --json=name | jq -r '.[] | .name' | ./move_repos.sh <source_org> <dest_org>
```

or via gh api:

```bash
gh api /orgs/<source_org>/repos --paginate | jq -r '.[] | select(.archived == true) | .name' | ./move_repos.sh <source_org> <dest_org>
````


# Licensing
This repo is covered by a MIT License. See the [LICENSE](LICENSE) file for more details.