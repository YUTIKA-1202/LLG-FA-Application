def parse_llg(grammar):
    lines = grammar.strip().splitlines()

    if not lines:
        raise ValueError("Grammar is empty.")

    productions = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if "->" not in line:
            raise ValueError(
                f"Invalid production: {line}. Use A -> Ba or A -> a"
            )

        left, right = line.split("->", 1)

        left = left.strip()
        right = right.strip()

        if not left or not right:
            raise ValueError(
                f"Invalid production: {line}"
            )

        productions.append((left, right))

    if not productions:
        raise ValueError("No valid productions found.")

    non_terminals = set()

    for left, right in productions:
        non_terminals.add(left)

        for symbol in right:
            if symbol.isupper():
                non_terminals.add(symbol)

    start_state = productions[0][0]
    final_state = "qf"

    states = set(non_terminals)
    states.add(final_state)

    transitions = []
    alphabet = set()

    for left, right in productions:

        # Example:
        # A -> a
        if len(right) == 1 and right not in non_terminals:

            terminal = right

            alphabet.add(terminal)

            transitions.append(
                (left, terminal, final_state)
            )

        # Example:
        # A -> Ba
        elif len(right) == 2:

            non_terminal = right[0]
            terminal = right[1]

            if non_terminal not in non_terminals:
                raise ValueError(
                    f"Invalid production: {left} -> {right}"
                )

            alphabet.add(terminal)

            # Left-linear grammar conversion
            transitions.append(
                (non_terminal, terminal, left)
            )

        else:
            raise ValueError(
                f"Unsupported production: {left} -> {right}"
            )

    return {
        "states": sorted(states),
        "alphabet": sorted(alphabet),
        "start_state": start_state,
        "final_states": [final_state],
        "transitions": transitions
    }


def convert_llg_to_fa_details(grammar):

    fa = parse_llg(grammar)

    result = []

    result.append("FINITE AUTOMATON")
    result.append("=" * 40)

    result.append(
        "States: " + ", ".join(fa["states"])
    )

    result.append(
        "Alphabet: " + ", ".join(fa["alphabet"])
    )

    result.append(
        "Start State: " + fa["start_state"]
    )

    result.append(
        "Final State: " +
        ", ".join(fa["final_states"])
    )

    result.append("")
    result.append("TRANSITIONS")
    result.append("-" * 40)

    for source, symbol, destination in fa["transitions"]:

        result.append(
            f"δ({source}, {symbol}) = {destination}"
        )

    fa["text"] = "\n".join(result)

    return fa


def convert_llg_to_fa(grammar):

    fa = convert_llg_to_fa_details(grammar)

    return fa["text"]