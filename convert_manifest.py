import json
improt sys

location_path = "/index.html"

apache_h2_push_template = """
<Location {}>
    {}
</Location>
"""

header_link_template = 'Header add Link "<{}>;rel=preload"'

with open(sys.argv[1]) as asset_file, open('httpd-http2-push.conf', 'w') as out_file:
    out_file.write(
        apache_h2_push_template.format(
            location_path,
            "\n    ".join([
                header_link_template.format(path.strip())
                for path in asset_file
            ])
        )
    )
