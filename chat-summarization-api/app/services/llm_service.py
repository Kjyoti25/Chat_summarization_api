import openai
from typing import List, Dict
from app.config import settings
from tenacity import retry, stop_after_attempt, wait_exponential

openai.api_key = settings.OPENAI_API_KEY

class LLMService:
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_summary(self, messages: List[str]) -> str:
        """Generate conversation summary using OpenAI"""
        try:
            prompt = (
                "Please summarize the following conversation in a concise paragraph. "
                "Highlight key points, decisions made, and action items:\n\n"
                + "\n".join(messages)
            
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"LLM service error: {str(e)}"
            )

    async def generate_insights(self, messages: List[str]) -> Dict:
        """Generate conversation insights"""
        try:
            prompt = (
                "Analyze this conversation and provide:\n"
                "1. Overall sentiment (positive/neutral/negative)\n"
                "2. Top 5 keywords\n"
                "3. Any action items\n"
                "Format as JSON with keys: sentiment, keywords, action_items\n\n"
                + "\n".join(messages))
            
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=300
            )
            
            return json.loads(response.choices[0].message.content.strip())
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"LLM service error: {str(e)}"
            )