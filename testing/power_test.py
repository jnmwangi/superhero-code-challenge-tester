from app import app
from models import Power, db
from random import choice
from test_data import powers

class TestPower:
    """Test the powers endpoints"""
    
    def init(self) -> None:
        Power.query.delete()            
        db.session.commit()
        
    
    def test_create_power(self):
        """Test posting a power"""
        with app.app_context():
            self.init()
            
            power = choice(powers)
            response = app.test_client().post("/powers", json=power)
            
            assert response.status_code == 201
            assert response.content_type == "application/json"
            response = response.json
            for key in power.keys():
                assert power[key] == response[key]
            
    
    def test_get_powers(self):
        """Test getting powers"""
        with app.app_context():
            self.init()
            
            for power in powers:
                db.session.add(Power(**power))
            db.session.commit()
            
            power = choice(powers)
            response = app.test_client().get("/powers")
            
            assert response.status_code == 200
            assert response.content_type == "application/json"
            powernames = [power["name"] for power in powers]
            dbpowers = Power.query.all()
            for power in dbpowers:
                assert power.name in powernames
            
         
    def test_get_power_by_id(self):
        """Test get power by id"""
        with app.app_context():
            self.init()
            
            response = app.test_client().get("/powers/0")            
            assert response.status_code == 404
            
            power = Power(**choice(powers))
            db.session.add(power)
            db.session.commit()
            
            response = app.test_client().get("/powers/"+str(power.id))
            
            assert response.status_code == 200
            assert response.content_type == "application/json"
            response = response.json
            assert power.name == response["name"]
            assert power.description == response["description"]
            
    
    def test_update_power(self):
        """Test updating power and if there is 404 when not found"""
        with app.app_context():
            self.init()
            
            power = Power(**choice(powers))
            db.session.add(power)
            db.session.commit()
            
            newname = "Fly over buildings"
            
            response = app.test_client().patch("/powers/0", json={"name":newname})
            assert response.status_code == 404
            
            response = app.test_client().patch("/powers/"+str(power.id), json={"name":newname})
            
            assert response.status_code == 200
            assert response.content_type == "application/json"
            response = response.json
            power_dict = power.to_dict()
            power_dict["name"] = newname
            for attr in response:
                assert power_dict[attr] == response[attr]
            
            
    def test_get_power_by_id_404(self):
        """Test delete hero and if we get status code 404 when not found"""
        with app.app_context():
            self.init()
            
            response = app.test_client().delete("/powers/0")
            assert response.status_code == 404
            
            power = Power(**choice(powers))
            db.session.add(power)
            db.session.commit()
            
            response = app.test_client().delete("/powers/"+str(power.id))
            assert response.status_code == 204
            
    