#!/usr/bin/env bash

HEALTH_SERVICES="%D7%A9%D7%99%D7%A8%D7%95%D7%AA%D7%99%20%D7%91%D7%A8%D7%99%D7%90%D7%95%D7%AA"
HEALTH_SERVICES_ITEM='{"url":"https://next.obudget.org/s/?q='${HEALTH_SERVICES}'","title":"'${HEALTH_SERVICES}'"}'
ACQUISITIONS_AND_MAINTANANCE="%D7%94%D7%A6%D7%98%D7%99%D7%99%D7%93%D7%95%D7%AA%20%D7%95%D7%90%D7%97%D7%96%D7%A7%D7%94"
ACQUISITIONS_AND_MAINTANANCE_ITEM='{"url":"https://next.obudget.org/s/?q='${ACQUISITIONS_AND_MAINTANANCE}'","title":"'${ACQUISITIONS_AND_MAINTANANCE}'"}'
TEST_ITEM='{"url":"https://next.obudget.org/s/?q=TEST","title":"TEST"}'
FOOBAR_ITEM='{"url":"https://next.obudget.org/s/?q=foobar","title":"foobar"}'
JWT_TOKEN="mock_jwt"
TEST_USER_ID=123

list_curl() {
    if [ "${DEBUG}" == "1" ]; then
        curl -v -H 'Content-Type: application/json' -X "${1}" $4 -g "localhost:5050/list?jwt=${2}&${3}"
    else
        curl -s -H 'Content-Type: application/json' -X "${1}" $4 -g "localhost:5050/list?jwt=${2}&${3}"
    fi
}

# add items
[ "true" != "$(list_curl PUT "${TEST_USER_ID}" "list=saved-searches" "-d ${HEALTH_SERVICES_ITEM}")" ] \
    && echo "failed to add health services item to saved search list" && exit 1

[ "true" != "$(list_curl PUT "${TEST_USER_ID}" "list=saved-searches" "-d ${ACQUISITIONS_AND_MAINTANANCE_ITEM}")" ] \
    && echo "failed to add acqusitions and maintanence item to saved search list" && exit 1

[ "true" != "$(list_curl PUT "${TEST_USER_ID}" "list=saved-searches" "-d ${TEST_ITEM}")" ] \
    && echo "failed to add test item to saved search list" && exit 1

[ "true" != "$(list_curl PUT "${TEST_USER_ID}" "list=saved-searches" "-d ${FOOBAR_ITEM}")" ] \
    && echo "failed to add foobar item to saved search list" && exit 1

# get items
ITEMS_RES=$(list_curl GET "${TEST_USER_ID}" "list=saved-searches")

[ "4" != "$(echo "${ITEMS_RES}" | jq '.items | length')" ] \
    && echo "didn't get expected number of items in saved-searches list" && exit 1

ITEM_ID=$(echo "${ITEMS_RES}" | jq '.items[0].id')
[ -z "${ITEM_ID}" ] && echo "failed to get item id" && exit 1

# delete item
[ "true" != "$(list_curl DELETE "${TEST_USER_ID}" "list=saved-searches&item_id=${ITEM_ID}")" ] \
    && echo "failed to delete item from saved-searches list" && exit 1

# verify item was deleted
ITEMS_RES=$(list_curl GET "${TEST_USER_ID}" "list=saved-searches")
[ "3" != "$(echo "${ITEMS_RES}" | jq '.items | length')" ] \
    && echo "didn't get expected number of items in saved-searches list after deletion" && exit 1

echo "Success!"
exit 0
