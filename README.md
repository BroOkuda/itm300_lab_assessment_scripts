To run the script
- Start the AWS Academy Learner Lab

On the Vocareum window
- Click on "Start lab"
- Click on "AWS Details"
- Click on "ASW CLI: Show"
- Copy the contet of the displayed window

In the termianl / PowerShell of your computer
- Paste the content of the displayed widown to ~/.aws/credentials as follows:
  - mkdir ~/.aws
  - cat > ~/.aws/credentials
  (paste the content and hit a return key)
  CTRL+D (press CTRL and D keys together)
- Install rich module if you have not installed it yet
  - python3 -m venv venv
  - pip install --upgrade pip
  - pip install rich
- Run this Python script
  - python3 skills_lab_1_assessment.py
  Or 
  - load this script in VS Code and run it
- Run this Pythong script and direcct the output to both the screen and a file
  On bash
    - python3 skills_lab_1_assessment.py | tee output.txt
  On PowerShell
    - python3 script.py | Tee-Object -FilePath "output.txt"
