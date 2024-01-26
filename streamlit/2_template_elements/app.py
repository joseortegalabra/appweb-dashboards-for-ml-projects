import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.linear_model import LinearRegression
import time
from datetime import datetime, timedelta

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#NOTEBOOK TEXT ELEMENTS: https://github.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/blob/master/05_text_elements/main.py
st.subheader("TEXT DISPLAT ELEMENTS")


# Give your app a title
st.divider()
st.title("st.tittle: Text DisplatyElements")

# Header
st.divider()
st.header("st.header: Main header")

# Subheader
st.divider()
st.subheader("st.subheader: This is a subheader")

# Markdown
st.divider()
st.markdown("st.markdown: This is markdown **text**")
st.markdown("# Header1 (markdown)")
st.markdown("## Header 2 (markdown)")
st.markdown("### Header 3 (markdown)")

# Caption
st.divider()
st.caption("st.caption: This is a caption")

# Code block
st.divider()
st.write("st.code:")
st.code("""import pandas as pd
pd.read_csv(my_csv_file)
""")

# Preformatted text
st.divider()
st.write('st.write: Some text - more natural')
st.text("st.text: Some text - minus natural")

# LaTeX
st.divider()
st.write('st.latex')
st.latex("x = 2^2")

# Divider
st.divider()
st.text('Text above divider')
st.divider()
st.text('Text below divider')


#st.write
st.divider()
st.write('Some text')


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.divider()
st.divider()
#NOTEBOOK DATA DISPLAY ELEMENTS: https://github.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/blob/master/06_data_display_elements/main.py
st.subheader("DATA DISPLAY ELEMENTS")

# read data
df = pd.read_csv("data/sample.csv", dtype="int")

# show dataframe with st.dataframe(df)
st.write('##### show dataframe with st.dataframe(df) - allows to interact with the table')
st.dataframe(df)

# show dataframe with st.write(df)
st.write('#### show dataframe with st.write(df) - allows to interact with the table')
st.write(df)

# show dataframe with st.table(df)
st.write('#### show dataframe with st.table(df) - allows to interact with the table')
st.table(df)

#show metrics with st.metric(df)
st.write('#### show metrics with st.metric(df)')
st.metric(label="Expenses", value=900, delta=20, delta_color="inverse")
st.metric(label="Incomes", value=800, delta=1, delta_color="normal")


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.divider()
st.divider()
# NOTEBOOK INPUT WIDGESTS 1: https://github.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/blob/master/08_input_widgets/main.py
# NOTEBOOK INPUT WIDGESTS 2: https://github.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/blob/master/09_input_widgets_part2/main.py
st.subheader("INPUT WIDGETS ELEMENTS")

# Buttons - interact and show a value according the interection
st.write('#### Buttons - interact and show a value according the interection')
primary_btn = st.button(label="Primary", type="primary")
secondary_btn = st.button(label="Secondary", type="secondary")

if primary_btn:
    st.write("Hello from primary")

if secondary_btn:
    st.write("Hello from secondary")


# Checkbox - interact and show a value according the interaction
st.divider()
st.write('#### Checkbox - interact and show a value according the interaction')
checkbox = st.checkbox("Remember me")

if checkbox:
    st.write("I will remember you")
else:
    st.write("I will forget you")


# Radio buttons
st.divider()
st.write('#### Radio Selector - 1 selection - interact and show a value according the interaction')

df = pd.read_csv("data/sample.csv")

radio = st.radio("Choose a column", options=df.columns[1:], index=1, horizontal=True)
st.write(radio)


# Selectbox
st.divider()
st.write('#### Select Box - 1 selection - interact and show a value according the interaction')

select = st.selectbox("Choose a column", options=df.columns[1:], index=0)
st.write(select)


# Mutliselect
st.divider()
st.write('#### Multiselect - select multiple choices - interact and show a value according the interaction')

multiselect = st.multiselect("Choose as many columns as you want", options=df.columns[1:], default=["col2"], max_selections=2)
st.write(f'Output multiselect:')
#st.write(type(multiselect))
st.write(multiselect)


# Slider
st.divider()
st.write('#### slider - interact selecting a value and show a value according the interaction')

slider = st.slider("Pick a number", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
st.write(slider)


# Text input
st.divider()
st.write('#### Text input - interact and show a value according the interaction')

text_input = st.text_input("What's your name?", placeholder="John Doe")
st.write(f"Your name is: {text_input}")


# Number input
st.divider()
st.write('#### Number input - interact adding a number and interact incressing decessing this value')

num_input = st.number_input("Pick a number", min_value=0, max_value=100, value=0, step=1)
st.write(f"You picked {num_input}")



# date input
st.divider()
st.write('#### Date Input')
date_to_show = st.date_input("Input a date please")
st.write(f"The date that you select is: {date_to_show}")


# Toggle
st.divider()
st.write('#### Toggle - component that could be activate / deactivate')
toggle_on = st.toggle('Activate feature')

if toggle_on:
    st.write('Feature activated!')



# Text area
st.divider()
st.write('#### Text Area - area to write a long text, the large of the area could be modified')

txt_area = st.text_area("What do you want to tell me?", height=150, placeholder="Write your message here")
st.write(txt_area)




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.divider()
st.divider()
# EXAMPLE A BUTTON UPLOAD FILE SINCE THE SIDE BAR - https://bgremoval.streamlit.app/
st.subheader("UPLOAD FILE - st.file_uploader")

# use st.file_uploader to load files
uploaded_file = st.file_uploader("Upload a data file", type=["csv", "xlsx"])

# process the file when it is uploaded
if uploaded_file is not None:

    # load a csv file
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        st.write(df)

    # read a excel file
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        st.write(df)




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.divider()
st.divider()
# Mine
st.subheader("DOWNLOAD A FILE - st.download_button")

# generate data
data = {'Name': ['John', 'Jane', 'Doe'],
        'Age': [28, 25, 32],
        'City': ['New York', 'San Francisco', 'Los Angeles']}
df = pd.DataFrame(data)
st.write('Example data')
st.write(df)

#---
st.write('---> download data. In this example two ways to downlaod the data were generated')

# button to download the data as csv file
csv_file = df.to_csv(index=False)
st.download_button("Download CSV", csv_file, file_name='data.csv', key='csv_key')

# button to dowload a txt file
text_data = "Este es un archivo de texto de ejemplo."
st.download_button("Download Texto", text_data, file_name='texto_ejemplo.txt', key='text_key')





""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.divider()
st.divider()
# NOTEBOOK INPUT FORM ELEMENT: https://github.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/blob/master/10_forms/main.py
st.subheader("INPUT FORM ELEMENT")

# create form
st.write('FORM: using form to input a lot of variables/numbers/etc and then upload the UI. This because when a user change one value always all the python code is running from top to bottom')
with st.form("form_key"):
    st.write("What would like to order")
    appetizer = st.selectbox("Appetizers", options=["choice1", "choice2", "choice3"])
    main = st.selectbox("Main course", options=["choice1", "choice2", "choice3"])
    dessert = st.selectbox("Dessert", options=["choice1", "choice2", "choice3"])
    wine = st.checkbox("Are you bringing wine?")
    visit_date = st.date_input("When are you coming?")
    visit_time = st.time_input("At what time are you coming?")
    allergies = st.text_area("Any allergies?", placeholder="Leave us a note for allergies")
    submit_btn = st.form_submit_button("Submit")


# display the output of the form
st.write(f"""
         \n**Your order summary:**
         \nAppetizer: {appetizer}
         \nMain course: {main}
         \nDessert: {dessert}
         \nAre you bringing your own wine: {"yes" if wine else "no"}
         \nDate of visit: {visit_date}
         \nTime of visit: {visit_time}
         \nAllergies: {allergies}
         """)








""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.divider()
st.divider()
# lINK IDEA: https://discuss.streamlit.io/t/form-and-submit-button-in-sidebar/12436/2
st.subheader("FORM IN A SIDEBAR")

with st.form(key ='Form1'):
    with st.sidebar:
        user_word = st.sidebar.text_input("Enter a keyword", "habs")    
        select_language = st.sidebar.radio('Tweet language', ('All', 'English', 'French'))
        include_retweets = st.sidebar.checkbox('Include retweets in data')
        num_of_tweets = st.sidebar.number_input('Maximum number of tweets', 100)
        submitted1 = st.form_submit_button(label = 'Search Twitter 🔎')

if submitted1:
    st.write(f"""
            \n**VALUES IN FORM IN A SIDEBAR:**
            \nuser_word: {user_word}
            \nselect_language: {select_language}
            \ninclude_retweets: {include_retweets}
            \nnum_of_tweets: {num_of_tweets}
            """)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.divider()
st.divider()
# NOTEBOOK LAYOUT UI: https://github.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/blob/master/11_layout/main.py
st.subheader("LAYOUT UI")


# Sidebar 
with st.sidebar:
    st.write("Text in the sidebar")
    st.markdown("st.markdown: This is markdown **text**")

# sidebar option V2
st.sidebar.write("Other way to write in sidebar")
st.sidebar.markdown("### Header 3 (markdown)")


# Columns
st.write('#### Columns. Divide the UI in multiple columns')
col1, col2, col3 = st.columns(3)

col1.write("Text in a column")

slider = col2.slider("Choose a number", min_value=0, max_value=10)

col3.write(slider)


# Tabs
st.write('#### Tabs. Change of sections of contents without changing the the page')
df = pd.read_csv("data/sample.csv")

tab1, tab2 = st.tabs(["Line plot", "Bar plot"])

with tab1:
    tab1.write("A line plot")
    st.line_chart(df, x="year", y=["col1", "col2", "col3"])

with tab2:
    tab2.write("A bar plot")
    st.bar_chart(df, x="year", y=["col1", "col2", "col3"])



# Expander (collapsible element)
st.write('#### Expander or Colapser element. The option similar a dropdown to show or doesnt a element')
with st.expander("Click to expand"):
    st.write("--------I am text that you only see when you expand---------")




# Container
st.write('#### Container. Group elements')
with st.container():
    st.write("This is inside the container")

st.write("This is outside the container")



# Container v2 - utilidades:  Organización del Contenido, ontrol del Diseño, Efectos de Estilo, Manejo de Elementos de Entrada, Mejora de la Experiencia del Usuario,
# Diseño Responsivo, Facilita el Mantenimiento del Código
st.write('#### Container v2. Group elements. Plot image with matplotlib')


# create container
with st.container():
    # all of this are inside the container
    st.write("##### Input Section")
    
    # ingress a number
    user_input = st.text_input("Type a number:", "10")
    processed_input = float(user_input)
    st.write(f"The input number * 2 is: {processed_input * 2}")

    # plot
    st.write("##### Plot inside the container")
    x = np.linspace(0, 10, 100)
    y = np.sin(processed_input * x)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    st.pyplot(fig) # show plot in streamlit

# After exiting the with block, anything written will be outside the container
st.write("This is also outside the container")


st.write('#### Container v3 - interesting example - make a matrix using  column elements')
# sources: https://docs.streamlit.io/library/api-reference/layout/st.container
row1 = st.columns(3)
row2 = st.columns(3)
for col in row1 + row2:
    tile = col.container(height=120)
    tile.title(":balloon:")
    tile.write(f'matrix content')


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.divider()
st.divider()
# Mine
st.subheader("PLOT DATA - MATPLOTLIB - SEABORN - STREAMLIT - PLOTLY")


# generate data to example
def get_data_to_plot_trend_timeseries():
    np.random.seed(42)
    time = np.arange(1, 101, 1)  # Time 1 to 100
    values_data = 2 * time + np.random.normal(scale=10, size=len(time))  # Trend plot with noise

    # adjust a trendline
    coef = np.polyfit(time, values_data, 1)
    trend = np.polyval(coef, time)
    
    # generate a dataframe
    data = {'Time': time, 'Trend': trend, 'Values_data':values_data}
    df = pd.DataFrame(data)
    
    return df
data_to_plot = get_data_to_plot_trend_timeseries()


# plot matplotlib
st.write('#### Plot data - matplotlib')
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(data_to_plot['Time'], data_to_plot['Values_data'], label='Values with noise')
ax.plot(data_to_plot['Time'], data_to_plot['Trend'], label='Trend', color='red')
ax.set_xlabel('Time')
ax.set_ylabel('Values')
ax.set_title('Trend in a time series')
ax.legend()
st.pyplot(fig) # IMPORTANTE show figure of plotly in seaborn


# plot seaborn
st.write('#### Plot data - seaborn')
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=data_to_plot, x='Time', y='Trend', label='Trend', color='red')
sns.scatterplot(data=data_to_plot, x='Time', y='Values_data', label='Values with Noise')
plt.xlabel('Time')
plt.ylabel('Values')
plt.title('Trend and Noise in Time Series')
plt.legend()
st.pyplot(fig)  # Show plot in Streamlit



# plot streamlit
st.write('#### Plot data - streamlit - interactive plot - limited in kind of plots that can do with it')
st.line_chart(data_to_plot, x="Time", y=["Values_data", "Trend"])


# Plot using Plotly
st.write('#### Plot data - plotly - interactive plot')
fig = px.scatter(data_to_plot, 
                 x='Time', 
                 y='Values_data', 
                 labels={'Values_data': 'Values with Noise'},
                 title='Trend and Noise in Time Series')
fig.add_trace(px.line(data_to_plot, x='Time', y='Trend', labels={'Trend': 'Trend'}).data[0])
st.plotly_chart(fig) # Show plot plotly in Streamlit - amazing one line of python code





""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.divider()
st.divider()
# Mine
st.subheader("SAVE IN CACHE -decorator- st.cache_data(xx) - st.cache_resource(xx)")


####------------####------------####------------####------------
st.write('#### @st.cache_data - sleep 15 segs')
st.write('Decorator to cache functions that return data (e.g. dataframe transforms, database queries, ML inference).')

@st.cache_data(show_spinner="Fetching data...")  # show spinner
def cache_this_function():
    time.sleep(15)
    out = "I'm done running"
    return out

out = cache_this_function()
st.write(out)


####------------####------------####------------####------------
st.write('#### st.cache_resource')
st.write('Decorator to cache functions that return global resources (e.g. database connections, ML models). Cached objects are shared across all users, sessions')

@st.cache_resource(show_spinner="Trainning model...")
def create_simple_linear_regression():
    time.sleep(2)
    X = np.array([1,2,3,4,5,6,7]).reshape(-1,1)
    y = np.array([1,2,3,4,5,6,7])
    model = LinearRegression().fit(X, y)
    return model

lr = create_simple_linear_regression()
X_pred = np.array([8]).reshape(-1,1)
pred = lr.predict(X_pred)

st.write(f"The prediction is: {pred[0]}")


####------------####------------####------------####------------
st.write('#### Button test cache')
st.write('This button is not connected to anything, but clicking it is considered user interaction and therefore runs the entire script and you can see the delay in cached codes')
st.button('Test cache')






""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.divider()
st.divider()
# link script explicacion: https://github.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/blob/master/23_state_advanced/main.py
# link documentation: https://docs.streamlit.io/library/api-reference/session-state

# link script example 1:https://github.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/blob/master/24_state_exercise/main.py
# link script example 2: 

st.subheader("SESSION STATE & CALLBACKS")
st.write('#### Utiliy')
st.write('**Session State is a way to share variables between reruns, for each user session**. In addition to the ability to store and persist state, \
Streamlit also exposes the ability to **manipulate state using Callbacks**. Session state also persists across apps inside a multipage app.')




###############################
st.divider()
st.write('#### Example 1: store value in session state a show it')
st.write("Store widget value in session state")
st.slider("Select a number", 0, 10, key="slider")
st.write(st.session_state)



###############################
st.divider()
st.write('#### Example 2: session state & callabacks - the output is written in the top of the web page')
def form_callback():
    st.write(st.session_state.my_slider)
    st.write(st.session_state.my_checkbox)

with st.form(key='my_form'):
    slider_input = st.slider('My slider', 0, 10, 5, key='my_slider')
    checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
    submit_button = st.form_submit_button(label='Submit', on_click=form_callback)



###############################
st.divider()
st.write('#### Example 3: Interactive temperature calculator - modify values of session states - persisting values')


if "celsius" not in st.session_state:
    st.session_state['celsius'] = 0.00

if "farenheit" not in st.session_state:
    st.session_state['farenheit'] = 32.00

if "kelvin" not in st.session_state:
    st.session_state['kelvin'] = 273.15

def celsius_conversion():
    celsius = st.session_state['celsius']
    
    st.session_state['farenheit'] = (celsius * 9 / 5) + 32
    st.session_state['kelvin'] = celsius + 273.15

def farenheit_conversion():
    farenheit = st.session_state['farenheit']

    st.session_state['celsius'] = (farenheit - 32) * 5 / 9
    st.session_state['kelvin'] = (farenheit - 32) * 5 / 9 + 273.15

def kelvin_conversion():
    kelvin = st.session_state['kelvin']

    st.session_state['celsius'] = kelvin - 273.15
    st.session_state['farenheit'] = (kelvin - 273.15) * 9 / 5 + 32

def add_to_celsius(num):
    st.session_state['celsius'] += num
    celsius_conversion()

def set_temperatures(celsius, farenheit, kelvin):
    st.session_state['celsius'] = celsius
    st.session_state['farenheit'] = farenheit
    st.session_state['kelvin'] = kelvin

col1, col2, col3 = st.columns(3)

col1.number_input("Celsius", step=0.01, key="celsius", on_change=celsius_conversion)
col2.number_input("Farenheit", step=0.01, key="farenheit", on_change=farenheit_conversion)
col3.number_input("Kelvin", step=0.01, key="kelvin", on_change=kelvin_conversion)

col1, _, _ = st.columns(3)
num = col1.number_input("Add to Celsius", step=1)
col1.button("Add", type="primary", 
            on_click=add_to_celsius, 
            args=(num,))

col1, col2, col3 = st.columns(3)

col1.button('🧊 Freezing point of water', 
            on_click=set_temperatures, 
            kwargs=dict(celsius=0.00, farenheit=32.00, kelvin=273.15))
col2.button('🔥 Boiling point of water',
            on_click=set_temperatures,
            kwargs=dict(celsius=100.00, farenheit=212.00, kelvin=373.15))
col3.button('🥶 Absolute zero',
            on_click=set_temperatures,
            kwargs=dict(celsius=-273.15, farenheit=-459.67, kelvin=0.00))

st.write('values in session state')
st.write(f'celsius: {st.session_state.celsius}')
st.write(f'farenheit: {st.session_state.farenheit}')
st.write(f'kelvin: {st.session_state.kelvin}')





""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.divider()
st.divider()
# link notebook: https://github.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/blob/master/18_caching_capstone/main.py
st.subheader("EXAMPLES STRUCTURE TO ADD PARAMETERS BY USER - THIS IS NOT USING FORM, SO EACH TIME THAT THE USE CHANGE A VALUE ALL THE WEB PAGE IS REFRESHED")


####------------####------------####------------####------------
st.write("##### Input values in columns)")
col1, col2, col3 = st.columns(3)
with col1:
    odor = st.selectbox('Odor', ('a - almond', 'l - anisel', 'c - creosote', 'y - fishy', 'f - foul', 'm - musty', 'n - none', 'p - pungent', 's - spicy'))
    stalk_surface_above_ring = st.selectbox('Stalk surface above ring', ('f - fibrous', 'y - scaly', 'k - silky', 's - smooth'))
    stalk_color_below_ring = st.selectbox('Stalk color below ring', ('n - brown', 'b - buff', 'c - cinnamon', 'g - gray', 'o - orange', 'p - pink', 'e - red', 'w - white', 'y - yellow'))
with col2:
    gill_size = st.selectbox('Gill size', ('b - broad', 'n - narrow'))
    stalk_surface_below_ring = st.selectbox('Stalk surface below ring', ('f - fibrous', 'y - scaly', 'k - silky', 's - smooth'))
    ring_type = st.selectbox('Ring type', ('e - evanescente', 'f - flaring', 'l - large', 'n - none', 'p - pendant', 's - sheathing', 'z - zone'))
with col3:
    gill_color = st.selectbox('Gill color', ('k - black', 'n - brown', 'b - buff', 'h - chocolate', 'g - gray', 'r - green', 'o - orange', 'p - pink', 'u - purple', 'e - red', 'w - white', 'y - yellow'))
    stalk_color_above_ring = st.selectbox('Stalk color above ring', ('n - brown', 'b - buff', 'c - cinnamon', 'g - gray', 'o - orange', 'p - pink', 'e - red', 'w - white', 'y - yellow'))
    spore_print_color = st.selectbox('Spore print color', ('k - black', 'n - brown', 'b - buff', 'h - chocolate', 'r - green', 'o - orange', 'u - purple', 'w - white', 'y - yellow'))


####------------####------------####------------####------------
st.write('\n\n')
st.write("##### Operate with input values (in this case, show values)")
pred_btn = st.button("Do actions with input values - show values", type="primary")

# if the button is press
if pred_btn:
    st.write('**column 1**')
    st.write('odor: ', odor)
    st.write('stalk_surface_above_ring: ', stalk_surface_above_ring)
    st.write('stalk_color_below_ring: ', stalk_color_below_ring)

    st.write('**column 2**')
    st.write('gill_size: ', gill_size)
    st.write('stalk_surface_below_ring: ', stalk_surface_below_ring)
    st.write('ring_type: ', ring_type)

    st.write('**column 3**')
    st.write('gill_color: ', gill_color)
    st.write('stalk_color_above_ring: ', stalk_color_above_ring)
    st.write('spore_print_color: ', spore_print_color)




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
st.divider()
st.divider()
# link notebook: https://github.com/chrieke/prettymapp/blob/main/streamlit-prettymapp/app.py
st.subheader("EXAMPLES STRUCTURE TO ADD PARAMETERS BY USER - THIS EXAMPLE USE FORM")
st.write('#### ADAPTED FROM https://github.com/chrieke/prettymapp/blob/main/streamlit-prettymapp/app.py')









st.write("")
form = st.form(key="form_settings")
col1, col2, col3 = form.columns([3, 1, 1])

address = col1.text_input(
    "Location address",
    key="address",
)
radius = col2.slider(
    "Radius",
    100,
    1500,
    key="radius",
)

expander = form.expander("Customize map style")
col1style, col2style, _, col3style = expander.columns([2, 2, 0.1, 1])

shape_options = ["circle", "rectangle"]
shape = col1style.radio(
    "Map Shape",
    options=shape_options,
    key="shape",
)

bg_shape_options = ["rectangle", "circle", None]
bg_shape = col1style.radio(
    "Background Shape",
    options=bg_shape_options,
    key="bg_shape",
)
bg_color = col1style.color_picker(
    "Background Color",
    key="bg_color",
)
bg_buffer = col1style.slider(
    "Background Size",
    min_value=0,
    max_value=50,
    help="How much the background extends beyond the figure.",
    key="bg_buffer",
)

col1style.markdown("---")
contour_color = col1style.color_picker(
    "Map contour color",
    key="contour_color",
)
contour_width = col1style.slider(
    "Map contour width",
    0,
    30,
    help="Thickness of contour line sourrounding the map.",
    key="contour_width",
)

name_on = col2style.checkbox(
    "Display title",
    help="If checked, adds the selected address as the title. Can be customized below.",
    key="name_on",
)
custom_title = col2style.text_input(
    "Custom title (optional)",
    max_chars=30,
    key="custom_title",
)
font_size = col2style.slider(
    "Title font size",
    min_value=1,
    max_value=50,
    key="font_size",
)
font_color = col2style.color_picker(
    "Title font color",
    key="font_color",
)
text_x = col2style.slider(
    "Title left/right",
    -100,
    100,
    key="text_x",
)
text_y = col2style.slider(
    "Title top/bottom",
    -100,
    100,
    key="text_y",
)
text_rotation = col2style.slider(
    "Title rotation",
    -90,
    90,
    key="text_rotation",
)
form.form_submit_button(label="Submit")