"""
- [ ] enable planning
- [ ] create class which contains all the functions 

- if the model is not able to find a certain function than it will just return that it didnt found a certain function 

"""
import json
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

    def get_tools(self):
        with open("tools.json", "r") as file:
            tools = json.load(file)
        return tools

    def generate_plan(self):
        prompt = f"""
        You are a helpful assistant. Your goal is to create a plan with clear steps on how to get the task done that is given to you. Here is the task:

        {self.user_input}

        You can only answer with the plan if the task can be done with the functions available in {self.get_tools()}. If you find a function, return the plan; otherwise, return "I am sorry, but I don't have a brain for this."

        Please provide a plan or "I am sorry, but I don't have a brain for this":
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

        If there is no plan, just return an empty list.

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