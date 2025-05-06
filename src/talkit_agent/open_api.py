import json


class OpenAPIClient:
    spec: dict

    def __init__(self, spec: dict = None) -> None:
        """
        Initialize the OpenAPI instance.
        Args:
            spec (dict, optional): OpenAPI specification. Defaults to None.
        """
        self.spec = spec
        if not self.validate_spec():
            raise Exception("Provided OpenAPI spec is not valid.")

    @classmethod
    def from_string(cls, data: str) -> "OpenAPIClient":
        """
        Create an OpenAPI instance from a JSON string.
        Args:
            data (str): JSON string containing the OpenAPI specification.
        Returns:
            OpenAPI: An instance of the OpenAPI class.
        """
        return cls(json.loads(data))

    @classmethod
    def from_file(cls, path: str) -> "OpenAPIClient":
        """
        Create an OpenAPI instance from a JSON file.
        Args:
            path (str): Path to the JSON file containing the OpenAPI specification.
        Returns:
            OpenAPI: An instance of the OpenAPI class.
        """
        with open(path, "r") as file:
            data = json.load(file)
        return cls(data)

    def validate_spec(self) -> bool:
        """
        Validate the OpenAPI specification.
        Returns:
            bool: True if the specification is valid, False otherwise.
        """
        required_fields = ["openapi", "info", "paths"]
        for field in required_fields:
            if field not in self.spec:
                return False
        return True

    def list_operations(self) -> list:
        """
        List all operations in the OpenAPI specification.
        Returns:
            list: A list of dictionaries containing operation details.
        """
        operations = []
        for path, methods in self.spec.get("paths", {}).items():
            for method, details in methods.items():
                operations.append(
                    {
                        "path": path,
                        "method": method,
                        "summary": details.get("summary", ""),
                        "description": details.get("description", ""),
                    }
                )
        return operations

    def get_operation_details(self, path: str, method: str) -> dict:
        """
        Get details of a specific operation.
        Args:
            path (str): The path of the operation.
            method (str): The HTTP method of the operation.
        Returns:
            dict: A dictionary containing operation details.
        """
        operation = self.spec.get("paths", {}).get(path, {}).get(method, {})
        responses = operation.get("responses", {})
        # Resolve $ref in responses if present
        for status_code, response in responses.items():
            schema = (
                response.get("content", {})
                .get("application/json", {})
                .get("schema", {})
            )
            if "$ref" in schema:
                responses[status_code]["resolved_schema"] = self.resolve_ref(
                    schema["$ref"]
                )
        return {
            "path": path,
            "method": method,
            "operationId": operation.get("operationId", ""),
            "summary": operation.get("summary", ""),
            "description": operation.get("description", ""),
            "parameters": operation.get("parameters", []),
            "responses": responses,
        }

    def get_operation_details_by_id(self, operation_id: str) -> dict:
        """
        Get details of an operation by its ID.
        Args:
            operation_id (str): The ID of the operation.
        Returns:
            dict: A dictionary containing operation details.
        """
        for path, methods in self.spec.get("paths", {}).items():
            for method, details in methods.items():
                if details.get("operationId") == operation_id:
                    return self.get_operation_details(path, method)
        raise ValueError(f"Operation ID {operation_id} not found in spec.")

    def resolve_ref(self, ref: str) -> dict:
        """
        Resolve a $ref string to its corresponding component.
        Args:
            ref (str): The $ref string to resolve.
        Returns:
            dict: The resolved component.
        """
        if not ref.startswith("#/components/"):
            raise ValueError(f"Unsupported $ref format: {ref}")
        ref_path = ref.split("/")[2:]  # Skip "#/" and "components/"
        component = self.spec.get("components", {})
        for part in ref_path:
            component = component.get(part, {})
        return component
