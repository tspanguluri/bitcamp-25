from fastapi import APIRouter, status

router = APIRouter()

@router.get(
    "/chatgpt",
    status_code=200,
    # response_model=#Create Response Model
)
def generate_chatgpt_stuff():
    #do chatgpt stuff