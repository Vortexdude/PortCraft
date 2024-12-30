import requests

url = "https://api.github.com/graphql"
query = """
{
  repository(owner: "vortexdude", name: "DockCraft") {
    defaultBranchRef {
      target {
        ... on Commit {
          history(first: 5) {
            edges {
              node {
                message
                committedDate
              }
            }
          }
        }
      }
    }
  }
}
"""

response = requests.post(url, json={"query": query}, headers=headers)
if response.status_code == 200:
    print(response.headers)
    print(response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")
    
