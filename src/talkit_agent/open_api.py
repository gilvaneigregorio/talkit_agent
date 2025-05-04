import json


class OpenAPI:
    spec: dict

    def load_from_data(self, data: str) -> None:
        """
        Load the OpenAPI specification from a JSON string.
        Args:
            data (str): JSON string containing the OpenAPI specification.
        """
        self.spec = json.loads(data)
        self.validate_spec()

    def load_from_path(self, path: str) -> None:
        """
        Load the OpenAPI specification from a JSON file.
        Args:
            path (str): Path to the JSON file containing the OpenAPI specification.
        """
        with open(path, "r") as f:
            spec_data = json.load(f)
        self.spec = spec_data
        self.validate_spec()

    def validate_spec(self) -> bool:
        """
        Validate the OpenAPI specification.
        Returns:
            bool: True if the specification is valid, False otherwise.
        Raises:
            Exception: If the OpenAPI specification is not valid.
        """
        required_fields = ["openapi", "info", "paths"]
        for field in required_fields:
            if field not in self.spec:
                raise Exception(
                    f"Provided OpenAPI spec is not valid. Missing {field} field."
                )
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
