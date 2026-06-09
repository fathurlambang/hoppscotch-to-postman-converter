class HoppscotchConverter < Formula
  include Language::Python::Virtualenv

  desc "Convert Hoppscotch exports to Postman v2.1 format"
  homepage "https://github.com/fathurlambang/hoppscotch-to-postman-converter"
  url "https://github.com/fathurlambang/hoppscotch-to-postman-converter/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "b6c865722cc70e948d6beeeebdff032e4ffc954affcaa0b567d8389b210b3c9b"
  license "MIT"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "hoppscotch-converter", shell_output("#{bin}/hoppscotch-converter --help")
  end
end
