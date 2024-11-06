import feedparser
import git
import os

# Velog RSS URL
# example : rss_url = 'https://api.velog.io/rss/@[velogid]'
rss_url = 'https://api.velog.io/rss/@minisong'

# GitHub repository path
repo_path = '.'

# Path to 'velog-posts' folder
posts_dir = os.path.join(repo_path, 'velog-posts')

# Create 'velog-posts' folder if it does not exist
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# Load the repository
repo = git.Repo(repo_path)

# Parse the RSS feed
feed = feedparser.parse(rss_url)

# Save each post as a file and commit
for entry in feed.entries:
    # Remove or replace invalid characters in file name
    file_name = entry.title
    file_name = file_name.replace('/', '-')  # Replace slash with dash
    file_name = file_name.replace('\\', '-')  # Replace backslash with dash
    # Add additional character replacements if necessary
    file_name += '.md'
    file_path = os.path.join(posts_dir, file_name)

    # Create the file if it does not already exist
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(entry.description)  # 글 내용을 파일에 작성

        # Commit to GitHub
        repo.git.add(file_path)
        repo.git.commit('-m', f'Add post: {entry.title}')

# Push changes to GitHub
repo.git.push()
