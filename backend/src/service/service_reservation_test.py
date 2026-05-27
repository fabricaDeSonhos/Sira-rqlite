import datetime

from service_reservation import create_reservation, get_reservation
import unittest

class TestServiceReservation(unittest.TestCase):
    
    # testing a successful reservation creation
    def test_create_reservation(self):
        self.assertEqual(create_reservation(
            {"user": "Joao da Silva", 
             "artifact": "Sala C08", 
            "date": datetime.date(2026, 5, 26),
             "start_time": datetime.time(14, 0),
             "end_time": datetime.time(15, 0),
         "purpose":"Aula Info 302 - Optativa Web / Hylson",
         "category":"Sala de Aula",
         "color_category":"#574DA5",
         "active":True,
         "batch_id":None,
         "observations":None,
         "created_at":datetime.datetime(2026, 5, 26, 13, 0),
         "canceler_user":None,
         "observers":None}), {"result":"ok", 
                                "details": {"user": "Joao da Silva",
                                            "artifact": "Sala C08", 
                                            "date": datetime.date(2026, 5, 26),
                                            "start_time": datetime.time(14, 0),
                                            "end_time": datetime.time(15, 0),
                                            "purpose":"Aula Info 302 - Optativa Web / Hylson",
                                            "category":"Sala de Aula",
                                            "color_category":"#574DA5",
                                            "active":True,
                                            "batch_id":None,
                                            "observations":None,
                                            "created_at":datetime.datetime(2026, 5, 26, 13, 0),
                                            "canceler_user":None,
                                            "observers":None,
                                            # the ID is the new field that
                                            # comes when a new reservation is created                                    
                                            "id":1
                                        } 
                                                     
                                })
        
    def test_get_reservation(self):

        # testing reservation id 1
        self.assertEqual(get_reservation(1), 
            {"result":"ok", "details": {
            "user": "Joao da Silva",
            "artifact": "Sala C08", 
            "date": datetime.date(2026, 5, 26),
            "start_time": datetime.time(14, 0),
            "end_time": datetime.time(15, 0),
            "purpose":"Aula Info 302 - Optativa Web / Hylson",
            "category":"Sala de Aula",
            "color_category":"#574DA5",
            "active":True,
            "batch_id":None,
            "observations":None,
            "created_at":datetime.datetime(2026, 5, 26, 13, 0),
            "canceler_user":None,
            "observers":None,
            "id":1
        }})
        
        # testing reservation id 2
        self.assertEqual(get_reservation(2), {"result":"ok", "details": {
            "user": "Maria Oliveira",
            "artifact": "Sala C09",
            "date": datetime.date(2026, 5, 27),
            "start_time": datetime.time(10, 0),
            "end_time": datetime.time(11, 0),
            "purpose":"Reunião de equipe",
            "category":"Sala de Reunião",
            "color_category":"#FF5733",
            "active":True,
            "batch_id":None,
            "observations":None,
            "created_at":datetime.datetime(2026, 5, 27, 9, 0),
            "canceler_user":None,
            "observers":None,
            "id":2
        }})

        # testing reservation id that does not exist
        self.assertEqual(get_reservation(999), {"result":"error", "details":"Reservation not found, id=999"})

