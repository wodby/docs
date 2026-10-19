"""Verify asset changes invalidate URLs without invalidating unchanged assets."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from mkdocs.config import load_config
from mkdocs.structure.files import Files

import version_assets


class AssetVersionTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'docs').mkdir()
        self.assets = self.root / 'theme' / 'assets'
        self.assets.mkdir(parents=True)
        for name, content in [('style.css', 'body { color: blue; }'),
                              ('app.js', 'console.log("ready");'),
                              ('logo.svg', '<svg/>')]:
            (self.assets / name).write_text(content)
        cfg = self.root / 'mkdocs.yml'
        cfg.write_text('''site_name: Test
site_dir: output
theme:
  name: material
  custom_dir: theme
  logo: assets/logo.svg
  favicon: assets/logo.svg
extra_css: [assets/style.css, 'https://example.com/external.css']
extra_javascript: [assets/app.js]
''')
        self.config = load_config(str(cfg))
        self.config.plugins._current_plugin = "asset-version-test"
        version_assets._source_urls.clear()

    def build_assets(self):
        return version_assets.on_files(Files([]), config=self.config)

    def test_local_assets_are_emitted_and_external_urls_preserved(self):
        files = self.build_assets()
        urls = [self.config.extra_css[0], self.config.extra_javascript[0],
                self.config.theme['logo'], self.config.theme['favicon']]
        self.assertEqual(len(files), 3)
        for url in urls:
            self.assertRegex(str(url), r'\.[0-9a-f]{16}\.')
            self.assertIsNotNone(files.get_file_from_path(str(url)))
        self.assertEqual(self.config.extra_css[1], 'https://example.com/external.css')
        self.assertEqual(files.get_file_from_path(urls[0]).content_bytes,
                         (self.assets / 'style.css').read_bytes())

    def test_unchanged_rebuild_keeps_urls(self):
        self.build_assets()
        previous = list(self.config.extra_css)
        self.build_assets()
        self.assertEqual(previous, self.config.extra_css)

    def test_changed_asset_gets_new_url_on_reused_config(self):
        self.build_assets()
        css = self.config.extra_css[0]
        logo = self.config.theme['logo']
        (self.assets / 'style.css').write_text('body { color: green; }')
        files = self.build_assets()
        self.assertNotEqual(css, self.config.extra_css[0])
        self.assertEqual(logo, self.config.theme['logo'])
        self.assertIsNotNone(files.get_file_from_path(self.config.extra_css[0]))


if __name__ == '__main__':
    unittest.main()
