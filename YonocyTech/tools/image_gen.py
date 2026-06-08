import os
import httpx
from typing import Optional

async def generate_image_pollinations(prompt: str) -> str:
    encoded_prompt = prompt.replace(" ", "%20")
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}"

async def generate_image_deepai(prompt: str) -> Optional[str]:
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

async def generate_image_hf_fal(prompt: str) -> Optional[str]:
    hf_token = os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN")
    if not hf_token:
        return None
    try:
        from huggingface_hub import InferenceClient
        client = InferenceClient(provider="fal-ai", api_key=hf_token)
        image = client.text_to_image(prompt, model="Tongyi-MAI/Z-Image-Turbo")
        return image.filename if hasattr(image, 'filename') else str(image)
    except Exception as e:
        print(f"HF fal-ai error: {e}")
        return None

async def generate_image(prompt: str, provider: str = "pollinations") -> str:
    if provider == "hf-fal":
        res = await generate_image_hf_fal(prompt)
        if res: return res
    if provider == "deepai":
        res = await generate_image_deepai(prompt)
        if res: return res
    return await generate_image_pollinations(prompt)
