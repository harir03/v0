from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.interface_generator import InterfaceGenerator

router = APIRouter()

class InterfaceGenerationRequest(BaseModel):
    prompt: str
    user_id: str = None

class InterfaceGenerationResponse(BaseModel):
    interface_id: str
    html: str
    css: str
    javascript: str
    components: dict
    success: bool

@router.post("/generate", response_model=InterfaceGenerationResponse)
async def generate_interface(request: InterfaceGenerationRequest):
    """Generate a user interface from a natural language prompt"""
    try:
        result = await InterfaceGenerator.generate_from_prompt(request.prompt)
        return InterfaceGenerationResponse(
            interface_id=result["id"],
            html=result["html"],
            css=result["css"],
            javascript=result["javascript"],
            components=result["components"],
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interface generation failed: {str(e)}")

@router.get("/{interface_id}")
async def get_interface(interface_id: str):
    """Get a previously generated interface"""
    interface = await InterfaceGenerator.get_interface(interface_id)
    if not interface:
        raise HTTPException(status_code=404, detail="Interface not found")
    return interface

@router.put("/{interface_id}/refine")
async def refine_interface(interface_id: str, refinement_prompt: str):
    """Refine an existing interface with additional instructions"""
    try:
        result = await InterfaceGenerator.refine_interface(interface_id, refinement_prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interface refinement failed: {str(e)}")

@router.post("/preview")
async def preview_interface(request: InterfaceGenerationRequest):
    """Generate a quick preview of an interface without saving"""
    try:
        result = await InterfaceGenerator.generate_preview(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preview generation failed: {str(e)}")