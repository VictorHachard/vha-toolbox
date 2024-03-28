import re
from typing import List, Dict, Union


def find_args(
        input_string: str,
        rules: Dict[str, Dict[str, Union[str, bool]]],
) -> Dict[str, str]:
    """
    Finds arguments in a string based on a dictionary of rules.

    Args:
        input_string (str): The string to search.
        rules (dict): A dictionary where keys are argument names and values are dictionaries containing rules for the argument.

    Returns:
        dict: A dictionary containing the arguments and their values.

    Example:
        >>> find_args('--arg value', {'arg': {'prefix': '--', 'value': True 'required': True, 'type': 'str'}})
        {'arg': 'value'}
        >>> find_args('--arg', {'arg': {'prefix': '--', 'value': False}})
        {'arg': True}
        >>> find_args('--arg1 value1 --arg2 value2', {'arg1': {'prefix': '--', 'value': True, 'required': True, 'type': 'str'}, 'arg2': {'prefix': '--', 'value': True, 'required': True, 'type': 'str'}})
        {'arg1': 'value1', 'arg2': 'value2'}

    Raises:
        ValueError: If a required argument is not found.
    """
    args = {}
    errors = []

    for arg_name, arg_rules in rules.items():
        prefix = arg_rules.get('prefix', '-')
        value = arg_rules.get('value', False)
        required = arg_rules.get('required', False)
        type_ = arg_rules.get('type', 'str')

        if value:
            pattern = f'{prefix}{arg_name}\\s+([^\\s]+)'
        else:
            pattern = f'{prefix}{arg_name}'

        match = re.search(pattern, input_string, re.IGNORECASE)
        if match:
            if value:
                arg_value = match.group(1)
                if type_ == 'int':
                    arg_value = int(arg_value)
                elif type_ == 'float':
                    arg_value = float(arg_value)
                elif type_ == 'bool':
                    arg_value = arg_value.lower() == 'true'
                args[arg_name] = arg_value
            else:
                args[arg_name] = True
        elif required:
            errors.append(f'Argument "{arg_name}" is required.')

        if errors:
            raise ValueError('\n'.join(errors))

    return args
