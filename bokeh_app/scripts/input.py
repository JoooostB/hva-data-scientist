from bokeh.io import output_file, show
from bokeh.models.widgets import TextAreaInput
from bokeh.models import Panel, Div, Toggle
from bokeh.layouts import column, row
from scripts.spark import Spark

btn = 'warning'
inpt = 'No input given'
toggle = Toggle(label=inpt, button_type=btn)
spark = Spark()


# In deze functie moeten we de sentiment analysis gaan aanroepen op de 'new' variabele
# en op basis daarvan het label en button type aanpassen.
def input_handler(attr, old, new):
    print("Previous label: " + old)
    print("Updated label: " + new)
    if spark.user_input(new):
        toggle.label = "Positief! 😀"
        toggle.button_type = 'success'
    else:
        toggle.label = "Negatief! 😥"
        toggle.button_type = 'danger'


# Deze functie genereert een textinput veld en roept de input_handler aan zodra de value van het tekstveld is veranderd.
def input_tab():
    output_file("bokeh_app/output/text_input.html")
    text_input = TextAreaInput(value="Voer je review hier in :)", rows=6, title="Sentiment tester")
    text_input.on_change("value", input_handler)
    tab = Panel(child=column(text_input, toggle), title='Tester')
    return tab

