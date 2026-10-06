import streamlit as st
from converter import convert_llg_to_fa_details
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from io import BytesIO


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="LLG to FA Converter",
    page_icon="🔄",
    layout="wide"
)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🔄 LLG → FA")
st.sidebar.write("Finite Automaton Conversion System")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🔄 Converter",
        "🧪 Test Cases",
        "📚 Algorithm",
        "ℹ️ Project Info"
    ]
)


# ==========================================================
# HOME PAGE
# ==========================================================

if page == "🏠 Home":

    st.title("🔄 Left Linear Grammar → Finite Automaton")

    st.subheader(
        "Grammar Conversion and Visualization System"
    )

    st.write(
        """
        This application converts a **Left Linear Grammar (LLG)**
        into a **Finite Automaton (FA)** and visually represents
        the generated automaton.
        """
    )

    st.divider()

    st.header("🎯 Project Objective")

    st.write(
        """
        The objective of this project is to develop an application
        that efficiently converts a Left Linear Grammar into a
        Finite Automaton and demonstrates the result using
        different valid and invalid inputs.
        """
    )

    st.header("✨ Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔄 Conversion")
        st.write(
            "Convert Left Linear Grammar productions "
            "into Finite Automaton transitions."
        )

    with col2:
        st.markdown("### 📊 Visualization")
        st.write(
            "Display states, alphabet, transition table "
            "and FA diagram."
        )

    with col3:
        st.markdown("### 📥 Excel Report")
        st.write(
            "Download the generated FA information "
            "as an Excel file."
        )

    st.divider()

    st.header("🚀 How to Use")

    st.write(
        """
        **Step 1:** Go to the Converter page.

        **Step 2:** Enter a Left Linear Grammar.

        **Step 3:** Click **Convert to FA**.

        **Step 4:** View the states, transitions and FA diagram.

        **Step 5:** Download the result as an Excel report.

        **Step 6:** Use the Test Cases page to demonstrate
        valid and invalid inputs.
        """
    )


# ==========================================================
# CONVERTER PAGE
# ==========================================================

elif page == "🔄 Converter":

    st.title("🔄 LLG → Finite Automaton Converter")

    st.write(
        "Enter a Left Linear Grammar and convert it into "
        "a Finite Automaton."
    )

    st.subheader("✍️ Enter Left Linear Grammar")

    grammar = st.text_area(
        "Grammar",
        height=180,
        placeholder="""S -> Aa
A -> b"""
    )

    if st.button("🔄 Convert to FA", type="primary"):

        if not grammar.strip():

            st.warning("⚠️ Please enter a grammar.")

        else:

            try:

                fa = convert_llg_to_fa_details(grammar)

                st.success(
                    "✅ Grammar successfully converted!"
                )

                # ------------------------------------------
                # FA INFORMATION
                # ------------------------------------------

                st.subheader("📋 Generated Finite Automaton")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.write("**States**")
                    st.info(", ".join(fa["states"]))

                with col2:
                    st.write("**Alphabet**")
                    st.info(", ".join(fa["alphabet"]))

                with col3:
                    st.write("**Start State**")
                    st.info(fa["start_state"])

                with col4:
                    st.write("**Final State**")
                    st.info(
                        ", ".join(fa["final_states"])
                    )

                # ------------------------------------------
                # TRANSITION TABLE
                # ------------------------------------------

                st.subheader("📊 Transition Table")

                table_data = []

                for source, symbol, destination in fa["transitions"]:

                    table_data.append({
                        "From State": source,
                        "Input": symbol,
                        "To State": destination
                    })

                st.dataframe(
                    table_data,
                    hide_index=True,
                    use_container_width=True
                )

                # ------------------------------------------
                # FA DIAGRAM
                # ------------------------------------------

                st.subheader(
                    "🔵 Finite Automaton Diagram"
                )

                dot = """
                digraph FA {

                    rankdir=LR;

                    node [
                        shape=circle
                    ];

                    start [
                        shape=point
                    ];
                """

                # Start arrow
                dot += f'''
                    start -> "{fa["start_state"]}";
                '''

                # Final states
                for final_state in fa["final_states"]:

                    dot += f'''
                        "{final_state}" [
                            shape=doublecircle
                        ];
                    '''

                # Transitions
                for source, symbol, destination in fa["transitions"]:

                    dot += f'''
                        "{source}" -> "{destination}"
                        [label="{symbol}"];
                    '''

                dot += """
                }
                """

                st.graphviz_chart(dot)

                # ------------------------------------------
                # FA DESCRIPTION
                # ------------------------------------------

                st.subheader("📄 FA Description")

                st.code(fa["text"])

                # ------------------------------------------
                # EXCEL REPORT
                # ------------------------------------------

                st.subheader("📊 Excel Report")

                workbook = Workbook()

                sheet = workbook.active
                sheet.title = "Conversion Result"

                # Header
                headers = [
                    "Input Grammar",
                    "States",
                    "Alphabet",
                    "Start State",
                    "Final State",
                    "From State",
                    "Input Symbol",
                    "To State"
                ]

                sheet.append(headers)

                # Data
                for source, symbol, destination in fa["transitions"]:

                    sheet.append([
                        grammar,
                        ", ".join(fa["states"]),
                        ", ".join(fa["alphabet"]),
                        fa["start_state"],
                        ", ".join(fa["final_states"]),
                        source,
                        symbol,
                        destination
                    ])

                # Header formatting
                for cell in sheet[1]:

                    cell.font = Font(bold=True)

                    cell.alignment = Alignment(
                        horizontal="center"
                    )

                # Column widths
                widths = {
                    "A": 30,
                    "B": 20,
                    "C": 15,
                    "D": 15,
                    "E": 15,
                    "F": 15,
                    "G": 15,
                    "H": 15
                }

                for column, width in widths.items():

                    sheet.column_dimensions[
                        column
                    ].width = width

                # Save Excel in memory
                excel_file = BytesIO()

                workbook.save(excel_file)

                excel_file.seek(0)

                st.download_button(
                    label="📥 Download FA Result as Excel",
                    data=excel_file,
                    file_name="LLG_to_FA_Result.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    )
                )

            except Exception as e:

                st.error(
                    f"❌ Error: {e}"
                )


# ==========================================================
# TEST CASES PAGE
# ==========================================================

elif page == "🧪 Test Cases":

    st.title("🧪 Valid and Invalid Test Cases")

    st.write(
        """
        This section demonstrates different valid and invalid
        Left Linear Grammar inputs.
        """
    )

    # ======================================================
    # VALID CASES
    # ======================================================

    st.header("✅ Valid Test Cases")

    valid_cases = [
        {
            "name": "Valid Case 1",
            "grammar": "S -> a"
        },
        {
            "name": "Valid Case 2",
            "grammar": """S -> Aa
A -> b"""
        },
        {
            "name": "Valid Case 3",
            "grammar": """S -> Aa
A -> Bb
B -> c"""
        }
    ]

    for case in valid_cases:

        with st.expander(
            f"✅ {case['name']}"
        ):

            st.code(
                case["grammar"],
                language="text"
            )

            try:

                fa = convert_llg_to_fa_details(
                    case["grammar"]
                )

                st.success("VALID INPUT")

                st.write(
                    "**States:**",
                    ", ".join(fa["states"])
                )

                st.write(
                    "**Alphabet:**",
                    ", ".join(fa["alphabet"])
                )

                st.write(
                    "**Start State:**",
                    fa["start_state"]
                )

                st.write(
                    "**Final State:**",
                    ", ".join(fa["final_states"])
                )

                st.write("**Transitions:**")

                for source, symbol, destination in fa[
                    "transitions"
                ]:

                    st.write(
                        f"δ({source}, {symbol}) = {destination}"
                    )

            except Exception as e:

                st.error(
                    f"Unexpected error: {e}"
                )

    # ======================================================
    # INVALID CASES
    # ======================================================

    st.header("❌ Invalid Test Cases")

    invalid_cases = [
        {
            "name": "Invalid Case 1",
            "grammar": "S a"
        },
        {
            "name": "Invalid Case 2",
            "grammar": "S ->"
        },
        {
            "name": "Invalid Case 3",
            "grammar": "S -> ABC"
        },
        {
            "name": "Invalid Case 4",
            "grammar": ""
        }
    ]

    for case in invalid_cases:

        with st.expander(
            f"❌ {case['name']}"
        ):

            if not case["grammar"]:

                st.code(
                    "(Empty Input)",
                    language="text"
                )

                st.error(
                    "INVALID INPUT: Grammar is empty."
                )

                continue

            st.code(
                case["grammar"],
                language="text"
            )

            try:

                convert_llg_to_fa_details(
                    case["grammar"]
                )

                st.warning(
                    "This input was accepted by the converter."
                )

            except Exception as e:

                st.error(
                    f"INVALID INPUT: {e}"
                )


# ==========================================================
# ALGORITHM PAGE
# ==========================================================

elif page == "📚 Algorithm":

    st.title("📚 LLG → FA Conversion Algorithm")

    st.write(
        """
        The following steps are used to convert a
        Left Linear Grammar into a Finite Automaton.
        """
    )

    st.header("Step 1 — Read the Grammar")

    st.write(
        """
        Read all productions of the Left Linear Grammar.
        """
    )

    st.header("Step 2 — Identify States")

    st.write(
        """
        Identify the non-terminal symbols of the grammar.
        These symbols are represented as states of the
        Finite Automaton.
        """
    )

    st.header("Step 3 — Add Final State")

    st.write(
        """
        Add a new final state called **qf**.
        """
    )

    st.header("Step 4 — Convert Productions")

    st.write(
        """
        For a production of the form:

        **A → Ba**

        create the transition:

        **δ(B, a) = A**

        For a production of the form:

        **A → a**

        create:

        **δ(A, a) = qf**
        """
    )

    st.header("Step 5 — Identify Start State")

    st.write(
        """
        The left-hand side of the first production is
        considered the start state.
        """
    )

    st.header("Step 6 — Display the FA")

    st.write(
        """
        Finally, display the states, alphabet, transition
        table and graphical representation of the Finite
        Automaton.
        """
    )

    st.success(
        "✅ The algorithm provides an automated way to "
        "demonstrate LLG to FA conversion."
    )


# ==========================================================
# PROJECT INFORMATION PAGE
# ==========================================================

elif page == "ℹ️ Project Info":

    st.title("ℹ️ Project Information")

    st.header("📌 Problem Statement")

    st.write(
        """
        Develop a model/application demonstrating the conversion
        of Left Linear Grammar into a Finite Automaton efficiently,
        while showcasing results for different valid and invalid
        inputs.
        """
    )

    st.header("🎯 Objective")

    st.write(
        """
        To design and implement an interactive application that
        converts Left Linear Grammar into Finite Automata and
        provides clear visualization and testing of the generated
        automaton.
        """
    )

    st.header("👩‍💻 Student Information")

    st.info(
        """
        **Student Name:** Yutika Manekar

        **Project:** Left Linear Grammar → Finite Automaton

        **Subject:** Theory of Computation

        **Application:** Streamlit Web Application
        """
    )

    st.header("🛠️ Technologies Used")

    technologies = [
        "Python",
        "Streamlit",
        "Graphviz",
        "OpenPyXL",
        "Finite Automata Theory"
    ]

    for technology in technologies:
        st.write(f"• {technology}")

    st.header("📦 Project Components")

    components = [
        "Grammar Input",
        "Grammar Validation",
        "LLG to FA Conversion",
        "Transition Table",
        "FA Diagram",
        "Valid Test Cases",
        "Invalid Test Cases",
        "Excel Report"
    ]

    for component in components:
        st.write(f"✅ {component}")

    st.divider()

    st.success(
        "🎓 This application demonstrates the complete "
        "LLG → FA conversion workflow."
    )