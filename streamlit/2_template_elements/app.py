import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.linear_model import LinearRegression
import time

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


# Text area
st.divider()
st.write('#### Text Area - area to write a long text, the large of the area could be modified')

txt_area = st.text_area("What do you want to tell me?", height=150, placeholder="Write your message here")
st.write(txt_area)




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
# NOTEBOOK LAYOUT UI: https://github.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/blob/master/11_layout/main.py
st.subheader("LAYOUT UI")


# Sidebar 
with st.sidebar:
    st.write("Text in the sidebar")


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
    st.header("Input Section")
    
    # ingress a number
    user_input = st.text_input("Type a number:", "10")
    processed_input = float(user_input)
    st.write(f"The input number * 2 is: {processed_input * 2}")

    # plot
    st.header("Plot inside the container")
    x = np.linspace(0, 10, 100)
    y = np.sin(processed_input * x)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    st.pyplot(fig) # show plot in streamlit

# After exiting the with block, anything written will be outside the container
st.write("This is also outside the container")





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
# Mine
st.subheader("SAVE IN CACHE -decorator- st.cache_data(xx) - st.cache_resource(xx)")


####------------####------------####------------####------------
st.write('#### @st.cache_data - sleep 15 segs')
st.write('Decorator to cache functions that return data (e.g. dataframe transforms, database queries, ML inference).')

@st.cache_data
def cache_this_function():
    time.sleep(15)
    out = "I'm done running"
    return out

out = cache_this_function()
st.write(out)


####------------####------------####------------####------------
st.write('#### st.cache_resource')
st.write('Decorator to cache functions that return global resources (e.g. database connections, ML models). Cached objects are shared across all users, sessions')

@st.cache_resource
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