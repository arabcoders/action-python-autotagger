import os


def main():
    version_tag = ""

    file = os.environ["INPUT_PATH"] if "INPUT_PATH" in os.environ else None
    if not file:
        raise ValueError("You must provide 'file' to parse the version.")

    regex = os.environ["INPUT_REGEX"] if "INPUT_REGEX" in os.environ else None
    if not regex:
        raise ValueError("You must provide 'regex' to parse the version.")

    with open(file, "r") as f:
        import re

        regex = re.compile(regex)
        for line in f.readlines():
            match = regex.match(line.strip())
            if match:
                version_tag = match.group(1)
                break
        else:
            raise ValueError(f"Could not find a line matching '{regex.pattern}'.")

    prefix = os.environ["INPUT_PREFIX"] if "INPUT_PREFIX" in os.environ else ""
    suffix = os.environ["INPUT_SUFFIX"] if "INPUT_SUFFIX" in os.environ else ""
    version_tag = f"{prefix}{version_tag}{suffix}"
    secret_token = os.environ["INPUT_TOKEN"]
    if "repo_name" in os.environ:
        repository = os.environ["repo_name"]
    else:
        repository = os.environ["GITHUB_REPOSITORY"]

    print(f"Configuration: {version_tag=}, {repository=}, {prefix=}, {suffix=}")

    from github import Github

    g = Github(secret_token)
    repo = g.get_repo(repository)

    for tag in repo.get_tags():
        if tag.name == version_tag:
            print(f"Tag {version_tag} already exists. Skipping.")
            return

    sha = repo.get_commits()[0].sha
    repo.create_git_ref(f"refs/tags/{version_tag}", sha)
    print(f"Created tag {version_tag}.")


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"::error::{e}")
        raise e
