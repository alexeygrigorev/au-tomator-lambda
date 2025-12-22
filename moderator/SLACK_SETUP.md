# Slack Configuration Guide for Message Moderator

## Required Slack App Configuration

### OAuth Scopes

Your Slack app needs the following scopes:

**Bot Token Scopes** (SLACK_TOKEN):
- `chat:write` - Post messages to channels and DMs
- `channels:history` - View messages in public channels
- `groups:history` - View messages in private channels
- `im:history` - View messages in DMs
- `mpim:history` - View messages in group DMs

**User Token Scopes** (USER_SLACK_TOKEN):
- `chat:write` - Delete messages
- `admin.users:write` - Deactivate users (requires workspace admin)

### Event Subscriptions

1. Go to your Slack App settings → Event Subscriptions
2. Enable Events
3. Set Request URL to your API Gateway endpoint (e.g., `https://your-api.execute-api.us-east-1.amazonaws.com/prod/slack/events`)
4. Subscribe to bot events:
   - `message.channels` - Messages posted to public channels
   - `message.groups` - Messages posted to private channels
   - `message.im` - Direct messages
   - `message.mpim` - Group direct messages

### Interactive Components

1. Go to your Slack App settings → Interactivity & Shortcuts
2. Enable Interactivity
3. Set Request URL to your API Gateway endpoint (same as events, or a dedicated endpoint)
4. The moderator lambda needs to handle interactive payloads when admin clicks buttons

### API Gateway Configuration

The interactive components send data as `application/x-www-form-urlencoded` with a `payload` parameter.

You need to configure API Gateway to:
1. Accept POST requests
2. Parse the form data
3. Extract the `payload` parameter
4. Pass it to the Lambda in the event

Example API Gateway Lambda Integration mapping template:
```json
{
  "payload": "$util.urlDecode($input.params('payload'))"
}
```

Or, configure your Lambda to handle the raw event and extract the payload itself.

### Environment Variables

Set these in your Lambda function configuration:

- `SLACK_TOKEN` - Your bot token (starts with `xoxb-`)
- `USER_SLACK_TOKEN` - Your user token with admin privileges (starts with `xoxp-`)
- `ADMIN_USER_ID` - Slack user ID of the admin (e.g., `U01AXE0P5M3`)
- `MESSAGE_TRACKER_TABLE` - DynamoDB table name (default: `slack-message-tracker`)
- `MESSAGE_THRESHOLD` - Number of messages to trigger alert (default: `5`)
- `TIME_WINDOW_SECONDS` - Time window in seconds (default: `180` = 3 minutes)

## Testing the Configuration

1. Post several messages quickly in a monitored channel
2. After 5 messages in 3 minutes, the admin should receive a DM with:
   - Summary of the messages
   - Three action buttons: Delete Messages, Deactivate User, Ignore
3. Click a button to test the interactive components

## Troubleshooting

### Messages not being tracked
- Check CloudWatch logs for the moderator lambda
- Verify event subscriptions are configured
- Ensure the router is routing message events to the moderator lambda

### Buttons not working
- Check that interactive components request URL is configured
- Verify the Lambda can parse the payload
- Check CloudWatch logs for errors when clicking buttons

### Cannot delete messages
- Ensure USER_SLACK_TOKEN has the correct scopes
- The token must be from a user (not a bot) with permission to delete messages
- Check that the message timestamps are valid

### Cannot deactivate users
- Requires `admin.users:write` scope
- The user token must be from a workspace admin
- Check Slack API response for specific error messages
