import streamlit as st
from crew import Optimizer
from pathlib import Path
from datetime import datetime


def save_uploaded_file(uploaded_file) -> str:
    """Save uploaded file and return the file path"""
    try:
        # Create uploads directory if it doesn't exist
        save_dir = Path("uploads")
        save_dir.mkdir(exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = save_dir / f"resume_{timestamp}_{uploaded_file.name}"

        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return str(file_path)
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        raise


st.markdown(
    """
    Resume Optimizer
    """
)

# User Inputs
upload_resume = st.file_uploader(
    "Choose a PDF resume file",
    type=["pdf"],
    help="Upload a PDF resume to analyze"
)

# Initialize agents,tasks and crew
optimizer = Optimizer()
crew = optimizer.crew()

# Button to run crew
if st.button("Optimize Resume"):
    if not upload_resume:
        st.error("Please upload resume!!")
    else:
        st.write("Optimizing your resume")

        # Initialize Inputs
        inputs = {
            'upload_cv': str(upload_resume),
            'path_to_jobs_csv': './src/optimizer/data/jobs.csv'
        }

        # run
        result = crew.kickoff(inputs=inputs)

        # Display results
        st.subheader("Your Optimized Resume")
        st.markdown(result)

        # Download button
        optimized_resume = str(result)

        st.download_button(
            label="Download Optimized Resume",
            data=optimized_resume,
            file_name="Optimized_Resume.pdf",
            mime="text/plain"
        )