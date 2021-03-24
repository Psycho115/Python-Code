import sys

if __name__ == '__main__':

    action = sys.argv[1]
    action_list = ['in', 'out']

    command = ''
    for act in action_list:
        if action == act:
            command = action
    if command == '':
        sys.exit()

    if command == 'in':
        pass
    elif command == 'out':
        pass
