# Budgeting-App
# TEAM BRAVO - MAJOR GROUP PROJECT 

## Team Members 
- Mehtap Mira Akinci
- Miriam Czech
- Mohamed Abdulrahman
- Darren Sandhu
- Istiyak Choudhury
- Heman Seegolam 
- Jana Alkhodir

## Description
Personal Spending Tracker is a user friendly website that encourages even those who don't like budgeting! 

## Deployed version of the application
The deployed version of the application can be found at **.

## Installation Instructions 
```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Create Media Directories:

```
$ mkdir media
```

```
$ cd media
```

```
$ mkdir media
```

```
$ cd ..
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run server with:
```
$ python3 manage.py runserver
```

Run all tests with:
```
$ python3 manage.py test
```

## Usage
Upon start up, the user must sign up with the required credentials to access the landing page for logged users. 
Initially, the user should add a category in “Manage your spending categories” so that they will then be able to add a spending which can be later viewed in “spending history”. Furthermore, the user can utilise the “points awards and achievements” which rewards the user for commendatory spending habits. The user can also edit their profile and log out of the app.

## Credentials
username : janedoe
password : Password123

## How to gain points 
* Do not exceed the category limit!
* Timely completion of the cycle’s accounts session 
* Spending as little as possible within a category
    * point_award = (limit/ spent_funds)*10 (maximum points earned is 100)
* Well distributed spending throughout the cycle
    * threshold = (limit/ number of days in the cycle) * 1.1
    * point_award = ((number of days when spending < threshold)/ number of days in the cycle that have already happened)*normalization_factor
* Cutting spending within a category by X% relative to the previous cycle
    * point_award = award max points if the X% reduction or more achieved, award some points if spending < spending in the previous cycle (let’s say 10 minimum, 100 max * normalisation factor) 
