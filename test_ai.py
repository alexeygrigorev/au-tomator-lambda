import lambda_function


event = {
    "version": "2.0",
    "routeKey": "ANY /slack",
    "rawPath": "/slack",
    "rawQueryString": "",
    "headers": {
        "accept": "*/*",
        "accept-encoding": "gzip,deflate",
        "content-length": "726",
        "content-type": "application/json",
        "host": "vmnqlq0emg.execute-api.eu-west-1.amazonaws.com",
        "user-agent": "Slackbot 1.0 (+https://api.slack.com/robots)",
        "x-amzn-trace-id": "Root=1-667d9393-784fc3e436a932c4126720f2",
        "x-forwarded-for": "3.237.26.23",
        "x-forwarded-port": "443",
        "x-forwarded-proto": "https",
        "x-slack-request-timestamp": "1719505810",
        "x-slack-signature": "v0=03e71a88058013f23da11e3bf7b12cf287e1e138e2791f812b6ce5d5944c9efb"
    },
    "requestContext": {
        "accountId": "387546586013",
        "apiId": "vmnqlq0emg",
        "domainName": "vmnqlq0emg.execute-api.eu-west-1.amazonaws.com",
        "domainPrefix": "vmnqlq0emg",
        "http": {
            "method": "POST",
            "path": "/slack",
            "protocol": "HTTP/1.1",
            "sourceIp": "3.237.26.23",
            "userAgent": "Slackbot 1.0 (+https://api.slack.com/robots)"
        },
        "requestId": "aCP_Bi0WDoEEMSQ=",
        "routeKey": "ANY /slack",
        "stage": "$default",
        "time": "27/Jun/2024:16:30:11 +0000",
        "timeEpoch": 1719505811093
    },
    "body": "{\"token\":\"uURN4G72mcTUEu4NNlJ0RAqA\",\"team_id\":\"T01ATQK62F8\",\"context_team_id\":\"T01ATQK62F8\",\"context_enterprise_id\":null,\"api_app_id\":\"A01S395330A\",\"event\":{\"type\":\"reaction_added\",\"user\":\"U01AXE0P5M3\",\"reaction\":\"ask-ai\",\"item\":{\"type\":\"message\",\"channel\":\"C01S3EGKMJP\",\"ts\":\"1719505805.593239\"},\"item_user\":\"U01AXE0P5M3\",\"event_ts\":\"1719505810.000100\"},\"type\":\"event_callback\",\"event_id\":\"Ev07A37MQV5Y\",\"event_time\":1719505810,\"authorizations\":[{\"enterprise_id\":null,\"team_id\":\"T01ATQK62F8\",\"user_id\":\"U01AXE0P5M3\",\"is_bot\":false,\"is_enterprise_install\":false}],\"is_ext_shared_channel\":false,\"event_context\":\"4-eyJldCI6InJlYWN0aW9uX2FkZGVkIiwidGlkIjoiVDAxQVRRSzYyRjgiLCJhaWQiOiJBMDFTMzk1MzMwQSIsImNpZCI6IkMwMVMzRUdLTUpQIn0\"}",
    "isBase64Encoded": False
}


lambda_function.lambda_handler(event, None)
