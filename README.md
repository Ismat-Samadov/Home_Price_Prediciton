# Real Estate Web Scraping and Home Price Prediction
[Detailed Article](https://medium.com/python-in-plain-english/home-price-prediction-e2e-web-app-581a8643b1d0)


This repository is dedicated to a project that involves web scraping real estate listings from popular websites and using machine learning to predict home prices. It's designed to help you gather data from real estate websites and then build a predictive model for estimating home prices based on various features.

## Project Structure

The repository is organized as follows:

- **data_preparation_and_modelling**: This directory contains scripts and files related to data preparation and modeling for the scraped data.
  
- **data_source/data_extraction**: Scripts for web scraping data from specific real estate websites like "bina.az" and "emlak.az" are stored here.

- **data_extraction**: Additional scripts and configurations for web scraping.

- **spiders**: Scrapy spider scripts for extracting data from websites.

- **bina_az_19092023.csv**, **bina_az_21092023.csv**, and **emlak_az_21092023.csv**: CSV files containing data extracted from the websites on specific dates.

- **items.py**: Definition of data items structure.

- **middlewares.py**: Middleware settings for web scraping, which can include user-agent and proxy handling.

- **pipelines.py**: Definitions of item processing pipelines.

- **settings.py**: Scrapy project settings and configurations.

- **scrapy.cfg**: The configuration file for the Scrapy project.

- **.gitignore**: Git configuration file specifying files and directories to be ignored by version control.

- **README.md**: This documentation file.

## How to Use

1. Start by running the web scraping scripts in the "spiders" directory to collect real estate data from websites. Make sure to configure the scraping targets and rules as needed.

2. Once data is collected, follow the data preparation and modeling steps in the "data_preparation_and_modelling" directory to clean, preprocess, and build predictive models for home prices.

3. For predictive modeling, the repository includes the pre-trained Random Forest Regressor model saved as "random_forest_regressor.pkl." You can use this model to predict home prices based on the features.

## Predictive Model Deployment to Heroku (Heroku Git)
1. Sign up for a free Heroku account if you haven't already done so.

2. Create an app, e.g., app.py.

3. Open a terminal and type `heroku login`. This will take you to a web-based login page.

4. Navigate to your project directory using `cd`.

5. Type `git init` to initialize a new Git repository.

6. Type `heroku git:remote -a myapp` to set up the Heroku remote.

7. Type `git add .` to stage all changes.

8. Type `git commit -am "version 1"` to commit changes.

9. Type `git push heroku master` to deploy your app to Heroku.

10. Allocate a dyno to do the work by typing `heroku ps:scale worker=1`.

11. Check the logs using `heroku logs --tail` to ensure it's working correctly.

12. Your code will continue to run until you stop the dyno. To stop it, scale it down using the command `heroku ps:scale worker=0`.

## Contributing

If you'd like to contribute to this project, feel free to open issues, suggest improvements, or submit pull requests. We welcome your input to make this project better and more robust.
