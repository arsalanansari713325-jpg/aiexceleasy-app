import streamlit as st
import pandas as pd
import json
import google.generativeai as genai
import io

st.title("📊 AI Excel Database Generator (Free)")
st.write("Customer ki demand copy-paste karein aur Excel sheet payein!")

api_key = st.text_input("Enter Google Gemini API Key:", type="password")
customer_demand = st.text_area("Yahan customer ki demand copy-paste karein:", placeholder="Example: Mujhe 5 kg Aata chahiye deepak ko dena hai rate 40...")

if st.button("Create Database 🚀"):
    if not api_key:
        st.error("Please enter your Gemini API Key first!")
    elif not customer_demand:
        st.error("Please paste some customer demand text!")
    else:
        with st.spinner("Gemini AI data process kar raha hai... Please wait..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                prompt = f"Convert the following raw customer demand text into a clean structured table data with fields: Customer Name, Product, Quantity, Rate, Total Amount. Return ONLY a valid JSON array of objects without markdown formatting or code blocks.\nText: {customer_demand}"
                
                response = model.generate_content(prompt)
                raw_content = response.text.strip()
                
                if raw_content.startswith("```json"):
                    raw_content = raw_content[7:-3].strip()
                elif raw_content.startswith("```"):
                    raw_content = raw_content[3:-3].strip()
                
                data = json.loads(raw_content)
                df = pd.DataFrame(data)
                
                st.success("Data Successfully Processed!")
                st.dataframe(df)
                
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name='Sheet1', index=False)
                
                st.download_button(
                    label="Download Excel File 📥",
                    data=buffer.getvalue(),
                    file_name="AI_Generated_Database.xlsx",
                    mime="application/vnd.ms-excel"
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")
