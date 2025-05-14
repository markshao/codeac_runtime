import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

notebook_path = 'notebook/demo.ipynb'
with open(notebook_path) as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(
    timeout=600,
    kernel_name='python3',
    allow_errors=True,
    extra_arguments=['--InteractiveShell.ast_node_interactivity=all']
)

resources = {
    'metadata': {
        'path': os.path.dirname(os.path.abspath(notebook_path))
    }
}

for index, cell in enumerate(nb.cells):
    if cell.cell_type == 'code':
        try:
            # 修正这里 - 直接传递resources而不是{resources}
            ep.preprocess_cell(cell, resources, index)
            print(f"成功执行 cell {index}: {cell.source[:50]}...")
        except Exception as e:
            print(f"执行 cell {index} 失败: {e}")
            print(str(e))

with open(notebook_path, mode='wt') as f:
    nbformat.write(nb, f)
