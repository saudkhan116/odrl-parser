# Copyright 2024 saud.khan
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import json

def parse_odrl_policy(odrl_json):
    # Extract the policy object
    policy = odrl_json.get('policy', {})

    # Initialize a list to store human-readable text
    human_readable = []

    # Process permissions

    permissions = policy.get('odrl:permission', [])
    prohibitions = policy.get('odrl:prohibition', [])
    obligations = policy.get('odrl:obligation', [])

    # process permissions
    for permission in permissions:
        action = permission.get('odrl:action', 'an action')

        # Begin forming the sentence
        sentence = f"You are allowed to {parse_action(permission)} the resource."

        # Check for constraints
        constraint = permission.get('odrl:constraint', {})
        or_constraints = constraint.get('odrl:or', [])
        and_constraints = constraint.get('odrl:and', [])
        condition_type = 'permission'

        if or_constraints:
            text = parse_contraints(or_constraints, sentence, condition_type,'or')
        if and_constraints:
             text = parse_contraints(and_constraints, sentence, condition_type, 'and')
            
        human_readable.append(text)

    # process prohibitions
    for prohibition in prohibitions:

        #action = prohibition.get('odrl:action', 'an action')

        # Begin forming the sentence
        sentence = f"You are prohibited to {parse_action(prohibition)} the resource."

        # Check for constraints
        constraint = prohibition.get('odrl:constraint', {})
        or_constraints = constraint.get('odrl:or', [])
        and_constraints = constraint.get('odrl:and', [])
        condition_type = 'prohibition'

        if or_constraints:
            text = parse_contraints(or_constraints, sentence, condition_type,'or')
        if and_constraints:
                text = parse_contraints(and_constraints, sentence, condition_type, 'and')

        human_readable.append(text)
    
    # process obligations
    for obligation in obligations:
        action = obligation.get('odrl:action', 'an action')

        # Begin forming the sentence
        sentence = f"You are obligated to {parse_action(obligation)} the resource."

        # Check for constraints
        constraint = prohibition.get('odrl:constraint', {})
        or_constraints = constraint.get('odrl:or', [])
        and_constraints = constraint.get('odrl:and', [])
        condition_type = 'obligation'

        if or_constraints:
            text = parse_contraints(or_constraints, sentence, condition_type, 'or')
        if and_constraints:
                text = parse_contraints(and_constraints, sentence, condition_type, 'and')

        human_readable.append(text)

    return " ".join(human_readable)


def parse_action(condition_type):

    action = None
    if  condition_type.get('odrl:action', {}):
        action = condition_type.get('odrl:action', {})
        type = condition_type.get('odrl:type', 'use')
        return type
    return {action.lower()} 
        
         
         


def parse_contraints(constraints, sentence, condition_type, logical_operator):
    
    condition_sentences = []
    for con in constraints:

        left_operand = con.get('odrl:leftOperand', 'something')
        if type(left_operand) != str:
            left_operand = left_operand.get('@id', 'id')

        operator = con.get('odrl:operator', {}).get('@id', 'unknown').split(":")[-1]
        right_operand = con.get('odrl:rightOperand', 'a value')
        
        # Create a human-readable condition
        condition_sentence = f"the {left_operand} {operator} {right_operand}"
        condition_sentences.append(condition_sentence)

    if logical_operator == 'or':
        # Join all conditions with 'or'
        conditions_text = " or ".join(condition_sentences)
    elif logical_operator == 'and':
        # Join all conditions with 'and'
        conditions_text = " and ".join(condition_sentences)
    else:
        # Join Single condition
        conditions_text = "".join(condition_sentences)
    if condition_type == 'permission':
        sentence += f" This is allowed if {conditions_text}."
    elif condition_type == 'prohibition':
        sentence += f" This is prohibited if {conditions_text}."
    else:
        sentence += f" This is obligated if {conditions_text}."
    return sentence


def readFromFile(file):
    data = None
    with open(file, 'r') as f:
        data = f.read()
    return data


file = sys.argv[1]
policy = readFromFile(file)
policy = json.loads(policy)


print('Your odrl policy:')
print(json.dumps(policy, indent=2))

print('Interpretation:')
policy_text = parse_odrl_policy(policy)
print(policy_text)
