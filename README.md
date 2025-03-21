## 🔔 GitHub → Discord Webhook Notifications

This project uses a custom **Flask-based webhook listener** hosted on a **Google Cloud VM** to send meaningful GitHub events (commits, pull requests, merges) to our **Discord team channel**.

### 🧠 Why Not Send GitHub Events Directly to Discord?

GitHub’s webhook payloads are complex and verbose — filled with raw JSON data about commits, branches, users, diffs, and more. Discord webhooks, on the other hand, expect a **simple message structure** with a `content` field (and optional embeds).

If you try to send GitHub's payloads directly to Discord, Discord will reject or ignore them — they simply speak different "languages."

### 🔁 Middleware: Flask Webhook Listener

To bridge the gap, we run a lightweight **Flask server** that:

1. **Listens for GitHub webhook events** (like pushes, PRs, merges)
2. **Parses & filters the payloads** to avoid noise (e.g., spammy merge commits)
3. **Formats clean, readable messages**
4. **Sends them to Discord** using its webhook API

### 🧱 Event Types We Handle

| GitHub Event        | Purpose                                         |
|---------------------|-------------------------------------------------|
| `push`              | Notifies on new commits across all branches     |
| `pull_request`      | Notifies when a new PR is opened                |
| `merge_group`       | Notifies when a branch is merged into another   |

> ✅ Only relevant details are forwarded. No clutter. No spam.

---

### 🛠️ Tech Stack

- **Python 3** & **Flask**: lightweight webhook handler
- **Google Cloud VM**: always-on deployment
- **Discord Webhook**: delivers updates to our channel

---

### 🔐 Security Notes

- Discord webhook URLs are **not publicly exposed**.
- GitHub webhook traffic is **filtered and controlled** by our own code.
- Optional: GitHub secret tokens can be added to validate authenticity.

---

### 📡 Want to Try It?

Make a commit, open a pull request, or trigger a merge.  

---

Want to contribute or improve the webhook flow? PRs are welcome!

