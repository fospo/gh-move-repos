#!/bin/bash
# This script transfers all repositories from one GitHub organization to another.

function transfer_repository_with_gh() {
    source_org=$1
    dest_org=$2
    repo_name=$3

    gh repo transfer $dest_org --repo $source_org/$repo_name -y

    # Check if transfer was successful
    owner=$(curl -s -H "Authorization: token $GH_TOKEN" "https://api.github.com/repos/$dest_org/$repo_name" | jq -r .owner.login)
    if [[ $owner == $dest_org ]]; then
        echo "Transfer of $repo_name to $dest_org was successful."
    else
        echo "Transfer of $repo_name to $dest_org failed."
    fi
}

source_org=$1
dest_org=$2

# Read from stdin (pipe) or from file
while IFS= read -r repo; do
    transfer_repository_with_gh $source_org $dest_org $repo
done