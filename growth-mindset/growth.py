import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title & Description
st.title("DataSweeper Sterling Integrator 🚀")
st.write("Transform your files between CSV and Excel formats with built-in 🧹 data cleaning and 📊 visualization.")

# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read file
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)  
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)  
            else:
                st.error(f"Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"Error reading {file.name}: {str(e)}")
            continue

        # File details
        st.write(f"Preview of `{file.name}`:")
        st.dataframe(df.head())  

        # Data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns  
                    if not numeric_cols.empty:
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("✅ Missing Values Filled!")
                    else:
                        st.warning("⚠️ No numeric columns found to fill missing values.")

        # Column selection
        st.subheader("Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data visualization
        st.subheader("Data Visualization 📊")
        if st.checkbox(f"Show visualization for {file.name}"):
            numeric_df = df.select_dtypes(include="number")
            
            if not numeric_df.empty:
                st.bar_chart(numeric_df.iloc[:, :2])  # First 2 numeric columns
            else:
                st.warning("⚠️ No numeric data available for visualization!")

        # Conversion options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            file_name = file.name.replace(file_ext, f".{conversion_type.lower()}")

            try:
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False, engine="openpyxl")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)

                # ✅ Download button
                st.download_button(
                    label=f"Download {file_name}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
                st.success(f"✅ {file.name} converted successfully!")

            except Exception as e:
                st.error(f"Error in conversion: {str(e)}")





