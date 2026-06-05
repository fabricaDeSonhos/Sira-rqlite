import datetime

from service_reservation \
    import create_reservation, get_reservation, \
           cancel_reservation, list_reservations, edit_reservation

# import data for testing, while using static data
from service_reservation_static_data import joao_data, maria_data

import unittest

class TestServiceReservation(unittest.TestCase):

# - creation tests ---------------------------------

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
        
# - getting tests ----------------------------------------

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

# - cancellation tests ----------------------------------------

    def test_cancel_reservation(self):
        
        # testing reservation id 1 cancellation
        self.assertEqual(cancel_reservation(1, "Joao da Silva", "Aula cancelada pelo professor, será resposta depois"), 
                         {"result":"ok", "details":"Reservation with id=1 cancelled by Joao da Silva"})

        # testing reservation id 2 cancellation
        self.assertEqual(cancel_reservation(2, "Maria Oliveira", "Reunião cancelada pela diretoria"), 
                         {"result":"ok", "details":"Reservation with id=2 cancelled by Maria Oliveira"})

        # testing reservation id that does not exist cancellation
        self.assertEqual(cancel_reservation(999, "Joao da Silva", "Aula cancelada devido a feriado nacional"), 
                         {"result":"error", "details":"Reservation not found, id=999"})
        
# - listing tests ----------------------------------------
    
    def test_list_reservations(self):
        
        self.assertEqual(list_reservations(), 
                         {"result":"ok", "details": [joao_data, maria_data]})
        
# - editing tests ----------------------------------------

    def test_edit_reservation(self):

        # testing reservation id 1 edition
        updated_reservation_data = joao_data
        # changing data
        updated_reservation_data["purpose"] = "Aula Info 302 - Optativa Web / Hylson - Aula Editada"

        # execute the edition
        new_reservation = edit_reservation(1, updated_reservation_data)
        
        # expected data: the new data with a NEW id (3 in static implementation)
        expected_new_reservation = updated_reservation_data
        expected_new_reservation['id'] = 3

        # test the result!
        self.assertEqual(new_reservation,
                         {"result":"ok", "details":expected_new_reservation})
        
        # testing reservation id that does not exist edition
        self.assertEqual(edit_reservation(999, updated_reservation_data), 
                         {"result":"error", "details":"Reservation not found, id=999"})
