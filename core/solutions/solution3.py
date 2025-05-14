from IPython.core.interactiveshell import InteractiveShell
import nbformat

notebook_path = 'notebook/demo.ipynb'
with open(notebook_path) as f:
    nb = nbformat.read(f, as_version=4)

shell = InteractiveShell.instance()
shell.run_cell(nb.cells[0].source, store_history=True)

print(shell.user_ns["calculator"])
result = shell.run_cell("calculator(100,1000)")

# 可以通过以下属性访问执行结果
print(f"执行成功: {result.success}")
print(f"执行结果: {result.result}")
print(f"错误信息: {result.error_in_exec}")