from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def get_openai_client():
    return OpenAI(
        max_retries=2,
        timeout=30.0,
    )