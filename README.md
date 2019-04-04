# bargain-notifier
A script to notify you when there's a bargain you're interested in on OzBargain
## Installation
```
git clone git@github.com:Shwuup/bargain-notifier.git
```
## Usage
Run the script by entering into terminal:
```
cd bargain-notifier
pipenv run python3 main.py -n {email OR text} -i {keywords separated by space}
```
Example using crontab for scheduling:
```
30 * * * * cd /path/to/bargain-notifier && pipenv run python3 main.py -n email -i switch lego 

```
