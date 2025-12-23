# Quick Reference: Message Moderation System

## What Was Built

A Slack message moderation system that:
- Monitors message rates per user
- Alerts admin when threshold exceeded (5 messages in 3 minutes)
- Provides interactive buttons for admin actions

## Architecture Flow

```
Slack Event → API Gateway → Router Lambda
                              ↓
                    (routes based on event type)
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
            Automator Lambda    Moderator Lambda
            (reactions)         (messages + buttons)
                                        ↓
                                  DynamoDB
                              (message tracking)
                                        ↓
                          Admin DM with Buttons
```

## Key Files

### Moderator Lambda
- `moderator/lambda_function.py` - Main handler
- `moderator/message_tracker.py` - DynamoDB tracking
- `moderator/slack_moderator.py` - Slack API integration
- `moderator/package.sh` - Build script
- `moderator/deploy.sh` - Deployment script

### Documentation
- `moderator/README.md` - Comprehensive guide
- `moderator/SLACK_SETUP.md` - Slack configuration
- `IMPLEMENTATION_SUMMARY.md` - This implementation

### Tests
- `tests/test_message_tracker.py` - Tracking logic tests
- `tests/test_moderator_lambda.py` - Lambda handler tests
- `integration_tests/test_moderator.py` - LocalStack integration test

## Admin Alert Example

```
⚠️ Message Rate Limit Exceeded

User @spammer has posted 5 messages in the last 3 minutes.

────────────────────────────────
Message 1 in #general:
> Hey everyone check this out!

Message 2 in #general:
> This is amazing!

Message 3 in #random:
> You won't believe this!
...
────────────────────────────────

[🗑️ Delete All Messages] [🚫 Deactivate User] [✅ Ignore]
```

## How It Works

1. **User posts messages** → Events sent to router
2. **Router** → Routes to moderator lambda
3. **Moderator** → Tracks in DynamoDB
4. **Threshold check** → If exceeded, send alert
5. **Admin clicks button** → Router → Moderator handles action
6. **Action executed** → Messages deleted / user deactivated / ignored

## Environment Setup

```bash
# Required
SLACK_TOKEN=xoxb-...
USER_SLACK_TOKEN=xoxp-...
ADMIN_USER_ID=U01AXE0P5M3
SLACK_TEAM_ID=T01234567

# Optional (defaults shown)
MESSAGE_THRESHOLD=5
TIME_WINDOW_SECONDS=180
MESSAGE_TRACKER_TABLE=slack-message-tracker
```

## Testing Locally

```bash
# Start LocalStack
docker-compose up -d

# Run tests
python3 -m unittest discover -s tests

# Run integration tests
python3 integration_tests/test_moderator.py
```

## Deployment

```bash
# Deploy router (handles routing)
cd router
bash publish.sh

# Deploy automator (handles reactions)
cd ../
make deploy

# Deploy moderator (handles messages)
cd moderator
bash package.sh
bash deploy.sh
```

## Common Issues & Solutions

**Messages not tracked?**
- Check event subscriptions in Slack app
- Verify router is routing message events
- Check CloudWatch logs

**Buttons not working?**
- Enable Interactivity in Slack app
- Set correct request URL
- Verify router parses form-encoded payloads

**Cannot delete messages?**
- USER_SLACK_TOKEN needs `chat:write` scope
- Token must be from user with permissions

**Cannot deactivate users?**
- Need `admin.users.session:write` scope
- Token must be from admin
- SLACK_TEAM_ID must be set

## Security Notes

✅ All secrets via environment variables
✅ Message text truncated to 500 chars
✅ No hardcoded credentials
✅ CodeQL scan passed (0 vulnerabilities)
✅ Input validation for Slack payloads

## Metrics & Monitoring

Check CloudWatch Logs for:
- Message tracking events
- Threshold exceeded events
- Admin action events
- Error messages

DynamoDB metrics:
- Read/write capacity
- Item count
- Table size
