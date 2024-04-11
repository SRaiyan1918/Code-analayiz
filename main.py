import streamlit as st
import ast

def analyze_code():
    try:
        # Parse the code into an abstract syntax tree (AST)
        tree = ast.parse(code)
    except SyntaxError as e:
        return {
            'error': 'SyntaxError',
            'message': str(e)
        }

    # Analyze code length
    total_lines = len(code.split('\n'))
    total_characters = len(code)

    # Analyze nesting levels
    max_nesting_level = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While, ast.If, ast.With)):
            max_nesting_level = max(max_nesting_level, get_nesting_level(node))

    # Analyze function complexity
    function_complexities = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_complexities[node.name] = calculate_complexity(node)

    # Calculate readability score
    readability_score = calculate_readability(total_lines, max_nesting_level, len(function_complexities))

    # Generate report
    report = {
        'total_lines': total_lines,
        'total_characters': total_characters,
        'max_nesting_level': max_nesting_level,
        'function_complexities': function_complexities,
        'readability_score': readability_score
    }
    return report

def get_nesting_level(node, level=0):
    if hasattr(node, 'body'):
        return max(get_nesting_level(child, level + 1) for child in node.body)
    return level

def calculate_complexity(node):
    try:
        return len(ast.walk(node)) - len(node.args.args) - 1
    except TypeError:
        return 0  # Skip 'generator' nodes

def calculate_readability(total_lines, max_nesting_level, num_functions):
    readability_score = 0
    if total_lines < 100 and max_nesting_level < 3 and num_functions < 10:
        readability_score += 10
    return readability_score

# Streamlit UI
st.title('Code Metrics Analyzer')

code_input = st.text_area('Enter your Python code here:')
if st.button('Analyze'):
    report = analyze_code(code_input)
    if 'error' in report:
        st.error(f"Error: {report['error']}\nMessage: {report['message']}")
    else:
        st.success("Analysis completed!")
        st.write(f"Total lines of code: {report['total_lines']}")
        st.write(f"Total characters: {report['total_characters']}")
        st.write(f"Max nesting level: {report['max_nesting_level']}")
        st.write("Function complexities:")
        for func_name, complexity in report['function_complexities'].items():
            st.write(f" - {func_name}: {complexity}")
        st.write(f"Readability score: {report['readability_score']}")
