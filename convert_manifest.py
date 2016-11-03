import json

location_path = "/index.html"

apache_h2_push_template = """
<Location {}>
    {}
</Location>
"""

header_link_template = 'Header add Link "<{}>;rel=preload"'

with open('push_manifest.json') as manifest_file, open('httpd-http2-push.conf', 'w') as out_file:
    manifest = json.load(manifest_file)
    out_file.write(
        apache_h2_push_template.format(
            location_path,
            "\n    ".join([
                header_link_template.format(path)
                for path in manifest.iterkeys()
            ])
        )
    )
