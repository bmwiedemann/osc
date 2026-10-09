import os
import unittest

import osc.commandline
import osc.core
import osc.oscerr

from .common import GET, PUT, OscTestCase


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'setlinkrev_fixtures')


def suite():
    return unittest.defaultTestLoader.loadTestsFromTestCase(TestSetLinkRev)


class TestSetLinkRev(OscTestCase):
    def setUp(self):
        super().setUp(copytree=False)

    def _get_fixtures_dir(self):
        return FIXTURES_DIR

    @GET('http://localhost/source/osctest/simple/_link', file='simple_link')
    @GET('http://localhost/source/srcprj/srcpkg?rev=latest', file='simple_filesremote')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Set+link+revision+to+42',
         exp='<link package="srcpkg" project="srcprj" rev="42" />', text='dummytext')
    def test_simple1(self):
        """a simple set_link_rev call without revision"""
        osc.core.set_link_rev('http://localhost', 'osctest', 'simple')

    @GET('http://localhost/source/osctest/simple/_link', file='simple_link')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Set+link+revision+to+42',
         exp='<link package="srcpkg" project="srcprj" rev="42" />', text='dummytext')
    def test_simple2(self):
        """a simple set_link_rev call with revision"""
        osc.core.set_link_rev('http://localhost', 'osctest', 'simple', '42')

    @GET('http://localhost/source/osctest/simple/_link', file='noproject_link')
    @GET('http://localhost/source/osctest/srcpkg?rev=latest&expand=1', file='expandedsrc_filesremote')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Set+link+revision+to+eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
         exp='<link package="srcpkg" rev="eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee" vrev="1" />', text='dummytext')
    def test_expandedsrc(self):
        """expand src package"""
        osc.core.set_link_rev('http://localhost', 'osctest', 'simple', expand=True)

    @GET('http://localhost/source/osctest/simple/_link', file='link_with_rev')
    @GET('http://localhost/source/srcprj/srcpkg?rev=latest', file='simple_filesremote')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Set+link+revision+to+42',
         exp='<link package="srcpkg" project="srcprj" rev="42" />', text='dummytext')
    def test_existingrev(self):
        """link already has a rev attribute, update it to current version"""
        # we could also avoid the superfluous PUT
        osc.core.set_link_rev('http://localhost', 'osctest', 'simple')

    @GET('http://localhost/source/osctest/simple/_link', file='link_with_rev')
    @GET('http://localhost/source/srcprj/srcpkg?rev=latest&expand=1', file='expandedsrc_filesremote')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Set+link+revision+to+eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
         exp='<link package="srcpkg" project="srcprj" rev="eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee" vrev="1" />',
         text='dummytext')
    def test_expandexistingrev(self):
        """link already has a rev attribute, update it to current version"""
        osc.core.set_link_rev('http://localhost', 'osctest', 'simple', expand=True)

    @GET('http://localhost/source/osctest', file='project_packagelist')
    @GET('http://localhost/source/osctest/simple/_link', file='simple_link')
    @GET('http://localhost/source/srcprj/srcpkg?rev=latest&expand=1', file='simple_filesremote')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Set+link+revision+to+42',
         exp='<link package="srcpkg" project="srcprj" rev="42" />', text='dummytext')
    @GET('http://localhost/source/osctest/simple2/_link', file='simple2_link')
    @GET('http://localhost/source/srcprj/srcpkg2?rev=latest&expand=1', file='simple2_filesremote')
    @PUT('http://localhost/source/osctest/simple2/_link?comment=Set+link+revision+to+7',
         exp='<link package="srcpkg2" project="srcprj" rev="7" />', text='dummytext')
    def test_project(self):
        """each package of a project gets the latest revision of its own link target"""
        out = self._run_osc("setlinkrev", "osctest")
        self.assertEqual(
            out,
            "Set link revision of package osctest/simple to 42\n"
            "Set link revision of package osctest/simple2 to 7\n",
        )

    @GET('http://localhost/source/osctest/simple/_link', file='simple_link')
    @GET('http://localhost/source/srcprj/srcpkg?rev=latest', file='simple_filesremote')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Set+link+revision+to+ffffffffffffffffffffffffffffffff',
         exp='<link package="srcpkg" project="srcprj" rev="ffffffffffffffffffffffffffffffff" vrev="1" />',
         text='dummytext')
    def test_md5(self):
        """md5=True never writes a numeric revision"""
        osc.core.set_link_rev('http://localhost', 'osctest', 'simple', md5=True)

    @GET('http://localhost/source/osctest/simple/_link', file='simple_link')
    @GET('http://localhost/source/srcprj/srcpkg?rev=latest&expand=1', file='simple_filesremote')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Set+link+revision+to+ffffffffffffffffffffffffffffffff',
         exp='<link package="srcpkg" project="srcprj" rev="ffffffffffffffffffffffffffffffff" vrev="1" />',
         text='dummytext')
    def test_md5_expand(self):
        """md5=True uses the srcmd5 if the expanded source is not a link"""
        osc.core.set_link_rev('http://localhost', 'osctest', 'simple', expand=True, md5=True)

    @GET('http://localhost/source/osctest/simple/_link', file='simple_link')
    @GET('http://localhost/source/srcprj/srcpkg?rev=42', file='simple_filesremote')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Set+link+revision+to+ffffffffffffffffffffffffffffffff',
         exp='<link package="srcpkg" project="srcprj" rev="ffffffffffffffffffffffffffffffff" vrev="1" />',
         text='dummytext')
    def test_md5_numeric_revision(self):
        """md5=True converts a given numeric revision to its srcmd5"""
        osc.core.set_link_rev('http://localhost', 'osctest', 'simple', '42', md5=True)

    @GET('http://localhost/source/osctest/simple/_link', file='noproject_link')
    @GET('http://localhost/source/osctest/srcpkg?rev=latest&expand=1', file='expandedsrc_filesremote')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Set+link+revision+to+eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
         exp='<link package="srcpkg" rev="eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee" vrev="1" />', text='dummytext')
    def test_md5_expandedsrc(self):
        """md5=True gives the same result as the default for an expanded link source"""
        osc.core.set_link_rev('http://localhost', 'osctest', 'simple', expand=True, md5=True)

    @GET('http://localhost/source/osctest/simple/_link', file='simple_link')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Set+link+revision+to+aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
         exp='<link package="srcpkg" project="srcprj" rev="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" />', text='dummytext')
    def test_md5_given_md5_revision(self):
        """md5=True keeps a given md5 revision without resolving it"""
        osc.core.set_link_rev('http://localhost', 'osctest', 'simple', 'a' * 32, md5=True)

    @GET('http://localhost/source/osctest/simple/_link', file='simple_link')
    @GET('http://localhost/source/srcprj/srcpkg?rev=latest&expand=1', file='simple_filesremote')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Set+link+revision+to+ffffffffffffffffffffffffffffffff',
         exp='<link package="srcpkg" project="srcprj" rev="ffffffffffffffffffffffffffffffff" vrev="1" />',
         text='dummytext')
    def test_md5_cli(self):
        """osc setlinkrev --md5"""
        out = self._run_osc("setlinkrev", "--md5", "osctest", "simple")
        self.assertEqual(out, "Set link revision of package osctest/simple to ffffffffffffffffffffffffffffffff\n")

    def test_md5_unset_cli(self):
        """osc setlinkrev --md5 --unset is rejected without touching the link"""
        out = self._run_osc("setlinkrev", "--md5", "--unset", "osctest", "simple")
        self.assertEqual(out, "")

    @GET('http://localhost/source/osctest/simple/_link', file='simple_link')
    @GET('http://localhost/source/srcprj/srcpkg?rev=latest', text='<directory name="srcpkg" rev="42" />')
    def test_md5_missing_srcmd5(self):
        """md5=True fails if the server does not return a srcmd5"""
        self.assertRaises(osc.oscerr.APIError, osc.core.set_link_rev, 'http://localhost', 'osctest', 'simple', md5=True)

    @GET('http://localhost/source/osctest/simple/_link', file='simple_link')
    @GET('http://localhost/source/srcprj/srcpkg?rev=latest&expand=1', text='conflict in file merge', code=400)
    def test_linkerror(self):
        """link is broken"""
        from urllib.error import HTTPError
        # the backend returns status 400 if we try to expand a broken _link
        self.assertRaises(HTTPError, osc.core.set_link_rev, 'http://localhost', 'osctest', 'simple', expand=True)

    @GET('http://localhost/source/osctest/simple/_link', file='rev_link')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Unset+link+revision',
         exp='<link package="srcpkg" project="srcprj" />', text='dummytext')
    def test_deleterev(self):
        """delete rev attribute from link xml"""
        osc.core.set_link_rev('http://localhost', 'osctest', 'simple', revision=None)

    @GET('http://localhost/source/osctest/simple/_link', file='md5_rev_link')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Unset+link+revision',
         exp='<link package="srcpkg" project="srcprj" />', text='dummytext')
    def test_deleterev_md5(self):
        """delete rev and vrev attribute from link xml"""
        osc.core.set_link_rev('http://localhost', 'osctest', 'simple', revision=None)

    @GET('http://localhost/source/osctest/simple/_link', file='simple_link')
    @PUT('http://localhost/source/osctest/simple/_link?comment=Unset+link+revision',
         exp='<link package="srcpkg" project="srcprj" />', text='dummytext')
    def test_deleterevnonexistent(self):
        """delete non existent rev attribute from link xml"""
        osc.core.set_link_rev('http://localhost', 'osctest', 'simple', revision=None)


if __name__ == '__main__':
    unittest.main()
