from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "your_discord_webhook_URL_goes_here"

@app.route("/github-webhook-handler", methods=["POST"])
def github_webhook():
    data = request.json
    event = request.headers.get("X-GitHub-Event")

    # Handle push events (commits)
    if event == "push" and "commits" in data and data["commits"]:
        repo_name = data["repository"]["name"]
        branch = data["ref"].split("/")[-1]

        for commit in data["commits"]:
            commit_id = commit["id"][:7]
            commit_msg = commit["message"]
            commit_url = commit["url"]
            author = commit["author"]["name"]

            discord_message = (
                f"**New commit in `{repo_name}`**\n"
                f"**Branch:** `{branch}`\n"
                f"**Author:** {author}\n"
                f"**Commit:** [{commit_id}]({commit_url})\n"
                f"**Message:** {commit_msg}"
            )

            requests.post(DISCORD_WEBHOOK_URL, json={"content": discord_message})

    # Handle pull_request opened events
    elif event == "pull_request" and data.get("action") == "opened":
        pr = data["pull_request"]
        repo_name = data["repository"]["name"]
        pr_title = pr["title"]
        pr_url = pr["html_url"]
        user = pr["user"]["login"]
        base_branch = pr["base"]["ref"]
        head_branch = pr["head"]["ref"]

        discord_message = (
            f"📦 **New Pull Request in `{repo_name}`**\n"
            f"**From:** `{head_branch}` → `{base_branch}`\n"
            f"**By:** {user}\n"
            f"**Title:** [{pr_title}]({pr_url})"
        )

        requests.post(DISCORD_WEBHOOK_URL, json={"content": discord_message})

    # Handle merge_group events
    elif event == "merge_group":
        repo_name = data["repository"]["name"]
        head_branch = data.get("head_ref", "unknown")
        base_branch = data.get("base_ref", "unknown")
        merge_state = data.get("state", "unknown")
        merge_commit = data.get("merge_commit_sha")

        commit_url = (
            f"{data['repository']['html_url']}/commit/{merge_commit}"
            if merge_commit else "N/A"
        )

        discord_message = (
            f"🔀 **Merge occurred in `{repo_name}`**\n"
            f"**From branch:** `{head_branch}`\n"
            f"**Into branch:** `{base_branch}`\n"
            f"**State:** `{merge_state}`\n"
            f"**Merge Commit:** {commit_url if commit_url != 'N/A' else '*Not available*'}"
        )

        requests.post(DISCORD_WEBHOOK_URL, json={"content": discord_message})

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
