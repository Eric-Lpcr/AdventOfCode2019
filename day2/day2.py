def run_program(program, noun, verb, debug=False):
    memory = program[:]  # keep original program untouched
    memory[1] = noun
    memory[2] = verb
    pointer = 0
    while pointer < len(memory):
        op = memory[pointer]
        if op == 99:
            break
        elif op == 1:
            pos1, pos2, pos3 = memory[pointer+1:pointer+4]
            memory[pos3] = memory[pos1] + memory[pos2]
            if debug and pos3 % 4 == 0 and pos3 > pointer:
                print("Warning, overwritten opcode at position", pos3, "with", memory[pos3])
            pointer += 4
        elif op == 2:
            pos1, pos2, pos3 = memory[pointer+1:pointer+4]
            memory[pos3] = memory[pos1] * memory[pos2]
            if debug and pos3 % 4 == 0 and pos3 > pointer:
                print("Warning, overwritten opcode at position", pos3, "with", memory[pos3])
            pointer += 4
        else:
            print("Program went wrong, got opcode", op, "at position", pointer)
            exit(1)
    return memory[0]


def find_inputs(program, expected_result):
    for noun in range(0, 100):
        for verb in range(0, 100):
            result = run_program(program[:], noun, verb)
            if result == expected_result:
                return noun, verb, result
    return None, None, None


def main():
    with open('input.txt') as f:
        line = f.readline()
        program = [int(val) for val in line.split(',')]

    noun, verb = 12, 2
    result = run_program(program, noun, verb)
    print(f"Got {result} with noun={noun} and verb={verb}")

    expected_result = 19690720
    noun, verb, result = find_inputs(program, expected_result)
    if noun is not None:
        print(f"Got {result} with noun={noun} and verb={verb}, answer is {100 * noun + verb}")
    else:
        print(f"Program can't produce {result}")


if __name__ == '__main__':
    main()
