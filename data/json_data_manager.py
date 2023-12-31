import json

from collections import Counter
from datetime import date


class JSONData:
    def __init__(self, filename) -> None:
        self.filename = filename

    def read_json(self, key=None):
        """
        Read data from the JSON file based on a specified key.

        This method reads the JSON file, retrieves the value associated with the provided key, and returns it.
        If no key is provided, return 1. If the key is not found, return 1. If the key is found, return 2.

        Parameters:
        - key (str, optional): The key used to retrieve the data from the JSON file.

        Returns:
        The value associated with the specified key in the JSON file if the key is present, else 1.

        Example:
        >>> json_data = JSONData("data.json")
        >>> result = json_data.read_json("my_key")
        >>> print(result)

        """
        try:
            with open(self.filename, 'r') as json_file:
                data = json.load(json_file)

                if key is not None and key in data:
                    result = data[key]
                    return result
                else:
                    return data

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading data from {self.filename}: {e}")
            return None

    def write_json(self, keys, value):
        """
        Write data to the JSON file using a specified set of keys.

        This method reads the JSON file, modifies the value associated with the specified set of keys, and updates the JSON file with the new data.

        Parameters:
        - keys (list): A list of keys to navigate through the JSON structure to locate the target value.
        - value: The new value to be written to the JSON file.

        Returns:
        A message indicating the successful update of the JSON file.

        Example:
        >>> json_data = JSONData("data.json")
        >>> result = json_data.write_json(["my", "nested", "key"], "new_value")
        >>> print(result)

        """
        try:
            with open(self.filename, 'r+') as json_file:
                data = json.load(json_file)
                nested_dict = data
                for key in keys[:-1]:
                    nested_dict = nested_dict.setdefault(key, {})
                nested_dict[keys[-1]] = value
                json_file.seek(0)
                json.dump(data, json_file, indent=4)
                json_file.truncate()
            return f"'{'/'.join(keys)}' updated in the JSON file"
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading or writing data: {e}")
            return None

    def write_to_interview_sessions(self, main_key, value):
        """
        Update data in the 'interview_sessions' key in the JSON file.

        This method updates the provided key with the new value in the 'interview_sessions' key of the JSON file.

        Parameters:
        - main_key: The key to update in the 'interview_sessions' key.
        - value: The new value to be associated with the key.

        Returns:
        A message indicating the successful update of the JSON file.

        Example:
        >>> json_data = JSONData("data.json")
        >>> result = json_data.write_to_interview_sessions("existing_key", "new_value")
        >>> print(result)

        """
        try:
            with open(self.filename, 'r+') as json_file:
                data = json.load(json_file)

                data["interview_sessions"] = value

                json_file.seek(0)
                json.dump(data, json_file, indent=4)
                json_file.truncate()

            return f"'{main_key}' updated in the 'interview_sessions' key of the JSON file"
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading or writing data: {e}")
            return None


class DateEncoder(json.JSONEncoder):
    """
        Convert date objects to ISO format when encoding to JSON.

        This method is used as part of the JSON encoding process to handle date objects.

        Parameters:
        - obj: The object being encoded.

        Returns:
        If the object is a date, its ISO format representation; otherwise, the default JSON encoding.

        Example:
        >>> json_data = {"date": date(2023, 11, 8)}
        >>> json_string = json.dumps(json_data, cls=DateEncoder)
        >>> print(json_string)

        """

    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)
