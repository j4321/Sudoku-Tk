# Maintainer: Juliette Monsel <j_4321@protonmail.com>
pkgname=sudoku-tk
_name=Sudoku-Tk
pkgver=1.2.0
pkgrel=1
pkgdesc="Sudoku games and puzzle solver"
arch=('any')
url="https://github.com/j4321/Sudoku-Tk"
license=('GPL3')
makedepends=('python-setuptools')
depends=('tk' 'python-pillow' 'python-numpy' 'gettext' 'desktop-file-utils')
optdepends=('python-tkfilebrowser: nicer file browser'
            'zenity: nicer file browser')
source=("$pkgname-$pkgver.tar.gz::https://github.com/j4321/$_name/archive/v$pkgver.tar.gz")
sha512sums=('e908a32c0d704fedccb33eae42f304aaeb13b756f28940bbc7fd9a3150329b8389d2ff2706b982fb431d9dad28886106b1da9300e6c68041465624a3cd89031e')

build() {
	cd "$srcdir/$_name-$pkgver"
    python setup.py build
}

package() {
    cd "$srcdir/$_name-$pkgver"
    python setup.py install --root="$pkgdir/" --prefix=/usr --optimize=1 --skip-build
}
