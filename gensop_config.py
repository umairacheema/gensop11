import yaml

class GenSOPConfig:
    def __init__(self, file_path=None):
        """Initializes the YAMLHandler with an optional file path.
        
        Args:
            file_path (str, optional): The path to a YAML file. Defaults to None.
        """
        self.file_path = file_path

    def read(self, file_path=None):
        """Reads a YAML file and returns the content as a Python object.
        
        Args:
            file_path (str, optional): The path to the YAML file to read. 
                                        If not provided, uses the instance's file_path.
        
        Returns:
            dict or list: The parsed data from the YAML file.
        
        Raises:
            FileNotFoundError: If the YAML file is not found.
            yaml.YAMLError: If the YAML file cannot be parsed.
        """
        if file_path is None and self.file_path is None:
            raise ValueError("No file path provided.")
        
        file_path = file_path or self.file_path
        
        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)  # Load data from the YAML file
            return data
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            raise
        except yaml.YAMLError as e:
            print(f"Error: Failed to parse the YAML file. {e}")
            raise

    def save(self, data, file_path=None):
        """Saves a Python object as a YAML file.
        
        Args:
            data (dict or list): The data to save to the YAML file.
            file_path (str, optional): The path to save the YAML file. 
                                        If not provided, uses the instance's file_path.
        
        Raises:
            yaml.YAMLError: If there is an error in writing to the YAML file.
        """
        if file_path is None and self.file_path is None:
            raise ValueError("No file path provided for saving.")
        
        file_path = file_path or self.file_path
        
        try:
            with open(file_path, 'w') as file:
                yaml.dump(data, file, default_flow_style=False, sort_keys=False)  # Save as YAML
            print(f"Data successfully saved to '{file_path}'.")
        except yaml.YAMLError as e:
            print(f"Error: Failed to write to the YAML file. {e}")
            raise
