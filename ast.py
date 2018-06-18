import subprocess


class Command:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def with_arg(self, arg):
        return Command(self.name, self.args + [arg])

    def evaluate(self, stdin, stdout, stderr):
        return subprocess.Popen([self.name] + self.args, stdin=stdin, stdout=stdout, stderr=stderr)


class Pipe:
    def __init__(self, cmd1, cmd2):
        self.cmd1 = cmd1
        self.cmd2 = cmd2

    def evaluate(self, stdin, stdout, stderr):
        input = self.cmd1.evaluate(stdin, subprocess.PIPE, stderr)
        output = self.cmd2.evaluate(input.stdout, stdout, stderr)
        return output


class TruncateFile:
    def __init__(self, cmd, filename):
        self.cmd = cmd
        self.filename = filename

    def evaluate(self, stdin, stdout, stderr):
        with open(self.filename, "w") as file:
            return self.cmd.evaluate(stdin, file, stderr)


class Assign(object):
    def __init__(self, name, value, context):
        nam = name.name
        valu = value.name
        context[nam] = valu

class IfStatement:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def evaluate(self, stdin, stdout, stderr):
        if self.condition.evaluate():
            for statement in self.statements:
                if type(statement) == Command:
                    statement.evaluate(stdin, stdout, stderr).wait()
        return


class IfElseStatement:
    def __init__(self, condition, if_statements, else_statements):
        self.condition = condition
        self.if_statements = if_statements
        self.else_statements = else_statements

    def evaluate(self, stdin, stdout, stderr):
        if self.condition.evaluate():
            for statement in self.if_statements:
                executeStatement(statement, stdin, stdout, stderr)
        else:
            for statement in self.else_statements:
                executeStatement(statement, stdin, stdout, stderr)
        return


class IfCondition():
    def __init__(self, arg1, operator, arg2):
        self.arg1 = arg1
        self.operator = operator
        self.arg2 = arg2


    def evaluate(self):
        operator_dict = { "-eq" : self.arg1 == self.arg2,
                      "-ne": self.arg1 != self.arg2,
                      "-gt": self.arg1 > self.arg2,
                      "-lt": self.arg1 < self.arg2}
        return operator_dict[self.operator]


def executeStatement(statement, stdin, stdout, stderr):
    if type(statement) == IfStatement or type(statement) == IfElseStatement:
        statement.evaluate(stdin, stdout, stderr)
    elif type(statement) == Command or type(statement) == Pipe:
        statement.evaluate(stdin, stdout, stderr).wait()