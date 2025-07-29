const fs = require("fs");
const { SecretsManagerClient, GetSecretValueCommand } = require("@aws-sdk/client-secrets-manager");

const config = JSON.parse(fs.readFileSync("config.json", "utf-8"));
const secretName = config.secretName;
const region = config.region;

const client = new SecretsManagerClient({ region });

(async () => {
  const command = new GetSecretValueCommand({ SecretId: secretName });
  const response = await client.send(command);
  const secrets = JSON.parse(response.SecretString);

  const lines = [
    `REACT_APP_TOKEN=${secrets.REACT_APP_TOKEN}`,
    `REACT_APP_API_IMPROVE=${secrets.REACT_APP_API_IMPROVE}`,
    `REACT_APP_API_RETRIEVE=${secrets.REACT_APP_API_RETRIEVE}`,
    `REACT_APP_API_GENERATE=${secrets.REACT_APP_API_GENERATE}`
  ];

  fs.writeFileSync(".env", lines.join("\n"));
  console.log("✅ .env updated from AWS Secrets Manager");
})();
