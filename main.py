import streamlit as st
from rag_engine import ask_policylens
from pdf_generator import generate_policy_pdf # Import our new tool

st.set_page_config(page_title="PolicyLens AI", page_icon="🏛️")
st.title("🏛️ PolicyLens AI")

# 1. User Profile Sidebar
with st.sidebar:
    st.header("👤 Citizen Profile")
    name = st.text_input("Full Name", "Citizen User")
    age = st.number_input("Age", 0, 100, 18)
    state = st.selectbox("State", ["Central", "Maharashtra", "Delhi", "Karnataka", "J&K", "Tamil Nadu"])
    income = st.text_input("Family Income (₹)", "250000")
    category = st.selectbox("Category", ["General", "OBC", "SC", "ST"])
    occupation = st.selectbox("Occupation", ["Student", "Farmer", "Unemployed", "Self-Employed"])

# 2. Query Area
user_query = st.text_area("What scholarship or scheme are you looking for?")

if st.button("Find Matching Schemes", type="primary"):
    if user_query:
        # Pass the state and profile into the query
        full_context = f"User is from {state}. Profile: {age}yo {occupation}, {category}, {income} income. Query: {user_query}"
        
        with st.spinner("🤖 AI is analyzing policies..."):
            answer = ask_policylens(full_context)
            
            # Save the answer in "session_state" so it stays on screen 
            # and doesn't disappear when we click the download button
            st.session_state['last_answer'] = answer
            st.session_state['detected_scheme'] = answer.split('\n')[0].replace('*', '')

# 3. Display Results and Download Button
if 'last_answer' in st.session_state:
    st.markdown("### 📋 Recommended Scheme")
    st.info(st.session_state['last_answer'])
    
    st.divider()
    st.subheader("📝 Take Next Step")
    st.write("Generate a pre-filled application draft to take to your nearest CSC or Government office.")
    
    # Prepare data for PDF
    applicant_data = {
        "Name": name,
        "Age": str(age),
        "State": state,
        "Income": income,
        "Category": category,
        "Occupation": occupation
    }
    
    # Generate the PDF
    pdf_bytes = generate_policy_pdf(applicant_data, st.session_state['detected_scheme'])
    
    st.download_button(
        label="📥 Download Application Draft (PDF)",
        data=bytes(pdf_bytes),
        file_name=f"PolicyLens_Draft_{name.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )