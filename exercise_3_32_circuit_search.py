

def fredkin_gate(state, w):
    new_state = state.copy()
    [w1, w2, w3] = w
    if new_state[w3]:
        a = new_state[w1]
        b = new_state[w2]
        new_state[w1] = b
        new_state[w2] = a
        return new_state
    return new_state

def toffoli_gate(state, w):
    new_state = state.copy()
    [w1, w2, w3] = w
    ab = new_state[w1] * new_state[w2]
    c = new_state[w3]
    if ab + c == 1:
        new_state[w3] = 1
        return new_state
    new_state[w3] = 0
    return new_state

def setup_possible_wires():
    #return {0, 1, 2, 3, 4}
    return {0, 1, 2}

def remove_impossible_wires(possible_wires, state, expected):
    impossible_wires = set()
    for possible_wire in possible_wires:
        if state[possible_wire] != expected:
            impossible_wires.add(possible_wire)
    return possible_wires - impossible_wires

def test_gates_ancilla(gates, ancilla_state):
    possible_a_wires = setup_possible_wires()
    possible_b_wires = setup_possible_wires()
    possible_c_wires = setup_possible_wires()
    for a in [0, 1]:
        for b in [0, 1]:
            for c in [0, 1]:
                # Calculating the affect of the gates
                state = ancilla_state.copy()
                state[0] = a
                state[1] = b
                state[2] = c
                for gate in gates:
                    #state = fredkin_gate(state, gate)
                    state = toffoli_gate(state, gate)

                # Calculating the expected output
                #[expected_a, expected_b, expected_c] = toffoli_gate([a, b, c], [0, 1, 2])
                [expected_a, expected_b, expected_c] = fredkin_gate([a, b, c], [0, 1, 2])

                # Testing
                possible_a_wires = remove_impossible_wires(possible_a_wires, state, expected_a)
                possible_b_wires = remove_impossible_wires(possible_b_wires, state, expected_b)
                possible_c_wires = remove_impossible_wires(possible_c_wires, state, expected_c)
                if len(possible_a_wires) == 0 or len(possible_b_wires) == 0 or len(possible_c_wires) == 0:
                    return False
    return [possible_a_wires, possible_b_wires, possible_c_wires]

def generate_possible_gates():
    possible_gates = []
    possible_wires = setup_possible_wires()
    for w1 in possible_wires:
        for w2 in possible_wires:
            if w1 == w2:
                continue
            for w3 in possible_wires:
                if w1 == w3 or w2 == w3:
                    continue
                possible_gates.append([w1, w2, w3])
    return possible_gates

def generate_possible_ancilla_states():
    length = len(setup_possible_wires())
    zero_state = [0] * length
    possible_ancilla_states = []
    for i in range(3, length + 1):
        possible_ancilla_state = zero_state.copy()
        for j in range(3, i):
            possible_ancilla_state[j] = 1
        possible_ancilla_states.append(possible_ancilla_state)
    return possible_ancilla_states

if __name__ == "__main__":
    possible_gates = generate_possible_gates()
    possible_ancilla_states = generate_possible_ancilla_states()
    for gate1 in possible_gates:
        for gate2 in possible_gates:
            for gate3 in possible_gates:
                for ancilla_state in possible_ancilla_states:
                    gates = [gate1, gate2, gate3]
                    possible = test_gates_ancilla(gates, ancilla_state)
                    if possible:
                        print("---")
                        print("Gates")
                        print(gates)
                        print("Ancilla")
                        print(ancilla_state)
                        print("Output")
                        print(possible)

