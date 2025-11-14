import ast
import operator
import sys

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def evaluate_expr(expr: str):
    try:
        expr = expr.strip()
        if not expr:
            return "Error: Empty expression"

        node = ast.parse(expr, mode='eval').body
        return _eval_ast(node)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: Invalid expression ({e})"

def _eval_ast(node):
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](left, right)
        else:
            raise ValueError(f"Unsupported operator {op_type}")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_ast(node.operand)
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](operand)
        else:
            raise ValueError(f"Unsupported unary operator {op_type}")
    elif isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Num):
        return node.n
    else:
        raise ValueError(f"Unsupported expression element: {type(node)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        expression = sys.argv[1]
        result = evaluate_expr(expression)
        print(result)
    else:
        print("Usage: python calculator.py <expression>")
