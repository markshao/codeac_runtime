def extract_code_from_markdown(markdown_str):
    """
    从Markdown字符串中提取代码部分，去除头尾的```标记
    :param markdown_str: 包含Markdown代码块的字符串
    :return: 提取出的纯代码字符串
    """
    lines = markdown_str.split('\n')
    # 去除开头的```python或```标记
    if lines and lines[0].startswith('```'):
        lines = lines[1:]
    # 去除结尾的```标记
    if lines and lines[-1].startswith('```'):
        lines = lines[:-1]
    return '\n'.join(lines)