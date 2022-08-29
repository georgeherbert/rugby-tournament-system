# Rugby-Tournament-System

'Rugby Tournament System' is a Django web application I produced for my A-Level Computer Science NEA. I added some additional unit tests as part of the ILO Mentoring Scheme during my first year at the University of Bristol.

## Report

The coursework report is in the file [Rugby Tournament System.pdf](Rugby%20Tournament%20System.pdf).

## Getting Started

To begin with, clone the repository:
```
git clone https://github.com/georgeherbert/rugby-tournament-system.git
```

Install the dependencies:
```
pip3 install -r requirements.txt
```

Synchronise the database state with the current set of models and migrations:
```
python3 manage.py migrate
```

Start a development web server on your local machine:
```
python3 manage.py runserver
```

Then navigate to http://127.0.0.1:8000/.