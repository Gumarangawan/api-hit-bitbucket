import requests
from datetime import datetime, timedelta, timezone

# Replace with your Bitbucket username and app password
USERNAME = ''
APP_PASSWORD = ''
# Replace with the target workspace and repository slug
WORKSPACE = ''
REPO_SLUG = ''
BRANCH_NAME = ''  # Replace 'main' with your target branch name

def get_diff_stats(commit_hash):
    """
    Fetch and parse the diff for a specific commit to determine lines added or deleted.
    This function would need to make a request to a hypothetical endpoint or locally
    calculate diff stats, which is not directly supported via Bitbucket API.
    """
    # Pseudocode / Conceptual approach:
    # url = f"https://api.bitbucket.org/2.0/repositories/{WORKSPACE}/{REPO_SLUG}/diff/{commit_hash}"
    # diff_response = requests.get(url, auth=(USERNAME, APP_PASSWORD))
    # Parse the diff_response content to calculate lines added and deleted
    # Return the calculated lines added and deleted
    return 0, 0  # Placeholder return

def get_commits(workspace, repo_slug, branch_name, days_back=28):
    """Fetch and print the list of recent commits for the given repository and branch."""
    url = f'https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/commits/{branch_name}'
    response = requests.get(url, auth=(USERNAME, APP_PASSWORD))

    if response.status_code == 200:
        commits = response.json()
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)

        # Print the header with added LOC and Deleted LOC columns
        header = f"{'Commit Hash':40} {'Author':20} {'Date':20} {'Message':60} {'Added LOC':10} {'Deleted LOC':12}"
        print(header)
        print('-' * len(header))

        for commit in commits['values']:
            commit_date = datetime.strptime(commit['date'], '%Y-%m-%dT%H:%M:%S%z')
            if commit_date > cutoff_date:
                # Here, you would call get_diff_stats to get LOC info
                added_loc, deleted_loc = get_diff_stats(commit['hash'])
                
                # Format each commit row
                row = f"{commit['hash'][:7]:40} {commit['author']['user']['display_name'][:20] if 'user' in commit['author'] else 'Unknown':20} {commit['date'][:10]:20} {commit['message'][:57].replace('\n',' '):60} {added_loc:10} {deleted_loc:12}"
                print(row)
            else:
                break
    else:
        print(f"Failed to fetch commits for branch '{branch_name}'. Status code: {response.status_code}")

if __name__ == '__main__':
    get_commits(WORKSPACE, REPO_SLUG, BRANCH_NAME)
