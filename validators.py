from prompt_toolkit.validation import Validator, ValidationError


class YesNoValidator(Validator):
    def validate(self, document):
        text = document.text
        if text:
            if text.lower() not in ['y', 'n', 'yes', 'no']:
                raise ValidationError(message="Enter one of the following: ['y', 'n', 'yes', 'no']")
        else:
            raise ValidationError(message='Cannot be an empty string.')


class NumberValidator(Validator):    
    def validate(self, document):
        text = document.text
        if text and not text.isdigit():
            raise ValidationError(message='Not A Number')


class NotStringValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(message='Cannot be an empty string.')
        elif not text.isdigit():
            raise ValidationError(message='Cannot be a string.')
