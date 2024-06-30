# Webscraper and Flappy Bird Project

## Authors
- **Yousuf Muhammud** from SLU
- **Danial Khurshid** from SLU

## Overview
This project includes two main components:
1. A web scraper using Python and Selenium to gather flight data.
2. The Flappy Bird game, sourced from this repository(https://github.com/MikeShi42/FlappyBird).

### Web Scraper
The web scraper was developed to automate the process of collecting flight prices and details from various travel websites. The scraper is designed to:
- Retrieve flight data from Expedia and Google Flights.
- Use headless Chrome for scraping to operate without a UI.
- Randomize user agents to mimic real browsing sessions.

### Technologies Used
- **Languages**: Python
- **Libraries**:
  - `Selenium`: For web scraping and browser automation.
  - `Flask`: To create the web application.
  - `dotenv`: For environment variable management.
  - `webdriver-manager`: To manage browser drivers.
- **Tools**:
  - **GitHub**: For version control and collaboration.

### Flappy Bird Game
We integrated the Flappy Bird game into our project, using the source code available from [this repository](https://github.com/MikeShi42/FlappyBird). The game was modified to fit within our web application, allowing users to play directly through the site.

### Project Structure
- `app.py`: Main application file for the Flask web app.
- `project.py`: Contains the web scraping functions and logic.
- `static/`: Contains static files for the web app (e.g., CSS, images).
- `templates/`: HTML templates for the web app.

