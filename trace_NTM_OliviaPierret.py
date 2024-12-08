import csv

class NTM:
    def __init__(self, machine_file):
        self.transitions = {}
        self.load_machine(machine_file)

    # read in csv and parse machine info
    def load_machine(self, machine_file):
        with open(machine_file, 'r') as file:
            reader = csv.reader(file)
            self.machine_name = next(reader)[0]  # Machine name
            self.states = set(next(reader)[0].split(','))
            self.input_symbols = set(next(reader)[0].split(','))
            self.tape_symbols = set(next(reader)[0].split(','))
            self.initial_state = next(reader)[0]
            self.accept_state = next(reader)[0]
            self.reject_state = next(reader)[0]

            # read transitions
            for row in reader:
                current_state, symbol_read, next_state, symbol_write, direction = row
                if (current_state, symbol_read) not in self.transitions:
                    self.transitions[(current_state, symbol_read)] = []
                self.transitions[(current_state, symbol_read)].append((next_state, symbol_write, direction))

    def process_string(self, input_string, max_steps):
        tape = list(input_string)   # input string
        configurations = [([], self.initial_state, tape[:])]   # start with initial configuration
        visited_configurations = set()  # track visited configurations
        all_steps = []  # trace what's been seen

        max_nondeterminism = 0  
        steps_taken = 0  

        while configurations:
            # pop the first configuration
            left_of_head, current_state, current_tape = configurations.pop(0)

            current_configuration = (tuple(left_of_head), current_state, tuple(current_tape))

            if current_configuration in visited_configurations:
                continue
            # add current configuration
            visited_configurations.add(current_configuration)
            all_steps.append((left_of_head[:], current_state, current_tape[:]))

            # tape is empty
            if not current_tape:
                current_tape = ['_']
            
            tape_head = current_tape[0]

            # check if we are in an accept state
            if current_state == self.accept_state:
                with open("output_data.txt", "a") as file:
                    file.write(f'Machine Name: {self.machine_name}\n')
                    file.write(f'Input String: {input_string}\n')
                    file.write(f"Accepted in {steps_taken} states\n")
                    file.write(f"Depth: {steps_taken - 1}\n")
                    file.write(f"Degree of Nondeterminism: {max_nondeterminism}\n")
                    self.print(all_steps, file=file)
                return
            elif current_state == self.reject_state:
                continue

            # make transitions
            if (current_state, tape_head) in self.transitions:
                transitions = self.transitions[(current_state, tape_head)]
                max_nondeterminism = max(max_nondeterminism, len(transitions))

                for next_state, write_symbol, direction in transitions:
                    new_tape = current_tape[:]
                    new_tape[0] = write_symbol
                    
                    # move the head based on the direction
                    if direction == "R":    # move right
                        new_left = left_of_head[:]
                        new_left.append(new_tape.pop(0))
                        if not new_tape:
                            new_tape.append('_')
                    elif direction == "L":      # move left
                        new_left = left_of_head[:]
                        if new_left:
                            new_tape.insert(0, new_left.pop())
                        else:
                            new_tape.insert(0, '_')
                    
                    # add the new configuration
                    configurations.append((new_left, next_state, new_tape))

            # update step counter
            steps_taken += 1  
            # make sure it hasnt exceeded max steps allowed
            if steps_taken > max_steps:
                with open("output_data.txt", "a") as file:
                    file.write(f'Machine Name: {self.machine_name}\n')
                    file.write(f'Input String: {input_string}\n')
                    file.write(f"Execution stopped after max transitions exceeded: {max_steps}\n")
                    file.write(f"Degree of Nondeterminism: {max_nondeterminism}\n")
                    file.write("\n")
                return

        # handle rejection
        with open("output_data.txt", "a") as file:
            file.write(f'Machine Name: {self.machine_name}\n')
            file.write(f'Input String: {input_string}\n')
            file.write(f'Rejected after {steps_taken} states\n')
            file.write(f"Depth: {steps_taken - 1}\n")
            file.write(f"Degree of Nondeterminism: {max_nondeterminism}\n")
            self.print(all_steps, file=file)

    # print the trace
    def print(self, all_steps, file):
        for left, state, tape in all_steps:
            file.write(f"{left} | {state} | {str(tape)}\n")
        file.write("\n")

def main():
    # file paths
    machine_file_path = "data_NTM_description.csv"
    input_file_path = "check_strings.csv"
    max_steps_file_path = "termination_flag.csv"

    # initialize the NTM
    ntm_machine = NTM(machine_file_path)

    # load max steps termination flag
    with open(max_steps_file_path, 'r') as file:
        reader = csv.reader(file)
        max_steps = int(next(reader)[0])

    # load all input strings
    with open(input_file_path, 'r') as file:
        reader = csv.reader(file)
        input_strings = [row[0] for row in reader]
    
    # process each input string
    for input_string in input_strings:
        ntm_machine.process_string(input_string, max_steps)


if __name__ == "__main__":
    main()
