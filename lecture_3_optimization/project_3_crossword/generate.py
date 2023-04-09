import sys
import copy

from crossword import *

"""CSP AS SEARCH PROBLEM"""
class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    """node consistency == unary constraints"""
    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """ 
        for v in self.domains: 
            var_len = v.length  
            # if variable and word length not match
            for x in self.domains[v].copy(): 
                if len(x) != var_len:
                    self.domains[v].remove(x)  

        # raise NotImplementedError

    """arc consistency == binary constraint""" 
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """ 
        revised = False 
        # overlap of x and y from dict overlaps 
        overlap = self.crossword.overlaps[x,y] 
        if overlap == None:
            return False 
        else:
           for xx in self.domains[x].copy():
                satisfy = False 
                # check if for any value in y satisfy the constraint
                for yy in self.domains[y]: 
                    if xx[overlap[0]] == yy[overlap[1]]:
                        satisfy = True 
                # if no value in y satisfy constraint with x 
                if satisfy == False:
                    self.domains[x].remove(xx) 
                    revised = True
        return revised
        # raise NotImplementedError

    """make all the nodes arc consistent"""
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # if arc is none , initialize it with all arcs 
        if arcs == None: 
            # list as queue 
            arcs = [] 
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    if x != y:
                        arcs.append((x,y)) 
        # ac3 algo 
        while len(arcs) > 0:
            (x,y) = arcs.pop(0)    # pop from front 
            # if the arc(x,y) is revised
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False 
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.append((z,x))
        return True
                
        # raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """ 
        # check if all variables are assigned
        for x in self.crossword.variables:
            if x not in assignment.keys():
                return False
        return True
        #raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """ 
        # no word repeat
        for x in assignment:
            for y in assignment:
                if x != y and assignment[x] == assignment[y]:
                    return False
        
        # length of value == variable.length() 
        for x in assignment:
            if x.length != len(assignment[x]):
                return False

        # no conflict with neighbor 
        for x in assignment:
            for z in self.crossword.neighbors(x):
                (i,j) = self.crossword.overlaps[x,z] 
                # if z is assigned 
                if z in assignment: 
                    # at the overlap point , alphabet should be same
                    if assignment[x][i] != assignment[z][j]:
                        return False 
        return True
        #raise NotImplementedError

    """return least constraining values heuristic
       on the basis of no of eliminations"""
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """ 
        lcv_heur = dict() 
        # for all domain values calc elimination  
        for x in self.domains[var]:
            eliminations = 0 
            # for all neighbors
            for z in self.crossword.neighbors(var):
                if z not in assignment: 
                    (i,j) = self.crossword.overlaps[var,z] 
                    # for all choices of neighbor 
                    for choices in self.domains[z]: 
                        # increment elim if x and choice conflict
                        if x[i] != choices[j]:
                            eliminations += 1 
            lcv_heur[x] = eliminations  
        # sort the heur according to value i.e, eliminations
        sorted_heur = sorted(lcv_heur.items(), key = lambda x:x[1]) 
        sorted_list = [] 
        for x in sorted_heur:
            sorted_list.append(x[0]) 
        return sorted_list 
        # raise NotImplementedError

    """minimum remaining values(mrv) heuristic + degrees heuristic
       on the basis of smallest non conflicting domain and no of neighbors"""
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """ 
        mrv_d_heur = dict() 
        # for unassigned var 
        for var in self.crossword.variables:
            if var not in assignment: 
                # find remaining values 
                total_choices = len(self.domains[var])
                poss_v = 0 
                # how many values of var does not conflict 
                for val in self.domains[var]:
                   for neigh in self.crossword.neighbors(var):
                       if neigh in assignment: 
                           (i,j) = self.crossword.overlaps[var,neigh] 
                           if val[i] == assignment[neigh][j]:
                               poss_v += 1 
                mrv = total_choices - poss_v 
                # find the degrees
                deg = len(self.crossword.neighbors(var)) 
                mrv_d_heur[var] = (mrv+deg) 
        # sort the mrv_d_heur according to mrv + d 
        # sorted_heur is list 
        sorted_heur = sorted(mrv_d_heur.items(),key = lambda x:x[1])  
        return sorted_heur[0][0]
        #raise NotImplementedError

    """BACKTRACKING SEARCH"""
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """ 
        if self.assignment_complete(assignment):
            return assignment 
        var = self.select_unassigned_variable(assignment) 
        # for all domain values of var
        for val in self.order_domain_values(var, assignment): 
            assignment[var] = str(val) 
            if self.consistent(assignment):
                result = self.backtrack(assignment) 
                if result:
                    return assignment
            del assignment[var] 
        return None
        #raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
