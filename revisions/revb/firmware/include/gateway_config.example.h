#pragma once
// Copy to gateway_config.local.h and edit before building.
// Use the CA that signs your HTTPS reverse proxy. Keep the device token private.
#define PAKY_GATEWAY_URL "https://paky.example.invalid/v1/ask"
#define PAKY_GATEWAY_TOKEN "replace-with-a-private-device-token"
#define PAKY_GATEWAY_NTP "ntp.example.invalid"
#define PAKY_GATEWAY_CA_PEM ""
