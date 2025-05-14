import os
import json
import nbformat
from jupyter_server.services.contents.filemanager import FileContentsManager
from IPython.core.interactiveshell import InteractiveShell


class IPyruntime:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.contents_manager = FileContentsManager(root_dir=root_dir)
        with open("./core/default_notebook.json", "r") as f:
            self.default_notebook = json.load(f)
        self.notebook_cache = dict()
        self.runtime = InteractiveShell.instance()

    def create_notebook(self, notebook_path, source_code):
        if notebook_path in self.notebook_cache:
            with open(self.notebook_cache[notebook_path], "r") as f:
                content = json.load(f)
        else:
            content = self.default_notebook.copy()
        # create_file
        content["cells"].append(
            {
                "id": 0,
                "cell_type": "code",
                "source": source_code,
                "execution_count": 0,
                "metadata": {},
                "outputs": [],
            }
        )
        self.contents_manager.save(
            {"type": "notebook", "content": self.default_notebook},
            notebook_path,
        )
        # write cache
        if not notebook_path in self.notebook_cache:
            self.notebook_cache[notebook_path] = notebook_path
        return notebook_path

    def execute_notebook(self, notebook_path):
        nbpath = os.path.join(self.root_dir, notebook_path)
        with open(nbpath) as f:
            nb = nbformat.read(f, as_version=4)
        for index, cell in enumerate(nb.cells):
            if cell.cell_type == "code":
                try:
                    result = self.runtime.run_cell(
                        cell.source, store_history=True)
                    if result.result is not None:
                        output = nbformat.v4.new_output(
                            output_type="execute_result",
                            data={"text/plain": str(result.result)},
                            execution_count=index + 1
                        )
                        cell.outputs = [output]
                except Exception as e:
                    print(f"执行 cell {index} 失败: {e}")
                    print(str(e))

        with open(nbpath, 'w') as f:
            nbformat.write(nb, f)

# runtime = IPyruntime("/Users/markshao/wspace/codeac_runtime/notebook")
# runtime.create_notebook("demo3.ipynb", "print('hello world')")
