from typing import Literal
import os
import tiktoken
import time
from loguru import logger
from daily_basic_function import logger_execute_time


@logger_execute_time(doc="tiktoken模型加载: cl100k_base")
def init_tiktoken():
    return tiktoken.get_encoding("cl100k_base")


def messages_token_count(messages, token_limit):
    """Calculate and return the total number of tokens in the provided messages."""
    start_time = time.time()
    tiktoken_encoding = init_tiktoken()
    logger.info(f"加载titoken: {time.time() - start_time}")
    encoding = tiktoken_encoding
    tokens_per_message = 4
    tokens_per_name = 1
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
            if num_tokens > token_limit:
                return num_tokens
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    logger.info(f"messages_token_count time: {time.time() - start_time}")
    return num_tokens


def string_token_count(str):
    """Calculate and return the token count in a given string."""
    tiktoken_encoding = init_tiktoken()
    tokens = tiktoken_encoding.encode(str)
    return len(tokens)


def cut_messages(messages, token_limit):
    message_last = messages[-1]
    if message_last.get("role") == "assistant":
        # 如果最后一个元素是assistant,则不要
        messages.pop()
        message_last = messages[-1]
    while messages_token_count(messages, token_limit) > token_limit:
        messages.pop(0)
    if len(messages) == 0:
        content = message_last.get("content", "")
        content = cut_string(content, token_limit=token_limit)
        message_last["content"] = content
        messages.append(message_last)
    return messages


def cut_string(str, token_limit):
    while string_token_count(str) > token_limit and len(str) > 3:
        str = str[3:]
    return str
