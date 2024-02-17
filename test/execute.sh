params='[5]'  # The parameters for the function, as a JSON array
target='0'  # The file that contains the function

json_data=$(jq -n \
                --arg target "$target" \
                --argjson params "$params" \
                '{"params":$params, "target":$target}')

curl -X POST -H "Content-Type: application/json" -d "$json_data" http://localhost:$port/api/execute/pascal_triangle
