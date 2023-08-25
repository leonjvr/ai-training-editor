import streamlit as st
import json

def is_json_str(value):
    """Check if a string is JSON format."""
    try:
        json.loads(value)
        return True
    except (ValueError, TypeError):
        return False


@st.cache_data
def load_data(uploaded_file):
    lines = [line.decode() for line in uploaded_file.readlines()]
    data = [json.loads(line) for line in lines]
    return data


@st.cache_data
def save_data(filename, data):
    with open(filename, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    return filename


def display_table_content(json_list, parent_key=""):
    """Display a list of dictionaries (rows) as a table and return edited content."""
    if not json_list or not all(isinstance(item, dict) for item in json_list):
        return json_list  # Return original list if it's not a list of dicts

    # Extract headers
    headers = list(json_list[0].keys())

    # Display headers
    col_headers = st.columns(len(headers))
    for i, header in enumerate(headers):
        col_headers[i].write(header)

    edited_table = []

    for idx, row in enumerate(json_list):
        edited_row = {}
        cols = st.columns(len(headers))
        
        for i, header in enumerate(headers):
            unique_key = parent_key + f"_{idx}_{header}"
            value = row.get(header, "")

            # Check for nested list of dictionaries
            if isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
                edited_row[header] = display_table_content(value, unique_key)
            else:
                edited_value = cols[i].text_input("", str(value), key=unique_key)
                if is_jsonable(edited_value):
                    edited_row[header] = json.loads(edited_value)
                else:
                    edited_row[header] = edited_value
        
        edited_table.append(edited_row)

    return edited_table


def is_jsonable(value):
    """Check if a string can be loaded as JSON."""
    try:
        json.loads(value)
        return True
    except (TypeError, json.JSONDecodeError):
        return False

def display_json_content(json_obj, level=0, parent_key=""):
    """Recursively display JSON content with Streamlit."""
    if isinstance(json_obj, dict):
        edited_data = {}
        for key, value in json_obj.items():
            st.write("  " * level + f"{key}:")
            unique_key = parent_key + "_" + key
            edited_data[key] = display_json_content(value, level+1, unique_key)
        return edited_data
    elif isinstance(json_obj, list):
        # Check if data appears to be a row (list of dictionaries with similar keys)
        if json_obj and all(isinstance(item, dict) for item in json_obj):
            return display_table_content(json_obj, parent_key)
        else:
            edited_list = []
            for idx, item in enumerate(json_obj):
                st.write("  " * level + f"Item {idx+1}:")
                unique_key = parent_key + "_" + str(idx)
                edited_item = display_json_content(item, level+1, unique_key)
                edited_list.append(edited_item)
            return edited_list
    else:
        return st.text_input("", json_obj, key=parent_key)



st.title("LLM Training Data Editor")

@st.cache_data
def get_cached_data(uploaded_file):
    return load_data(uploaded_file)

uploaded_file = st.file_uploader("Upload your .jsonl file", type=["jsonl"])

if uploaded_file:
    data = get_cached_data(uploaded_file)

    data_options = [f"Data Point {i+1}" for i in range(len(data))]
    selected_option = st.selectbox("Choose a data point to edit:", data_options)
    selected_index = data_options.index(selected_option)

    selected_data = data[selected_index]

    edited_messages = []
    for idx, message in enumerate(selected_data.get("messages", [])):
        st.subheader(f"Message {idx + 1}")

        role = st.text_input(f"Role {idx + 1}", message["role"])

        if is_json_str(message["content"]):
            # Recursively display JSON content for editing
            st.write("Content:")
            edited_content = display_json_content(json.loads(message["content"]))
            edited_messages.append({"role": role, "content": json.dumps(edited_content)})
        else:
            content = st.text_area(f"Content {idx + 1}", message["content"])
            edited_messages.append({"role": role, "content": content})

    if st.button("Apply Changes"):
        data[selected_index]["messages"] = edited_messages

    if st.button("Save Changes"):
        save_option = st.radio("Save Option", ["Overwrite Original File", "Save As New File"])

        if save_option == "Save As New File":
            new_file_name = st.text_input("Enter new file name (with .jsonl extension)")
            if new_file_name:
                save_data(new_file_name, data)
                st.success(f"Saved changes to {new_file_name}")
        else:
            import base64

            save_file_name = "modified_data.jsonl"
            save_data(save_file_name, data)
            st.write(f"Data saved to {save_file_name}. Download [here](/{save_file_name})")

