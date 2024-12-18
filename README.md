# octoprint-status-discord
 Python bot that relays Octoprint status to Discord. It uses a dedicated Discord channel to occasionally update the status on multiple printers. Useful for makerspaces or printer farms. 

## How do I configure it?

Make a copy of config.json.exmaple and name it config.json

Configure the following variables 
- `discord_token` - create a Discord bot
- `channel_id` - Discord channel ID
  - Recommended you create a dedicated server channel
- `update_interval` - How often you want updates on printer status
  - Not recommend to set less than 120 seconds, Discord rate limiting will hit you
- `printers` - JSON array containing all of the printers you want to track
  - You can have more than three, have not tested with more than five printers

## How do I run it?

I recommend running it via Docker Compose using the provided compose file. 

## How does it work?

Every X minutes it will call the Octoprint API and update a message that it creates in a Discord channel. 

It can report:
- Printer status
- Print progress as a percentage
- Time remaining
- File name being printed
- How long ago the last update was provided

<img width="475" alt="Screenshot 2024-12-18 at 12 03 39 PM" src="https://github.com/user-attachments/assets/35dbb5e2-ba15-41ff-879c-73893cf4e376" />
