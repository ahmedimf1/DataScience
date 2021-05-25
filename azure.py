import os
import cmd
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

keyVaultName = os.environ["anomalyDetectorAPI"]
KVUri = f"https://anomalykey.vault.azure.net/secrets/anomalyDetectorAPI/c0396feaa9c04f69b9f7acbbe82b7892"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)


print(f"Retrieving your secret from {keyVaultName}.")

retrieved_secret = client.get_secret(secretName)

print(f"Your secret is '{retrieved_secret.value}'.")

print(" done.")
