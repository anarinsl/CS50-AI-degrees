import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    play_game = 'yes'

    while play_game == 'yes':
        source = person_id_for_name(input("Name: "))
        if source is None:
            sys.exit("Person not found.")
        target = person_id_for_name(input("Name: "))
        if target is None:
            sys.exit("Person not found.")
    
        path = shortest_path(source, target)
    
        if path is None:
            print("Not connected.")
        else:
            degrees = len(path)
            print(f"{degrees} degrees of separation.")
            path = [(None, source)] + path
            for i in range(degrees):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i + 1][1]]["name"]
                movie = movies[path[i + 1][0]]["title"]
                print(f"{i + 1}: {person1} and {person2} starred in {movie}")
        
        play_game = input('Enter "yes" to play again: ')        


def shortest_path(source, target):
    """
    Inputs are both person ids
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # creat function that traces back the path from a node
    def trace_path(node):
        '''
        traces the path taken from the initial state to the input node.
        input: a node
        output: a list of 2 tuples. first element is the action taken.
        second element is the resulting state. action tuples are in order
        first to last.
        '''
        # create path variable to track path to from target node to initial node
        path = []

    
        # trace back the path from the input node
        # while we have not yet reached the initial node with no parent keep tracing back
        while node.get_parent() != None:
            # add the action to the path
            path.append(node.get_action())
            # update the node to be the parent of the current node
            node = node.get_parent()
        
        # reverse the order of path to get the path from initial node to input node
        path.reverse()
        # return result
        return path
    
    # create list to track explored nodes
    explored_states = []
    # create queue frontier
    frontier = QueueFrontier()
    
    # create initial state node
    current_node = Node(source, None, None)
    
    # start search
    # continue to search while nothing has been returned
    while True:
        # expand current node
        # get the state space. list of possible actions and resulting states in 2 tuples
        state_space = neighbors_for_person(current_node.get_state())
        
        # iterate over state_space
        for action_state in state_space:
            # create a node from the action_state
            node = Node(action_state[1], current_node, action_state)
            # check if the state is the target state
            if node.get_state() == target:
                return trace_path(node)
            

            # add the node to the frontier if its state is not already in the frontier
            # and it has not yet been explored
            # this way all nodes in the frontier are valid options for search
            if not frontier.contains_state(node.get_state()) and node.get_state() not in explored_states:
                frontier.add(node)
                
        # add the current node state to the explored states
        explored_states.append(current_node.get_state())
        
        if frontier.empty():
            # no solution
            return None
            
        else:
            # update the current node to be one from the frontier
            current_node = frontier.remove()
            
        


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
