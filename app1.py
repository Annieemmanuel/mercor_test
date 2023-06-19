import requests
import json
import openai

# Set up OpenAI API credentials
openai.api_key = 'Your-API-KEY'

def fetch_user_repositories(github_url):
    username = github_url.split("/")[-1]
    api_url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(api_url)

    if response.status_code == 200:
        repositories = response.json()
        return repositories
    else:
        print(f"Failed to fetch repositories. Error: {response.status_code}")

def apply_chunking(content, chunk_size):
    chunks = []
    length = len(content)

    for i in range(0, length, chunk_size):
        chunk = content[i:i+chunk_size]
        chunks.append(chunk)

    return chunks



def evaluate_code_complexity(code):
    prompt_template = "Evaluate the technical complexity of the following code snippet:\n\n{code}\n\nConsider factors such as code readability, algorithmic efficiency, and maintainability. Provide insights and suggestions for improvement."

    
    # Fill in the template with the code
    prompt = prompt_template.format(code=code)

    # Define GPT-3.5 parameters
    model = 'text-davinci-003'
    max_tokens = 200  # Adjust the value based on your requirements

    

    # Prepend or append the prompt to the code
    input_text = f"{prompt}\n\n{code}"  # You can also append the prompt if desired

    # Generate response from GPT
    response = openai.Completion.create(
        engine=model,
        prompt=input_text,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Process the response and extract generated text
    if 'choices' in response and len(response['choices']) > 0:
        generated_text = response['choices'][0]['text']
        return generated_text
    else:
        return "Failed to generate a response."

def fetch_code_from_repository(repo_api_url):
    if repo_api_url is not None:
        response = requests.get(repo_api_url)
        if response.status_code == 200:
            code_files = json.loads(response.content)

            max_complexity_chunk = None
            max_complexity_score = -1

            for code_file in code_files:
                file_name = code_file["name"]
                file_api_url = code_file["download_url"]

                file_response = requests.get(file_api_url)
                if file_response.status_code == 200:
                    file_content = file_response.content
                    

                    # Apply chunking to the file_content
                    chunk_size = 400  # Define your desired chunk size here
                    chunks = apply_chunking(file_content, chunk_size)
                  
                    

                    for chunk in chunks:
                        complexity_insights = evaluate_code_complexity(chunk)
                        print("Chunk:")
                        print(chunk)
                        print("Complexity Insights:")
                        print(complexity_insights)
                        print("----------------------")

                        # Check if the current chunk has a higher complexity score
                        complexity_score = compute_complexity_score(complexity_insights)
                        if complexity_score > max_complexity_score:
                            max_complexity_chunk = chunk
                            max_complexity_score = complexity_score

            if max_complexity_chunk:
                print("Chunk with the highest technical complexity:")
                print(max_complexity_chunk)
                print("Complexity Score:")
                print(max_complexity_score)
            else:
                print("No chunks found with technical complexity.")

        else:
            print(f"Failed to fetch code files for repository. Error: {response.status_code}")
    else:
        print("Invalid repository API URL.")

def compute_complexity_score(complexity_insights):
    # Compute the complexity score based on the length of the insights
    # You can customize the scoring logic as per your requirements
    insight_length = len(complexity_insights)

    if insight_length <= 50:
        return 1  # Low complexity
    elif 50 < insight_length <= 100:
        return 2  # Medium complexity
    else:
        return 3  # High complexity

github_url = "https://github.com/Annieemmanuel"
repositories = fetch_user_repositories(github_url)

max_repo_complexity = None
max_repo_score = -1
max_complexity_chunk = None
max_complexity_score = -1


for repo in repositories:
    repo_name = repo["name"]
    repo_owner = repo["owner"]["login"]
    repo_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"

    if repo_api_url is None:
        print(f"Skipping repository: {repo_name} (No API URL)")
        continue

    fetch_code_from_repository(repo_api_url)

    if max_complexity_score > max_repo_score:
        max_repo_complexity = repo
        max_repo_score = max_complexity_score

if max_repo_complexity:
    print("Repository with the highest technical complexity:")
    print(max_repo_complexity)
    print("Complexity Score:")
    print(max_repo_score)

    # Fetch and print the complexity insights
    #repo_owner = max_repo_complexity["owner"]["login"]
    #repo_name = max_repo_complexity["name"]
    #repo_api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"

    #fetch_code_from_repository(repo_api_url)

    #print("Complexity Insights:")
    #print(complexity_insights)

else:
    print("No repositories found with technical complexity.")
