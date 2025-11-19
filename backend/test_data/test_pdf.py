from PyPDFForm import PdfWrapper

# Load the form
form = PdfWrapper("senior_citizen_form_all.pdf")

# Print all field names and their current values
# This tells you exactly what keys to use in your dictionary
print(form.schema)