import csv

class NTM:
    def __init__(self, file_name):
        self.transitions = {}
        self.load_machine(file_name)

    # read in csv and parse machine info
    def load_machine(self, file_name):
        with open(file_name, 'r') as file:
            # load machine info
            reader = csv.reader(file)
            self.name = next(reader)[0]
            self.states = set(next(reader)[0].split(','))
            self.input_symbols = set(next(reader)[0].split(','))
            self.tape_symbols = set(next(reader)[0].split(','))
            self.start_state = next(reader)[0]
            self.accept_state = next(reader)[0]
            self.reject_state = next(reader)[0]

            # read in tranisitions
            for row in reader:
                state, input, next_state, write, direction = row
                if (state, input) not in self.transitions:
                    self.transitions[(state, input)] = []
                self.transitions[(state, input)].append((next_state, write, direction))

    def simulate(self, input_string, max_depth=10):
        initial_config = (self.start_state, input_string, 0, [])  # (state, tape, head position, path)
        tree = [initial_config]
        steps = 0

        while tree and steps < max_depth:
            next_level = []
            for state, tape, head, path in tree:
                path_trace = path + [(list(tape), state)]

                # print info once it reaches accept state
                if state == self.accept_state:
                    print(f"Name of the machine: {self.name}")
                    print(f"Original input string: {input_string}")
                    print(f"String accepted in {steps} transitions")
                    print(f"Degree of nondeterminism: {len(tree)}")
                    print("Tracing path to accepting state:")
                    for tape_snapshot, state_name in path_trace:
                        print(f"{tape_snapshot} | {state_name} | {list(tape)}")
                    return True

                tape_list = list(tape)
                current_symbol = tape_list[head] if head < len(tape_list) else '_'

                # follow transitions
                if (state, current_symbol) in self.transitions:
                    for next_state, write_symbol, move in self.transitions[(state, current_symbol)]:
                        new_tape = tape_list[:]
                        if head < len(new_tape):
                            new_tape[head] = write_symbol
                        else:
                            new_tape.append(write_symbol)

                        new_head = head + 1 if move == 'R' else max(0, head - 1)
                        new_config = (next_state, ''.join(new_tape), new_head, path_trace)
                        next_level.append(new_config)

            tree = next_level
            steps += 1

        # print if reaches reject state
        print(f"Name of the machine: {self.name}")
        print(f"Original input string: {input_string}")
        if steps < 10:
            print(f"String rejected after {steps} transitions")
        else:
            print(f"Max depth of 10 exceeded")
        print(f"Degree of nondeterminism: {len(tree)}")
        return False

def main():
    # read in files
    machine_file = "data_NTM_description.csv"
    input_file = "check_strings.csv"

    ntm = NTM(machine_file) # create class
    
    # read in each of the input strings
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        input_strings = [row[0] for row in reader]
    
    # trace for each of the input strings
    for input_string in input_strings:
        ntm.simulate(input_string)
        print("\n")


if __name__ == "__main__":
    main()