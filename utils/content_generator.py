import os
from openai import OpenAI
from typing import Dict, List, Optional

class ContentGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
        self.model = "gpt-4o"

    def generate_content(self, source_content: Dict, keywords: List[str]) -> Dict:
        """Generate unique content from source material"""
        try:
            prompt = f"""
            Create a unique blog post based on this content:
            Title: {source_content['title']}
            Source Content: {source_content['content']}
            Keywords to include: {', '.join(keywords)}

            Please format the response as a JSON object with the following structure:
            {{
                "title": "SEO optimized title",
                "content": "Generated blog post content with proper formatting",
                "meta_description": "SEO meta description",
                "keywords": "Comma-separated keywords used"
            }}

            Ensure the content is unique, engaging, and optimized for SEO.
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")

    def generate_image_prompt(self, content: Dict) -> str:
        """Generate image prompt based on content"""
        try:
            prompt = f"""
            Based on this blog post title and content, create a detailed image prompt for DALL-E:
            Title: {content['title']}
            Content summary: {content['content'][:200]}

            Generate a creative and specific image description that would work well as a blog header image.
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Error generating image prompt: {str(e)}")

    def generate_image(self, prompt: str) -> Optional[str]:
        """Generate image using DALL-E"""
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                n=1
            )

            return response.data[0].url

        except Exception as e:
            raise Exception(f"Error generating image: {str(e)}")