from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class WordCounterInput(BaseModel):
    """Input Schema for WordCounterTool."""
    text: str = Field(..., description="The next to count words in.")

class WordCounterTool(BaseTool):
    name: str = "Word Counter Tool"
    description: str = "Counts the number of words in a given text."
    args_schema: Type[BaseModel] = WordCounterInput

    def _run(self, text: str) -> int:
        # Count the number of words in text
        word_count = len(text.split())
        return word_count
    
if __name__ == "__main__":
    tool = WordCounterTool()
    test_text = "This is sample text to count the number of words."

    # Run the tool
    result = tool._run(text=test_text)
    print("Word Count:", result)