
class Combinator:
    def __init__(self, input):
        self.input = input
        self.output = []

    def create_combinations(self):
        actions = self.input.keys()
        self.recursor(list(actions), 0, {})
        pass

    def recursor(self, actions, level, combination_output):
        if level < len(actions):
            action = actions[level]
            combinations = self.input[action]
            for combination in combinations:
                combination_output[action] = combination
                self.recursor(actions, level + 1, combination_output)

        else:
            combination_output_wrapper = {}
            combination_output_wrapper['name'] = self.get_combination_name(combination_output)
            combination_output_wrapper['values'] = combination_output.copy()
            self.output.append(combination_output_wrapper)

    def get_combination_name(self, combination_output):
        name = ''
        for action in combination_output.keys():
            name += str(combination_output[action]) + ':' + str(action) + '|'

        return name

if __name__ == '__main__':
    combinator = Combinator({
        'a':[1, 2, 3],
        'b': [1, 2, 3],
        'c': [1, 2, 3]
    })

    combinator.create_combinations()
    formattted_output = ''
    for combination in combinator.output:
        for value in combination['values'].values():
            formattted_output += '\t' + str(value)
        formattted_output += '\n'
    print(formattted_output)