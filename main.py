import xml.etree.ElementTree as ET
import typer
from typing import Optional
from core.helper import KMap
import core.flipflop as FF

app = typer.Typer()

@app.command()
def solve(
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive design setup."),
    transition_file: Optional[str] = typer.Argument(""),
    design_file: Optional[str] = typer.Argument("")
):
    if interactive:
        # TODO: Create Interactive Mode
        pass
    else:
        transition_file = open(transition_file, 'r').read()
        design_file = open(design_file, 'r').read()

        trans_root = ET.fromstring(transition_file)
        design_root = ET.fromstring(design_file)

        states = [ state.text for state in design_root.find('variables/states').getchildren() ]
        inputs = [ state.text for state in design_root.find('variables/inputs').getchildren() ]
        outputs = [ state.text for state in design_root.find('variables/outputs').getchildren() ]

        states_ff = {}
        for state in states:
            states_ff[state] = design_root.find('flip-flop/'+state).text

        design_type = trans_root.attrib['type']

        row_count = (len(states)+len(inputs))//2
        col_count = len(states)+len(inputs) - row_count

        join_list = states+inputs

        row_name = ",".join(join_list[:row_count])
        col_name = ",".join(join_list[row_count:])

        # Initialize KMap
        state_kmaps = {}
        output_kmaps = {}
        for state in states:
            state_kmaps[state] = {}
            if states_ff[state] == 'JKFF':
                state_kmaps[state]['J'] = KMap(row_count, col_count, row_name, col_name)
                state_kmaps[state]['K'] = KMap(row_count, col_count, row_name, col_name)
            elif states_ff[state] == 'DFF':
                state_kmaps[state]['D'] = KMap(row_count, col_count, row_name, col_name)
            elif states_ff[state] == 'TFF':
                state_kmaps[state]['T'] = KMap(row_count, col_count, row_name, col_name)
            else:
                raise ValueError("Unknown flip-flop type.")

        for output in outputs:
            output_kmaps[output] = KMap(row_count, col_count, row_name, col_name)


        # Fill KMap
        for state in trans_root:
            state_val = state.attrib['value']
            if design_type.upper() == 'MOORE': output_val = state.attrib['output']
            for input in state:
                input_val = input.attrib['value']
                next_state_val = input.text
                if design_type.upper() == 'MEALY': output_val = input.attrib['output']
            
                row_id = (state_val + input_val)[:row_count]
                col_id = (state_val + input_val)[row_count:]

                for kmap_id in range(len(states)):
                    present_state = state_val[kmap_id]
                    next_state = next_state_val[kmap_id]

                    if states_ff[states[kmap_id]] == 'JKFF':
                        J_val, K_val = FF.JKFF.excitation(present_state, next_state)

                        state_kmaps[states[kmap_id]]['J'].set(row_id, col_id, J_val)
                        state_kmaps[states[kmap_id]]['K'].set(row_id, col_id, K_val)

                    elif states_ff[states[kmap_id]] == 'DFF':
                        D_val = FF.DFF.excitation(present_state, next_state)

                        state_kmaps[states[kmap_id]]['D'].set(row_id, col_id, D_val)

                    elif states_ff[states[kmap_id]] == 'TFF':
                        T_val = FF.TFF.excitation(present_state, next_state)

                        state_kmaps[states[kmap_id]]['T'].set(row_id, col_id, T_val)

                for kmap_id in range(len(outputs)):
                    output_kmaps[outputs[kmap_id]].set(row_id, col_id, output_val[kmap_id])

        typer.secho("Results", fg=typer.colors.GREEN, bold=True)
        typer.echo()
        typer.secho("States", fg=typer.colors.BLUE)
        typer.echo()
        
        for state in states:
            if states_ff[state] == 'JKFF':
                typer.echo(state+" - J")
                typer.echo(str(state_kmaps[state]["J"]))

                typer.echo(state+" - K")
                typer.echo(str(state_kmaps[state]["K"]))

            elif states_ff[state] == 'DFF':
                typer.echo(state+" - D")
                typer.echo(str(state_kmaps[state]["D"]))

            elif states_ff[state] == 'TFF':
                typer.echo(state+" - T")
                typer.echo(str(state_kmaps[state]["T"]))

        typer.secho("Outputs", fg=typer.colors.MAGENTA)
        typer.echo()

        for output in outputs:
            typer.echo(output)
            typer.echo(str(output_kmaps[output]))


if __name__ == "__main__":
    app()