conda create -n crewai-env python=3.12
conda activate crewai-env

pip install crewai crewai-tools

crewai create crew rfp_management_crew

uv add <tool-name>
cd rfp_management_crew

crewai install

crewai run


crewai run > output.txt 2>&1 & type output.txt
