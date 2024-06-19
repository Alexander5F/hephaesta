import os
import shutil
import json
import ast
import mimetypes
import logging
from git import Repo, GitCommandError
import weaviate
from openai import OpenAI
from dotenv import load_dotenv
from gpt_response import gpt_response

# FUNCTIONS IN THIS FILE:
# clone_repo
# is_text_file
# extract_ast_details
# extract_codebase_structure_v2_and_store
# search_codebase
# create_schema

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Weaviate client configuration
client = weaviate.Client(
    url="https://hephaesta-weaviate-6znke700.weaviate.network",
    auth_client_secret=None
)

openai_client = OpenAI(api_key=openai_api_key)

def clone_repo(repo_url, clone_dir='cloned_repo'):
    logging.debug(f"Attempting to clone repository: {repo_url}")
    try:
        if os.path.exists(clone_dir):
            logging.info(f"Directory {clone_dir} already exists, skipping cloning.")
            return clone_dir

        logging.info(f"Cloning repository {repo_url} into {clone_dir}")
        Repo.clone_from(repo_url, clone_dir)
        return clone_dir
    except GitCommandError as e:
        logging.error(f"Failed to clone repository: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

def is_text_file(filepath):
    """Check if the file is a text file or specific recognized type."""
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type and mime_type.startswith('text'):
        return True
    file_ext = os.path.splitext(filepath)[1]
    return file_ext in ['.py', '.html', '.json', '.md', '.txt', '.yaml', '.yml', '.js', '.css']

def extract_ast_details(tree):
    logging.debug("Extracting AST details")
    imports = []
    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            imports.append({
                'module': node.names[0].name,
                'alias': node.names[0].asname
            })
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_start_line = node.lineno
            func_end_line = max((n.lineno for n in ast.walk(node) if hasattr(n, 'lineno')), default=func_start_line)
            loc = func_end_line - func_start_line + 1

            functions.append({
                'name': node.name,
                'args': [arg.arg for arg in node.args.args],
                'calls': [
                    n.func.id for n in ast.walk(node)
                    if isinstance(n, ast.Call) and hasattr(n.func, 'id')
                ],
                'loc': loc
            })
        elif isinstance(node, ast.ClassDef):
            classes.append({
                'name': node.name,
                'methods': [{
                    'name': n.name,
                    'args': [arg.arg for arg in n.args.args],
                    'calls': [
                        call.func.id for call in ast.walk(n)
                        if isinstance(call, ast.Call) and hasattr(call.func, 'id')
                    ],
                    'loc': max((m.lineno for m in ast.walk(n) if hasattr(m, 'lineno')), default=n.lineno) - n.lineno + 1
                } for n in node.body if isinstance(n, ast.FunctionDef)]
            })

    return imports, functions, classes

def extract_codebase_structure_v2_and_store(root_dir, client):
    logging.debug(f"Extracting codebase structure from directory: {root_dir}")

    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if is_text_file(file_path):
                logging.info(f"Parsing file: {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        tree = ast.parse(f.read(), filename=file_path)
                        imports, functions, classes = extract_ast_details(tree)

                        codefile_data = {
                            "filePath": file_path,
                            "imports": [imp['module'] for imp in imports],
                            "functions": [func['name'] for func in functions],
                            "classes": [cls['name'] for cls in classes]
                        }

                        client.data_object.create(codefile_data, "CodeFile")

                    except SyntaxError as se:
                        logging.warning(f"SyntaxError in file {file_path}: {se}")
                    except Exception as e:
                        logging.error(f"Failed to parse {file_path}: {e}")

    logging.info("Codebase structure extracted and stored in Weaviate.")

#def gpt_response(prompt):
    #response = openai_client.embeddings.create(input=prompt, model="text-embedding-ada-002")
    #return response.data[0].embedding

def search_codebase(prompt):
    search_vector = gpt_response(prompt)
    near_vector = {"vector": search_vector, "certainty": 0.7}
    
    result = (
        client.query
        .get("CodeFile", ["filePath", "imports", "functions", "classes"])
        .with_near_vector(near_vector)
        .with_limit(10)
        .do()
    )

    logging.info(f"Search result: {result}")
    return result

def create_schema(client):
    try:
        schema = {
            "classes": [
                {
                    "class": "CodeFile",
                    "description": "A code file in the repository",
                    "properties": [
                        {
                            "name": "filePath",
                            "dataType": ["string"],
                            "description": "Path to the file"
                        },
                        {
                            "name": "imports",
                            "dataType": ["text[]"],
                            "description": "List of imports in the file"
                        },
                        {
                            "name": "functions",
                            "dataType": ["text[]"],
                            "description": "List of functions in the file"
                        },
                        {
                            "name": "classes",
                            "dataType": ["text[]"],
                            "description": "List of classes in the file"
                        }
                    ]
                }
            ]
        }
        client.schema.create(schema)
    except weaviate.exceptions.UnexpectedStatusCodeException as e:
        if 'class name CodeFile already exists' in str(e):
            logging.info("Class CodeFile already exists, skipping schema creation.")
        else:
            logging.error(f"Unexpected error while creating schema: {e}")

def main():
    github_repo_url = "https://github.com/Alexander5F/hephaesta"

    # Create Weaviate schema
    create_schema(client)

    # Check if the repository is already cloned
    clone_dir = 'cloned_repo'
    if not os.path.exists(clone_dir):
        # Clone the repository if it doesn't exist
        clone_dir = clone_repo(github_repo_url)
    
    if clone_dir:
        # Extract and store codebase structure in Weaviate
        extract_codebase_structure_v2_and_store(clone_dir, client)
    
        # Example search
        prompt = "Find my easter egg'"
        search_results = search_codebase(prompt)
        
        if 'data' in search_results:
            for result in search_results['data']['Get']['CodeFile']:
                print(f"File Path: {result['filePath']}")
                print(f"Imports: {result['imports']}")
                print(f"Functions: {result['functions']}")
                print(f"Classes: {result['classes']}")
                print("\n")
        else:
            logging.error(f"Unexpected search results structure: {search_results}")

if __name__ == "__main__":
    main()
