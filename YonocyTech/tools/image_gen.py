import os
import httpx
from typing import Optional

async def generate_image_pollinations(prompt: str) -> str:
    """
    Generates an image using Pollinations.ai (Free, no key).
    """
    # Pollinations uses a URL-based generation system
    encoded_prompt = prompt.replace(" ", "%20")
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}"

async def generate_image_deepai(prompt: str) -> Optional[str]:
    """
    Generates an image using DeepAI if API key is present.
    """
    api_key = os.getenv("DEEPAI_API_KEY")
    if not api_key:
        return None

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.deepai.org/api/text2image",
                data={"text": prompt},
                headers={"api-key": api_key}
            )
            data = resp.json()
            return data.get("output_url")
    except Exception as e:
        print(f"DeepAI error: {e}")
        return None

async def generate_image(prompt: str, provider: str = "pollinations") -> str:
    """
    Auto-fallback image generation.
    """
    if provider == "deepai":
        res = await generate_image_deepai(prompt)
        if res: return res

    # Default to pollinations
    return await generate_image_pollinations(prompt)
