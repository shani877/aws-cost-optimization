# 📊 AWS Cost Optimisation Using `aws-cost-cli`

## 🛠️ Prerequisites

### 1. Update and Install AWS CLI
```bash
sudo apt update
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt-get install unzip -y
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

### 2. Configure AWS CLI
```bash
aws configure
```

---

## 🚀 Install Node.js & `aws-cost-cli`

### 1. Install Node.js using NVM
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

nvm install 22
node -v
```
> ℹ️ Reference: [Node.js Downloads](https://nodejs.org/en/download)

### 2. Install `aws-cost-cli`
```bash
npm install -g aws-cost-cli
```

### 3. Usage Examples
```bash
aws-cost                         # Retrieves total cost breakdown by service
aws-cost --summary               # Displays total cost only
aws-cost --text                  # Outputs the cost report in plain text format
```

---

## 📢 Slack Integration

### ✅ Step 1: Create a Slack App
1. Visit [Slack API - Create App](https://api.slack.com/apps)
2. Click **Create New App** → Choose **From Scratch**
3. Enter App Name: `AWS Cost Notifier`
4. Select your Slack Workspace

### ✅ Step 2: Set Permissions
1. Go to **OAuth & Permissions**
2. Under **Bot Token Scopes**, add:
   - `chat:write`
   - `chat:write.public` *(optional)*
   - `files:write`

### ✅ Step 3: Install the App
1. Click **Install App to Workspace**
2. Approve the permissions
3. Copy the **Bot User OAuth Token** (starts with `xoxb-...`)

### ✅ Step 4: Get Slack Channel ID
1. Open Slack
2. Navigate to your desired channel
3. Click channel name → **View channel details**
4. Copy the **Channel ID** (starts with `C...`)

### ✅ Step 5: Invite Bot to Channel
```bash
/invite @AWS-COST-Report
```

---

## 🐍 Upload Cost Report to Slack using Python

### 1. Install Python and Dependencies
```bash
sudo apt install python3-pip
python3 -m venv venv
source venv/bin/activate
pip install slack-sdk
```

### 2. Create `upload_cost_report.py`
```python
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = "xoxb-your-slack-token-here"
client = WebClient(token=slack_token)

try:
    response = client.files_upload_v2(
        channel="C08PVFZV9PF",  # Replace with your channel ID
        initial_comment="AWS Cost Report",
        file="cost-report.txt"
    )
    print("File uploaded successfully:", response)
except SlackApiError as e:
    print(f"Error uploading file: {e.response['error']}")
```

### 3. Generate and Upload Cost Report
```bash
aws-cost --text > cost-report.txt
python upload_cost_report.py
```

---

Refrence: https://youtu.be/kBs59NlNxys?si=e76XIkZkzyl2r_XO
