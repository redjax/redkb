#!/bin/bash

THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTAINER_CERT_DIR="${THIS_DIR}/.certs/nginx"

if [[ ! -d "${CONTAINER_CERT_DIR}" ]]; then
  echo "SSL certificate directory '${CONTAINER_CERT_DIR}' does not exist. Creating."
  mkdir -pv "${CONTAINER_CERT_DIR}"
fi

read -p "What is your domain (i.e. hostname.home, localhost.home, etc): " DOMAIN

echo "Generating SSL certificate for edit.* domains"
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ${CONTAINER_CERT_DIR}/edit_key.key -out ${CONTAINER_CERT_DIR}/edit_cert.crt -subj "/CN=edit.${DOMAIN}"

echo "Generating SSL certificate for docs.* domains"
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ${CONTAINER_CERT_DIR}/docs_key.key -out ${CONTAINER_CERT_DIR}/docs_cert.crt -subj "/CN=docs.${DOMAIN}"
