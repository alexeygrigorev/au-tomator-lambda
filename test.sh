
docker build -t automator-test .

docker run -d --rm \
    --name automator-test \
    -e GROQ_API_KEY=${GROQ_API_KEY} \
    -e SLACK_TOKEN=${SLACK_TOKEN} \
    -e USER_SLACK_TOKEN=${USER_SLACK_TOKEN} \
    -p 8080:8080 \
    automator-test

sleep 5

python test_ai.py

docker logs automator-test 
docker stop automator-test