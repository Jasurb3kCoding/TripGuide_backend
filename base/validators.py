from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(
    regex=r"^[\+]?[(]?[0-9]{5}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{2}[-\s\.]?[0-9]{2}$",
    message="Invalid phone number"
)
