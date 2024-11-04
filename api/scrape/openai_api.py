
import json
from openai import OpenAI
from pydantic import BaseModel


client = OpenAI()

class QuestionOptions(BaseModel):
    question: str
    options: list[str]


def get_question_with_options(website_content: str):
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a  expert ai asistant, I will give you a website's content, please generates a question with multiple-choice options based on the contentThe aim is to classify the visitor’s intent. (For example, if someone enters apple.com, your program should return a question like: 'Which product category are you interested in?' with options such as ' Mac, iPad, iPhone, Watch.' These options should reflect the primary categories or content themes found on the input site. ) (Please return the answer in json format, so I can get them easily programmaticly)"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": website_content
                    }
                ]
            }
        ],
        response_format=QuestionOptions
    )

    message_content = response.choices[0].message.parsed
    format_content = {
        "question": message_content.question,
        "options": message_content.options
    }
    return json.dumps(format_content)
