#!/usr/bin/env bash

rm -f ./db.sqlite
DATABASE_URL="sqlite:///db.sqlite" ENABLE_MOCK_OAUTH=1 python server.py
