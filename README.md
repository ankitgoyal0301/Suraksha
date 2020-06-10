# Suraksha
Suraksha is a web based application designed, keeping women empowerment and safety in mind. 

Some salient features are:
1. News articles highlighting issues pertaining to gender based crimes, 
2. An emergency button for connecting trusted people, 
3. Various maps features for aleviated location based awareness 
4. Information pertaining to the rights and law provided under the the Indain Penal Code and Indian Constitution.

Run instructions:
1. Clone the repository;
2. Install all the requirements from requirements.txt by running a command in terminal/cmd: 


For linux/macOS users: <br>
1. Check for virtual env: <br>
<code>python3 -m pip install virtualenv </code>
2. Create virtual env with name suraksha: <br>
<code>python3 -m venv suraksha</code>
3. Activate virtual env: <br>
<code>source suraksha/bin/activate</code>
4. Install required dependencies: <br>
<code>pip install -r requirements.txt</code>
5. Change directory to website:
<code>cd website</code>
6. Run Project Server:
<code>python manage.py runserver</code> or <code>python3 manage.py runserver</code> [depending on python version installed]

For windows users:<br>
1. Check for virtual env: <br>
<code>py -m pip install --user virtualenv</code>
2. Create virtual env with name suraksha: <br>
<code>py -m venv suraksha</code>
3. Activate virtual env: <br>
<code>.\suraksha\Scripts\activate</code>
4. Install required dependencies:  <br>
<code>pip install -r requirements.txt</code>
5. Change directory to website:
<code>cd website</code>
6. Run Project Server:
<code>python manage.py runserver</code>
