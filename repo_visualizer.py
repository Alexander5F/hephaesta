import os
import shutil
import json
import ast
import mimetypes
import logging
from git import Repo, GitCommandError
import pydot
import streamlit as st
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)

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
            imports.append(ast.dump(node))
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
                'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            })

    return imports, functions, classes

def extract_codebase_structure(root_dir):
    logging.debug(f"Extracting codebase structure from directory: {root_dir}")
    codebase = defaultdict(lambda: {'imports': [], 'functions': [], 'classes': []})

    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if is_text_file(file_path):
                logging.info(f"Parsing file: {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        tree = ast.parse(f.read(), filename=file_path)
                        imports, functions, classes = extract_ast_details(tree)
                        codebase[file_path]['imports'].extend(imports)
                        codebase[file_path]['functions'].extend(functions)
                        codebase[file_path]['classes'].extend(classes)
                    except SyntaxError as se:
                        logging.warning(f"SyntaxError in file {file_path}: {se}")
                    except Exception as e:
                        logging.error(f"Failed to parse {file_path}: {e}")
    return codebase

def save_structure_to_json(structure, filename='codebase_struct.json'):
    logging.debug(f"Saving structure to JSON file: {filename}")
    try:
        with open(filename, 'w') as f:
            json.dump(structure, f, indent=4)
        logging.info(f"Codebase structure saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save JSON file: {e}")

def visualize_codebase_structure(structure, output_file='codebase_graph.png'):
    logging.debug("Visualizing codebase structure")
    graph = pydot.Dot(graph_type='digraph', layout='neato', overlap=False, splines=True, resolution=120)
    graph.set_graph_defaults(size="12,12!", dpi="780")

    file_nodes = {}
    function_nodes = {}
    class_nodes = {}
    folder_clusters = defaultdict(list)

    def add_node_and_edges(file, details):
        if file not in file_nodes:
            file_node = pydot.Node(file, shape='box', style='filled', fillcolor='lightgrey', fontsize=16, fontcolor='black', width=3.0, height=0.3)
            graph.add_node(file_node)
            file_nodes[file] = file_node
            folder = os.path.dirname(file)
            folder_clusters[folder].append(file_node)

        for cls in details['classes']:
            cls_label = f"{cls['name']} (Class)"
            if cls_label not in class_nodes:
                class_node = pydot.Node(cls_label, shape='ellipse', style='filled', fillcolor='blue', fontcolor='white', fontsize=20)
                graph.add_node(class_node)
                class_nodes[cls_label] = class_node

            graph.add_edge(pydot.Edge(file_nodes[file], class_nodes[cls_label], color='blue', penwidth=2.0))

            for method in cls['methods']:
                method_label = f"{cls['name']}.{method} (Method)"
                method_node = pydot.Node(method_label, shape='ellipse', style='filled', fillcolor='green', fontcolor='white', fontsize=20)
                graph.add_node(method_node)
                graph.add_edge(pydot.Edge(class_nodes[cls_label], method_node, color='green', penwidth=2.0))

        for func in details['functions']:
            func_label = func['name']  # Modified line
            size = max(func['loc'] / 10.0, 1.0)
            if func_label not in function_nodes:
                function_node = pydot.Node(func_label, shape='circle', style='filled', fillcolor='black', fontcolor='white', fontsize=30, width=size, height=size)
                graph.add_node(function_node)
                function_nodes[func_label] = function_node
            else:
                function_node = function_nodes[func_label]

            graph.add_edge(pydot.Edge(file_nodes[file], function_node, color='purple', penwidth=2.0))

            for call in func['calls']:
                call_label = call  # Modified line
                if call_label not in function_nodes:
                    call_node = pydot.Node(call_label, shape='circle', style='filled', fillcolor='black', fontcolor='white', fontsize=20, width=size, height=size)
                    graph.add_node(call_node)
                    function_nodes[call_label] = call_node
                else:
                    call_node = function_nodes[call_label]

                graph.add_edge(pydot.Edge(function_node, call_node, label=f"args: {', '.join(func['args'])}", labeldistance=2, labelangle=45, color='purple', penwidth=2.0))  # Unchanged line

    # Process the structure in parts to manage memory usage
    for file, details in structure.items():
        add_node_and_edges(file, details)
        if len(graph.get_node_list()) % 100 == 0:  # Periodically write to file to free up memory
            try:
                graph.write_png(output_file)
                logging.info(f"Intermediate visualization saved to {output_file}")
                graph.del_node(file_nodes[file])
                for cls in details['classes']:
                    graph.del_node(class_nodes[f"{cls['name']} (Class)"])
                for func in details['functions']:
                    graph.del_node(function_nodes[f"{func['name']}\nargs: {', '.join(func['args'])}"])
            except Exception as e:
                logging.error(f"Failed to generate intermediate graph: {e}")

    dot_data = graph.to_string()
    logging.debug(f"DOT file content:\n{dot_data}")

    try:
        graph.write_png(output_file)
        logging.info(f"Final visualization saved to {output_file}")
    except Exception as e:
        logging.error(f"Failed to generate final graph: {e}")

def visualiserepo(github_link):
    logging.debug(f"Starting visualization for repo: {github_link}")
    clone_dir = clone_repo(github_link)
    if clone_dir:
        codebase_structure = extract_codebase_structure(clone_dir)
        save_structure_to_json(codebase_structure)
        visualize_codebase_structure(codebase_structure)
        st.image('codebase_graph.png', caption='Codebase Structure Visualization')
    else:
        logging.error("Cloning failed, skipping visualization.")
