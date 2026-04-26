from typing import Dict
from app.services.template_engine import TemplateEngine
from app.core.logger import get_logger

logger = get_logger(__name__)


class AIService:
    """
    Core AI service for prompt generation and improvement.
    Uses rule-based intent detection + template engine.
    Can be extended with OpenAI/Groq API calls.
    """

    def __init__(self):
        self.template_engine = TemplateEngine()

    def detect_intent(self, user_input: str) -> str:
        """Detect the user's intent from their raw input."""
        input_lower = user_input.lower()

        intent_keywords = {
            "code": ["code", "program", "function", "script", "debug", "fix", "develop"],
            "writing": ["write", "essay", "blog", "article", "story", "content"],
            "analysis": ["analyze", "compare", "evaluate", "review", "assess"],
            "summarize": ["summarize", "summary", "shorten", "brief", "tldr"],
            "brainstorm": ["ideas", "brainstorm", "suggest", "creative", "think"],
            "explain": ["explain", "what is", "how does", "teach", "understand"],
            "marketing": ["marketing", "ad", "campaign", "sales", "copywrite"],
            "data": ["data", "sql", "query", "database", "csv", "excel"],
        }

        for intent, keywords in intent_keywords.items():
            if any(kw in input_lower for kw in keywords):
                return intent

        return "general"


# THIS IS USEFULL WHEN WE USE AI IT WILL IMPROVE THE INPUT TEXT
    def improve_prompt(self, raw_prompt: str, tone: str, style: str) -> str:
        """Apply tone and style improvements to a prompt."""
        tone_map = {
            "professional": "Use a formal, professional tone.",
            "casual": "Use a friendly, conversational tone.",
            "technical": "Use precise technical language.",
            "creative": "Use an imaginative, creative tone.",
        }

        style_map = {
            "detailed": "Provide detailed, step-by-step instructions.",
            "concise": "Keep the response focused and concise.",
            "structured": "Use headers, bullet points, and clear sections.",
        }

        tone_instruction = tone_map.get(tone, tone_map["professional"])
        style_instruction = style_map.get(style, style_map["detailed"])

        improved = (
            f"{raw_prompt}\n\n"
            f"[Tone: {tone_instruction}] "
            f"[Format: {style_instruction}]"
        )
        return improved

    def generate_prompt(
        self,
        user_input: str,
        tone: str = "professional",
        style: str = "detailed",
    ) -> Dict:
        """
        Full pipeline:
        user_input → intent detection → template → improvement → final prompt
        """
        logger.info(f"Generating prompt for input: {user_input[:50]}...")

        # Detect intent
        intent = self.detect_intent(user_input)
        logger.info(f"Detected intent: {intent}")

        # Get template
        template_name, raw_prompt = self.template_engine.build_prompt(
            intent=intent,
            user_input=user_input,
        )

        # Improve with tone/style
        final_prompt = self.improve_prompt(raw_prompt, tone, style)

        return {
            "generated_prompt": final_prompt,
            "detected_intent": intent,
            "template_used": template_name,
        }

    def auto_tag(self, content: str) -> list:
        """Auto-generate tags from prompt content."""
        tech_tags = {
            "python", "javascript", "sql", "api", "machine learning",
            "data science", "marketing", "writing", "analysis", "coding"
        }
        content_lower = content.lower()
        return [tag for tag in tech_tags if tag in content_lower]
