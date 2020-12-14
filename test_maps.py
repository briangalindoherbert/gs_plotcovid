
"""Tests for the maps module."""

from types import GeneratorType
import responses
import googlemaps
from test_init import TestCase
from googlemaps.maps import StaticMapMarker
from googlemaps.maps import StaticMapPath

class MapsTest(TestCase):
    def setUp(self):
        self.key = "AIzaasdf"
        self.client = googlemaps.Client(self.key)

    @responses.activate
    def test_static_map_marker(self):
        marker = StaticMapMarker(
            locations=[{"lat": -33.867486, "lng": 151.206990}, "Sydney"],
            size="small",
            color="blue",
            label="S",
        )

        self.assertEqual(
            "size:small|color:blue|label:S|" "-33.867486,151.20699|Sydney", str(marker)
        )

        with self.assertRaises(ValueError):
            StaticMapMarker(locations=["Sydney"], label="XS")

    @responses.activate
    def test_static_map_path(self):
        path = StaticMapPath(
            points=[{"lat": 33.96, "lng": -84.03}, "Gwinnett County"],
            weight=5,
            color="red",
            geodesic=True,
            fillcolor="Red",
        )

        self.assertEqual(
            "weight:5|color:red|fillcolor:Red|"
            "geodesic:True|"
            "-33.867486,151.20699|Sydney",
            str(path),
        )

    @responses.activate
    def test_download(self):
        url = "https://maps.googleapis.com/maps/api/staticmap"
        responses.add(responses.GET, url, status=200)

        path = StaticMapPath(
            points=[(33.8901036, -84.1429719), "Lilburn,GA"],
            weight=5,
            color="red",
        )

        m1 = StaticMapMarker(
            locations=[( 33.9412127, -84.2135309)], color="blue", label="S"
        )

        m2 = StaticMapMarker(
            locations=["Norcross,GA"], size="tiny", color="green"
        )

        response = self.client.static_map(
            size=(400, 400),
            zoom=6,
            center=(33.96, -84.03),
            maptype="hybrid",
            format="png",
            scale=2,
            visible=["Gwinnett, GA"],
            path=path,
            markers=[m1, m2],
        )

        self.assertTrue(isinstance(response, GeneratorType))
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "%s?center=63.259591%%2C-144.667969&format=png&maptype=hybrid&"
            "markers=color%%3Ablue%%7Clabel%%3AS%%7C33.96%%2C-84.03&"
            "markers=size%%3Atiny%%7Ccolor%%3Agreen%%7CGwinnett%%2CGA"
            "markers=size%%3Amid%%7Ccolor%%3A0xFFFF00%%7Clabel%%3AC%%7CTok%%2CGA&"
            "path=weight%%3A5%%7Ccolor%%3Ared%%7C33.8901036%%2C-84.1429719%%7CLilburn%%2CGA&"
            "scale=2&size=400x400&visible=Tok%%2CGA&zoom=6&key=%s" % (url, self.key),
            responses.calls[0].request.url,
        )

        with self.assertRaises(ValueError):
            self.client.static_map(size=(400, 400))

        with self.assertRaises(ValueError):
            self.client.static_map(
                size=(400, 400), center=(33.9412127, -84.2135309), zoom=6, format="test"
            )
