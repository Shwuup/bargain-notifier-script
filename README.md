# bargain-notifier

A script to notify you when there's a bargain you're interested in on OzBargain

## Installation

```
git clone git@github.com:Shwuup/bargain-notifier.git
```

## Usage

Make sure you have created the prequisite secrets file for email and/or text notifications.

Run the script by entering into terminal:

```
cd bargain-notifier
pipenv run python3 main.py -n {email OR text} -i {keywords separated by space}
```

Example using crontab for scheduling:

```
30 * * * * cd /path/to/bargain-notifier && pipenv run python3 main.py -n email -i switch lego

```

## Secrets formats

### Email

Create app password for your email provider ([Gmail](https://support.google.com/accounts/answer/185833?hl=en), [Outlook](https://support.microsoft.com/en-au/help/12409/microsoft-account-app-passwords-and-two-step-verification))

Make a file called email_secrets.txt in folder bargain-notifier with format:

```
email address
app password
```

### Text

Create a twilio account [here](https://www.twilio.com/try-twilio)

Make a file called text_secrets.txt in folder bargain-notifier with format:

```
account sid
auth token
twilio phone number
your phone number
```
