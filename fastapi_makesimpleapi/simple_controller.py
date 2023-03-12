from fastapi import APIRouter

from fastapi_makesimpleapi.utils import make_simple_api
from fastapi_makesimpleapi.simple_service import SimpleService


router = APIRouter(prefix="/simple")


make_simple_api(
    router=router,
    http_method="get",
    url="/get_name",
    klass=SimpleService,
    method_name="get_name",
)
