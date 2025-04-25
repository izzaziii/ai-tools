class Prompt:
    """
    Utility class to create structured prompts for OpenAI API.

    Example:
        builder = PromptBuilder(
            role="data analyst",
            instructions="analyze the dataset and provide insights",
            reasoning_steps="Think step-by-step before writing the report.",
            output_format="Limit your report to a maximum of 300 words.",
            context="This is a telecommunications company dataset."
        )
        prompt = builder.create_prompt()
        print(prompt)
    """

    def __init__(
        self,
        role: str,
        instructions: str,
        reasoning_steps: str,
        output_format: str,
        context: str,
        detailed_instructions: str = None,
        examples: str = None,
    ) -> None:
        """
        Initialize PromptBuilder.

        Args:
            role (str): The role of the AI (e.g., "data analyst").
            instructions (str): Instructions for the task.
            reasoning_steps (str): Steps to follow in reasoning.
            output_format (str): Desired format of the output.
            context (str): Contextual information about the task.
            detailed_instructions (str, optional): Additional detailed instructions.
            examples (str, optional): Examples to illustrate the task.
        """
        self.role = role
        self.instructions = instructions
        self.reasoning_steps = reasoning_steps
        self.output_format = output_format
        self.context = context
        self.examples = examples

    def create_prompt(self) -> str:
        """
        Create a formatted prompt string.

        Returns:
            str: Formatted prompt string.

        Raises:
            ValueError: If prompt creation fails.
        """
        try:
            parts = [
                f"Assume the role of a {self.role}.",
                f"Your task is to {self.instructions}.",
            ]
            parts.append(self.reasoning_steps)
            if self.examples:
                parts.append(self.examples)
            parts.append(self.output_format)
            parts.append(f"Context: {self.context}")
            return "\n\n".join(parts)
        except Exception as e:
            raise ValueError(f"Error creating prompt: {e}")


if __name__ == "__main__":
    builder = Prompt(
        role="data analyst",
        instructions="analyze the dataset and provide insights",
        reasoning_steps="Think step-by-step before writing the report.",
        output_format="Limit your report to a maximum of 300 words.",
        context="This is a telecommunications company dataset.",
    )
    print(builder.create_prompt())
