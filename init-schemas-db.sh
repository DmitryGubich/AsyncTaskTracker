#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username postgres --dbname postgres <<-EOSQL
	CREATE SCHEMA auth_schema;
	CREATE SCHEMA tracker_schema;
	CREATE SCHEMA analytics_schema;
	CREATE SCHEMA accounting_schema;
EOSQL