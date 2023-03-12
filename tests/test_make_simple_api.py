""" Test make simple api."""
import importlib

import pytest
from fastapi import APIRouter
from fastapi.testclient import TestClient
from pydantic import BaseModel

from fastapi_makesimpleapi.utils import make_simple_api
from fastapi_makesimpleapi.main import create_app


class TestMakeSimpleAPI:
    """Test make-simple-api function."""

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        """Setup method."""
        self.test_prefix = "/test"
        self.router = APIRouter(prefix=self.test_prefix, tags=["test"])
        self.app = create_app()

        class TestModule:
            class TestModuleService:
                def service(self, *args, **kwargs):
                    """test service code."""

        importlib.import_module = lambda _: TestModule
        self.test_service_klass = TestModule.TestModuleService

    def test_use_query_param_without_list(self) -> None:
        """Test using basic type query param except list.
        Scenarios:
            1. Valid input
            2. Invalid input
        """

        def service(self, query_str_param: str, query_int_param: int) -> str:
            """Test service."""
            return query_str_param

        self.test_service_klass.service = service

        make_simple_api(
            router=self.router,
            http_method="get",
            url="",
            service_klass=self.test_service_klass,
            method_name="service",
        )
        self.app.include_router(self.router)

        # 1. Valid input
        client = TestClient(self.app)
        response = client.get(
            self.test_prefix,
            params={
                "query_str_param": "test",
                "query_int_param": 1,
            },
        )
        assert response.status_code == 200

        # 2. Missing input
        response = client.get(
            self.test_prefix,
            params={
                "query_str_param": 1,
            },
        )
        assert response.status_code == 422

    def test_with_default_values(self) -> None:
        """Test service method with default values.
        Scenarios:
            1. Without input
            2. With input
        """

        def service(self, query_default_param: bool = True) -> str:
            """Test service."""
            return "TRUE" if query_default_param else "FALSE"

        self.test_service_klass.service = service

        make_simple_api(
            router=self.router,
            http_method="get",
            url="",
            service_klass=self.test_service_klass,
            method_name="service",
        )
        self.app.include_router(self.router)

        # 1. Without input
        client = TestClient(self.app)
        response = client.get(
            self.test_prefix,
        )
        assert response.status_code == 200
        assert response.json() == "TRUE"

        # 1. Without input
        client = TestClient(self.app)
        response = client.get(
            self.test_prefix,
            params={
                "query_default_param": False,
            },
        )
        assert response.status_code == 200
        assert response.json() == "FALSE"

    def test_use_query_param_with_list(self) -> None:
        """Test using basic type query param with list type.
        Scenarios:
            1. Valid input
            2. Invalid input
        """

        def service(self, query_list_param: list[int]) -> list[int]:
            """Test service."""
            return query_list_param

        self.test_service_klass.service = service

        make_simple_api(
            router=self.router,
            http_method="get",
            url="",
            service_klass=self.test_service_klass,
            method_name="service",
        )
        self.app.include_router(self.router)

        # 1. Valid input
        client = TestClient(self.app)
        response = client.get(
            self.test_prefix,
            params={
                "query_list_param": [1, 2, 3],
            },
        )
        assert response.status_code == 200

    def test_use_query_param_with_schema(self) -> None:
        """Test using basic type query param with schema.
        Scenarios:
            1. Valid input
            2. Invalid input
        """

        class TestSchema(BaseModel):
            query_str_param: str
            query_int_param: int

        def service(self, query_schema_param: TestSchema) -> int:
            """Test service."""
            # return query_schema_param
            return 1

        self.test_service_klass.service = service

        make_simple_api(
            router=self.router,
            http_method="post",
            url="",
            service_klass=self.test_service_klass,
            method_name="service",
        )
        self.app.include_router(self.router)

        # 1. Valid input
        client = TestClient(self.app)
        response = client.post(
            self.test_prefix,
            json={
                "query_str_param": "test",
                "query_int_param": 1,
            },
        )
        assert response.status_code == 200

        # 2. Invalid input
        response = client.post(
            self.test_prefix,
            json={
                "query_str_param": "123",
                "query_int_param": "asdf",
            },
        )
        assert response.status_code == 422

    def test_use_path_parameter(self) -> None:
        """Test using path parameter.
        Scenarios:
            1. Valid input
            2. Invalid input
        """

        def service(self, path_param: int) -> int:
            """Test service."""
            return path_param

        self.test_service_klass.service = service

        make_simple_api(
            router=self.router,
            http_method="get",
            url="/{path_param}",
            service_klass=self.test_service_klass,
            method_name="service",
        )
        self.app.include_router(self.router)

        # 1. Valid input
        client = TestClient(self.app)
        response = client.get(
            self.test_prefix + "/1",
        )
        assert response.status_code == 200

        # 2. Invalid input
        response = client.get(
            self.test_prefix + "/test",
        )
        assert response.status_code == 422
