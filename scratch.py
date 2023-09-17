# Mocking OpenAI's API response
def mock_openai_api(model, messages):
    return {
        "choices": [
            {
                "message": {
                    "content": "Mocked API response based on: "
                    + messages[-1]["content"]
                }
            }
        ]
    }


# Your updated class
class OpenaiChatCompletion:
    def __init__(self, sys):
        self.sys = sys
        self.full_history = [{"role": "system", "content": self.sys}]

    def __call__(self, user_input):
        # Append user's message to full history
        self.full_history.append({"role": "user", "content": user_input})

        # Get the last 5 turns (or fewer if not available)
        last_turns = self.full_history[-5:]

        # Make the API call
        completion = mock_openai_api(model="gpt-3.5-turbo", messages=last_turns)

        # Extract and append the bot's message to full history
        bot_message = completion["choices"][0]["message"]["content"]
        self.full_history.append({"role": "assistant", "content": bot_message})

        return bot_message


# Using the updated class
my_chat = OpenaiChatCompletion(sys="You are a super smart MathBot")

while True:
    user_input = input("Write message here: ")
    response = my_chat(user_input)
    print(f"MathBot: {response}")
