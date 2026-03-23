from pydantic import BaseModel, Field


class ImageGenerateRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Text prompt describing the image to generate",
        examples=["A futuristic city skyline at sunset with flying cars"],
    )


class ImageData(BaseModel):
    url: str = Field(..., description="URL of the generated image")


class ImageGenerateResponse(BaseModel):
    image: ImageData = Field(..., description="Generated image object")
    prompt: str = Field(..., description="The original prompt used for generation")
    response_time_ms: float = Field(
        ..., description="Time taken to generate the image in milliseconds"
    )


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")
