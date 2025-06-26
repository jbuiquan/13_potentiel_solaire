#!/bin/bash

# Get parent directory of this script
APPLICATION_DIR=$(dirname "$(readlink -f "$0")")

# Get the current date
ALGORITHME_VERSION="0.1.0"
CURRENT_DATE=$(date +%Y%m%d)
IMAGE_NAME="ghcr.io/dataforgoodfr/13_potentiel_solaire_app:$ALGORITHME_VERSION.$CURRENT_DATE"

# Build docker image
docker build \
	-t $IMAGE_NAME \
	--build-arg DATABASE_PATH=/app/database/data.duckdb \
	-f $APPLICATION_DIR/Dockerfile .

# Check if the previous command was successful
if [ $? -ne 0 ]; then
    echo "Docker build failed."
    exit 1
else
    echo "Docker build succeeded."

    # Créer un token personnel sur son compte github, avec comme droit : write:packages
    # cf https://docs.github.com/fr/packages/working-with-a-github-packages-registry/working-with-the-container-registry
    read -p "Enter your personal access token (github) with write:packages scope: " CR_PAT
    echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin

    # Push the image to GitHub Container Registry
    docker push $IMAGE_NAME
fi
