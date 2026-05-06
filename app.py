import streamlit as st
from rag_engine import search_product

st.set_page_config(page_title="Product Search Copilot", layout="wide")

st.title("🛍️ Product Search Copilot (AI Powered)")

# Sidebar filter
st.sidebar.title("🔍 Filters")
max_price = st.sidebar.slider("Max Price", 1000, 100000, 50000)

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("💬 Ask something (e.g., cheap phone under 20000)")

if query:
    results = search_product(query)

    # Apply sidebar filter
    filtered_results = []
    for r in results:
        try:
            price = int(r.split("-")[-1])
            if price <= max_price:
                filtered_results.append(r)
        except:
            filtered_results.append(r)

    st.session_state.history.append(("User", query))
    st.session_state.history.append(("Bot", filtered_results))

# Display chat
for role, msgs in st.session_state.history:
    if role == "User":
        st.markdown(f"**🧑 You:** {msgs}")
    else:
        st.markdown("**🤖 Bot:**")
        for msg in msgs:
            parts = msg.split(" - ")

            if len(parts) == 3:
                st.markdown(f"### 📱 {parts[0]}")
                st.write(f"📝 {parts[1]}")
                st.write(f"💰 ₹{parts[2]}")
                st.divider()
            else:
                st.write(msg)

# Support system
st.subheader("📦 Customer Support")

issue = st.text_input("Raise an issue")

if issue:
    st.success("✅ Your ticket has been created. Our team will contact you soon.")