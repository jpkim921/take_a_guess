from prompt_toolkit import prompt, PromptSession


from validators import NumberValidator

session = PromptSession()

number = int(session.prompt('Give a number: ', validator=NumberValidator()))
print(f"you typed: {number}")