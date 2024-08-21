
<!-- 
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
!-->

# ODRL Parser
This simple odrl parser is a policy parser, developed in python that translates odrl based policies to the human readable text.


### Usage

```python
python odrl-parser.py sample-policy.json
```

### Condition types:
* Permissions
* Prohitbitions
* Obligations

### Example Policy

```json
{
    "@context": {
        "odrl": "http://www.w3.org/ns/odrl/2/"
    },
    "@type": "PolicyDefinitionRequestDto",
    "@id": "example-policy",
    "policy": {
        "@type": "odrl:Set",
        "odrl:permission": [
            {
                "odrl:action": {
                    "odrl:type": "USE"
                },
                "odrl:constraint": {
                    "@type": "LogicalConstraint",
                    "odrl:and": [
                        {
                            "@type": "Constraint",
                            "odrl:leftOperand": {
                                "@id": "Membership"
                            },
                            "odrl:operator": {
                                "@id": "odrl:eq"
                            },
                            "odrl:rightOperand": "active"
                        },
                        {
                            "@type": "Constraint",
                            "odrl:leftOperand": {
                                "@id": "UsagePurpose"
                            },
                            "odrl:operator": {
                                "@id": "odrl:eq"
                            },
                            "odrl:rightOperand": "non-commercial"
                        }
                    ]
                }
            }
        ],
        "odrl:prohibition": [
            {
                "odrl:action": {
                    "odrl:type": "USE"
                },
                "odrl:constraint": {
                    "@type": "LogicalConstraint",
                    "odrl:and": [
                        {
                            "@type": "Constraint",
                            "odrl:leftOperand": {
                                "@id": "purpose"
                            },
                            "odrl:operator": {
                                "@id": "odrl:eq"
                            },
                            "odrl:rightOperand": "http://example.com/music/4567"
                        }
                    ]
                }
            }
        ]
    }
}
```



