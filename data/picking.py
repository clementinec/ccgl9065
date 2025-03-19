import streamlit as st
import random

# Define the list of group
group = [
    "Educators and academics from STEM",
    "Policy makers and government officials",
    "Business leaders and entrepreneurs in energy sector",
    "Social scientists and ethicists",
    "Tech industry professionals",
    "Self-defined (Pick as you wish)",
    "Space Exploration Advocacy (Anti-CC)",
    "Space exploration should be paused (Pro-CC)"
]

# Initialize session state variables if they don't exist
if 'remaining_group' not in st.session_state:
    st.session_state.remaining_group = group.copy()
if 'selected_group' not in st.session_state:
    st.session_state.selected_group = []
if 'occurrences' not in st.session_state:
    st.session_state.occurrences = 0
if 'phase_two_group' not in st.session_state:
    st.session_state.phase_two_group = []
if 'selected_phase_two' not in st.session_state:
    st.session_state.selected_phase_two = []

# Random selection function for Group assignment
def select_item_phase_one():
    if st.session_state.remaining_group:
        st.session_state.occurrences += 1
        selected = random.choice(st.session_state.remaining_group)
        if selected not in ["Space Exploration Advocacy (Anti-CC)", "Space exploration should be paused (Pro-CC)"]:
            st.session_state.phase_two_group.append(selected)
        st.session_state.selected_group.append((st.session_state.occurrences, selected))
        st.session_state.remaining_group.remove(selected)
    else:
        st.warning('All group in Group assignment have been selected!')

# Random selection function for phase two
def select_item_phase_two():
    if st.session_state.phase_two_group:
        selected = random.choice(st.session_state.phase_two_group)
        st.session_state.selected_phase_two.append(selected)
        st.session_state.phase_two_group.remove(selected)
    else:
        st.warning('All group in phase two have been selected!')

# Display UI elements for Group assignment
st.header("Initial Group Assignment")
if st.button('Assign Group'):
    select_item_phase_one()

# Display the selected group with occurrence numbers and increased font size
if st.session_state.selected_group:
    st.markdown("<h2 style='font-size:24px;'>Selected group in Group assignment:</h2>", unsafe_allow_html=True)
    for occ, item in st.session_state.selected_group:
        st.markdown(f"<span style='font-size:20px;'>Group {occ}: {item}</span>", unsafe_allow_html=True)

# Display UI elements for phase two
st.header("Let's hear it from the people")
if st.button('Presenting Group'):
    select_item_phase_two()

# Display the selected group for phase two
if st.session_state.selected_phase_two:
    st.markdown("<h2 style='font-size:24px;'>Selected group in Phase Two:</h2>", unsafe_allow_html=True)
    for item in st.session_state.selected_phase_two:
        st.markdown(f"<span style='font-size:20px;'>{item}</span>", unsafe_allow_html=True)
