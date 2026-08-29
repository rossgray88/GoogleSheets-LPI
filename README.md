# Setting Up a New Google Sheets API Token

This guide walks through creating a fresh OAuth token file that works with the existing `shotsheet` class for reading Google Sheets data.

## Step 1: Create a Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Click **Select a project → New Project**
3. Give it a name (e.g. `shotsheet-reader`) and click **Create**

## Step 2: Enable the Google Sheets API

1. In the Cloud Console, go to **APIs & Services → Library**
2. Search for **Google Sheets API**
3. Click it, then click **Enable**

## Step 3: Create OAuth Credentials

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth client ID**
3. If prompted, configure the consent screen first (choose **Internal** — this restricts sign-in to accounts on your own Google Workspace org, which is the setup this guide assumes)
4. For **Application type**, choose **Desktop app**
5. Give it a name and click **Create**
6. Click **Download JSON** — save this file as `credentials.json`

## Step 4: Install Required Packages

This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage dependencies. If you don't have it installed, follow the link above, then run:

```bash
uv venv
uv sync
```

- `uv venv` creates a local virtual environment (`.venv`) for this project, isolated from your system Python.
- `uv sync` installs everything listed in `pyproject.toml` (including the packages this guide's scripts need) into that environment.

## Step 5: Generate the Token File

This repo already includes [`Generate_Token.py`](Generate_Token.py), which does the following:

```python
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

with open('token.pickle', 'wb') as token:
    pickle.dump(creds, token)
```

Make sure `credentials.json` (from Step 3) is in the same folder as this script, then run it:

```bash
uv run Generate_Token.py
```

This opens a browser window. Log in with the Google account that has access to the target spreadsheet(s), and approve the requested permission.

> **Troubleshooting:** If you get an error like *"This account belongs to an organization that isn't the app's organization"* even though you're sure you're using the right account, it's likely your system's **default browser** auto-selected the wrong signed-in profile (e.g. a personal account instead of your org account). Copy the URL from the terminal/browser window and open it manually in Chrome, signed in with the correct account, to be sure.

## Step 6: Confirm the Token File Was Created

A file named `token.pickle` should now exist in the folder. This is the file path you'll pass as `tokenloc` when calling `googlesheetsloader`.

## Step 7: Make Sure the Sheet Is Shared

The Google account used in Step 5 needs at least **Viewer** access to any spreadsheet you want to read. Share the sheet with that account if it isn't already.

## Step 8: Test It

This repo includes [`Example_Sheet_Read.py`](Example_Sheet_Read.py), which you can run directly:

```bash
uv run Example_Sheet_Read.py
```

If this prints rows of data, the setup is complete. To point it at a different spreadsheet, edit the `id` argument in the script to your target spreadsheet's ID.

## Notes

- The token is scoped to **read-only** access (`spreadsheets.readonly`), matching the original setup.
- Each person following this guide will have their own project, credentials, and token — nothing here depends on or reuses the original setup.
- `credentials.json` and `token.pickle` both contain sensitive data. Don't commit them to version control or share them outside the team.
