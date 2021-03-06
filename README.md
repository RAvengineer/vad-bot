# VAD-Bot
### :robot: Vaccine Availability Discord Bot
---

## Features
- [x] Discord notification
- [x] Search-by mode customization
- [x] Search for list of pincodes
- [x] Randomized intevals of requests
- [ ] Logging

## :man_technologist: How to use?
1.  Clone the repository :octocat:
    ```bash
    git clone https://github.com/RAvengineer/vad-bot.git
    cd vad-bot
    ```
1.  Create a webhook in the desired Discord channel. Follow this [Intro to Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) official guide for learning how to create & manage a webhook.
1.  Follow the guidelines for `.env` file provided below (next section) :arrow_double_down:
1.  *(Optional)* Create a virtual environment *[Requires Python 3+]*
    ```bash
    python -m venv venv
    source ./venv/bin/activate
    ```
1.  Install required libraries
    ```bash
    pip install -r requirements.txt
    ```
1.  Execute in terminal
    ```bash
    python vad-bot.py
    ```


## :notebook: Guidelines: `.env` file
Create file named `.env` in the root directory of the project & paste the content provided below
```yaml
# Discord Webhook URL for the channel in which you want notifications
DISCORD_WEBHOOK_URL = YOUR-DISCORD-CHANNEL-URL-HERE

# Search centers by District or List of Pincodes
# Comment out the mode you are not using
#SEARCH_BY = DISTRICT
SEARCH_BY = PINCODE

# Set District ID, if SEARCH_BY mode chosen as DISTRICT
# (Ex.: 391)
DISTRICT_ID = YOUR-3-DIGIT-DISTRICT-ID-HERE

# List Pincodes, if SEARCH_BY mode chosen as PINCODE
LIST_OF_PINCODES = [201301, 301233, 401408, 501209, 801301, 901304]
```
**:computer: Setup .env file from terminal (For Linux/MacOS users):**
1.  Type the following
    ```bash
    nano .env
    ```
1.  Use `Ctrl + Shift + V` to paste the copied text contents
1.  Press `Ctrl + S`, followed by `Ctrl + X` to save & exit the file

**:question: How to find your DISTRICT_ID?**
1.  Open [this](https://cdn-api.co-vin.in/api/v2/admin/location/states) link containing the list of `state_id` & `state_name`
1.  Press `Ctrl+F` and type your State name. You will be find you state in the form of
    ```json
    {"state_id":21,"state_name":"Maharashtra"}
    ```
1.  Note down the State ID, for the above example it is `21`.
1.  Copy & paste 
    `https://cdn-api.co-vin.in/api/v2/admin/location/districts/state_id`
    in your address bar (Don't hit search/Enter/Return yet!)
1.  Replace `state_id` in the above link with the State ID noted down in the 4th step. Then, hit Enter/Return/search
1. Again, there will be a list of districts displayed with `district_id` & `district_name`
1. Press `Ctrl+F` and type your District name. You will be find you district in the form of
    ```json
    {"district_id":395,"district_name":"Mumbai"}
    ```
1.  Replace `YOUR-3-DIGIT-DISTRICT-ID-HERE` in `.env` file with the District ID found in the previous step

### Note for `PINCODE` mode users
> **TL;DR:** In `PINCODE` mode, limit the number of pincodes in the list to **6**

> ... The appointment availability data is cached and may be upto 30 minutes old. Further, these **APIs are subject to a rate limit of 100 API calls per 5 minutes per IP** ...
[Updated on 5 May 2021]
Source: [API Setu](https://apisetu.gov.in/public/marketplace/api/cowin)

Considering the above limit & the fact that this bot requests data from the API in an interval decided by a psudo-random function which returns values between 20 to 40 inclusively,
it is evident that number of Pincodes provided in the list should NOT exceed 6.
*Explanation:*
```math
5 minutes = 5 * 60 seconds = 300 seconds
```
In worst case scenario, the psudo-random function returns the value 20 on every call. Thus, the `fetchData` function will be called
```math
300/20 = 15 times
```
Now, each pincode requires a seperate request.
Therefore, number of possible pincodes to avoid your IP being blocked are
![\lfloor100/15\rfloor = 6 pincodes](https://bit.ly/2Slz56z)

---

## :link: References:
- API Helpers
    - [CoWIN API Documentation | API Setu](https://apisetu.gov.in/public/marketplace/api/cowin)
    - [Python strftime() - datetime to string | Programiz](https://www.programiz.com/python-programming/datetime/strftime)
- Discord Webhook
    - [Webhook | Discord Developer Portal](https://discord.com/developers/docs/resources/webhook)
    - [allowed_mentions - Channel | Discord Developer Portal](https://discord.com/developers/docs/resources/channel#allowed-mentions-object)
    - [create-message - Channel | Discord Developer Portal](https://discord.com/developers/docs/resources/channel#create-message)
- Misc
    - Avoid Repetion of centers: [set difference using subtraction | StackOverflow](https://stackoverflow.com/a/48038480)
    - [Add comments in .env](https://akhromieiev.com/how-to-add-comment-in-env-file/)
    - [Running & killing Python programs in the background | GeeksForGeeks](https://www.geeksforgeeks.org/running-python-program-in-the-background/)
