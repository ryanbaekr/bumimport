"""Testing for flat_import"""

import os
import sys

from bumimport import flat_import

FIXTURES = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fixtures")

def test_module_bad_value() -> None:
    """Test flat_import with a string that is not the name of a module"""

    module = "this_is_not_a_module"
    path = FIXTURES

    try:
        flat_import(module, path)
        message = ""
    except Exception as e:  # pylint: disable=broad-exception-caught
        message = str(e)

    assert message == f"No module named: {module}"


def test_package_w_module_w_stdlib_name() -> None:
    """Test flat_import with a package with a module with a stdlib name"""

    os_sep = os.sep

    from .fixtures import package_w_module_w_stdlib_name  # pylint: disable=import-outside-toplevel,import-error

    mod1 = getattr(package_w_module_w_stdlib_name, "os")
    assert mod1.func1() == "foo"

    mod2 = getattr(package_w_module_w_stdlib_name, "module2")
    assert mod2.func2() == os_sep

    assert os.sep == os_sep


def test_package_w_module_w_dot_in_name() -> None:
    """Test flat_import with a package with a module with a dot in its name"""

    from .fixtures import package_w_module_w_dot_in_name  # pylint: disable=import-outside-toplevel,import-error

    mod1 = getattr(package_w_module_w_dot_in_name, "mod.ule1")
    assert mod1.func1() == "foo"

    mod2 = getattr(package_w_module_w_dot_in_name, "module2")
    assert mod2.func2() == "bar"


def test_package_w_module_w_dash_in_name() -> None:
    """Test flat_import with a package with a module with a dash in its name"""

    from .fixtures import package_w_module_w_dash_in_name  # pylint: disable=import-outside-toplevel,import-error

    mod1 = getattr(package_w_module_w_dash_in_name, "mod-ule1")
    assert mod1.func1() == "foo"

    mod2 = getattr(package_w_module_w_dash_in_name, "module2")
    assert mod2.func2() == "bar"


def test_package_w_duplicate_module_names() -> None:
    """Test flat_import with a package with multiple modules with the same name"""

    try:
        from .fixtures import package_w_duplicate_module_names  # pylint: disable=import-outside-toplevel,import-error
    except Exception as e:  # pylint: disable=broad-exception-caught
        message = str(e)

    assert message == "Multiple modules named: module1"
