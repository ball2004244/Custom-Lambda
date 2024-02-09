content="
def pascal_triangle(n):
    triangle = []
    for i in range(n):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
    return triangle
"
json_content=$(jq -n --arg str "$content" '{"content":$str}')
curl -X POST -H "Content-Type: application/json" -d "$json_content" http://localhost:9999/api/functions/pascal_triangle
