import unittest
from server.lib.chart_connection import ChartsConnection


class TestIsSameSong(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.may_charts = ChartsConnection(is_test=True)

    def test_same_song_one_artist(self):
        # Same songs
        self.assertTrue(
            self.may_charts.is_same_song('Richer (feat. Polo G)', 'Rod Wave', 'Richer', 'Rod Wave Featuring Polo G'))

    def test_same_song_one_artist2(self):
        self.assertTrue(
            self.may_charts.is_same_song('Richer', 'Rod Wave Featuring Polo G', 'Richer (feat. Polo G)', 'Rod Wave'))

    def test_same_3_artists(self):
        self.assertTrue(
            self.may_charts.is_same_song('Peaches (feat. Daniel Caesar & Giveon)', 'Justin Bieber',
                                         'Peaches', 'Justin Bieber Featuring Daniel Caesar & Giveon'))

    def test_same_3_artists_b(self):
        self.assertTrue(
            self.may_charts.is_same_song('Headshot (feat. Polo G & Fivio Foreign)', 'Lil Tjay',
                                         'Headshot', 'Lil Tjay, Polo G & Fivio Foreign'))

    def test_diff(self):
        # Different songs
        self.assertFalse(
            self.may_charts.is_same_song('goosebumps', 'Travis Scott', 'Goosebumps', 'Travis Scott & HVME'))

    def test_diff_song_same_artist(self):
        self.assertFalse(
            self.may_charts.is_same_song('Street Runner', 'Rod Wave', 'Richer', 'Rod Wave Featuring Polo G'))

    def test_diff_song_same_artists(self):
        self.assertFalse(self.may_charts.is_same_song('Richer (feat. Polo G)', 'Rod Wave',
                                                      'Street Runner', 'Rod Wave Featuring Polo G'))

    def test_diff_song_and_artist(self):
        self.assertFalse(
            self.may_charts.is_same_song('Leave The Door Open', 'Silk Sonic (Bruno Mars & Anderson .Paak)',
                                         'RAPSTAR', 'Polo G'))

    # TODO: Deal with this Silk Sonic business?
    def test_same_song_3_artists(self):
        self.assertTrue(self.may_charts.is_same_song('Leave The Door Open', 'Silk Sonic (Bruno Mars & Anderson .Paak)',
                                                     'Leave The Door Open', 'Bruno Mars, Anderson .Paak, Silk Sonic'))

    def test_diff_song_1_common_artist(self):
        self.assertFalse(self.may_charts.is_same_song('Leave The Door Open', 'Silk Sonic (Bruno Mars & Anderson .Paak)',
                                                      'Talking to the Moon', 'Bruno Mars'))

    def test_same_song_same_3_artists(self):
        self.assertTrue(self.may_charts.is_same_song('Peaches', 'Justin Bieber Featuring Daniel Caesar & Giveon',
                                                     'Peaches (feat. Daniel Caesar & Giveon)', 'Justin Bieber'))

    def test_diff_song_1_same_artist(self):
        self.assertFalse(
            self.may_charts.is_same_song('Peaches', 'Justin Bieber Featuring Daniel Caesar & Giveon',
                                         'Hold On', 'Justin Bieber'))

    def test_same_song(self):
        self.assertTrue(self.may_charts.is_same_song(
            'RAPSTAR', 'Polo G', 'RAPSTAR', 'Polo G'))


if __name__ == '__main__':
    unittest.main()
