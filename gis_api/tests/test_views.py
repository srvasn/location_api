import json

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from gis_api.models import Region


# __author__ = 'Sourav Banerjee'
# __email__ = ' srvasn@gmail.com'


class RegionTests(APITestCase):
    """
    Test if a registered user can create a view
    """

    def setUp(self):
        self.user = User.objects.create_user("derek", "derek@wind.com", "testpassword")
        self.client.login(username="derek", password="testpassword")
        self.data = \
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                20.6705551147461,
                                -20.89135645852043
                            ],
                            [
                                20.64171600341797,
                                20.89288988217029
                            ],
                            [
                                -20.63690948486328,
                                20.880110226947934
                            ],
                            [
                                -20.549583435058,
                                -20.214077038175
                            ],
                            [
                                20.6705551147461,
                                -20.89135645852043
                            ]
                        ]
                    ]
                },
                "properties": {
                    "name": "Snowland",
                    "price": 200
                }
            }

    def test_user_can_create_region(self):
        response = self.client.post(reverse("region-list"), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadRegionTest(APITestCase):
    """
    Test if a registered user can read the region list and region details
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.create(username="mike")

    def test_can_read_region_list(self):
        response = self.client.get(reverse('region-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_region_detail(self):
        response = self.client.get(reverse('region-list'), args=[self.user.id])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateRegionTest(APITestCase):
    """
    Test if a user can update an existing region
    """

    def setUp(self):
        self.user = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.data = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            20.6705551147461,
                            -20.89135645852043
                        ],
                        [
                            28.64171600341797,
                            19.89288988217029
                        ],
                        [
                            -21.63690948486328,
                            17.880110226947934
                        ],
                        [
                            -20.549583435058,
                            -20.214077038175
                        ],
                        [
                            20.6705551147461,
                            -20.89135645852043
                        ]
                    ]
                ]
            },
            "name": "Hrothgar",
            "price": 150
        }
        # response_dict = self.client.post(reverse('region-list'), self.data,format='json')
        self.new_region = Region.objects.create(name="Hrothgar", price="150", area=json.dumps(self.data["geometry"]))
        self.new_region.save()
        self.data.update({'price': 250, 'id': self.new_region.id})
        self.data["area"] = self.data.pop("geometry")

    def test_can_update_region(self):
        response = self.client.put(reverse("region-update", args=[self.new_region.id]), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteRegionTest(APITestCase):
    """
    Test if a user can delete an existing region
    """

    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.data = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            20.6705551147461,
                            -20.89135645852043
                        ],
                        [
                            28.64171600341797,
                            19.89288988217029
                        ],
                        [
                            -21.63690948486328,
                            17.880110226947934
                        ],
                        [
                            -20.549583435058,
                            -20.214077038175
                        ],
                        [
                            20.6705551147461,
                            -20.89135645852043
                        ]
                    ]
                ]
            },
            "name": "Hrothgar",
            "price": 150
        }

        self.new_region = Region.objects.create(name="Hrothgar", price="150", area=json.dumps(self.data["geometry"]))

    def test_can_delete_user(self):
        response = self.client.delete(reverse('region-update', args=[self.new_region.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
