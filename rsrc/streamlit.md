08:58:45 [@x13 app]$ python -m venv venv
08:58:56 [@x13 app]$ source ./venv/bin/activate

#https://github.com/streamlit/streamlit/wiki/Installing-in-a-virtual-environment
(venv) 14:18:59 [@x13 app]$ pip freeze -l > requirements.txt

##https://stackoverflow.com/questions/32407365/can-i-move-a-virtualenv
## recreate venv with requirements
python -m venv prj_venv
08:58:56 [@x13 app]$ source ./prj_venv/bin/activate
python -m pip install -r requirements.txt

#https://forum.cursor.com/t/cursor-cannot-detect-different-venvs-based-on-directory/17898
This worked for me and maybe it will work for you: Open Command Palette: Press Ctrl+Shift+P (or Cmd+Shift+P on macOS). 
Select Python Interpreter: Search for Python: Select Interpreter. 
A list of Python interpreters will appear. Select the one corresponding to your venv folder

14:46:54 [@x13 project]$ docker build . -t streamlit_app
14:46:54 [@x13 project]$ docker run  --network lxdbr_dock0 -p 8501:8501 streamlit_app


