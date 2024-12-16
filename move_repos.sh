#!/bin/bash
# This script transfers all repositories from one GitHub organization to another.

function transfer_repository_with_gh() {
    source_org=$1
    dest_org=$2
    repo_name=$3

    echo "Transferring $repo_name from $source_org to $dest_org"

    # Transfer repository via GH CLI
    gh api repos/$source_org/$repo_name/transfer -f new_owner=$dest_org --silent

    # Check if transfer was successful
    # Sleeping a bit to allow transfer to complete
    echo "Checking transfer status..."
    sleep 2
    # Get new owner and test against expected destination
    owner=$(gh api repos/$dest_org/$repo_name --jq '.owner.login')
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