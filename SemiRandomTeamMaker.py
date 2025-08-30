import random
from characters import characters

def generate_teams(characters_dict, num_teams=10000):
    """
    Generate random teams of 4 characters from the character dictionary.
    
    Args:
        characters_dict: Dictionary of characters with their attributes
        num_teams: Number of teams to generate (default: 100)
    
    Returns:
        List of teams, where each team is a list of 4 character dictionaries
    """
    # Convert dictionary to list of character dictionaries with names included
    char_list = []
    for name, attributes in characters_dict.items():
        char_dict = attributes.copy()
        char_dict['name'] = name  # Add the name to the character dictionary
        char_list.append(char_dict)
    
    teams = []
    for _ in range(num_teams):
        # Randomly select 4 unique characters
        team = random.sample(char_list, 4)
        teams.append(team)
    return teams

def calculate_team_score(team):
    """
    Calculate a score for a team based on various criteria.
    
    Scoring considerations:
    1. Element diversity (more elements = higher score)
    2. Role balance (having different roles = higher score)
    3. Weapon diversity (different weapons = higher score)
    4. Region diversity (different regions = higher score)
    5. Elemental reaction potential
    
    Args:
        team: List of 4 character dictionaries
        
    Returns:
        Score for the team (higher is better)
    """
    score = 0

    for char in team:
        score += char['score']
    
    # Count unique elements
    elements = set(char['element'] for char in team)
    element_count = len(elements)
    
    # More elements generally means better elemental reaction potential
    if element_count == 4:
        score += 5  # Maximum diversity bonus
    elif element_count == 3:
        score += 10
    elif element_count == 2:
        score += 5
    
    # Count unique roles
    roles = set(char['role'] for char in team)
    role_count = len(roles)
    
    # Balanced teams with different roles get higher scores
    if role_count >= 3:
        score += 10
    
    # Count unique weapons
    weapons = set(char['weapon'] for char in team)
    weapon_count = len(weapons)
    
    # Weapon diversity bonus
    if weapon_count == 4:
        score += 2
    elif weapon_count == 3:
        score += 3
    elif weapon_count == 2 or weapon_count == 1:
        score -= 1
    
    # Count unique regions
    regions = set(char['region'] for char in team)
    region_count = len(regions)
    
    # Region diversity bonus
    if regions == 'Natlan' and roles == 'Support':
        score += 10
    
    # Check for specific elemental synergies
    element_pairs = set()
    for i in range(len(team)):
        for j in range(i+1, len(team)):
            element_pairs.add((team[i]['element'], team[j]['element']))
    
    # Add points for beneficial elemental combinations
    for elem1, elem2 in element_pairs:
        if (elem1, elem2) in [('Pyro', 'Cryo'), ('Cryo', 'Pyro')]:
            score += 15  # Melt reaction
        elif (elem1, elem2) in [('Pyro', 'Hydro'), ('Hydro', 'Pyro')]:
            score += 15  # Vaporize reaction
        elif (elem1, elem2) in [('Electro', 'Hydro'), ('Hydro', 'Electro')]:
            score += 5  # Electro-Charged
        elif (elem1, elem2) in [('Electro', 'Cryo'), ('Cryo', 'Electro')]:
            score -= 5  # Superconduct
        elif (elem1, elem2) in [('Pyro', 'Electro'), ('Electro', 'Pyro')]:
            score += 3  # Overload
        elif (elem1, elem2) in [('Dendro', 'Pyro'), ('Pyro', 'Dendro')]:
            score += 2  # Burning
        elif (elem1, elem2) in [('Dendro', 'Electro'), ('Electro', 'Dendro')]:
            score += 15  # Quicken
        elif (elem1, elem2) in [('Dendro', 'Hydro'), ('Hydro', 'Dendro')]:
            score += 2  # Bloom
    if element_pairs == 1:
        score += 5
    
    # Bonus for having at least one Main DPS
    has_any_dps = any('Main DPS' in char['role'] for char in team)
    if has_any_dps == 1:
        score += 12

    # Count number of Main DPS characters
    dps_count = sum(1 for char in team if 'Main DPS' in char['role'])

    # Bonus for having exactly one Main DPS
    if dps_count == 1:
        score += 15
    # Penalty for having multiple Main DPS
    elif dps_count > 1:
        score -= 20
    # Small penalty for having no Main DPS
    elif dps_count == 0:
        score -= 10
    
    # Bonus for having at least one healer/support
    has_support = any('Support' in char['role'] or 'Healer' in char['role'] for char in team)
    if has_support:
        score += 10

    support_count = sum(1 for char in team if 'Support' in char['role'])

    # Bonus for having exactly one Support
    if support_count == 1:
        score += 15
    # Penalty for having multiple Support
    elif support_count == 2:
        score += 20
    # Small penalty for having no Support
    elif support_count == 0:
        score -= 20
    return score


def find_best_team(characters_dict, num_teams=1000):
    """
    Generate multiple teams and return the one with the highest score.
    
    Args:
        characters_dict: Dictionary of characters
        num_teams: Number of teams to generate and evaluate
        
    Returns:
        Tuple of (best_team, best_score)
    """
    teams = generate_teams(characters_dict, num_teams)
    best_team = None
    best_score = -1
    
    for team in teams:
        score = calculate_team_score(team)
        if score > best_score:
            best_score = score
            best_team = team
    
    return best_team, best_score

def print_team(team, score):
    """
    Print a team and its score in a formatted way.
    
    Args:
        team: List of characters in the team
        score: The team's score
    """
    print(f"Team Score: {score}")
    print("Characters:")
    for char in team:
        print(f"  - {char['name']} ({char['element']}, {char['weapon']}, {char['role']}, {char['region']})")
    print()

# Main execution
if __name__ == "__main__":
    # Generate and evaluate teams
    best_team, best_score = find_best_team(characters, 10000)
    
    # Display the best team
    print("Best Team Found:")
    print_team(best_team, best_score)