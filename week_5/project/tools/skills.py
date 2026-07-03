from skills.loader import load_skill


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "load_skill",
            "description": (
                "Load the full instructions for a skill. "
                "Use this when the user asks to perform a workflow "
                "that matches one of the available skills."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": (
                            "The name of the skill to load."
                        )
                    }
                },
                "required": [
                    "name"
                ]
            }
        }
    }
]
