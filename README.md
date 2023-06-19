# mercor_test
This is a Flask application that analyzes the technical complexity of GitHub repositories. The test.py is the Flask app that handles the API endpoint. There is a threshold that determines the highest complexity. If no repositories were found with high complexity, it returns "No repositories with high technical complexity", else it will give the repo with the complexity score and the insights.
## Software and Tools requirement
1. [Github Account](https://github.com)
2. [VSCODE](https://code.visualstudio.com/)
3.[Pythonanywhere](https://www.pythonanywhere.com)

## Create a new environment

Created from the terminal section and activated using the command

'''
.venv\Scripts\activate.bat
'''

## Install the required libraries

'''
pip install -r requirements.txt
'''

## Set up OpenAI API credentials:

1. Obtain an API key from OpenAI.
2. Replace 'Your-API-KEY' in the code with your actual API key.
## Start the Flask server:

1. python test.py
2. Open the application in your web browser by navigating to http://localhost:5000.
3. Enter a GitHub repository URL and click the "Analyze" button.
4. View the analyzed repository's complexity insights.
   
   ## Deploy the solution using Pythonanywhere


