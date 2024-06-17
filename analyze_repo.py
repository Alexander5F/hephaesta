import os
import shutil
import json
import ast
import mimetypes
import logging
from git import Repo, GitCommandError

logging.basicConfig(level=logging.INFO)

def clone_repo(repo_url, clone_dir='cloned_repo'):
    logging.debug(f"Attempting to clone repository: {repo_url}")
    try:
        if os.path.exists(clone_dir):
            logging.warning(f"Directory {clone_dir} already exists, deleting...")
            shutil.rmtree(clone_dir)
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

def extract_codebase_structure_v2(root_dir, temp_file='temp_codebase_v2.json'):
    logging.debug(f"Extracting codebase structure from directory: {root_dir}")
    codebase = {"repo_name": os.path.basename(root_dir), "files": []}

    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if is_text_file(file_path):
                logging.info(f"Parsing file: {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        tree = ast.parse(f.read(), filename=file_path)
                        imports, functions, classes = extract_ast_details(tree)

                        for func in functions:
                            func['calls'] = [
                                {
                                    'function': call,
                                    'file': file_path,
                                    'args_passed': func['args']
                                }
                                for call in func['calls']
                            ]
                        
                        for cls in classes:
                            for method in cls['methods']:
                                method['calls'] = [
                                    {
                                        'function': call,
                                        'file': file_path,
                                        'args_passed': method['args']
                                    }
                                    for call in method['calls']
                                ]
                        
                        file_details = {
                            'file_path': file_path,
                            'imports': imports,
                            'functions': functions,
                            'classes': classes
                        }
                        
                        codebase['files'].append(file_details)
                    except SyntaxError as se:
                        logging.warning(f"SyntaxError in file {file_path}: {se}")
                    except Exception as e:
                        logging.error(f"Failed to parse {file_path}: {e}")

    with open(temp_file, 'w') as tempf:
        json.dump(codebase, tempf, indent=4)
    
    return codebase

def create_json_of_interactions(github_repo_url):
    logging.debug(f"Starting analysis for repo: {github_repo_url}")
    clone_dir = clone_repo(github_repo_url)
    temp_file = 'temp_codebase_v2.json'
    if clone_dir:
        repo_json = extract_codebase_structure_v2(clone_dir, temp_file=temp_file)
        with open('repo_json_for_LLM.json', 'w') as f:
            json.dump(repo_json, f, indent=4)
        logging.info(f"Cleaning up: removing cloned repository directory {clone_dir}")
        shutil.rmtree(clone_dir)
        if os.path.exists(temp_file):
            logging.info(f"Cleaning up: removing temporary file {temp_file}")
            os.remove(temp_file)
        return repo_json
    else:
        logging.error("Cloning failed, skipping analysis.")
        return None

def read_code(repo_json_for_LLM, filename, github_repo_url):
    logging.debug(f"Reading code for file: {filename} from repo JSON.")
    code_details = next((file for file in repo_json_for_LLM['files'] if file['file_path'].endswith(filename)), None)
    if not code_details:
        logging.error(f"File {filename} not found in the repo JSON.")
        return None, None

    clone_dir = clone_repo(github_repo_url)
    if not clone_dir:
        logging.error("Failed to clone the repository to read the code.")
        return None, None

    file_path = os.path.join(clone_dir, filename)
    if not os.path.exists(file_path):
        logging.error(f"File {filename} does not exist in the cloned repository.")
        return None, None

    with open(file_path, 'r', encoding='utf-8') as f:
        code_string = f.read()
        nLOC = len(code_string.splitlines())
    
    logging.info(f"Cleaning up: removing cloned repository directory {clone_dir}")
    shutil.rmtree(clone_dir)

    return nLOC, code_string