import sys
sys.stdout.reconfigure(encoding='utf-8')

import streamlit as st
import subprocess
import time


def run_crewai():
    """
    Runs the crew command in the main thread and updates a placeholder
    with the subprocess’s output as it arrives.
    """
    # Launch the crew process (ensure 'crewai' is in your PATH)
    process = subprocess.Popen(
        ["crewai", "run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    logs = []  # List to accumulate output lines
    log_placeholder = st.empty()  # Placeholder to update the UI

    # Read the process output line by line
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            logs.append(line)
            # Update the UI placeholder with the current log
            log_placeholder.text("".join(logs))
        time.sleep(0.1)  # Small delay to yield control

    return "".join(logs)

def main():
    st.title("CrewAI Runner")
    st.write("Click the button below to trigger `crewai run` and see live console output.")

    if st.button("Run CrewAI"):
        with st.spinner("Running crew..."):
            output = run_crewai()  # This call blocks until the process finishes
        st.success("Crew execution completed!")
        st.text_area("Final Output", output, height=300)
    else:
        st.write("Press the button to run the crew.")

if __name__ == "__main__":
    main()
