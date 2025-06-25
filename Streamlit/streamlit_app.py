from my_module import df_stock
import streamlit as st
import pandas as pd 
import time
from my_module import df_stock, pivot_df_stock, grouped_df_stock, df_map, fig_mat, fig_sns


st.title("File Upload Test")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    st.success("File uploaded!")
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())



st.title("Original df_stock")
st.table(df_stock.head())

st.title("pivot_df_stock")
st.table(pivot_df_stock.head())

st.title("line chart")
st.line_chart(pivot_df_stock, x_label="Time", y_label="Closed Value",color=("#be3fe1", "#ffaa00", "#3fe1cd"))

st.header("header here")
st.subheader('subheader here')
st.title("Your title text here")
st.write("create a table:")
df = pd.DataFrame({'id':[1,2,3], 'name':['avi','shir','danny']})
st.write(df)
st.dataframe(df.style.highlight_max(axis=0))
st.info("important info")
st.success("Something successfully!")
st.error("Something failed!")
st.warning("Something warning!")
st.markdown("**Bold Text** and _Italic Text_")
st.markdown("# H1 Header\n## H2 Header\n- Bullet list item")
st.markdown("[Google](https://www.google.com)")
st.markdown("💡 Tip: Use emoji for fun UI!")
st.table(df)
with st.echo():
    st.write("This text and the code that generated it will be shown!")

with st.spinner("Loading..."):
    time.sleep(5)  # Simulate a long task

st.success("Done!")

progress_bar = st.progress(0)  # Start at 0%
placeholder = st.empty() # creates a placeholder in your Streamlit app that you can later update or replace dynamically.



# USING OBJECTS
for percent_complete in range(101):
    time.sleep(0.1)
    placeholder.write(f"{percent_complete}%")
    progress_bar.progress(percent_complete)

st.success("Task completed!")

tab1, tab2 = st.tabs(["matplotlib Chart", "seaborn Chart"])

with tab1:
    st.write("Matplotlib Chart")
    st.pyplot(fig_mat)

with tab2:
    st.write("Seaborn Chat")
    st.pyplot(fig_sns)

with st.expander("See more details"):
    st.write("Here are some hidden details")
    st.image("https://media2.dev.to/dynamic/image/width=1080,height=1080,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fqo23tbzej4ll5mdkrwnd.jpg", caption="Example Image", width = 200)
left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
b = left_column.button('Press me!')
if b:
    st.write('Button was pressed')

# Or even better, call Streamlit functions inside a "with" block:
# "with" makes sure content is placed inside a layout container
with right_column:
    chosen = st.radio('Pick Name',['avi', 'shir', 'danny'])
    st.write(f"Your name is {chosen}")

add_slider = st.sidebar.slider('x', 0.0, 100.0, (25.0, 75.0))  # widget

# Add a selectbox to the sidebar  
add_selectbox = st.sidebar.selectbox(
    'Pick a name',
    ['avi','shir','danny'])