from typing import Tuple, Dict
from app.core.logger import get_logger

logger = get_logger(__name__)


class TemplateEngine:
    """
    Structured prompt generation using predefined templates.
    Each template is tailored for a specific intent category.
    """

    TEMPLATES: Dict[str, str] = {
        "code": (
            "You are an expert software engineer.\n"
            "Task: {user_input}\n\n"
            "Requirements:\n"
            "- Write clean, well-documented code\n"
            "- Handle edge cases and errors\n"
            "- Follow best practices and design patterns\n"
            "- Explain your implementation\n\n"
            "Output: Provide complete, working code with comments."
        ),
        "writing": (
            "You are a professional content writer.\n"
            "Task: {user_input}\n\n"
            "Requirements:\n"
            "- Engaging and well-structured content\n"
            "- Clear introduction, body, and conclusion\n"
            "- Appropriate vocabulary and flow\n"
            "- Original and compelling writing\n\n"
            "Output: Complete, polished written content."
        ),
        "analysis": (
            "You are a critical thinking expert and analyst.\n"
            "Task: {user_input}\n\n"
            "Requirements:\n"
            "- Thorough and objective analysis\n"
            "- Use evidence and logical reasoning\n"
            "- Identify patterns, strengths, weaknesses\n"
            "- Provide actionable insights\n\n"
            "Output: Structured analysis with clear conclusions."
        ),
        "summarize": (
            "You are a professional summarizer.\n"
            "Task: {user_input}\n\n"
            "Requirements:\n"
            "- Capture all key points accurately\n"
            "- Maintain original meaning\n"
            "- Concise without losing important context\n"
            "- Well-organized summary\n\n"
            "Output: Clear, comprehensive summary."
        ),
        "brainstorm": (
            "You are a creative ideation expert.\n"
            "Task: {user_input}\n\n"
            "Requirements:\n"
            "- Generate diverse, innovative ideas\n"
            "- Include both conventional and creative approaches\n"
            "- Brief explanation for each idea\n"
            "- Prioritize feasibility and impact\n\n"
            "Output: Numbered list of creative ideas with brief descriptions."
        ),
        "explain": (
            "You are an expert educator and communicator.\n"
            "Task: {user_input}\n\n"
            "Requirements:\n"
            "- Clear and accessible explanation\n"
            "- Use analogies and examples where helpful\n"
            "- Progress from simple to complex\n"
            "- Address common misconceptions\n\n"
            "Output: Clear explanation suitable for the target audience."
        ),
        "marketing": (
            "You are a world-class marketing strategist.\n"
            "Task: {user_input}\n\n"
            "Requirements:\n"
            "- Compelling and persuasive messaging\n"
            "- Focus on customer value and pain points\n"
            "- Clear call-to-action\n"
            "- Brand-appropriate tone\n\n"
            "Output: Complete marketing copy ready for use."
        ),
        "data": (
            "You are a senior data analyst and database expert.\n"
            "Task: {user_input}\n\n"
            "Requirements:\n"
            "- Accurate and optimized queries/analysis\n"
            "- Handle data quality issues\n"
            "- Explain methodology clearly\n"
            "- Consider performance implications\n\n"
            "Output: Complete solution with explanation."
        ),
        "general": (
            "You are a highly capable AI assistant.\n"
            "Task: {user_input}\n\n"
            "Requirements:\n"
            "- Provide accurate and helpful response\n"
            "- Be thorough yet concise\n"
            "- Use clear and professional language\n"
            "- Organize information logically\n\n"
            "Output: Complete, high-quality response."
        ),
    }
# out put prompt that user wants
    def build_prompt(self, intent: str, user_input: str) -> Tuple[str, str]:
        """
        Build a structured prompt using the appropriate template.
        Returns: (template_name, rendered_prompt)
        """
        template_key = intent if intent in self.TEMPLATES else "general"
        template = self.TEMPLATES[template_key]
        rendered = template.format(user_input=user_input)

        logger.info(f"Built prompt using template: {template_key}")
        return template_key, rendered

    def list_templates(self) -> list:
        """Return all available template names."""
        return list(self.TEMPLATES.keys())
