#!/bin/bash
ENV_FILE=$1
CONTAINERAPP_NAME=$2
RESOURCE_GROUP=$3

# Function to convert env var name to valid Azure secret name
to_secret_name() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | tr '_' '-' | sed 's/[^a-z0-9-]//g' | sed 's/^-*//' | sed 's/-*$//'
}

# Parse the .env File and Set Secrets
while IFS='=' read -r key value || [[ -n "$key" ]]; do
  [[ -z "$key" || "$key" == \#* ]] && continue
  key=$(echo "$key" | xargs)
  value=$(echo "$value" | xargs)
  secret_name=$(to_secret_name "$key")
  echo "Adding secret: $secret_name"
  az containerapp secret set \
    --name "$CONTAINERAPP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --secrets "$secret_name=$value"
done < "$ENV_FILE"

# Inject the Secrets as Env Vars Using secretref
ENV_VARS=""
while IFS='=' read -r key _ || [[ -n "$key" ]]; do
  [[ -z "$key" || "$key" == \#* ]] && continue
  secret_name=$(to_secret_name "$key")
  ENV_VARS+="$key=secretref:$secret_name "
done < "$ENV_FILE"

ENV_VARS=$(echo "$ENV_VARS" | xargs)

az containerapp update \
  --name "$CONTAINERAPP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --set-env-vars $ENV_VARS