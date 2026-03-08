prompt = """
Write a concise summary of the following text.
Focus on key ideas and conclusions.

TEXT:
{text}
"""

COMBINE_THIS_PROMPT = """
You are a professional summarizer.

Combine the following summaries into ONE concise summary.
Remove repetition and keep the most important ideas.

SUMMARIES:
{text}

Guidelines:
- Do NOT include introductory phrases such as
"Here's a concise summary combining the key ideas:
"""