import replicate
from creds import API_TOKEN

replicate=replicate.Client(API_TOKEN)

input = {
    "prompt": "what is the meaning of life",
    "temperature": 0.2
}

for event in replicate.stream("snowflake/snowflake-arctic-instruct",input=input):
    print(event.data)