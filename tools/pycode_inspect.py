import argparse
import concurrent.futures
from datetime import datetime
import hashlib
import json
import os
import tempfile
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional
from typing import Union

import pandas as pd

MAX_FILENAME_LENGTH = 255

suppressed_messages_ids = [

]

suppressed_symbols_ids = [

]


def file_exists(file_path: str) -> bool:
    """
    Check if the file exists and is a Python file.

    Args:
        file_path (str): The path to the file to be checked.

    Returns:
        bool: True if the file exists and is a Python file, False otherwise.
    """
    return os.path.isfile(file_path) and file_path.endswith('.py')


def parse_pylint(output: str,
                 output_type: str) -> None:
    """
    Parse the specified type of output from pylint analysis.

    Args:
        output (str): The output of pylint analysis.
        output_type (str): The type of output to parse (errors, warnings, info).

    Returns:
        str: The parsed output.
    """
    if output_type == "errors":
        # implementation of parse_pylint_errors function using regular expressions
        pass
    elif output_type == "warnings":
        # implementation of parse_pylint_warnings function using regular expressions
        pass
    elif output_type == "info":
        # implementation of parse_pylint_info function using regular expressions
        pass
    else:
        raise ValueError("Invalid output type specified.")


def parse_pylint_output(output: str) -> str:
    """
    Parse the output of pylint analysis.

    Args:
        output (str): The output of pylint analysis.

    Returns:
        str: The parsed output.
    """
    # implementation of parse_pylint_output function using regular expressions
    pass


def parse_pylint_errors(output: str) -> str:
    """
    Parse the errors from the output of pylint analysis.

    Args:
        output (str): The output of pylint analysis.

    Returns:
        str: The parsed errors.
    """
    # implementation of parse_pylint_errors function using regular expressions
    pass


def parse_pylint_warnings(output: str) -> str:
    """
    Parse the warnings from the output of pylint analysis.

    Args:
        output (str): The output of pylint analysis.

    Returns:
        str: The parsed warnings.
    """
    # implementation of parse_pylint_warnings function using regular expressions
    pass


def parse_pylint_info(output: str) -> str:
    """
    Parse the info messages from the output of pylint analysis.

    Args:
        output (str): The output of pylint analysis.

    Returns:
        str: The parsed info messages.
    """
    # implementation of parse_pylint_info function using regular expressions
    pass


def run_pylint_cmdline(file_path: str):
    """
    Run pylint on the specified file and return the output.

    Args:
        file_path (str): The path to the file to be analyzed.

    Returns:
        str: A tuple containing the stdout and stderr of pylint analysis.

    Raises:
        FileNotFoundError: If the file does not exist.
        subprocess.CalledProcessError: If the pylint command fails.
    """
    if not file_exists(file_path):
        raise FileNotFoundError("File does not exist.")

    try:
        result = subprocess.run(['pylint', '--output-format=json', file_path], stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, text=True)

        # result = subprocess.run(['pylint', file_path], capture_output=True, text=True)
        return result.stdout
    except FileNotFoundError:
        raise FileNotFoundError("File does not exist.")
    except subprocess.CalledProcessError as output:
        raise output


def analyze_file(file_path: str) -> list:
    pylint_result = run_pylint_cmdline(file_path)
    print(file_path)
    print(f"************{file_path} completed**********")
    # flake8_result = run_flake8(file_path)

    pylint_errors = parse_result(pylint_result, file_path, 'Pylint')
    # flake8_errors = parse_result(flake8_result, file_path, 'Flake8')

    # return pylint_errors + flake8_errors
    return pylint_errors


# def run_flake8(file_path: str):
#     """
#     Run flake8 on the specified file and return the output.
#
#     Args:
#         file_path (str): The path to the file to be analyzed.
#
#     Returns:
#         list: The output of flake8 analysis as a list of messages.
#     """
#     try:
#         style_guide = flake8.api.legacy_style_guide.StyleGuide()
#         report = style_guide.check_files([file_path])
#         return [error for error in report]
#     except FileNotFoundError:
#         raise FileNotFoundError("File does not exist.")


def analyze_files(files_to_analyze: list[str],
                  tools: dict,
                  multi_process=False) -> list:
    """
    Analyze multiple files concurrently using executor.map.

    Args:
        files_to_analyze (str): List of file paths to analyze.
        tools (dict): Dictionary of tool name and availability.
        multi_process (bool): Whether to perform multiprocessing or not

    Returns:
        list: List of results from analyzing the files.
    """
    if multi_process:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            try:
                results = executor.map(analyze_file, files_to_analyze)
                return list(results)
            except Exception as e:
                print(f"Error analyzing files: {str(e)}")
                return []
    else:
        return [analyze_file(file_to_analyze) for file_to_analyze in files_to_analyze]


def parse_result(result: str,
                 file_path: str,
                 tool: str) -> list:
    errors = []
    result_json = json.loads(result)
    for item in result_json:
        if 'message' in item and 'module' in item and "type" in item and "message-id" in item and 'symbol' in item:
            message_id = item["message-id"]
            symbol = item["symbol"]
            if message_id in suppressed_messages_ids and symbol in suppressed_symbols_ids:
                errors.append({
                    "file": file_path,
                    "tool": tool,
                    "line": item['line'],
                    "message": item['message'],
                    "module": item['module'],
                    "message-id": message_id,
                    "symbol": symbol
                })
    return errors


def get_files_to_analyze(directory_path: str,
                         file_extension: str = ".py",
                         include_subdirectories: bool = True,
                         last_modified_days: Optional[int] = None) -> list[str]:
    """
    Get a list of file paths to analyze in the given directory.

    Args:
        directory_path: The path of the directory to search for files.
        file_extension: The file extension to filter the files.
        include_subdirectories: Whether to include subdirectories in the search.
        last_modified_days: The number of days to filter files based on their last modified date.

    Returns:
        A list of file paths to analyze, or None if an error occurred.
    """
    file_paths = []
    # handle to exclude folder
    try:
        for file_path in Path(directory_path).rglob(f'*{file_extension}'):
            if not include_subdirectories and file_path.parent != Path(directory_path):
                continue
            if last_modified_days is None or (
                    datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)).days <= last_modified_days:
                file_paths.append(str(file_path))
        return file_paths
    except (PermissionError, FileNotFoundError) as e:
        print(f"Error occurred while getting files to analyze: {str(e)}")
        return file_paths


def is_valid_hash(hash_value: str) -> bool:
    """
    Check if a hash value is valid.

    Args:
        hash_value: The hash value to be checked.

    Returns:
        True if the hash value is valid, False otherwise.
    """
    # Check if the hash value is a valid hash
    pattern = re.compile(r'^[a-fA-F0-9]{32}$')
    if pattern.match(hash_value):
        return True
    else:
        return False


def save_cached_hashes(hashes: list, cache_file: str = "cached_hashes.json") -> None:
    """
    Save the cached hashes to a temporary file.

    Args:
        hashes: A list of hashes to be saved.
        cache_file: The filename of the cache file.

    Returns:
        None
    """
    if not isinstance(hashes, list):
        raise ValueError("Invalid hashes format. Expected a list.")

    invalid_hashes = [hash_value for hash_value in hashes if not isinstance(hash_value, str)]
    if invalid_hashes:
        raise ValueError("Invalid hash format. Expected a valid hash string.")

    if not hashes:
        return

    temp_dir = tempfile.gettempdir()
    cache_path = os.path.join(temp_dir, cache_file)

    try:
        with open(cache_path, "w") as file:
            json.dump(hashes, file)
    except (IOError, json.JSONDecodeError) as e:
        raise ValueError("Error occurred while saving cached hashes.") from e


def load_cached_hashes(cache_file: str = "cached_hashes.json", expire_after: int = None) -> set:
    """
    Load cached hashes from a temporary file, checking for file existence, last modified time, and expiration.

    Args:
        cache_file: The filename of the cache file.
        expire_after: The time in seconds after which the cache should be considered expired.

    Returns:
        set: The set of cached hashes, or an empty set if the cache is not valid.
    """
    temp_dir = tempfile.gettempdir()
    cache_path = os.path.join(temp_dir, cache_file)

    if not os.path.exists(cache_path):
        return set()

    last_modified_time = os.path.getmtime(cache_path)

    if expire_after is not None and (datetime.now().timestamp() - last_modified_time) > expire_after:
        reset_cache()
        return set()

    try:
        with open(cache_path, "r") as file:
            return set(json.load(file))
    except (IOError, json.JSONDecodeError):
        return set()


def reset_cache(cache_file: str = "cached_hashes.json") -> None:
    """
    Reset the cached hashes by deleting the cache file.

    Args:
        cache_file: The filename of the cache file.

    Returns:
        None
    """
    temp_dir = tempfile.gettempdir()
    cache_path = os.path.join(temp_dir, cache_file)

    if os.path.exists(cache_path):
        os.remove(cache_path)


def analyze_directory(directory_path: str,
                      tools: dict,
                      batch_size: int = 50) -> list:
    if not Path(directory_path).is_dir():
        raise ValueError("Invalid directory path")

    # Get all files to analyze
    files_to_analyze = get_files_to_analyze(directory_path)

    # Load previously analyzed file hashes from cache file
    cached_hashes = load_cached_hashes()

    # Filter out files with unchanged content
    files_to_analyze = [file for file in files_to_analyze if calculate_hash(file) not in cached_hashes]

    # Analyze remaining files
    file_batches = [files_to_analyze[i:i + batch_size] for i in range(0, len(files_to_analyze), batch_size)]
    results = [analyze_files(file_batch, tools, multi_process=True) for file_batch in file_batches]

    # Save newly analyzed file hashes to the cache file
    save_cached_hashes([calculate_hash(file) for file in files_to_analyze])

    return results


def calculate_hash(file_path: str, algorithm: str = 'sha256', buffer_size: int = 4096) -> tuple[str, str]:
    """
    Calculate the hash of a file using the specified algorithm.

    Args:
        file_path: The path to the file.
        algorithm: The hashing algorithm to use. Defaults to 'sha256'.
        buffer_size: The size of the buffer used for reading the file. Defaults to 4096.

    Returns:
        A tuple containing the file path and its hash value, or raises an exception if an error occurred.
    """
    try:
        if not Path(file_path).is_file():
            raise ValueError("File does not exist or is not a regular file.")
        if algorithm not in hashlib.algorithms_available:
            raise ValueError("Unsupported hashing algorithm.")
        with open(file_path, 'rb') as file:
            file_hash = hashlib.new(algorithm)
            while True:
                buffer = file.read(buffer_size)
                if not buffer:
                    break
                file_hash.update(buffer)
            file_hash = file_hash.hexdigest()
            return file_path, file_hash
    except Exception as e:
        raise ValueError(f"Error occurred while calculating hash for file {file_path}: {str(e)}")


def valid_filename(value: str) -> str:
    if not is_valid_filename(value):
        raise argparse.ArgumentTypeError("Invalid output filename")
    return value


def validate_directory_path(directory_path: str) -> None:
    if not os.path.exists(directory_path):
        print(f"Invalid directory path: {directory_path}")
        sys.exit(1)


def validate_output_filename(filename: Union[str, bytes]) -> None:
    # Check if the filename is a string or bytes-like object
    if not isinstance(filename, (str, bytes)):
        raise ValueError("Filename should be a string or bytes-like object")

    # Convert filename to string if it's bytes-like (if needed)
    if isinstance(filename, bytes):
        filename = filename.decode()

    if not is_valid_filename(filename):
        print("Invalid output filename")
        sys.exit(1)


def install_tool(tool: str) -> None:
    if sys.platform.startswith('linux'):
        subprocess.run(['sudo', 'apt', 'install', tool])
    elif sys.platform.startswith('win'):
        subprocess.run(['pip', 'install', tool])
    elif sys.platform.startswith('darwin'):
        subprocess.run(['brew', 'install', tool])
    else:
        print(f"Platform '{sys.platform}' not supported for automated installation.")
        print(f"Please install {tool} manually.")
        sys.exit(1)


def is_tool_available(tool: str) -> bool:
    """
    Check if a tool is available.

    Args:
        tool (str): The name of the tool to check.

    Returns:
        bool: True if the tool is available, False otherwise.
    """
    if not isinstance(tool, str):
        return False
    try:
        result = subprocess.run([tool, '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def parse_arguments() -> dict:
    parser = argparse.ArgumentParser(
        description='This script analyzes a directory and saves the results to an Excel file.')
    parser.add_argument('directory_path', help='Path to the directory', type=str)
    parser.add_argument('output_filename', help='Name of the output file', default=sys.stdout)
    parser.add_argument('tools', help='Names of the tools to run', choices=['pylint', 'flake8'], nargs='+',
                        default=['pylint'])
    parser.add_argument('--overwrite', help='Overwrite existing file', action=argparse.BooleanOptionalAction)

    # For debugging purposes, set default arguments
    default_directory = "D:\opt\corestack_projects\heatstack"
    default_output = 'output.xlsx'

    # Simulating command-line arguments
    args = parser.parse_args([
        default_directory,
        default_output,
        'pylint',  # Replace 'pylint' with the tool you want to test
        '--overwrite'  # Include this argument if needed
    ])

    # args = parser.parse_args()

    return vars(args)


def is_valid_filename(filename: str) -> bool:
    """
    Check if the filename is valid.

    Args:
        filename: The name of the file.

    Raises:
        ValueError: If the filename is invalid.

    Returns:
        True if the filename is valid.
    """
    # Check if the filename contains any invalid characters
    if not re.match(r'^[^/\\:*?"<>|]*$', filename):
        raise ValueError("Filename contains invalid characters")

    # Check if the filename is too long
    if len(filename) > MAX_FILENAME_LENGTH:
        raise ValueError("Filename is too long")

    return True


def setup_inspect_tool(args: dict) -> dict:
    """
    set an inspect tool based on the provided arguments and return a dictionary with tool names as keys and their availability as values
    if cmdline not installed system will set default tools

    :param args:
    :return:
    """
    if not isinstance(args, dict):
        raise ValueError("Invalid input. 'args' must be a dictionary.")

    tools_availability = {}
    for tool in args.get("tools", []):
        if not isinstance(tool, str):
            raise ValueError("Invalid input. 'tools' must be a list of strings.")

        is_cmdline_tool_available = False
        tool_available = is_tool_available(tool)
        if not tool_available:
            response = input(f"{tool} is not available. Do you want to install {tool}? (yes/no): ").lower()
            if response == 'yes':
                install_tool(tool)
                is_cmdline_tool_available = is_tool_available(tool)
        tools_availability[tool] = is_cmdline_tool_available

    if any(tools_availability.values()):
        tools_availability["system_tools"] = True

    return tools_availability


def main() -> None:
    args = parse_arguments()
    directory_path = args['directory_path']
    overwrite = args['overwrite']
    output_filename = args['output_filename']
    validate_directory_path(directory_path)
    validate_output_filename(output_filename)
    tools_availability = setup_inspect_tool(args)

    directory_path = os.path.abspath(directory_path)
    analysis_results = analyze_directory(directory_path)
    df = pd.DataFrame(analysis_results)

    mode = 'x' if not overwrite else 'w'
    with open(output_filename, mode) as file:
        df.to_excel(file, index=False)


if __name__ == '__main__':
    main()
