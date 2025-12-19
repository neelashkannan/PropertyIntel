import streamlit as st
import json
import os
import pandas as pd
import re
import time
from datetime import datetime
import uuid

# --- LOAD DATA ---
postcode_df = pd.read_csv("postcode_to_datazone.csv")
postcode_df["Postcode"] = postcode_df["Postcode"].str.strip().str.upper().str.replace(" ", "")

# --- SESSION STATE INIT ---
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "property_list" not in st.session_state:
    st.session_state.property_list = []
if "editing_index" not in st.session_state:
    st.session_state.editing_index = None
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "form_key" not in st.session_state:
    st.session_state.form_key = str(uuid.uuid4())

# --- HEADER & LOGO ---
col1, col2 = st.columns([4, 1])
with col2:
    # Only show logo if file exists
    if os.path.exists("logo.png"):
        st.image("logo.png", width=100)
    else:
        st.write("🏠")  # House emoji as placeholder
with col1:
    st.markdown(
        """
        # Purva.ai  
        #### Empowering Smarter Property Decisions
        """
    )
    st.markdown(
        """
        <marquee behavior="scroll" direction="left" 
                 style="color:#2ecc71; font-size:16px; margin-top:-10px;">
          I am your smart property agent. Please enter the details below 
          for a holistic, intelligent property evaluation.
        </marquee>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# --- LOGIN/CREATE ACCOUNT ---
if not st.session_state.user_logged_in:
    st.subheader("Please insert your user ID")
    option = st.radio("Are you a new or returning user?", ["Login", "Create Account"], horizontal=True)
    user_id = st.text_input("User ID", key="login_user_id")
    login_btn = st.button(option)
    if login_btn and user_id.strip():
        user_id = user_id.strip()
        st.session_state.user_logged_in = True
        st.session_state.user_name = user_id
        user_dir = os.path.join("data", user_id.replace(" ", "_"), "json")
        prop_list = []
        if os.path.exists(user_dir):
            property_files = sorted(os.listdir(user_dir))
            for f in property_files:
                with open(os.path.join(user_dir, f), "r") as pf:
                    prop_list.append(json.load(pf))
        st.session_state.property_list = prop_list
        st.session_state.show_form = False
        st.session_state.editing_index = None
        st.session_state.form_key = str(uuid.uuid4())
        st.rerun()
    elif login_btn:
        st.warning("Please enter your User ID to continue.")
    st.stop()

# --- WELCOME + PROPERTY LISTING ---
st.success(f"Welcome, {st.session_state.user_name}!")

# --- SHOW PROPERTY LIST, EDIT & REMOVE BUTTONS ---
if st.session_state.property_list:
    st.markdown("---")
    st.subheader("📋 Your Listed Properties")
    for idx, prop in enumerate(st.session_state.property_list):
        col1, col2, col3 = st.columns([6, 1, 2])
        with col1:
            st.markdown(
                f"**Property #{idx + 1}: {prop.get('house_number','')} {prop.get('street_name','')} - {prop.get('postcode','')}**"
            )
        with col2:
            if st.button("Edit", key=f"edit_{idx}"):
                st.session_state.editing_index = idx
                st.session_state.show_form = True
                st.session_state.form_key = str(uuid.uuid4()) # For form reset
                st.rerun()
        with col3:
            if st.button("Remove", key=f"del_{idx}"):
                st.session_state.property_list.pop(idx)
                user_dir = os.path.join("data", st.session_state.user_name.replace(" ", "_"), "json")
                file_list = sorted(os.listdir(user_dir))
                if idx < len(file_list):
                    os.remove(os.path.join(user_dir, file_list[idx]))
                st.success("Property removed.")
                st.session_state.form_key = str(uuid.uuid4())
                st.rerun()
    st.markdown("")

# --- ADD PROPERTY & ANALYSE BUTTONS ---
colA, colB = st.columns([2, 2])
with colA:
    if st.button("Add New Property"):
        st.session_state.editing_index = None
        st.session_state.show_form = True
        st.session_state.form_key = str(uuid.uuid4())
        st.rerun()
with colB:
    if st.session_state.property_list:
        if st.button("Analyse Properties"):
            st.session_state.analyse_now = True
    else:
        st.session_state.analyse_now = False

# --- PROPERTY FORM ---
if st.session_state.show_form:
    # Prefill if editing
    initial = {}
    if st.session_state.editing_index is not None:
        prop = st.session_state.property_list[st.session_state.editing_index]
        initial = {
            "property_type_selected": prop.get("property_type", "Select"),
            "house_number": prop.get("house_number", ""),
            "street_name": prop.get("street_name", ""),
            "postcode": prop.get("postcode", ""),
            "bedrooms": str(prop.get("bedrooms", "Select")),
            "bathrooms": str(prop.get("bathrooms", "Select")),
            "size_sqft": prop.get("size_sqft", 0),
            "new_build": prop.get("new_build", "Select"),
            "solar": prop.get("solar_panels", "Select"),
            "parking": prop.get("parking", "Select"),
            "parking_type": prop.get("parking_type", "Select"),
            "garden": prop.get("garden", "Select"),
            "garden_type": prop.get("garden_type", "Select"),
            "floor_number": str(prop.get("floor_number", "Select")),
            "lift_available": prop.get("lift_available", "Select"),
            "sunroom": prop.get("sunroom", False),
            "basement": prop.get("basement", False),
            "loft": prop.get("loft", False),
            "parking_additional": prop.get("parking_additional", False),
            "notes": prop.get("misc_notes", ""),
            "epc_rating": prop.get("epc_rating", "Unknown"),
            "council_tax_band": prop.get("council_tax_band", "Unknown"),
        }
    else:
        initial = {}

    # ----------- FORM -----------
    with st.form(key="property_form_"+st.session_state.form_key, clear_on_submit=False):
        st.markdown("---")
        st.subheader("1. Address")
        house_number = st.text_input("House/Flat Number", value=initial.get("house_number",""))
        street_name = st.text_input("Street Name", value=initial.get("street_name",""))
        postcode = st.text_input("Postcode", value=initial.get("postcode",""))

        st.markdown("---")
        st.subheader("2. Property Details")
        property_type_selected = st.selectbox(
            "Property Type", ["Select", "house", "detached", "semi-detached", "flat", "bungalow"],
            index=["Select", "house", "detached", "semi-detached", "flat", "bungalow"].index(initial.get("property_type_selected", "Select"))
        )
        bedrooms = st.selectbox(
            "Number of Bedrooms", ["Select"] + list(range(1, 6)), 
            index=int(initial.get("bedrooms","0")) if initial.get("bedrooms","Select").isdigit() else 0
        )
        bathrooms = st.selectbox(
            "Number of Bathrooms", ["Select"] + list(range(1, 6)), 
            index=int(initial.get("bathrooms","0")) if initial.get("bathrooms","Select").isdigit() else 0
        )
        size_sqft = st.number_input("Property Size (sq ft)", min_value=0, value=int(initial.get("size_sqft",0)))
        new_build = st.selectbox(
            "New Build", ["Select", "Yes", "No"],
            index=["Select", "Yes", "No"].index(initial.get("new_build","Select"))
        )
        solar = st.selectbox(
            "Solar Panels", ["Select", "Yes", "No"],
            index=["Select", "Yes", "No"].index(initial.get("solar","Select"))
        )
        epc_rating = st.selectbox(
            "EPC Rating", ["Unknown", "A", "B", "C", "D", "E", "F", "G"],
            index=["Unknown", "A", "B", "C", "D", "E", "F", "G"].index(initial.get("epc_rating","Unknown"))
        )
        council_tax_band = st.selectbox(
            "Council Tax Band", ["Unknown", "A", "B", "C", "D", "E", "F", "G", "H"],
            index=["Unknown", "A", "B", "C", "D", "E", "F", "G", "H"].index(initial.get("council_tax_band","Unknown"))
        )

        st.markdown("---")
        st.subheader("3. Facilities & Extras")

        # ------- PATCHED SECTION: Parking & Garden -------
        # Parking
        parking = st.selectbox(
            "Parking", ["Select", "Yes", "No"],
            index=["Select", "Yes", "No"].index(initial.get("parking","Select")),
            key="parking_"+st.session_state.form_key
        )

        parking_type = (
            st.selectbox(
                "Parking Type", ["Select", "Garage", "Double Garage", "Driveway", "Roadside"],
                index=["Select", "Garage", "Double Garage", "Driveway", "Roadside"].index(initial.get("parking_type","Select")),
                key="parking_type_"+st.session_state.form_key
            )
            if parking == "Yes" else "Select"
        )

        # Garden
        garden = st.selectbox(
            "Garden", ["Select", "Yes", "No"],
            index=["Select", "Yes", "No"].index(initial.get("garden","Select")),
            key="garden_"+st.session_state.form_key
        )

        garden_type = (
            st.selectbox(
                "Garden Type", ["Select", "Front Garden", "Rear Garden", "Both"],
                index=["Select", "Front Garden", "Rear Garden", "Both"].index(initial.get("garden_type","Select")),
                key="garden_type_"+st.session_state.form_key
            )
            if garden == "Yes" else "Select"
        )
        # ------- END PATCHED SECTION -------

        if property_type_selected == "flat":
            floor_number = st.selectbox(
                "Floor Number", ["Select"] + list(range(0, 11)),
                index=int(initial.get("floor_number","0")) if initial.get("floor_number","Select").isdigit() else 0,
            )
            lift_available = st.selectbox(
                "Lift", ["Select", "Yes", "No"],
                index=["Select", "Yes", "No"].index(initial.get("lift_available","Select"))
            )
        else:
            floor_number = None
            lift_available = None

        sunroom = st.checkbox("Sunroom/Conservatory Present", value=initial.get("sunroom", False))
        basement = st.checkbox("Basement", value=initial.get("basement", False))
        loft = st.checkbox("Loft", value=initial.get("loft", False))
        parking_additional = st.checkbox("Additional Parking Features", value=initial.get("parking_additional", False))
        notes = st.text_area("Other Miscellaneous Notes (e.g., EV charger, smart thermostat)", value=initial.get("notes",""))
        media = st.file_uploader("Upload Images or Video", accept_multiple_files=True)

        submit_col, cancel_col = st.columns([2,1])
        with submit_col:
            save_property = st.form_submit_button("Save Property")
        with cancel_col:
            cancel_property = st.form_submit_button("Cancel")

    # --- SAVE/EDIT LOGIC ---
    if save_property:
        # Validation
        if not st.session_state.user_name:
            st.warning("Please enter a User ID.")
        elif property_type_selected == "Select":
            st.warning("Please choose a property type.")
        elif not house_number or not street_name or not postcode:
            st.warning("Please complete the address fields.")
        elif bedrooms == "Select" or bathrooms == "Select":
            st.warning("Please select bedrooms and bathrooms.")
        else:
            postcode_clean = re.sub(r"\s+", "", postcode.strip().upper())
            dz_match = postcode_df[postcode_df["Postcode"] == postcode_clean]
            dz_code = dz_match.iloc[0]["DataZone2011Code"] if not dz_match.empty else None

            prop = {
                "timestamp": datetime.now().isoformat(),
                "user_name": st.session_state.user_name,
                "house_number": house_number,
                "street_name": street_name,
                "postcode": postcode,
                "property_type": property_type_selected,
                "floor_number": floor_number if property_type_selected == "flat" else None,
                "lift_available": lift_available if property_type_selected == "flat" else None,
                "bedrooms": int(bedrooms) if bedrooms != "Select" else None,
                "bathrooms": int(bathrooms) if bathrooms != "Select" else None,
                "size_sqft": size_sqft,
                "new_build": new_build if new_build in ["Yes", "No"] else None,
                "solar_panels": solar if solar in ["Yes", "No"] else None,
                "epc_rating": epc_rating,
                "council_tax_band": council_tax_band,
                "parking": parking if parking in ["Yes", "No"] else None,
                "parking_type": parking_type if parking == "Yes" and parking_type != "Select" else None,
                "garden": garden if garden in ["Yes", "No"] else None,
                "garden_type": garden_type if garden == "Yes" and garden_type != "Select" else None,
                "sunroom": sunroom,
                "basement": basement,
                "loft": loft,
                "parking_additional": parking_additional,
                "misc_notes": notes,
                "datazone": dz_code,
                "media_files": [f.name for f in media] if media else [],
            }

            user_dir = os.path.join("data", st.session_state.user_name.replace(" ", "_"))
            media_dir = os.path.join(user_dir, "media")
            os.makedirs(media_dir, exist_ok=True)
            if media:
                for file in media:
                    with open(os.path.join(media_dir, file.name), "wb") as out:
                        out.write(file.read())

            json_dir = os.path.join(user_dir, "json")
            os.makedirs(json_dir, exist_ok=True)
            filename = f"property_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(os.path.join(json_dir, filename), "w") as f:
                json.dump(prop, f, indent=4)

            if st.session_state.editing_index is not None:
                st.session_state.property_list[st.session_state.editing_index] = prop
                st.success("✅ Property updated successfully.")
                st.session_state.editing_index = None
            else:
                st.session_state.property_list.append(prop)
                st.success("✅ Property added successfully.")

            st.session_state.show_form = False
            st.session_state.form_key = str(uuid.uuid4())
            st.rerun()
    elif cancel_property:
        st.session_state.show_form = False
        st.session_state.editing_index = None
        st.session_state.form_key = str(uuid.uuid4())
        st.rerun()

# --- ANALYSE ALL ---
if "analyse_now" in st.session_state and st.session_state.analyse_now and st.session_state.property_list:
    st.info("🔍 Analysing all your properties. Please give us a moment...")
    progress = st.progress(0)
    for i in range(1, 101):
        time.sleep(0.01)
        progress.progress(i)
    user_dir = os.path.join("data", st.session_state.user_name.replace(" ", "_"), "batch")
    os.makedirs(user_dir, exist_ok=True)
    batch_file = f"all_properties_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(os.path.join(user_dir, batch_file), "w") as f:
        json.dump(st.session_state.property_list, f, indent=4)
    st.success("✅ Analysis complete. Your results will appear here soon.")
    st.session_state.analyse_now = False
