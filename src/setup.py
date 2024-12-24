import ast

class ForStmtCounter(ast.NodeVisitor):
    current_for_node = None
    stmt_count = 0

    def generic_visit(self, node):
        if self.current_for_node:
            if isinstance(node, ast.stmt):
                self.stmt_count += 1

        elif isinstance(node, ast.For):
            self.current_for_node = node
            self.stmt_count = 0

        super().generic_visit(node)

        if node is self.current_for_node:
            print(f"For node contains {self.stmt_count} statements")
            self.current_for_node = None

for_statement_counter = ForStmtCounter()

tree = ast.parse('''
for i in range(10):
    print(i)

for item in items:
    if item == 42:
        print('Magic item found!')
        break
''')


for_statement_counter.visit(tree)


