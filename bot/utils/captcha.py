import random
from typing import Tuple, List

def generate_math_captcha() -> Tuple[str, int, List[int]]:
    """Generates a random math question, the correct answer, and a set of multiple choices."""
    num1 = random.randint(1, 15)
    num2 = random.randint(1, 10)
    operator = random.choice(["+", "-"])
    
    if operator == "+":
        answer = num1 + num2
    else:
        # Prevent negative results for simplicity
        if num1 < num2:
            num1, num2 = num2, num1
        answer = num1 - num2
        
    question = f"{num1} {operator} {num2}"
    
    # Generate choices including the correct answer
    choices = {answer}
    while len(choices) < 4:
        offset = random.randint(-5, 5)
        if offset != 0:
            choices.add(answer + offset)
            
    choices_list = list(choices)
    random.shuffle(choices_list)
    
    return question, answer, choices_list
