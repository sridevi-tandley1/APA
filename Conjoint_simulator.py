import streamlit as st

# Part-Worth Utilities for each attribute level
part_worths = {
    "Screen Size": {5.5: 2, 6.0: 3, 6.5: 4},
    "Battery Life": {3000: 1, 4000: 3, 5000: 5},
    "Camera Quality": {8: 1, 12: 3, 16: 5},
    "Price": {300: 5, 500: 3, 700: 1}
}

# Function to calculate total utility based on user input
def calculate_utility(screen_size, battery_life, camera_quality, price):
    total_utility = (
        part_worths["Screen Size"][screen_size] +
        part_worths["Battery Life"][battery_life] +
        part_worths["Camera Quality"][camera_quality] +
        part_worths["Price"][price]
    )
    return total_utility

# Streamlit app layout
st.title("Conjoint Analysis Simulator")
st.write("### Simulate Consumer Preferences Based on Product Attributes")

# Sidebar for user inputs
st.sidebar.header("Select Product Features")
screen_size = st.sidebar.selectbox("Select Screen Size (in inches)", [5.5, 6.0, 6.5])
battery_life = st.sidebar.selectbox("Select Battery Life (mAh)", [3000, 4000, 5000])
camera_quality = st.sidebar.selectbox("Select Camera Quality (MP)", [8, 12, 16])
price = st.sidebar.selectbox("Select Price (USD)", [300, 500, 700])

# Calculate utility based on the selections
utility = calculate_utility(screen_size, battery_life, camera_quality, price)

# Display results
st.write(f"### Selected Product Configuration:")
st.write(f"Screen Size: {screen_size} inches")
st.write(f"Battery Life: {battery_life} mAh")
st.write(f"Camera Quality: {camera_quality} MP")
st.write(f"Price: ${price}")

st.write(f"### Predicted Utility for the selected product:")
st.write(f"The total utility for this product configuration is: **{utility}**")

# Provide some explanation to the user
st.write("""
### How It Works:
This simulator calculates the **total utility** for the selected product based on **consumer preferences** for each attribute. 
- A higher utility indicates a more desirable product configuration.
- The part-worth utilities (values assigned to each attribute level) are based on hypothetical consumer preferences.
""")

# Show part-worth utilities (optional for deeper insight)
st.write("### Part-Worth Utilities for each attribute level:")
st.write(part_worths)

# Add a button to display the utility score again (Optional)
if st.button("Recalculate Utility"):
    st.write(f"The total utility for the selected product configuration is: **{utility}**")

