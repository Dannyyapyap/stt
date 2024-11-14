from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/data",
    tags=["Interface with Database"],
    responses={
        404: {"description": "Not Found"}
    }
)


@router.post("/transcription")
async def get_all_transcription():
    
    try:
        return {"message": "Audio file received successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
        )
        

@router.post("/search")
async def search_all_transcription():
    
    try:
        return {"message": "Audio file received successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
        )