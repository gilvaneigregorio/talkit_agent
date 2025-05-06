import json
import os
import sys
import tempfile
import unittest

# Get the absolute path to the src directory
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
sys.path.insert(0, src_path)

from talkit_agent.open_api import OpenAPIClient  # noqa: E402


class TestOpenAPIClient(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.valid_spec = {
            "openapi": "3.0.0",
            "info": {"title": "Test API", "version": "1.0.0"},
            "paths": {
                "/test": {
                    "get": {
                        "operationId": "getTest",
                        "summary": "Get test",
                        "description": "Get test description",
                        "parameters": [
                            {
                                "name": "id",
                                "in": "query",
                                "required": True,
                                "schema": {"type": "string"},
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Success",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/TestResponse"
                                        }
                                    }
                                },
                            }
                        },
                    }
                }
            },
            "components": {
                "schemas": {
                    "TestResponse": {
                        "type": "object",
                        "properties": {"result": {"type": "string"}},
                    }
                }
            },
        }
        self.invalid_spec = {"info": {"title": "Test API", "version": "1.0.0"}}

    def test_init_with_valid_spec(self):
        """Test initialization with a valid OpenAPI spec"""
        client = OpenAPIClient(self.valid_spec)
        self.assertEqual(client.spec, self.valid_spec)

    def test_init_with_invalid_spec(self):
        """Test initialization with an invalid OpenAPI spec"""
        with self.assertRaises(Exception):
            OpenAPIClient(self.invalid_spec)

    def test_from_string(self):
        """Test creating an OpenAPIClient from a JSON string"""
        json_string = json.dumps(self.valid_spec)
        client = OpenAPIClient.from_string(json_string)
        self.assertEqual(client.spec, self.valid_spec)

    def test_from_file(self):
        """Test creating an OpenAPIClient from a JSON file"""
        # Create a temporary file with the spec
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            json.dump(self.valid_spec, tmp)
            tmp_path = tmp.name

        try:
            client = OpenAPIClient.from_file(tmp_path)
            self.assertEqual(client.spec, self.valid_spec)
        finally:
            # Clean up the temporary file
            os.unlink(tmp_path)

    def test_validate_spec_valid(self):
        """Test spec validation with a valid spec"""
        client = OpenAPIClient(self.valid_spec)
        self.assertTrue(client.validate_spec())

    def test_validate_spec_invalid(self):
        """Test spec validation with an invalid spec"""
        client = OpenAPIClient.__new__(OpenAPIClient)
        client.spec = self.invalid_spec
        self.assertFalse(client.validate_spec())

    def test_list_operations(self):
        """Test listing all operations in the spec"""
        client = OpenAPIClient(self.valid_spec)
        operations = client.list_operations()
        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0]["path"], "/test")
        self.assertEqual(operations[0]["method"], "get")
        self.assertEqual(operations[0]["summary"], "Get test")
        self.assertEqual(operations[0]["description"], "Get test description")

    def test_get_operation_details(self):
        """Test getting details of a specific operation"""
        client = OpenAPIClient(self.valid_spec)
        details = client.get_operation_details("/test", "get")
        self.assertEqual(details["path"], "/test")
        self.assertEqual(details["method"], "get")
        self.assertEqual(details["operationId"], "getTest")
        self.assertEqual(details["summary"], "Get test")
        self.assertEqual(details["description"], "Get test description")
        self.assertTrue("parameters" in details)
        self.assertTrue("responses" in details)
        self.assertTrue("200" in details["responses"])
        self.assertTrue("resolved_schema" in details["responses"]["200"])

    def test_get_operation_details_by_id(self):
        """Test getting operation details by ID"""
        client = OpenAPIClient(self.valid_spec)
        details = client.get_operation_details_by_id("getTest")
        self.assertEqual(details["path"], "/test")
        self.assertEqual(details["method"], "get")
        self.assertEqual(details["operationId"], "getTest")

    def test_get_operation_details_by_id_not_found(self):
        """Test getting operation details with an invalid ID"""
        client = OpenAPIClient(self.valid_spec)
        with self.assertRaises(ValueError):
            client.get_operation_details_by_id("nonExistentId")

    def test_resolve_ref(self):
        """Test resolving a $ref string to its component"""
        client = OpenAPIClient(self.valid_spec)
        resolved = client.resolve_ref("#/components/schemas/TestResponse")
        self.assertEqual(resolved["type"], "object")
        self.assertTrue("properties" in resolved)
        self.assertTrue("result" in resolved["properties"])

    def test_resolve_ref_invalid(self):
        """Test resolving an invalid $ref string"""
        client = OpenAPIClient(self.valid_spec)
        with self.assertRaises(ValueError):
            client.resolve_ref("invalid/ref/format")


if __name__ == "__main__":
    unittest.main()
