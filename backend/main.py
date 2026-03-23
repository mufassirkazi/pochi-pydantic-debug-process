import os
import time

import logfire
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI

from models import ErrorResponse, ImageData, ImageGenerateRequest, ImageGenerateResponse

load_dotenv()

# ── Logfire setup ──────────────────────────────────────────────────────────────
logfire.configure()

# ── OpenAI client ──────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set")

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# ── FastAPI app ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Image Generator",
    description="Generate images from text prompts using OpenAI DALL·E",
    version="1.0.0",
)

logfire.instrument_fastapi(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post(
    "/generate",
    response_model=ImageGenerateResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Generate an image from a text prompt",
)
async def generate_image(request: ImageGenerateRequest):
    """
    Accept a text prompt and return a URL to the AI-generated image.
    """
    with logfire.span("generate_image", prompt=request.prompt):
        logfire.info("Image generation started", prompt=request.prompt)

        start_time = time.perf_counter()

        try:
            response = await openai_client.images.generate(
                model="dall-e-3",
                prompt=request.prompt,
                n=1,
                size="1024x1024",
                quality="standard",
            )
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            logfire.error(
                "OpenAI API error",
                prompt=request.prompt,
                error=str(exc),
                response_time_ms=round(elapsed_ms, 2),
            )
            raise HTTPException(
                status_code=500,
                detail=f"Image generation failed: {exc}",
            )

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        image_url = response.data[0].url if response.data else None
        image_url_exists = image_url is not None

        if not image_url_exists:
            raise HTTPException(
                status_code=500,
                detail="No image URL returned from OpenAI",
            )

        result = ImageGenerateResponse(
            image=ImageData(url=image_url),
            prompt=request.prompt,
            response_time_ms=round(elapsed_ms, 2),
        )

        # Serialise the response to inspect its exact outbound shape
        result_dict = result.model_dump()
        response_keys = list(result_dict.keys())
        response_has_top_level_image_url = "image_url" in result_dict

        logfire.info(
            "Image generation completed",
            # ── request echo ──────────────────────────────────────────
            prompt=request.prompt,
            # ── upstream signal ───────────────────────────────────────
            image_url_exists=image_url_exists,
            # ── outbound contract snapshot ────────────────────────────
            success=True,
            http_status=200,
            response_keys=response_keys,
            response_has_top_level_image_url=response_has_top_level_image_url,
            # ── timing ────────────────────────────────────────────────
            response_time_ms=round(elapsed_ms, 2),
        )

        return result
