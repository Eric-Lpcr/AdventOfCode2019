class Instruction:
    pass


class Add(Instruction):
    op_code = 1

    def __call__(self, *args, **kwargs):
        ctx: ExecutionContext = args[0]
        a = ctx.get_parameter(1)
        b = ctx.get_parameter(2)
        write_address = ctx.get_address(3)
        ctx.computer.write_memory(write_address, a + b)
        ctx.pointer += 4


class Mul(Instruction):
    op_code = 2

    def __call__(self, *args, **kwargs):
        ctx: ExecutionContext = args[0]
        a = ctx.get_parameter(1)
        b = ctx.get_parameter(2)
        write_address = ctx.get_address(3)
        ctx.computer.write_memory(write_address, a * b)
        ctx.pointer += 4


class Input(Instruction):
    op_code = 3

    def __call__(self, *args, **kwargs):
        ctx: ExecutionContext = args[0]
        write_address = ctx.get_address(1)
        if len(ctx.computer.inputs) == 0:
            ctx.status = "ERROR"
            ctx.computer.outputs.append(f"At pointer {ctx.pointer}, program has no input left")
        else:
            ctx.computer.write_memory(write_address, ctx.computer.inputs.pop(0))
        ctx.pointer += 2


class Output(Instruction):
    op_code = 4

    def __call__(self, *args, **kwargs):
        ctx: ExecutionContext = args[0]
        a = ctx.get_parameter(1)
        ctx.computer.outputs.append(a)
        ctx.pointer += 2


class JumpIfTrue(Instruction):
    op_code = 5

    def __call__(self, *args, **kwargs):
        ctx: ExecutionContext = args[0]
        p = ctx.get_parameter(1)
        if p != 0:
            ctx.pointer = ctx.get_parameter(2)
        else:
            ctx.pointer += 3


class JumpIfFalse(Instruction):
    op_code = 6

    def __call__(self, *args, **kwargs):
        ctx: ExecutionContext = args[0]
        p = ctx.get_parameter(1)
        if p == 0:
            ctx.pointer = ctx.get_parameter(2)
        else:
            ctx.pointer += 3


class LessThan(Instruction):
    op_code = 7

    def __call__(self, *args, **kwargs):
        ctx: ExecutionContext = args[0]
        a = ctx.get_parameter(1)
        b = ctx.get_parameter(2)
        write_address = ctx.get_address(3)
        if a < b:
            ctx.computer.write_memory(write_address, 1)
        else:
            ctx.computer.write_memory(write_address, 0)
        ctx.pointer += 4


class Equals(Instruction):
    op_code = 8

    def __call__(self, *args, **kwargs):
        ctx: ExecutionContext = args[0]
        a = ctx.get_parameter(1)
        b = ctx.get_parameter(2)
        write_address = ctx.get_address(3)
        if a == b:
            ctx.computer.write_memory(write_address, 1)
        else:
            ctx.computer.write_memory(write_address, 0)
        ctx.pointer += 4


class Halt(Instruction):
    op_code = 99

    def __call__(self, *args, **kwargs):
        ctx: ExecutionContext = args[0]
        ctx.status = 'HALTED'


class IntCodeComputer:
    def __init__(self, *instructions):
        self.instructions = {}
        for instruction in instructions:
            self.instructions[instruction.op_code] = instruction()  # instruction is a class, register an instance
        self.memory = []
        self.status = 'EMPTY'
        self.inputs = None
        self.outputs = []

    def load_memory(self, program):
        self.memory = program[:]
        self.status = 'LOADED'

    def run(self, inputs, pointer=0):
        self.inputs = list(inputs)
        self.status = 'RUNNING'
        ctx = ExecutionContext(self, pointer)
        while self.status == 'RUNNING':
            if ctx.pointer >= len(self.memory):
                self.status = 'ENDED'
            else:
                op_code = self.read_memory(ctx.pointer, 1)
                ctx.parameter_modes = [op_code // 100 % 10,
                                       op_code // 1000 % 10,
                                       op_code // 10000 % 10]
                op = op_code % 100
                if op in self.instructions:
                    self.instructions[op](ctx)
                    self.status = ctx.status
                else:
                    self.status = 'ERROR'
                    self.outputs.append(f"At pointer {ctx.pointer}, unknown opcode {op}")

    def get_outputs(self):
        return self.outputs

    # TODO Check memory access
    def read_memory(self, address, mode):
        parameter = self.memory[address]
        if mode == 0:  # POSITION
            return self.memory[parameter]
        else:  # IMMEDIATE
            return parameter

    def write_memory(self, address, value):
        self.memory[address] = value


class ExecutionContext:
    def __init__(self, computer, pointer=0):
        self.computer = computer
        self.pointer = pointer
        self.parameter_modes = None
        self.status = "RUNNING"

    def get_parameter(self, offset):
        parameter = self.computer.read_memory(self.pointer + offset, self.parameter_modes[offset - 1])
        return parameter

    def get_address(self, offset):
        address = self.computer.read_memory(self.pointer + offset, 1)  # address is always an IMMEDIATE mode parameter
        return address


def main():
    with open('input.txt') as f:
        line = f.readline()
        program = [int(val) for val in line.split(',')]

    computer = IntCodeComputer(Add, Mul, Input, Output, JumpIfTrue, JumpIfFalse, LessThan, Equals, Halt)

    computer.load_memory(program)
    computer.run(inputs=[1])
    print(f"With input 1, program {computer.status} with outputs {computer.outputs}")

    computer.load_memory(program)
    computer.run(inputs=[5])
    print(f"With input 5, program {computer.status} with outputs {computer.outputs}")


if __name__ == '__main__':
    main()

# TODO Implement tests !
