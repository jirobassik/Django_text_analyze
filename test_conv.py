import cloudconvert
from file_use.file_use import download_file_from_url

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiN2RmMDYyZjU2OWRhYmU5MTQ1YWNhYjQ5NjYyOT" \
          "g4NzZhNDJmOGNiYzA1NGNlNGE5ZTc2YWI0MWJkMDk0ZDZlNjYxNTk0ZjhmZDMwMzgwMDIiLCJpYXQiOjE2NzkwNjgzMzguOTI5Miw" \
          "ibmJmIjoxNjc5MDY4MzM4LjkyOTIwMSwiZXhwIjo0ODM0NzQxOTM4LjkxNzE2OSwic3ViIjoiNjI2Mjg1MTQiLCJzY29wZXMiOlsid" \
          "XNlci5yZWFkIiwidXNlci53cml0ZSIsInRhc2sucmVhZCIsInRhc2sud3JpdGUiLCJ3ZWJob29rLnJlYWQiLCJ3ZWJob29rLndyaXRlI" \
          "iwicHJlc2V0LnJlYWQiLCJwcmVzZXQud3JpdGUiXX0.M8CJ4rvD2RTIgjiYgPrQXMjSGG8MOpq3IN26HwniI-oQNxPMYUCItLD5Q2ve" \
          "l63ME-wOQE0Z3CaFX_h_LnPkzFAyUFR1mmMsFe2CrQYJ7wMXw3Y5aPzW2S-BtQOpoNwzS5bkc8XN14146jV9ZlOyAI1AhgX9VPdXZj" \
          "c4_VgrAnfXRJArl983BPcoSWe56npWYoJrtosCLgX14l-a9i6kSqTv0-_rAdLzmx-jbPBUi2GFECNxnjSgK089ZoH1cYoZUA-3L8Q" \
          "4CGoNs3TAvGjttP-QpOHCzK-S1TuaMAdSZdWgL-cEjT71envg1yWMlHLZKHzMYQPETqbj-qHoxSJUQYbmjRMU9HKljB16rMMM4x-Pk" \
          "gYhbshpV6VqhU1TzcjJ6FAKbbC2eWr58l3hyMCag2hh-kEl5RBq1WYdpHAGKPPc7NuM3UQTX18cNXzGRd-Zo2Nc3OuyCFWZEZDGlyl3" \
          "0E7_nWvRFmfcFNMHV095moZvVEZCy-79d8w3dOkkT1OYzxkjgdzqiGet-OgQKhej96bxzAHyKXhLz1aApiZmWU8veJkL71KPqxxpgwS" \
          "h4FF1AeynqdnxFg_MdvGpHOnAKszvsU3cSbDVGWGTK7OLyt23qkzZXXsmA5tTMZ5K4a8ITUDgsqyAJBQqq4olFIvg7Gee9QYCz2JNkh" \
          "tP3fG_csA"

def cloud_converter():
    cloudconvert.configure(api_key=api_key, sandbox=False)
    job = cloudconvert.Job.create(payload={
        'tasks': {
            'upload-my-file': {
                'operation': 'import/upload'
            },
            'convert-my-file': {
                'operation': 'convert',
                'input': 'upload-my-file',
                'output_format': 'png',
            },
            'export-my-file': {
                'operation': 'export/url',
                'input': 'convert-my-file',
            }
        }
    })

    upload_task_id = job['tasks'][0]['id']
    upload_task = cloudconvert.Task.find(id=upload_task_id)
    cloudconvert.Task.upload(file_name='role/static/upload/role.svg', task=upload_task)

    exported_url_task_id = job['tasks'][2]['id']
    res = cloudconvert.Task.wait(id=exported_url_task_id)
    file = res.get("result").get("files")[0]
    download_file_from_url(file['url'])
    return True
