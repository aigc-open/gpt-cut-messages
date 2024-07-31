# gpt-cut-messages

gpt 相关 token 预计算，token 超过长度裁剪至目标长度

## install

```bash
pip install git+https://github.com/aigc-open/gpt-cut-messages.git
```

## gpt_cut_messages

```python
def test_cut_messages():
    from gpt_cut_messages import cut_messages, cut_string, messages_token_count
    question = "hi你是谁呢"*100
    messages=[{"role": "user", "content": question}]*100
    token_limit = 200
    print(messages_token_count(messages,token_limit=200000))
    cut_messages(messages=messages, token_limit=token_limit)
    print(messages)
    print(len(messages))
    print(messages_token_count(messages,token_limit=200000))
```
