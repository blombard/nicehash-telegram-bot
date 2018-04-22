# Starting out

1.  Step 1: Serverless framework

    ```bash
    npm install -g serverless
    ```

2.  Export credentials:

  ```bash
  export AWS_ACCESS_KEY_ID=<Access key ID>
  export AWS_SECRET_ACCESS_KEY=<Secret access key>
  export TELEGRAM_TOKEN=<Your Telegram Token>
  ```

3.  Install pip requirements:

  ```bash
  pip install -r requirements.txt -t vendored
  ```

4.  Deploy to AWS::

  ```bash
  serverless deploy
  ```
