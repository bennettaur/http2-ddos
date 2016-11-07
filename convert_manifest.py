import json
import sys

location_path = "/index.html"

apache_h2_push_template = """
<Location {}>
    {}
</Location>
"""

header_link_template = 'Header add Link "<{}>;rel=preload"'

file_name = sys.argv[1]

with open(file_name) as asset_file, open('configs/apache2/httpd-http2-push.conf', 'w') as out_file:

    if file_name.endswith("json"):
        assets = json.load(asset_file).keys()
    else:
        assets = asset_file

    out_file.write(
        apache_h2_push_template.format(
            location_path,
            "\n    ".join([
                header_link_template.format(path.strip())
                for path in assets
            ])
        )
    )
