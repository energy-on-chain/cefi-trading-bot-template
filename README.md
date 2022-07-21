# Welcome to Energy On Chain's "cefi-trading-bot-template"!

## [ DESCRIPTION ]
This repo contains the boiler plate code for an automated trading bot that reads in real-time price data, applies trading strategy logic, then executes trades on CEFI exchanges. Because it was written with extensibility in mind, trading strategies, exchange connections, etc. can be easily swapped in and out by adding / removing single lines of code in the main run file (run.py). Whether you have a complicated idea for a strategy or a simple one, you'll be able to implement it here.

## [ STACK ]
- Python (key packages include pandas, numpy, schedule)
- Google Cloud Services (for pulling and storing real-time data)

## [ BACKGROUND ]
Energy On Chain has used this base repo to implement automated trading strategies for clients that vary from simple threshold monitors to more complicated machine-learning-based algorithms. Feel free to take the basic ideas and run with them yourself, or get in touch to work on building your idea for a strategy together! 
