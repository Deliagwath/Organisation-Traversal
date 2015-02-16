import sys
import os

# structure is a dictionary
# Where each unit contains information about its ID
# and his/her manager's ID and his/her connections
# Layout: {ID: ((Name, Manager ID), [Connections])}
# Example: {2: (("Gonzo the Great", 1), [1, 6])}

# This question is a graph related question and will be treated as such
# Hence the search implementation will be implemented as a Depth First Search


class BT:

    file_name = None
    from_unit = None
    from_id = None
    to_unit = None
    to_id = None
    structure = {}
    searched = {}

    def __init__(self, args):

        if len(args) < 4:
            print "Not enough arguments"
            sys.exit()
        elif len(args) > 4:
            print "Too much arguments"
            sys.exit()

        # Parsing inputs
        self.file_name = args[1]

        # Preprocessing and parsing 2nd argument
        from_unit_input = args[2].strip().split(' ')
        from_unit_filtered = []
        for item in from_unit_input:
            if item != "":
                from_unit_filtered.append(item.lower())
        self.from_unit = ' '.join(from_unit_filtered)

        # Preprocessing and parsing 3rd argument
        to_unit_input = args[3].strip().split(' ')
        to_unit_filtered = []
        for item in to_unit_input:
            if item != "":
                to_unit_filtered.append(item.lower())
        self.to_unit = ' '.join(to_unit_filtered)

        self.start()

    # Parses file given from program parameters
    # then loads all the information into memory
    # using a dictionary
    def parse_structure(self):

        # Checks if file exists
        if os.path.exists(self.file_name):

            # Brings data into the program memory
            reader = open(self.file_name, 'r')
            data = reader.readlines()
            first = True

            # Parsing data
            for line in data:
                if first:
                    first = False
                    continue

                # Preprocessing
                stripped = line.strip()
                splitted = stripped.split('|')
                filtered = [item.strip() for item in splitted
                            if len(item.strip()) != 0]

                if len(filtered) == 2:
                    filtered.append('None')

                # Processing for units with same names
                if filtered[1] in self.structure:

                    # Rename until an acceptible name is found
                    index = 1
                    name = filtered[1]

                    # Keep increasing number if no valid name is found
                    while True:
                        name += '_' + str(index)
                        if name in self.structure:
                            name = '_'.join(name.split('_')[:-1])
                            index += 1
                        else:
                            break

                # Assumes data comes in as ID, Name, Manager
                self.structure[filtered[0]] = ((filtered[1], filtered[2]), [])

            self.post_process_structure()

        else:
            print "File " + self.file_name + " does not exist"
            sys.exit()

    # This method is to add to the structure so that it populates each
    # unit with their children so the graph search will be easier
    def post_process_structure(self):

        # Up the tree
        for unit_id in self.structure:
            unit_data, children = self.structure[unit_id]
            unit_name, manager_id = unit_data

            if unit_name.lower() == self.from_unit:
                self.from_id = unit_id
            elif unit_name.lower() == self.to_unit:
                self.to_id = unit_id

            if manager_id == 'None':
                continue

            self.structure[manager_id][1].append(unit_id)

    # Main program
    # DOES NOT WORK
    # ABANDONED DUE TO NOT FULFILLING SPECIFICATION
    # LOOP DETECTION INCORRECTLY IMPLEMENTED AS WELL
    # Searches through the graph and returns either a list of connections
    # Or returns False if its recursive search was a dead end
    # Recursive call uses boolean for three states
    # None for ongoing search
    # False for dead end
    # True for found path
    def single_search(self, current, previous, end, boolean):

        if current == end:
            return [current], True

        # If loop is not done
        if boolean is None:

            for children in self.structure[current][1]:

                # Prevent recursion from moving through previous
                if previous is not None and previous == children:
                    continue

                path, return_boolean = self.single_search(children, current,
                                                          end, None)

                if return_boolean is False:
                    return None, False

                # Loop detection
                # As IDs are distinct, if already occured in path once
                # Then it is looping
                if current is not None and current in path:
                    return None, False

                if return_boolean is True:
                    return path.append(current), True

            manager_id = self.structure[current][0][1]

            path, return_boolean = self.single_search(manager_id, current,
                                                      end, None)

            if current is not None and current in path:
                return None, False

            if return_boolean is True:
                return path.append(current), True

            # Dead End
            return None, False

    # Main program
    # Different algorithm to allow returning of multiple paths
    def multi_search(self, current, previous, end, path, boolean):

        # print "-----"
        # print "Current: " + str(current)
        # print "Current ID: " + str(id(current))
        # print "Previous: " + str(previous)
        # print "End: " + str(end)
        # print "Path: " + str(path)
        # print "Boolean: " + str(boolean)
        # print "-----"

        # Loop Detection
        if current in path:
            # print "Loop Break"
            return None, False

        if current == end:
            # print "Path found, Returning Current: " + str(current)
            return [[current]], True

        total_paths = []
        path.append(current)

        # If loop is not done
        if boolean is None:

            for children in self.structure[current][1]:

                # Prevent recursion from moving through previous
                if previous is not None and previous == children:
                    continue

                # print "Going into Child: " + str(children)
                return_path, return_boolean = self.multi_search(
                    children, current, end, path[:], None)

                # print "Current: " + str(current)
                # print "Return path: " + str(return_path)
                # print str(type(return_path))
                # print "Current path: " + str(path)
                # print "Return boolean: " + str(boolean)
                # print str(type(return_boolean))

                if return_boolean is False:
                    # print "Boolean is False, ignoring path"
                    continue

                if return_boolean is True:
                    for p in return_path:
                        p.append(current)
                        total_paths.append(p[:])

            manager_id = self.structure[current][0][1]

            if manager_id != 'None' and manager_id != previous:

                # print "Going into Manager: " + str(manager_id)
                return_path, return_boolean = self.multi_search(
                    manager_id, current, end, path[:], None)

                # print "Current: " + str(current)
                # print "Return path: " + str(return_path)
                # print str(type(return_path))
                # print "Current path: " + str(path)
                # print "Return boolean: " + str(return_boolean)
                # print str(type(return_boolean))

                # if current is not None and current in path:
                #     "Loop Break"
                #     return None, False

                if return_boolean is False:
                    # print "Boolean is False, ignoring path"
                    pass

                if return_boolean is True:
                    for p in return_path:
                        p.append(current)
                        total_paths.append(p[:])

            if len(total_paths) > 0:
                return total_paths, True

            # Dead End
            return None, False

    def stringify(self, path):
        string = ""

        for index in range(0, len(path)):

            string += self.structure[path[index]][0][0] + \
                " (" + path[index] + ") "

            if index < len(path) - 1:

                if self.structure[path[index]][0][1] == path[index + 1]:
                    string += "-> "
                elif self.structure[path[index + 1]][0][1] == path[index]:
                    string += "<- "

        return string

    def clean_path(self, path):

        import itertools

        path.sort()
        filtered_paths = [path[::-1] for path, _ in itertools.groupby(path)]

        return filtered_paths

    def start(self):
        self.parse_structure()
        self.post_process_structure()
        path, boolean = self.multi_search(self.from_id, None,
                                          self.to_id, [], None)

        if boolean is True:
            new_path = self.clean_path(path)
            for routes in new_path:
                print self.stringify(routes)


if __name__ == '__main__':
    BT(sys.argv)