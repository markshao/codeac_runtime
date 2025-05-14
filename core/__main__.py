import random
import string

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.deepseek import DeepSeekProvider

from core.runtime import IPyruntime
from core.utils import extract_code_from_markdown

model = OpenAIModel(
    'deepseek-chat',
    provider=DeepSeekProvider(api_key='sk-91d44bb2cb0b41dc9a03ebf35e60b598'),
)
agent = Agent(model)

runtime = IPyruntime("/Users/markshao/wspace/codeac_runtime/notebook")


def gen_file_name():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.ipynb'


@agent.system_prompt
def codeact_system_prompt():
    with open("./core/system_prompt.md", "r") as f:
        return f.read()


result = (agent.run_sync("9999年之前有多少个闰年"))
source = extract_code_from_markdown(result.output)
notebook_name = gen_file_name()

nb = runtime.create_notebook(notebook_name, source)
runtime.execute_notebook(nb)
