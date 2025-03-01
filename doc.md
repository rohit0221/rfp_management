conda create -n crewai-env python=3.12
conda activate crewai-env

pip install crewai crewai-tools

crewai create crew rfp_management_crew

uv add <tool-name>
cd rfp_management_crew

crewai install

crewai run


crewai run > output.txt 2>&1 & type output.txt

cmd /c "set CREWAI_DEBUG=1 && crewai run > output.txt 2>&1 && type output.txt"

tasklist | findstr python
taskkill /F /IM python.exe

uv pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.0/en_core_web_sm-3.6.0.tar.gz

