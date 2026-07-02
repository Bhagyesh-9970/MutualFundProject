# Project Summary

## Overview

This repository is a complete mutual fund analytics project that combines data ingestion, cleaning, exploratory analysis, SQL-based storage, visualization, and advanced portfolio analytics. It was developed as a capstone-style project for financial data analysis and reporting.

## What the project does

- Loads and cleans mutual fund datasets from CSV files
- Stores cleaned data in SQLite for structured querying
- Performs exploratory analysis of NAV trends, fund performance, AUM growth, and SIP inflows
- Builds an interactive Streamlit dashboard for fund comparison and filtering
- Implements Monte Carlo simulation to project future NAV growth under uncertainty
- Implements portfolio optimization using an efficient frontier approach
- Generates HTML-based weekly report summaries for email distribution
- Supports scheduled NAV ETL for weekdays at 8 PM

## Main modules

- app.py: Streamlit web dashboard
- efficient_frontier.py: portfolio optimization logic
- monte_carlo.py: Monte Carlo NAV projection
- email_report.py: automated weekly report generator
- scripts/live_nav_fetch.py: live NAV fetch from mfapi.in
- scripts/clean_*.py: ETL and cleaning utilities
- sql/schema.sql and sql/queries.sql: database schema and example queries

## Project value

The project demonstrates end-to-end analytics for mutual fund data, including:

- data preparation
- financial insights
- portfolio analysis
- reporting automation
- deployment-friendly dashboarding

## Outcome

The project is now complete and ready to showcase as a practical analytics solution for mutual fund performance monitoring and portfolio decision support.
