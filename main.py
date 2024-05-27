"""
the plan is that it should be possible for someone to instantiate a sample agent

the input is always a question of the user first. like convert me the file to pdf

i started building the agent from scratch lets see where i land. this is going to be good
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


def main():
    """
    user input like "convert me the file to pdf"

    the first step is to make a good planning

    the planning agent needs to return a list of action items
    """
    agent = PlannerAgent()
    plan = agent.generate_plan("convert me the file to pdf")
    print(plan)
    pass


class Brain:
    def __init__(self, messages):
        self.messages = messages
        self.model = "gpt-3.5-turbo"
        self.response = self.make_request()

    def make_request(self):
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        chat_completion = client.chat.completions.create(
            messages=self.messages,
            model=self.model,
        )
        return chat_completion.choices[0].message.content


class PlannerAgent:
    def __init__(self, user_input):
        self.user_input = user_input
        self.plan = self.generate_plan()
        self.steps = self.extract_plan()

    def generate_plan(self):
        prompt = f"""
        You are a helpful assistant. Your goal is to create a plan with clear steps on how to get the task done that is given to you. Here is the task:

        {self.user_input}

        Please provide a plan:
        """
        messages = [
            {
                "role": "system",
                "content": prompt
            }
        ]
        brain = Brain(messages)
        response = brain.response
        return response

    def extract_plan(self):
        prompt = f"""
        Extract the plan from the following text:

        {self.plan}

        Store each step of the plan in a list like this:

        [
        "Step 1",
        "Step 2",
        "Step 3"
        ]

        ONLY return the list and nothing else.
        """
        messages = [
            {
                "role": "system",
                "content": prompt
            }
        ]
        brain = Brain(messages)
        response = brain.response
        return response

    def __repr__(self):
        return self.steps

# Example usage:
if __name__ == "__main__":
    agent = PlannerAgent("convert me the file to pdf")
    print(agent)