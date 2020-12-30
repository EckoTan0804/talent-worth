# TalentWorth

## Built with

- [Dash](https://dash.plot.ly/) : Main server and interactive components
- [Plotly Python](https://plot.ly/python/) : interactive plots
- [Dash DAQ](https://dash.plot.ly/dash-daq) : Styled technical components for industrial applications
- [pandas](https://pandas.pydata.org/): data analysis and manipulation

## Requirements

Clone from repo:

```bash
git clone https://github.com/EckoTan0804/talent-worth.git
```

Create a separate virtural environment:

```bash
cd talent-worth
python3 -m virtualenv venv
source venv/bin/activate
```

Install all of the required packages to this environment:

```bash
pip install -r requirements.txt
```

## Run

Run this app locally:

```bash
python app.py
```

Then open http://127.0.0.1:8052/ in browser, you'll see a live-updating app.

## Deployment

- This app is deployed on [Heroku](https://www.heroku.com/). 
- Every push to `main` branch will deploy a new version of this app automatically.

## Resources

- Documentation: [Dash User Guide](https://dash.plotly.com/)
- Getting started: [Dash Tutorial](https://dash.plotly.com/installation)