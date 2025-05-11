def unit_propagate(clauses):
    unit_literals = {literal for clause in clauses if len(clause) == 1 for literal in clause}
    while unit_literals:
        literal = unit_literals.pop()
        clauses = [clause for clause in clauses if literal not in clause]  
        for clause in clauses:
            if -literal in clause:
                clause.remove(-literal)  
                if len(clause) == 1:
                    unit_literals.add(next(iter(clause)))  
    return clauses


def pure_literal(clauses):
    literals = {literal for clause in clauses for literal in clause}
    pure_literals = {literal for literal in literals if -literal not in literals}
    for literal in pure_literals:
        clauses = [clause for clause in clauses if literal not in clause] 
    return clauses


def resolve_simple(clause1, clause2):
   
    for literal in clause1:
        if -literal in clause2:
            new_clause = (clause1 | clause2) - {literal, -literal}
            return new_clause
    return None


def is_satisfiable(clauses):
    
    clauses = unit_propagate(clauses)
    clauses = pure_literal(clauses)

    while True:
        new_clauses = []
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                resolvent = resolve_simple(clauses[i], clauses[j])
                if resolvent is not None and resolvent not in clauses and resolvent not in new_clauses:
                    new_clauses.append(resolvent)
        
        if not new_clauses:
            return True
        clauses.extend(new_clauses)
        clauses = unit_propagate(clauses)
        clauses = pure_literal(clauses)

        if any(not clause for clause in clauses): 
            return False

"""
clauses = [
    {1, -2},   # (x1 OR NOT x2)
    {-1, 3},   # (NOT x1 OR x3)
    {-3},      # (NOT x3)
    {2},       # (x2)
]
clauses = [
    {1, -2},   
    {1, 3},    
    {-2, 3},   
    {-1, 2},   
    {2, -3},   
    {-1, -3}, 
]
"""
clauses = [
    {1, -2, 3},   # (A ∨ ¬B ∨ C)
    {2, 3},       # (B ∨ C)
    {-1, 3},      # (¬A ∨ C)
    {2, -3},      # (B ∨ ¬C)
    {-2},         # (¬B)
]
print("Satisfiabil?", is_satisfiable(clauses))
