import os

from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()


YOUGILE_LOGIN = os.getenv('YOUGILE_LOGIN')
YOUGILE_PASSWORD = os.getenv('YOUGILE_PASSWORD')
assert YOUGILE_LOGIN is not None and YOUGILE_PASSWORD is not None, "Отсутствуют логин и пароль от yougile"


async def run_browser_yougile_agent(task):
    prompt = (
        'Перейди на "https://ru.yougile.com/team/", '
        f'введи логин {YOUGILE_LOGIN} и пароль {YOUGILE_PASSWORD}.\n'
        f'Далее сделай следующее:\n{task}'
    )
    agent = Agent(
        task=prompt,
        llm=ChatOpenAI(model="gpt-4o-mini"),
    )
    result = await agent.run()
    return result


if __name__ == '__main__':
    test_prompt = (
        'перейди во вкладку "My Tasks" '
        'и узнай сколько у меня задач и какие они '
        'в полях "Important tasks" и "Incoming tasks"'
    )

    asyncio.run(run_browser_yougile_agent(test_prompt))
