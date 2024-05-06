from fastapi import APIRouter

router = APIRouter()

@router.get('/health', summary='健康检查', tags=['服务健康'])
def health():
    return {'code':0, 'msg':'success'}