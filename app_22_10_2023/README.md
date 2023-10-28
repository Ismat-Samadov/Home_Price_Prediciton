```markdown
# Home Price Prediction

## Overview

This is a web application for home price prediction. Given user input, it returns the predicted price using an API.

## Installation

To set up the project, you can follow these installation steps:

```bash
git clone https://github.com/Ismat-Samadov/home-price-prediction.git
cd home-price-prediction
pip install -r requirements.txt
```

## Usage

To run the project, use the following command:

```bash
streamlit run app.py
```

## Acknowledgments

## Deployment to Heroku Instructions (Heroku Git)

1. Sign up for a free Heroku account if you haven't already done so.
2. Create an app, e.g., 'myapp' (the name of the app).
3. Open your terminal and type `heroku login`. This will take you to a web-based login page.
4. Navigate to your project directory on your local drive.
5. Type `git init` to initialize a Git repository.
6. Type `heroku git:remote -a home-price-prediction`.
7. Add your project files with `git add .`.
8. Commit your changes with `git commit -am "Version 1"`.
9. Deploy your app to Heroku with `git push heroku master`.
10. Allocate a dyno to run your app with `heroku ps:scale web=1`.
11. To check the logs and make sure it's working, use `heroku logs --tail`.
12. You can stop the dyno by scaling it down with `heroku ps:scale worker=0`.

Note: These instructions are specific to deploying your project on Heroku using Heroku Git. Make sure you have the Heroku CLI installed and configured for a successful deployment.
```

