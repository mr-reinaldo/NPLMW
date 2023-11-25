from fastapi import APIRouter


from api.v1.endpoints import user, device, facts, interfaces, static_route, ping


api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(device.router, prefix="/devices", tags=["devices"])
api_router.include_router(facts.router, prefix="/facts", tags=["NAPALM"])
api_router.include_router(interfaces.router, prefix="/interfaces", tags=["NAPALM"])
api_router.include_router(static_route.router, prefix="/static-routes", tags=["NAPALM"])
api_router.include_router(ping.router, prefix="/ping", tags=["NAPALM"])