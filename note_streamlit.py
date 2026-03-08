import streamlit as st
import requests
import time

# App_url = "http://127.0.0.1:8000"
API_URL = "https://notes-api-backend-mxqk.onrender.com"


try:
    response = requests.get(f"{API_URL}/notes/")
    data = response.json()
    st.write(data)
except Exception as e:
    st.error(f"❌ Connection error: {e}")


# Initialize session state
if "note_title" not in st.session_state:
    st.session_state["note_title"] = ""
if "note_content" not in st.session_state:
    st.session_state["note_content"] = ""
if "current_note_id" not in st.session_state:
    st.session_state["current_note_id"] = ""
if "add_note_title" not in st.session_state:
    st.session_state["add_note_title"] = ""
if "add_note_content" not in st.session_state:
    st.session_state["add_note_content"] = ""
if "all_notes" not in st.session_state:
    st.session_state["all_notes"] = []
if "last_update_time" not in st.session_state:
    st.session_state["last_update_time"] = 0

st.title("📝 Notes Management APP")

menu = st.sidebar.selectbox("Select Operation",
                            ["➕ Add Note", "📋 Get All Notes", "🔍 Get Note by Id", "✏️ Update Note", "🗑️ Delete Note"])

# ==================== ADD NOTE ====================
if menu == "➕ Add Note":
    st.header("➕ Add New Note")

    # Fetch all notes to check for duplicates
    try:
        response = requests.get(f"{API_URL}/all_notes/",
                                headers={'Cache-Control': 'no-cache'})
        if response.status_code == 200:
            existing_notes = response.json()["details"]
        else:
            existing_notes = []
    except:
        existing_notes = []

    # Use session state for input fields
    title = st.text_input("Title", key="add_title", value=st.session_state.add_note_title)
    content = st.text_area("Content", key="add_content", value=st.session_state.add_note_content, height=150)

    col1, col2 = st.columns(2)
    with col1:
        add_btn = st.button("📝 Add Note", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("🔄 Clear Form", use_container_width=True)

    if clear_btn:
        st.session_state.add_note_title = ""
        st.session_state.add_note_content = ""
        st.rerun()

    if add_btn:
        if title.strip() == "":
            st.warning("⚠️ Please enter a note title")
        elif content.strip() == "":
            st.warning("⚠️ Please enter note content")
        else:
            # Check for duplicate
            is_duplicate = False
            for note in existing_notes:
                if note["title"].lower() == title.strip().lower() and note[
                    "content"].lower() == content.strip().lower():
                    is_duplicate = True
                    break

            if is_duplicate:
                st.error("❌ This note already exists! Please add a different note.")
            else:
                payload = {
                    "title": title.strip(),
                    "content": content.strip(),
                }
                try:
                    response = requests.post(f"{API_URL}/notes/", json=payload)
                    if response.status_code == 200:
                        st.success("✅ Note added successfully!")
                        st.balloons()
                        # Clear the form
                        st.session_state.add_note_title = ""
                        st.session_state.add_note_content = ""
                        # Clear cached notes
                        st.session_state["all_notes"] = []
                        st.session_state["last_update_time"] = time.time()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to add note: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {e}")

# ==================== GET ALL NOTES ====================
elif menu == "📋 Get All Notes":
    st.header("📋 All Notes")

    col1, col2 = st.columns([1, 5])
    with col1:
        refresh = st.button("🔄 Refresh", type="primary", use_container_width=True)
    with col2:
        st.write("")

    # Force refresh if button clicked or if it's time to refresh
    current_time = time.time()
    if refresh or not st.session_state["all_notes"] or (current_time - st.session_state["last_update_time"] > 5):
        try:
            response = requests.get(f"{API_URL}/all_notes/",
                                    headers={'Cache-Control': 'no-cache'})

            if response.status_code == 200:
                notes = response.json()["details"]
                st.session_state["all_notes"] = notes
                st.session_state["last_update_time"] = current_time
            else:
                st.error(f"❌ Failed to fetch notes: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Connection error: {e}")

    # Display notes
    if st.session_state["all_notes"]:
        st.success(f"Found {len(st.session_state['all_notes'])} note(s)")
        for note in st.session_state["all_notes"]:
            with st.expander(f"📌 {note['title']} (ID: {note['id']})"):
                st.write(f"**Content:** {note['content']}")
                st.caption(f"Note ID: {note['id']}")
    else:
        st.info("📭 No notes available")

# ==================== GET NOTE BY ID ====================
elif menu == "🔍 Get Note by Id":
    st.header("🔍 Fetch Note by ID")

    note_id = st.text_input("Enter Note ID", key="get_note_id")

    col1, col2 = st.columns(2)
    with col1:
        get_btn = st.button("🔍 Get Note", type="primary", use_container_width=True)
    with col2:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state['last_fetched_note'] = None
            st.rerun()

    if get_btn and note_id:
        try:
            # Simple GET request without complex headers for in-memory storage
            response = requests.get(f"{API_URL}/notes/{int(note_id)}")

            if response.status_code == 200:
                note = response.json()["detail"]
                st.success("✅ Note found!")

                # Display note in a nice format
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Note ID", note['id'])
                with col2:
                    st.metric("Title", note['title'])

                st.text_area("Content", note['content'], height=150, disabled=True)

                # Store in session state
                st.session_state['last_fetched_note'] = note
            else:
                st.error(f"❌ Note with ID {note_id} not found")
        except ValueError:
            st.error("❌ Please enter a valid numeric ID")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Connection error: {e}")

# ==================== UPDATE NOTE ====================
elif menu == "✏️ Update Note":
    st.header("✏️ Update Note")

    # Input for Note ID
    note_id = st.text_input("Enter Note ID to Update",
                            value=st.session_state["current_note_id"],
                            key="update_note_id")

    col1, col2 = st.columns(2)

    with col1:
        fetch_btn = st.button("🔍 Fetch Note", type="primary", use_container_width=True)

    with col2:
        if st.button("🗑️ Clear Form", use_container_width=True):
            st.session_state["note_title"] = ""
            st.session_state["note_content"] = ""
            st.session_state["current_note_id"] = ""
            st.rerun()

    # Fetch note when button is clicked
    if fetch_btn and note_id:
        try:
            response = requests.get(f"{API_URL}/notes/{int(note_id)}")

            if response.status_code == 200:
                note = response.json()["detail"]
                st.session_state["note_title"] = note["title"]
                st.session_state["note_content"] = note["content"]
                st.session_state["current_note_id"] = note_id
                st.success("✅ Note fetched successfully!")

                # Display current values
                st.info(f"**Current Values:**\n- Title: {note['title']}\n- Content: {note['content']}")
            else:
                st.error(f"❌ Note with ID {note_id} not found")
                st.session_state["note_title"] = ""
                st.session_state["note_content"] = ""
        except ValueError:
            st.error("❌ Please enter a valid numeric ID")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Connection error: {e}")

    # Create a separator
    st.markdown("---")

    # Update form - only show if we have a note ID
    if st.session_state["current_note_id"]:
        st.subheader("Update Note Details")

        # Display current note ID being updated
        st.caption(f"Updating Note ID: {st.session_state['current_note_id']}")

        # Input fields for update
        new_title = st.text_input("New Title",
                                  value=st.session_state["note_title"],
                                  key="update_title")
        new_content = st.text_area("New Content",
                                   value=st.session_state["note_content"],
                                   height=150,
                                   key="update_content")

        update_btn = st.button("📝 Update Note", type="primary", use_container_width=True)

        if update_btn:
            # Prepare update payload - MATCHING YOUR BACKEND EXPECTATIONS
            payload = {}

            # Check if title has changed
            if new_title.strip() and new_title.strip() != st.session_state["note_title"]:
                payload["new_title"] = new_title.strip()  # Using 'new_title' as backend expects

            # Check if content has changed
            if new_content.strip() and new_content.strip() != st.session_state["note_content"]:
                payload["new_content"] = new_content.strip()  # Using 'new_content' as backend expects

            if payload:
                try:
                    # Debug: Show what's being sent
                    st.write("📤 Sending payload:", payload)

                    # Send update request
                    response = requests.put(
                        f"{API_URL}/update_notes/{int(st.session_state['current_note_id'])}",
                        json=payload
                    )

                    if response.status_code == 200:
                        st.success("✅ Note updated successfully!")
                        st.balloons()

                        # Update session state with new values immediately
                        if "new_title" in payload:
                            st.session_state["note_title"] = payload["new_title"]
                        if "new_content" in payload:
                            st.session_state["note_content"] = payload["new_content"]

                        # Clear cached data
                        st.session_state["all_notes"] = []

                        # Show success message with updated values
                        st.info(f"**Updated Title:** {st.session_state['note_title']}")
                        st.info(f"**Updated Content:** {st.session_state['note_content']}")

                        # Small delay then rerun
                        time.sleep(2)
                        st.rerun()

                    elif response.status_code == 404:
                        st.error("❌ Note not found")
                    else:
                        st.error(f"❌ Failed to update note: {response.text}")

                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {e}")
            else:
                st.warning("⚠️ No changes detected. Please modify title or content to update.")
    else:
        st.info("👆 Please enter a Note ID and click 'Fetch Note' to update it")
# ==================== DELETE NOTE ====================
elif menu == "🗑️ Delete Note":
    st.header("🗑️ Delete Note")

    note_id = st.text_input("Enter Note ID to Delete", key="delete_note_id")

    if note_id:
        try:
            # First check if note exists
            check_response = requests.get(
                f"{API_URL}/notes/{int(note_id)}",
                headers={'Cache-Control': 'no-cache'}
            )

            if check_response.status_code == 200:
                note = check_response.json()["detail"]
                st.warning(f"You are about to delete: **{note['title']}**")

                # Show note details
                with st.expander("View Note Details"):
                    st.write(f"**Title:** {note['title']}")
                    st.write(f"**Content:** {note['content']}")

                # Confirmation checkbox
                confirm = st.checkbox("✅ I understand this action cannot be undone")

                if confirm:
                    delete_btn = st.button("🗑️ Delete Note", type="primary", use_container_width=True)
                    if delete_btn:
                        response = requests.delete(f"{API_URL}/delete_notes/{int(note_id)}")
                        if response.status_code == 200:
                            st.success("✅ Note deleted successfully!")
                            st.balloons()
                            # Clear cached data
                            st.session_state["all_notes"] = []
                            st.session_state["last_update_time"] = 0
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to delete: {response.text}")
            else:
                st.error(f"❌ Note with ID {note_id} not found")
        except ValueError:
            st.error("❌ Please enter a valid numeric ID")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Connection error: {e}")
    else:
        st.info("👆 Enter a Note ID to delete")