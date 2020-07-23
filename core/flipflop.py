from core.helper import is_boolean

class JKFF:
    
    @classmethod
    def excitation(cls, present_state, next_state):
        
        if not(is_boolean(present_state) and is_boolean(next_state)):
            raise ValueError("Present state and Next state must be 0 or 1.")
        
        present_state = int(present_state)
        next_state = int(next_state)

        excitation_table = [
            [('0','X'), ('1', 'X')],
            [('X', '1'), ('X', '0')]
        ]
        
        return excitation_table[present_state][next_state]


class DFF:
    
    @classmethod
    def excitation(cls, present_state, next_state):
        
        if not(is_boolean(present_state) and is_boolean(next_state)):
            raise ValueError("Present state and Next state must be 0 or 1.")
        
        present_state = int(present_state)
        next_state = int(next_state)

        excitation_table = [
            ['0', '1'],
            ['0', '1']
        ]
        
        return excitation_table[present_state][next_state]


class TFF:
    
    @classmethod
    def excitation(cls, present_state, next_state):
        
        if not(is_boolean(present_state) and is_boolean(next_state)):
            raise ValueError("Present state and Next state must be 0 or 1.")
        
        present_state = int(present_state)
        next_state = int(next_state)

        excitation_table = [
            ['0', '1'],
            ['1', '0']
        ]
        
        return excitation_table[present_state][next_state]