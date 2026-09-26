# ITM300 Lab Assessment Scripts

## Running the Script

### 1. Start the AWS Academy Learner Lab

In the Vocareum window:

- Click **Start lab**.
- Click **AWS Details**.
- Click **AWS CLI: Show**.
- Copy the contents of the displayed window.

### 2. Configure AWS Credentials

In the terminal or PowerShell on your computer, paste the copied content into:

```text
~/.aws/credentials
```

For Bash or macOS/Linux:

```bash
mkdir ~/.aws
cat > ~/.aws/credentials
```

Paste the credentials, press **Return**, and then press **Ctrl+D**.

### 3. Install the `rich` Module

If you have not installed it yet:

```bash
python3 -m venv venv
pip install --upgrade pip
pip install rich
```

### 4. Run the Python Script

Run the script with:

```bash
python3 skills_lab_1_assessment.py
```

Alternatively, open the script in VS Code and run it there.

## Save the Output to a File

### Bash

To display the output on the screen and save it to `output.txt`:

```bash
python3 skills_lab_1_assessment.py | tee output.txt
```

### PowerShell

```powershell
python3 script.py | Tee-Object -FilePath "output.txt"
```
