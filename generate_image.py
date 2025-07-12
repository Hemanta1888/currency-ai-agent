from vertexai.vision_models import ImageGenerationModel
from functools import lru_cache


import vertexai
from io import BytesIO
import base64

from settings import get_settings


settings = get_settings()
vertexai.init(project=settings.project_id, location=settings.location)


def generate_currency_image(currency_code: str) -> str:
    """Generate a high-quality image of the specified currency note."""

    model = ImageGenerationModel.from_pretrained(settings.image_generation_model_name)


    prompt = (
        f"A high-resolution, realistic photo of a {currency_code} currency note, "
        f"placed in a culturally relevant setting of the corresponding country. "
        f"The background should include iconic landmarks, traditional elements, or scenery "
        f"that represents the culture. Studio-quality lighting, sharp focus, and natural textures."
    )

    
    response = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        aspect_ratio="1:1",
        guidance_scale=12.0
    )

    image_bytes = response.images[0]._image_bytes
    img_str = base64.b64encode(image_bytes).decode("utf-8")
    return img_str
