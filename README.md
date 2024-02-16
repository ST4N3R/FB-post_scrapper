# undefined

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)

## About <a name = "about"></a>

I wanted to track the results of my scout team's fan page, but unfortunately, FB didn't have the tools that satisfied me. So, I created this application! Thanks to it, I can add entries about posts to the database hosted on the Google Cloud Platform and download data from it to create charts. You can access it at this page: [forteca-reactions](https://forteca-reactions.lm.r.appspot.com/)

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To run the program, you need the following libraries:
- Python
- Pandas
- Numpy
- Mechanize
- Beautifulsoup
- google.cloud.datastore
- python.dotenv

You also need to have a google cloud platform project created. I were using "app engine" and "firestore". 

### Installing

1) Download all required libraries
2) Create gcp project
3) Create datastore databse. You have to have three columns: "fb_post_url": str, "reaction_num": int, "release_date": list
4) Donwload access file from gcp and name it "serviceKey.json"
5) Create .env file with fb credentials. You need to name them: FAKE_FB_EMAIL and FAKE_FB_PASSWORD
6) Everything should be running now