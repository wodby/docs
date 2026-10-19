"""Give custom theme assets content-addressed URLs for safe long-lived caching."""

from hashlib import sha256
from pathlib import Path
from urllib.parse import urlsplit

from mkdocs.structure.files import File

# MkDocs serve can reuse the mutated config between builds.
_source_urls = {}


def on_files(files, *, config):
    theme_dir = Path(config.theme.custom_dir)
    generated = set()

    def version(url):
        original = _source_urls.get(str(url), str(url))
        parsed = urlsplit(original)
        if parsed.scheme or parsed.netloc or original.startswith('/'):
            return url
        source = theme_dir / parsed.path
        if not source.is_file():
            return url
        content = source.read_bytes()
        path = Path(parsed.path)
        digest = sha256(content).hexdigest()[:16]
        target = path.with_name(f'{path.stem}.{digest}{path.suffix}').as_posix()
        if target not in generated:
            files.append(File.generated(config, target, content=content))
            generated.add(target)
        _source_urls[target] = original
        return target

    config.extra_css = [version(url) for url in config.extra_css]
    config.extra_javascript = [version(url) for url in config.extra_javascript]
    for name in ('logo', 'favicon'):
        if config.theme.get(name):
            config.theme[name] = version(config.theme[name])
    return files
